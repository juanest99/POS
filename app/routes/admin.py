"""
ADMIN ROUTES - Panel de administración
Maneja todas las rutas para el administrador del sistema
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from services.gasto_service import GastoService
from services.reporte_service import ReporteService
from services.dashboard_service import DashboardService
from models.categoria_repository import CategoriaRepository
from models.usuario_repository import UsuarioRepository

admin_bp = Blueprint('admin', __name__)

# ==================== DASHBOARD ====================

@admin_bp.route('/')
@login_required
def dashboard():
    """Panel principal del administrador con estadísticas"""
    # Verificar que sea admin (usando .lower() para comparar)
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado. Se requieren privilegios de administrador.', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    # Obtener estadísticas para el dashboard
    today_sales = DashboardService.get_today_sales()
    products_sold_today = DashboardService.get_products_sold_today()
    avg_sale = DashboardService.get_average_sale_value_today()
    peak_hour = DashboardService.get_peak_hour_today()
    sales_by_hour = DashboardService.get_sales_by_hour_today()
    payment_methods = DashboardService.get_payment_methods_today()
    preferred_payment = DashboardService.get_preferred_payment_method_today()
    top_product = DashboardService.get_top_product_week()
    unsold_product = DashboardService.get_unsold_product_week()
    
    return render_template('admin/dashboard.html',
                         today_sales=today_sales,
                         products_sold_today=products_sold_today,
                         avg_sale=avg_sale,
                         peak_hour=peak_hour,
                         sales_by_hour=sales_by_hour,
                         payment_methods=payment_methods,
                         preferred_payment=preferred_payment,
                         top_product=top_product,
                         unsold_product=unsold_product,
                         business_start='08:00',
                         business_end='20:00')


# ==================== GESTIÓN DE PRODUCTOS ====================
@admin_bp.route('/buscar-producto')
def buscar_producto():

    nombre_producto = request.args.get('buscar')

    productos = ProductoService.buscar_por_nombre(nombre_producto)

    return render_template(
        'admin/productos_list.html',
        productos=productos
    )

@admin_bp.route('/productos')
@login_required
def productos():
    """Lista todos los productos"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    productos = ProductoService.listar_productos()
    return render_template('admin/productos_list.html', productos=productos)


@admin_bp.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def producto_nuevo():
    """Crear nuevo producto"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    categorias = CategoriaRepository.listar_todas()
    
    if request.method == 'POST':
        try:
            id_categoria = int(request.form.get('id_categoria'))
            nombre = request.form.get('nombre')
            stock = int(request.form.get('stock'))
            precio = float(request.form.get('precio'))
            
            producto = ProductoService.crear_producto(id_categoria, nombre, stock, precio)
            
            if producto:
                flash(f'✅ Producto "{nombre}" creado exitosamente', 'success')
                return redirect(url_for('admin.productos'))
            else:
                flash('❌ Error al crear el producto', 'danger')
        except ValueError:
            flash('❌ Error: Datos inválidos', 'danger')
    
    return render_template('admin/productos_form.html', categorias=categorias, producto=None)


@admin_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def producto_editar(id):
    """Editar producto existente"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    producto = ProductoService.buscar_producto(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('admin.productos'))
    
    categorias = CategoriaRepository.listar_todas()
    
    if request.method == 'POST':
        try:
            id_categoria = int(request.form.get('id_categoria'))
            nombre = request.form.get('nombre')
            stock = int(request.form.get('stock'))
            precio = float(request.form.get('precio'))
            
            producto_actualizado = ProductoService.actualizar_producto(id, id_categoria, nombre, stock, precio)
            
            if producto_actualizado:
                flash(f'✅ Producto "{nombre}" actualizado exitosamente', 'success')
                return redirect(url_for('admin.productos'))
            else:
                flash('❌ Error al actualizar el producto', 'danger')
        except ValueError:
            flash('❌ Error: Datos inválidos', 'danger')
    
    return render_template('admin/productos_form.html', categorias=categorias, producto=producto)


@admin_bp.route('/producto/eliminar/<int:id>')
@login_required
def producto_eliminar(id):
    """Eliminar producto"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    if ProductoService.eliminar_producto(id):
        flash('✅ Producto eliminado exitosamente', 'success')
    else:
        flash('❌ Error al eliminar producto', 'danger')
    
    return redirect(url_for('admin.productos'))


# ==================== GESTIÓN DE INVENTARIO ====================

@admin_bp.route('/inventario/entrada', methods=['GET', 'POST'])
@login_required
def inventario_entrada():
    """Registrar entrada de productos al inventario"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    productos = ProductoService.listar_productos()
    
    if request.method == 'POST':
        try:
            id_producto = int(request.form.get('id_producto'))
            cantidad = int(request.form.get('cantidad'))
            motivo = request.form.get('motivo')
            
            resultado = InventarioService.registrar_entrada(
                id_producto=id_producto,
                id_usuario=current_user.id_usuario,
                cantidad=cantidad,
                motivo=motivo
            )
            
            if resultado:
                flash(f'✅ Entrada registrada: {cantidad} unidades', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('❌ Error al registrar entrada', 'danger')
        except ValueError:
            flash('❌ Error: Datos inválidos', 'danger')
    
    return render_template('admin/inventario_entrada.html', productos=productos)


@admin_bp.route('/inventario/salida', methods=['GET', 'POST'])
@login_required
def inventario_salida():
    """Registrar salida de productos del inventario"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    productos = ProductoService.listar_productos()
    
    if request.method == 'POST':
        try:
            id_producto = int(request.form.get('id_producto'))
            cantidad = int(request.form.get('cantidad'))
            motivo = request.form.get('motivo')
            
            resultado = InventarioService.registrar_salida(
                id_producto=id_producto,
                id_usuario=current_user.id_usuario,
                cantidad=cantidad,
                motivo=motivo
            )
            
            if resultado:
                flash(f'✅ Salida registrada: {cantidad} unidades', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('❌ Error al registrar salida', 'danger')
        except ValueError:
            flash('❌ Error: Datos inválidos', 'danger')
    
    return render_template('admin/inventario_salida.html', productos=productos)


# ==================== REPORTES ====================

@admin_bp.route('/reportes')
@login_required
def reportes():
    """Panel de reportes y estadísticas"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    # Obtener reportes
    total_dinero, total_transacciones = ReporteService.total_ventas_hoy()
    unidades_vendidas = ReporteService.unidades_vendidas_hoy()
    ventas_por_hora = ReporteService.ventas_por_hora()
    top_producto, top_categoria, top_unidades = ReporteService.producto_mas_vendido_semana()
    low_producto, low_categoria, low_unidades = ReporteService.producto_menos_vendido_semana()
    pagos_hoy = ReporteService.total_por_metodo_pago_hoy()
    promedio_venta = ReporteService.promedio_venta_hoy()
    hora_pico = ReporteService.hora_pico_hoy()
    metodo_preferido = ReporteService.metodo_pago_preferido_hoy()
    
    return render_template('admin/reportes.html',
                         total_dinero=total_dinero,
                         total_transacciones=total_transacciones,
                         unidades_vendidas=unidades_vendidas,
                         ventas_por_hora=ventas_por_hora,
                         top_producto=top_producto,
                         top_categoria=top_categoria,
                         top_unidades=top_unidades,
                         low_producto=low_producto,
                         low_categoria=low_categoria,
                         low_unidades=low_unidades,
                         pagos_hoy=pagos_hoy,
                         promedio_venta=promedio_venta,
                         hora_pico=hora_pico,
                         metodo_preferido=metodo_preferido,
                         apertura='08:00',
                         cierre='20:00',
                         on_duty={'nombre': current_user.nombre, 'rol': current_user.rol, 'horario': '08:00 - 20:00'})


# ==================== GESTIÓN DE GASTOS ====================

@admin_bp.route('/gastos', methods=['GET', 'POST'])
@login_required
def gastos():
    """Gestión de gastos"""
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('cashier.dashboard'))
    
    if request.method == 'POST':
        try:
            categoria = request.form.get('categoria')
            monto = float(request.form.get('monto'))
            descripcion = request.form.get('descripcion')
            
            resultado = GastoService.registrar_gasto(
                id_usuario=current_user.id_usuario,
                categoria=categoria,
                monto=monto,
                descripcion=descripcion
            )
            
            if resultado:
                flash(f'✅ Gasto registrado: ${monto:.2f}', 'success')
            else:
                flash('❌ Error al registrar gasto', 'danger')
        except ValueError:
            flash('❌ Error: Monto inválido', 'danger')
    
    resumen = GastoService.ver_resumen_gastos()
    gastos_lista = GastoService.listar_gastos()
    
    return render_template('admin/gastos.html', resumen=resumen, gastos=gastos_lista)