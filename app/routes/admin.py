from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from models.categoria_repository import CategoriaRepository
from werkzeug.exceptions import abort
from datetime import datetime
from services.dashboard_service import DashboardService
from datetime import datetime
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if current_user.rol != 'Admin':
        abort(403)

# Panel principal
# Luego modificar la función dashboard:
@admin_bp.route('/dashboard')
def dashboard(): # type: ignore
    today_sales = DashboardService.get_today_sales()
    products_sold_today = DashboardService.get_products_sold_today()
    top_product = DashboardService.get_top_product_week()
    unsold_product = DashboardService.get_unsold_product_week()
    payment_methods = DashboardService.get_payment_methods_today()
    avg_sale = DashboardService.get_average_sale_value_today()
    sales_by_hour = DashboardService.get_sales_by_hour_today()
    peak_hour = DashboardService.get_peak_hour_today()
    preferred_payment = DashboardService.get_preferred_payment_method_today()
    
    # Horario de negocio (podría ser desde configuraciones)
    business_start = "8:00 AM"
    business_end = "10:00 PM"
    
    return render_template('admin/dashboard.html',
                           today_sales=today_sales,
                           products_sold_today=products_sold_today,
                           top_product=top_product,
                           unsold_product=unsold_product,
                           payment_methods=payment_methods,
                           avg_sale=avg_sale,
                           sales_by_hour=sales_by_hour,
                           peak_hour=peak_hour,
                           preferred_payment=preferred_payment,
                           business_start=business_start,
                           business_end=business_end)

# Listado de productos
@admin_bp.route('/productos')
def productos():
    productos = ProductoService.listar_productos()
    return render_template('admin/productos_list.html', productos=productos)

# Crear producto
@admin_bp.route('/producto/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    if request.method == 'POST':
        try:
            id_categoria = int(request.form['id_categoria'])
            nombre = request.form['nombre']
            stock = int(request.form['stock'])
            precio = float(request.form['precio'])
            producto = ProductoService.crear_producto(id_categoria, nombre, stock, precio)
            if producto:
                flash('Producto creado exitosamente', 'success')
                return redirect(url_for('admin.productos'))
            else:
                flash('Error al crear producto', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    categorias = CategoriaRepository.listar_todas()
    return render_template('admin/producto_form.html', categorias=categorias)

# Editar producto
@admin_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    producto = ProductoService.buscar_producto(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('admin.productos'))
    
    if request.method == 'POST':
        try:
            id_categoria = int(request.form['id_categoria'])
            nombre = request.form['nombre']
            stock = int(request.form['stock'])
            precio = float(request.form['precio'])
            producto_actualizado = ProductoService.actualizar_producto(
                id, id_categoria, nombre, stock, precio
            )
            if producto_actualizado:
                flash('Producto actualizado', 'success')
                return redirect(url_for('admin.productos'))
            else:
                flash('Error al actualizar', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    
    categorias = CategoriaRepository.listar_todas()
    return render_template('admin/producto_form.html', producto=producto, categorias=categorias)

# Eliminar producto
@admin_bp.route('/producto/eliminar/<int:id>')
def producto_eliminar(id):
    producto = ProductoService.buscar_producto(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
    else:
        if ProductoService.eliminar_producto(id):
            flash('Producto eliminado', 'success')
        else:
            flash('Error al eliminar', 'danger')
    return redirect(url_for('admin.productos'))

# Registrar entrada de inventario
@admin_bp.route('/inventario/entrada', methods=['GET', 'POST'])
def inventario_entrada():
    if request.method == 'POST':
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        motivo = request.form['motivo']
        resultado = InventarioService.registrar_entrada(
            id_producto, current_user.id_usuario, cantidad, motivo
        )
        if resultado:
            flash('Entrada registrada correctamente', 'success')
        else:
            flash('Error al registrar entrada', 'danger')
        return redirect(url_for('admin.inventario_entrada'))
    productos = ProductoService.listar_productos()
    return render_template('admin/inventario_entrada.html', productos=productos)

def dashboard():
    now = datetime.now().strftime("%A, %d de %B de %Y")
    return render_template(..., now=now) # type: ignore

@admin_bp.route('/reportes')
def reportes():
    from services.reporte_service import ReporteService
    
    total_dinero, total_transacciones = ReporteService.total_ventas_hoy()
    unidades_vendidas = ReporteService.unidades_vendidas_hoy()
    ventas_por_hora = ReporteService.ventas_por_hora()
    top_producto, top_categoria, top_unidades = ReporteService.producto_mas_vendido_semana()
    low_producto, low_categoria, low_unidades = ReporteService.producto_menos_vendido_semana()
    pagos_hoy = ReporteService.total_por_metodo_pago_hoy()
    promedio_venta = ReporteService.promedio_venta_hoy()
    hora_pico = ReporteService.hora_pico_hoy()
    metodo_preferido = ReporteService.metodo_pago_preferido_hoy()

    # Personal en turno (simulado)
    on_duty = {"nombre": "María González", "rol": "Cajero", "horario": "8:00 AM - 6:00 PM"}
    fecha_actual = datetime.now().strftime('%A, %d de %B de %Y')
    
    context = {
        'total_dinero': total_dinero,
        'total_transacciones': total_transacciones,
        'unidades_vendidas': unidades_vendidas,
        'apertura': "8:00 AM",
        'cierre': "10:00 PM",
        'top_producto': top_producto,
        'top_categoria': top_categoria,
        'top_unidades': top_unidades,
        'low_producto': low_producto,
        'low_categoria': low_categoria,
        'low_unidades': low_unidades,
        'on_duty': on_duty,
        'pagos_hoy': pagos_hoy,
        'promedio_venta': promedio_venta,
        'hora_pico': hora_pico,
        'metodo_preferido': metodo_preferido,
        'sales_by_hour': ventas_por_hora,
        'fecha_actual': fecha_actual,
    }
    return render_template('admin/reportes.html', **context)

@admin_bp.route('/inventario/salida', methods=['GET', 'POST'])
def inventario_salida():
    if request.method == 'POST':
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        motivo = request.form['motivo']
        resultado = InventarioService.registrar_salida(
            id_producto, current_user.id_usuario, cantidad, motivo
        )
        if resultado:
            flash('Salida registrada correctamente', 'success')
        else:
            flash('Error al registrar salida (stock insuficiente?)', 'danger')
        return redirect(url_for('admin.inventario_salida'))
    productos = ProductoService.listar_productos()
    return render_template('admin/inventario_salida.html', productos=productos)