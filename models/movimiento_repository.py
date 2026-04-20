from database.connection import conexion
from models.movimiento_inventario import MovimientoInventario
from typing import List, Optional

class MovimientoRepository:
    """Repositorio para operaciones de movimientos de inventario"""
    
    @staticmethod
    def _tupla_a_movimiento(tupla: tuple) -> MovimientoInventario:
        """MÉTODO PRIVADO: Convierte una tupla de la BD en un objeto MovimientoInventario"""
        return MovimientoInventario(
            _id_movimiento=tupla[0],
            _id_producto=tupla[1],
            _id_usuario=tupla[2],
            _tipo=tupla[3],
            _cantidad=tupla[4],
            _motivo=tupla[5],
            _fecha=tupla[6]
        )
    
    @staticmethod
    def guardar(movimiento: MovimientoInventario) -> Optional[MovimientoInventario]:
        """
        INSERT: Guarda un movimiento de inventario en la base de datos
        """
        try:
            query = """
                INSERT INTO MOVIMIENTO_INVENTARIO 
                (id_producto, id_usuario, tipo, cantidad, motivo)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """
            params = (
                movimiento.id_producto,
                movimiento.id_usuario,
                movimiento.tipo,
                movimiento.cantidad,
                movimiento.motivo
            )
            resultado = conexion(query, params)
            
            if resultado:
                print(f"✅ Movimiento registrado: {movimiento.tipo} de {movimiento.cantidad} unidades")
                return MovimientoRepository._tupla_a_movimiento(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al guardar movimiento: {e}")
            return None
    
    @staticmethod
    def listar_por_producto(id_producto: int) -> List[MovimientoInventario]:
        """
        SELECT: Obtiene todos los movimientos de un producto específico
        """
        try:
            query = """
                SELECT * FROM MOVIMIENTO_INVENTARIO 
                WHERE id_producto = %s
                ORDER BY fecha DESC
            """
            resultados = conexion(query, (id_producto,))
            
            if resultados:
                return [MovimientoRepository._tupla_a_movimiento(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar movimientos: {e}")
            return []
    
    @staticmethod
    def listar_todos(limite: int = 50) -> List[MovimientoInventario]:
        """
        SELECT: Obtiene los últimos movimientos (últimos 50 por defecto)
        """
        try:
            query = """
                SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
                FROM MOVIMIENTO_INVENTARIO m
                JOIN PRODUCTO p ON m.id_producto = p.id_producto
                JOIN USUARIO u ON m.id_usuario = u.id_usuario
                ORDER BY m.fecha DESC
                LIMIT %s
            """
            resultados = conexion(query, (limite,))
            
            if resultados:
                return [MovimientoRepository._tupla_a_movimiento(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar movimientos: {e}")
            return []
    
    @staticmethod
    def calcular_stock_actual(id_producto: int) -> int:
        """
        Calcula el stock actual de un producto sumando todos los movimientos
        Entradas (+cantidad), Salidas (-cantidad)
        """
        try:
            query = """
                SELECT 
                    SUM(CASE WHEN tipo = 'entrada' THEN cantidad ELSE 0 END) -
                    SUM(CASE WHEN tipo = 'salida' THEN cantidad ELSE 0 END) as stock_actual
                FROM MOVIMIENTO_INVENTARIO
                WHERE id_producto = %s
            """
            resultado = conexion(query, (id_producto,))
            
            if resultado and resultado[0][0] is not None:
                return resultado[0][0]
            return 0
        except Exception as e:
            print(f"❌ Error al calcular stock: {e}")
            return 0
    
    @staticmethod
    def obtener_resumen_por_tipo(id_producto: Optional[int] = None) -> dict:
        """
        Obtiene resumen de movimientos agrupados por tipo
        id_producto puede ser None para resumen general
        """
        try:
            if id_producto is not None:
                query = """
                    SELECT tipo, COUNT(*) as total_movimientos, SUM(cantidad) as total_unidades
                    FROM MOVIMIENTO_INVENTARIO
                    WHERE id_producto = %s
                    GROUP BY tipo
                """
                resultados = conexion(query, (id_producto,))
            else:
                query = """
                    SELECT tipo, COUNT(*) as total_movimientos, SUM(cantidad) as total_unidades
                    FROM MOVIMIENTO_INVENTARIO
                    GROUP BY tipo
                """
                resultados = conexion(query, None)
            
            resumen = {'entrada': 0, 'salida': 0, 'ajuste': 0}
            if resultados:
                for r in resultados:
                    resumen[r[0]] = r[2]  # total_unidades
            return resumen
        except Exception as e:
            print(f"❌ Error al obtener resumen: {e}")
            return {'entrada': 0, 'salida': 0, 'ajuste': 0}
