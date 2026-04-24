from typing import List, Tuple, Optional
from models.producto_repository import ProductoRepository
from models.venta_repository import VentaRepository
from models.movimiento_repository import MovimientoRepository
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from services.inventario_service import InventarioService

class CarritoItem:
    """Item del carrito de compras"""
    def __init__(self, id_producto: int, nombre: str, precio: float, cantidad: int = 1):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
    
    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio

class VentaService:
    """Servicio con la lógica de negocio para ventas"""
    
    def __init__(self):
        self.carrito: List[CarritoItem] = []
    
    def agregar_al_carrito(self, id_producto: int, cantidad: int = 1) -> bool:
        """
        Agrega un producto al carrito
        Reglas:
        1. Producto debe existir
        2. Stock debe ser suficiente
        3. Cantidad debe ser positiva
        """
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Producto con ID {id_producto} no existe")
            return False
        
        if cantidad <= 0:
            print("❌ La cantidad debe ser mayor a 0")
            return False
        
        # Verificar stock disponible
        stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
        if stock_actual < cantidad:
            print(f"❌ Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}")
            return False
        
        # Buscar si ya está en el carrito
        for item in self.carrito:
            if item.id_producto == id_producto:
                nueva_cantidad = item.cantidad + cantidad
                if stock_actual < nueva_cantidad:
                    print(f"❌ Stock insuficiente para agregar más. Stock: {stock_actual}")
                    return False
                item.cantidad = nueva_cantidad
                print(f"✅ Actualizado: {item.nombre} x {item.cantidad}")
                return True
        
        # Agregar nuevo item
        self.carrito.append(CarritoItem(id_producto, producto.nombre, producto.precio, cantidad))
        print(f"✅ Agregado: {producto.nombre} x {cantidad}")
        return True
    
    def quitar_del_carrito(self, id_producto: int) -> bool:
        """Elimina un producto del carrito"""
        for i, item in enumerate(self.carrito):
            if item.id_producto == id_producto:
                nombre = item.nombre
                del self.carrito[i]
                print(f"✅ Eliminado: {nombre}")
                return True
        print(f"❌ Producto no encontrado en el carrito")
        return False
    
    def modificar_cantidad(self, id_producto: int, nueva_cantidad: int) -> bool:
        """Modifica la cantidad de un producto en el carrito"""
        if nueva_cantidad <= 0:
            return self.quitar_del_carrito(id_producto)
        
        for item in self.carrito:
            if item.id_producto == id_producto:
                # Verificar stock
                stock_actual = MovimientoRepository.calcular_stock_actual(id_producto)
                if stock_actual < nueva_cantidad:
                    print(f"❌ Stock insuficiente. Disponible: {stock_actual}")
                    return False
                item.cantidad = nueva_cantidad
                print(f"✅ Cantidad actualizada: {item.nombre} x {item.cantidad}")
                return True
        return False
    
    def ver_carrito(self) -> Tuple[List[CarritoItem], float]:
        """Muestra el carrito y retorna (items, total)"""
        if not self.carrito:
            print("\n🛒 El carrito está vacío")
            return [], 0.0
        
        print("\n" + "="*60)
        print("🛒 CARRITO DE COMPRAS")
        print("="*60)
        print(f"{'CANT':<6} {'PRODUCTO':<30} {'P.UNIT':<10} {'SUBTOTAL':<12}")
        print("-"*60)
        
        total = 0.0
        for item in self.carrito:
            subtotal = item.subtotal
            total += subtotal
            print(f"{item.cantidad:<6} {item.nombre:<30} ${item.precio:<10.2f} ${subtotal:<12.2f}")
        
        print("-"*60)
        print(f"{'TOTAL':<47} ${total:<12.2f}")
        print("="*60)
        
        return self.carrito, total
    
    def vaciar_carrito(self):
        """Vacía el carrito de compras"""
        self.carrito.clear()
        print("🛒 Carrito vaciado")
    
    def procesar_pago(self, id_usuario: int, metodo_pago: str, monto_recibido: float) -> Optional[int]:
        """
        Procesa el pago y registra la venta
        Reglas:
        1. El carrito no puede estar vacío
        2. El monto recibido debe ser >= total
        3. Se actualiza el stock automáticamente
        4. Se registra movimiento de inventario
        """
        if not self.carrito:
            print("❌ El carrito está vacío")
            return None
        
        _, total = self.ver_carrito()
        
        if monto_recibido < total:
            print(f"❌ Monto insuficiente. Total: ${total:.2f}, Recibido: ${monto_recibido:.2f}")
            return None
        
        cambio = monto_recibido - total
        
        # Crear objeto Venta
        venta = Venta(
            _id_usuario=id_usuario,
            _metodo_pago=metodo_pago,
            _total=total,
            _monto_recibido=monto_recibido,
            _cambio=cambio
        )
        
        # Crear detalles de venta
        detalles = []
        for item in self.carrito:
            detalle = DetalleVenta(
                _id_producto=item.id_producto,
                _cantidad=item.cantidad,
                _precio_unitario=item.precio
            )
            detalles.append(detalle)
        
        # Guardar la venta
        id_venta = VentaRepository.guardar(venta, detalles)
        
        if id_venta:
            # Actualizar stock y registrar movimientos
            for item in self.carrito:
                InventarioService.registrar_salida(
                    id_producto=item.id_producto,
                    id_usuario=id_usuario,
                    cantidad=item.cantidad,
                    motivo="venta"
                )
            
            print(f"\n💰 Venta completada!")
            print(f"   Total: ${total:.2f}")
            print(f"   Recibido: ${monto_recibido:.2f}")
            print(f"   Cambio: ${cambio:.2f}")
            print(f"   Método: {metodo_pago}")
            print(f"   Venta #: {id_venta}")
            
            # Vaciar carrito después de la venta
            self.vaciar_carrito()
        
        return id_venta
    
    @staticmethod
    def mostrar_factura(id_venta: int):
        """Muestra la factura de una venta"""
        venta = VentaRepository.buscar_por_id(id_venta)
        if not venta:
            print(f"❌ Venta #{id_venta} no encontrada")
            return
        
        detalles = VentaRepository.obtener_detalles(id_venta)
        
        print("\n" + "="*60)
        print(f"              FACTURA DE VENTA")
        print("="*60)
        print(f"Factura N°: {id_venta}")
        print(f"Fecha: {venta.fecha}")
        print(f"Método de pago: {venta.metodo_pago}")
        print("-"*60)
        print(f"{'CANT':<6} {'PRODUCTO':<30} {'P.UNIT':<10} {'SUBTOTAL':<12}")
        print("-"*60)
        
        for d in detalles:
            # Obtener nombre del producto
            from models.producto_repository import ProductoRepository
            producto = ProductoRepository.buscar_por_id(d.id_producto)
            nombre = producto.nombre if producto else f"ID:{d.id_producto}"
            print(f"{d.cantidad:<6} {nombre:<30} ${d.precio_unitario:<10.2f} ${d.subtotal:<12.2f}")
        
        print("-"*60)
        print(f"{'TOTAL':<47} ${venta.total:<12.2f}")
        print(f"{'MONTO RECIBIDO':<47} ${venta.monto_recibido:<12.2f}")
        print(f"{'CAMBIO':<47} ${venta.cambio:<12.2f}")
        print("="*60)
        print("              ¡GRACIAS POR SU COMPRA!")
        print("="*60)
    
    @staticmethod
    def obtener_estadisticas_rapidas() -> dict:
        """Obtiene estadísticas rápidas para el dashboard"""
        ventas_hoy = VentaRepository.obtener_ventas_hoy()
        total_hoy = sum(v.total for v in ventas_hoy)
        
        return {
            'ventas_hoy': len(ventas_hoy),
            'total_hoy': total_hoy,
            'promedio_hoy': total_hoy / len(ventas_hoy) if ventas_hoy else 0
        }