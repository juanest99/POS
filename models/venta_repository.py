from database.connection import conexion
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from typing import List, Optional

class VentaRepository:
    """Repositorio para operaciones de ventas"""
    
    @staticmethod
    def _tupla_a_venta(tupla: tuple) -> Venta:
        """Convierte una tupla de BD en objeto Venta"""
        return Venta(
            _id_venta=tupla[0],
            _id_usuario=tupla[1],
            _metodo_pago=tupla[2],
            _total=float(tupla[3]),
            _monto_recibido=float(tupla[4]),
            _cambio=float(tupla[5]),
            _fecha=tupla[6]
        )
    
    @staticmethod
    def guardar(venta: Venta, detalles: List[DetalleVenta]) -> Optional[int]:
        """
        Guarda una venta y sus detalles en la base de datos
        Retorna el ID de la venta creada
        """
        try:
            # 1. Insertar la venta
            query_venta = """
                INSERT INTO VENTA (id_usuario, metodo_pago, total, monto_recibido, cambio)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_venta
            """
            params_venta = (venta.id_usuario, venta.metodo_pago, 
                           venta.total, venta.monto_recibido, venta.cambio)
            resultado = conexion(query_venta, params_venta)
            
            if not resultado:
                print("❌ Error al guardar la venta")
                return None
            
            id_venta = resultado[0][0]
            
            # 2. Insertar los detalles de la venta (sin subtotal porque es GENERATED)
            query_detalle = """
                INSERT INTO DETALLE_VENTA (id_producto, id_venta, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            
            for detalle in detalles:
                detalle.id_venta = id_venta
                params_detalle = (detalle.id_producto, detalle.id_venta,
                                  detalle.cantidad, detalle.precio_unitario)
                conexion(query_detalle, params_detalle)
            
            print(f"✅ Venta #{id_venta} registrada exitosamente")
            return id_venta
            
        except Exception as e:
            print(f"❌ Error al guardar venta: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id_venta: int) -> Optional[Venta]:
        """Busca una venta por su ID"""
        try:
            query = "SELECT * FROM VENTA WHERE id_venta = %s"
            resultado = conexion(query, (id_venta,))
            if resultado:
                return VentaRepository._tupla_a_venta(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al buscar venta: {e}")
            return None
    
    @staticmethod
    def listar_por_usuario(id_usuario: int, limite: int = 20) -> List[Venta]:
        """Lista las ventas de un usuario específico"""
        try:
            query = """
                SELECT * FROM VENTA 
                WHERE id_usuario = %s 
                ORDER BY fecha DESC 
                LIMIT %s
            """
            resultados = conexion(query, (id_usuario, limite))
            if resultados:
                return [VentaRepository._tupla_a_venta(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar ventas: {e}")
            return []
    
    @staticmethod
    def listar_todas(limite: int = 50) -> List[Venta]:
        """Lista las últimas ventas"""
        try:
            query = """
                SELECT v.*, u.nombre as usuario_nombre
                FROM VENTA v
                JOIN USUARIO u ON v.id_usuario = u.id_usuario
                ORDER BY v.fecha DESC
                LIMIT %s
            """
            resultados = conexion(query, (limite,))
            if resultados:
                return [VentaRepository._tupla_a_venta(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar ventas: {e}")
            return []
    
    @staticmethod
    def obtener_detalles(id_venta: int) -> List[DetalleVenta]:
        """Obtiene los detalles de una venta"""
        try:
            query = """
                SELECT dv.id_producto, dv.id_venta, dv.cantidad, dv.precio_unitario, dv.subtotal, p.nombre as producto_nombre
                FROM DETALLE_VENTA dv
                JOIN PRODUCTO p ON dv.id_producto = p.id_producto
                WHERE dv.id_venta = %s
            """
            resultados = conexion(query, (id_venta,))
            
            detalles = []
            if resultados:
                for r in resultados:
                    detalle = DetalleVenta(
                        _id_producto=r[0],
                        _id_venta=r[1],
                        _cantidad=r[2],
                        _precio_unitario=float(r[3]),
                        _subtotal=float(r[4]) if r[4] else 0.0
                    )
                    detalles.append(detalle)
            return detalles
        except Exception as e:
            print(f"❌ Error al obtener detalles: {e}")
            return []
    
    @staticmethod
    def obtener_ventas_hoy() -> List[Venta]:
        """Obtiene las ventas del día actual"""
        try:
            query = """
                SELECT * FROM VENTA 
                WHERE DATE(fecha) = CURRENT_DATE
                ORDER BY fecha DESC
            """
            resultados = conexion(query, None)
            if resultados:
                return [VentaRepository._tupla_a_venta(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al obtener ventas de hoy: {e}")
            return []
    
    @staticmethod
    def obtener_total_ventas_hoy() -> float:
        """Obtiene el total de ventas del día"""
        try:
            query = "SELECT COALESCE(SUM(total), 0) FROM VENTA WHERE DATE(fecha) = CURRENT_DATE"
            resultado = conexion(query, None)
            if resultado and resultado[0][0]:
                return float(resultado[0][0])
            return 0.0
        except Exception as e:
            print(f"❌ Error al obtener total de ventas: {e}")
            return 0.0