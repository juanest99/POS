"""
CASHIER ROUTES - Panel de cajero
Maneja todas las rutas para el cajero del sistema
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from services.venta_service import VentaService
from services.producto_service import ProductoService
from services.reporte_service import ReporteService
from models.venta_repository import VentaRepository
from models.usuario_repository import UsuarioRepository
cashier_bp = Blueprint('cashier', __name__)

@cashier_bp.route('/')
@login_required
def dashboard():
    """Panel principal del cajero"""
    # Si es admin, redirigir a su panel
    if current_user.rol.lower() == 'admin':
        return redirect(url_for('admin.dashboard'))
    
    return render_template('cashier/dashboard.html',
                         apertura='08:00',
                         cierre='20:00')


@cashier_bp.route('/nueva-venta', methods=['GET', 'POST'])
@login_required
def nueva_venta():
    """Nueva venta - punto de venta principal"""
    # Si es admin, redirigir
    if current_user.rol.lower() == 'admin':
        flash('Los administradores no pueden realizar ventas', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    # Inicializar carrito en sesión si no existe
    if 'carrito' not in session:
        session['carrito'] = []
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'agregar':
            id_producto = int(request.form.get('id_producto'))
            cantidad = int(request.form.get('cantidad', 1))
            
            producto = ProductoService.buscar_producto(id_producto)
            if producto:
                encontrado = False
                for item in session['carrito']:
                    if item['id_producto'] == id_producto:
                        nueva_cantidad = item['cantidad'] + cantidad
                        if nueva_cantidad <= producto.stock:
                            item['cantidad'] = nueva_cantidad
                        else:
                            flash(f'Stock insuficiente. Stock disponible: {producto.stock}', 'warning')
                        encontrado = True
                        break
                
                if not encontrado and cantidad <= producto.stock:
                    session['carrito'].append({
                        'id_producto': id_producto,
                        'nombre': producto.nombre,
                        'precio': float(producto.precio),
                        'cantidad': cantidad
                    })
                elif not encontrado:
                    flash(f'Stock insuficiente para {producto.nombre}', 'warning')
                
                session.modified = True
                flash(f'✅ {producto.nombre} agregado al carrito', 'success')
            else:
                flash('❌ Producto no encontrado', 'danger')
        
        elif action == 'quitar':
            id_producto = int(request.form.get('id_producto'))
            session['carrito'] = [item for item in session['carrito'] if item['id_producto'] != id_producto]
            session.modified = True
            flash('✅ Producto eliminado del carrito', 'success')
        
        elif action == 'actualizar_cantidad':
            id_producto = int(request.form.get('id_producto'))
            nueva_cantidad = int(request.form.get('cantidad'))
            
            for item in session['carrito']:
                if item['id_producto'] == id_producto:
                    producto = ProductoService.buscar_producto(id_producto)
                    if nueva_cantidad <= producto.stock:
                        item['cantidad'] = nueva_cantidad
                        flash('✅ Cantidad actualizada', 'success')
                    else:
                        flash(f'⚠️ Stock insuficiente. Máximo: {producto.stock}', 'warning')
                    break
            session.modified = True
        
        elif action == 'vaciar':
            session['carrito'] = []
            session.modified = True
            flash('🛒 Carrito vaciado', 'info')
        
        elif action == 'procesar':
            if not session['carrito']:
                flash('❌ El carrito está vacío', 'warning')
                return redirect(url_for('cashier.nueva_venta'))
            
            metodo_pago = request.form.get('metodo_pago')
            monto_recibido = float(request.form.get('monto_recibido', 0))
            total = sum(item['precio'] * item['cantidad'] for item in session['carrito'])
            
            if monto_recibido < total:
                flash(f'❌ Monto insuficiente. Total: ${total:.2f}', 'danger')
                return redirect(url_for('cashier.nueva_venta'))
            
            venta_service = VentaService()
            
            for item in session['carrito']:
                venta_service.agregar_al_carrito(item['id_producto'], item['cantidad'])
            
            id_venta = venta_service.procesar_pago(
                id_usuario=current_user.id_usuario,
                metodo_pago=metodo_pago,
                monto_recibido=monto_recibido
            )
            
            if id_venta:
                session['carrito'] = []
                session.modified = True
                
                flash(f'✅ Venta #{id_venta} completada exitosamente. Cambio: ${monto_recibido - total:.2f}', 'success')
                return redirect(url_for('cashier.venta_exitosa', id_venta=id_venta))
            else:
                flash('❌ Error al procesar la venta', 'danger')
    
    carrito_con_detalle = []
    total_carrito = 0
    for item in session.get('carrito', []):
        subtotal = item['precio'] * item['cantidad']
        total_carrito += subtotal
        carrito_con_detalle.append({
            **item,
            'subtotal': subtotal
        })
    
    productos = ProductoService.listar_productos()
    
    return render_template('cashier/nueva_venta.html',
                         carrito=carrito_con_detalle,
                         total=total_carrito,
                         productos=productos)


@cashier_bp.route('/venta-exitosa/<int:id_venta>')
@login_required
def venta_exitosa(id_venta):
    """Mostrar página de venta exitosa"""
    return render_template('cashier/venta_exitosa.html', id_venta=id_venta)


@cashier_bp.route('/buscar-producto')
@login_required
def buscar_producto():
    """API: Buscar productos por nombre o código"""
    query = request.args.get('q', '')
    productos = ProductoService.listar_productos()
    
    resultados = []
    for p in productos:
        if query.lower() in p.nombre.lower() or query == str(p.id_producto):
            resultados.append({
                'id': p.id_producto,
                'nombre': p.nombre,
                'precio': float(p.precio),
                'stock': p.stock
            })
    
    return jsonify(resultados)


@cashier_bp.route('/historial')
@login_required
def historial():
    """Historial de ventas del cajero"""
    ventas = VentaRepository.listar_por_usuario(current_user.id_usuario, limite=50)
    return render_template('cashier/historial.html', ventas=ventas)


@cashier_bp.route('/estadisticas')
@login_required
def estadisticas():
    """Estadísticas del día para el cajero (solo sus ventas)"""  
    ventas_hoy = VentaRepository.obtener_ventas_hoy()
    ventas_cajero = [v for v in ventas_hoy if v.id_usuario == current_user.id_usuario]
    
    total_hoy = sum(v.total for v in ventas_cajero)
    
    stats = {
        'ventas_hoy': len(ventas_cajero),
        'total_hoy': total_hoy,
        'promedio_hoy': total_hoy / len(ventas_cajero) if ventas_cajero else 0
    }
    
    return render_template('cashier/estadisticas.html', stats=stats)

@cashier_bp.route('/confirmacion', methods =['POST'])
@login_required
def registrar():
    
    usuario = UsuarioRepository.buscar_por_nombre(current_user.nombre)

    metodo_pago = request.form['metodo_pago']
    total = float(request.form['total'])
    monto = float(request.form['monto_recibido'])

    carrito = session.get('carrito',[])
    #print('este es el carrito xd', carrito)
    #print('id del usuario', usuario[0][0])
   
    venta = VentaService.procesar_pagotest(
        usuario=usuario[0][0],
        metodo_pago=metodo_pago,
        monto=monto,
        total = total,
        carrito=carrito)
    
    return render_template('cashier/venta_exitosa.html')