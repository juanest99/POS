from typing import Optional, List, Tuple
from models.movimiento_inventario import MovimientoInventario
from models.movimiento_repository import MovimientoRepository
from models.producto_repository import ProductoRepository
from models.usuario_repository import UsuarioRepository

class InventarioService:
    """Servicio con la lógica de negocio para inventario"""
    
    @staticmethod
    def registrar_entrada(id_producto: int, id_usuario: int, cantidad: int, motivo: str = "compra") -> Optional[MovimientoInventario]:
        """
        REGISTRAR ENTRADA: Cuando llega mercancía nueva
        Reglas:
        1. Producto debe existir
        2. Usuario debe existir
        3. Cantidad debe ser positiva
        4. Motivo válido: 'compra', 'devolucion_proveedor', 'ajuste_inventario'
        """
        
        # Regla 1: Validar producto
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Error: Producto con ID {id_producto} no existe")
            return None
        
        # Regla 2: Validar usuario
        usuario = UsuarioRepository.buscar_por_id(id_usuario)
        if not usuario:
            print(f"❌ Error: Usuario con ID {id_usuario} no existe")
            return None
        
        # Regla 3: Validar cantidad
        if cantidad <= 0:
            print("❌ Error: La cantidad debe ser mayor a 0")
            return None
        
        # Regla 4: Validar motivo
        motivos_validos = ['compra', 'devolucion_proveedor', 'ajuste_inventario']
        if motivo not in motivos_validos:
            print(f"❌ Error: Motivo '{motivo}' no válido. Use: {motivos_validos}")
            return None
        
        # Crear movimiento
        movimiento = MovimientoInventario(
            _id_producto=id_producto,
            _id_usuario=id_usuario,
            _tipo="entrada",
            _cantidad=cantidad,
            _motivo=motivo
        )
        
        # Guardar movimiento
        movimiento_guardado = MovimientoRepository.guardar(movimiento)
        
        if movimiento_guardado:
            # Actualizar stock en la tabla PRODUCTO
            stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
            ProductoRepository.actualizar_stock(id_producto, stock_actual)
            if producto.nombre:
                print(f"📦 Stock actual de '{producto.nombre}': {stock_actual} unidades")
        
        return movimiento_guardado
    
    @staticmethod
    def registrar_salida(id_producto: int, id_usuario: int, cantidad: int, motivo: str = "venta") -> Optional[MovimientoInventario]:
        """
        REGISTRAR SALIDA: Cuando se vende o se retira mercancía
        Reglas:
        1. Producto debe existir
        2. Usuario debe existir
        3. Cantidad debe ser positiva
        4. NO puede haber stock negativo
        5. Motivo válido: 'venta', 'merma', 'devolucion_cliente', 'ajuste_inventario'
        """
        
        # Regla 1: Validar producto
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Error: Producto con ID {id_producto} no existe")
            return None
        
        # Regla 2: Validar usuario
        usuario = UsuarioRepository.buscar_por_id(id_usuario)
        if not usuario:
            print(f"❌ Error: Usuario con ID {id_usuario} no existe")
            return None
        
        # Regla 3: Validar cantidad
        if cantidad <= 0:
            print("❌ Error: La cantidad debe ser mayor a 0")
            return None
        
        # Regla 4: Validar stock suficiente
        stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
        if stock_actual < cantidad:
            print(f"❌ Error: Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}")
            return None
        
        # Regla 5: Validar motivo
        motivos_validos = ['venta', 'merma', 'devolucion_cliente', 'ajuste_inventario']
        if motivo not in motivos_validos:
            print(f"❌ Error: Motivo '{motivo}' no válido. Use: {motivos_validos}")
            return None
        
        # Crear movimiento
        movimiento = MovimientoInventario(
            _id_producto=id_producto,
            _id_usuario=id_usuario,
            _tipo="salida",
            _cantidad=cantidad,
            _motivo=motivo
        )
        
        # Guardar movimiento
        movimiento_guardado = MovimientoRepository.guardar(movimiento)
        
        if movimiento_guardado:
            # Actualizar stock en la tabla PRODUCTO
            stock_nuevo = stock_actual - cantidad
            ProductoRepository.actualizar_stock(id_producto, stock_nuevo)
            if producto.nombre:
                print(f"📦 Stock actual de '{producto.nombre}': {stock_nuevo} unidades")
        
        return movimiento_guardado
    
    @staticmethod
    def registrar_ajuste(id_producto: int, id_usuario: int, nueva_cantidad: int, motivo: str = "ajuste_fisico") -> Optional[MovimientoInventario]:
        """
        REGISTRAR AJUSTE: Para corregir diferencias entre sistema y físico
        Reglas:
        1. Producto debe existir
        2. Usuario debe existir
        3. Calcula diferencia y crea movimiento automático
        """
        
        # Regla 1: Validar producto
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Error: Producto con ID {id_producto} no existe")
            return None
        
        # Regla 2: Validar usuario
        usuario = UsuarioRepository.buscar_por_id(id_usuario)
        if not usuario:
            print(f"❌ Error: Usuario con ID {id_usuario} no existe")
            return None
        
        # Regla 3: Validar nueva cantidad
        if nueva_cantidad < 0:
            print("❌ Error: La cantidad no puede ser negativa")
            return None
        
        # Calcular diferencia
        stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
        diferencia = nueva_cantidad - stock_actual
        
        if diferencia == 0:
            print("ℹ️ No hay diferencia. El stock ya está correcto.")
            return None
        
        # Determinar tipo de movimiento según la diferencia
        tipo = "entrada" if diferencia > 0 else "salida"
        cantidad_abs = abs(diferencia)
        
        print(f"📊 Ajuste detectado: Stock actual: {stock_actual}, Nuevo stock: {nueva_cantidad}")
        print(f"   Diferencia: {diferencia} unidades ({tipo})")
        
        # Crear movimiento
        movimiento = MovimientoInventario(
            _id_producto=id_producto,
            _id_usuario=id_usuario,
            _tipo=tipo,
            _cantidad=cantidad_abs,
            _motivo=motivo
        )
        
        # Guardar movimiento
        movimiento_guardado = MovimientoRepository.guardar(movimiento)
        
        if movimiento_guardado:
            # Actualizar stock en la tabla PRODUCTO
            ProductoRepository.actualizar_stock(id_producto, nueva_cantidad)
            if producto.nombre:
                print(f"✅ Stock ajustado a {nueva_cantidad} unidades")
        
        return movimiento_guardado
    
    @staticmethod
    def consultar_stock(id_producto: int) -> Tuple[Optional[int], str]:
        """
        Consulta el stock actual de un producto
        Retorna (stock, nombre_producto)
        """
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            return None, ""
        
        stock = MovimientoRepository.calcular_stock_actual(id_producto)
        nombre = producto.nombre if producto.nombre else ""
        return stock, nombre
    
    @staticmethod
    def ver_historial_producto(id_producto: int):
        """
        Muestra el historial completo de movimientos de un producto
        """
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Producto con ID {id_producto} no existe")
            return
        
        movimientos = MovimientoRepository.listar_por_producto(id_producto)
        
        nombre_producto = producto.nombre if producto.nombre else "Producto"
        
        if not movimientos:
            print(f"📦 No hay movimientos registrados para '{nombre_producto}'")
            return
        
        print(f"\n{'='*80}")
        print(f"HISTORIAL DE MOVIMIENTOS - {nombre_producto}")
        print(f"{'='*80}")
        print(f"{'ID':<6} {'FECHA':<12} {'TIPO':<10} {'CANTIDAD':<10} {'MOTIVO':<20}")
        print(f"{'-'*80}")
        
        for m in movimientos:
            fecha_str = m.fecha.strftime("%Y-%m-%d") if m.fecha else "N/A"
            signo = "+" if m.tipo == "entrada" else "-"
            print(f"{m.id_movimiento:<6} {fecha_str:<12} {m.tipo:<10} {signo}{m.cantidad:<9} {m.motivo:<20}")
        
        print(f"{'='*80}")
        stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
        print(f"📦 STOCK ACTUAL: {stock_actual} unidades")
    
    @staticmethod
    def ver_resumen_general():
        """
        Muestra un resumen general del inventario
        """
        print(f"\n{'='*60}")
        print("RESUMEN GENERAL DE INVENTARIO")
        print(f"{'='*60}")
        
        resumen = MovimientoRepository.obtener_resumen_por_tipo()
        
        print(f"📊 Movimientos registrados:")
        print(f"   🟢 Entradas: {resumen['entrada']} unidades")
        print(f"   🔴 Salidas:  {resumen['salida']} unidades")
        print(f"   🟡 Ajustes:  {resumen['ajuste']} unidades")
        
        # Listar productos con stock bajo
        print(f"\n📋 PRODUCTOS CON STOCK BAJO (< 10 unidades):")
        productos = ProductoRepository.listar_todos()
        productos_bajo_stock = []
        
        for p in productos:
            # Asegurar que id_producto no es None
            if p.id_producto is not None:
                stock = MovimientoRepository.calcular_stock_actual(p.id_producto)
                if stock < 10:
                    nombre = p.nombre if p.nombre else "Sin nombre"
                    productos_bajo_stock.append((nombre, stock))
        
        if productos_bajo_stock:
            for nombre, stock in productos_bajo_stock:
                print(f"   ⚠️ {nombre}: {stock} unidades")
        else:
            print("   ✅ Todos los productos tienen stock suficiente")