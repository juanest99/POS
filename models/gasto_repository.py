from database.connection import conexion
from models.gasto import Gasto
from typing import List, Optional
from datetime import date

class GastoRepository:
    """Repositorio para operaciones de gastos"""
    
    @staticmethod
    def _tupla_a_gasto(tupla: tuple) -> Gasto:
        """Convierte una tupla de BD en objeto Gasto"""
        # Tu estructura: id_gasto, id_usuario, monto, descripcion, fecha
        return Gasto(
            _id_gasto=tupla[0],
            _id_usuario=tupla[1],
            _monto=float(tupla[2]) if tupla[2] else 0.0,
            _descripcion=tupla[3] if len(tupla) > 3 else "",
            _fecha=tupla[4] if len(tupla) > 4 else None
        )
    
    @staticmethod
    def guardar(gasto: Gasto) -> Optional[Gasto]:
        """Guarda un nuevo gasto en la base de datos"""
        try:
            query = """
                INSERT INTO GASTO (id_usuario, monto, descripcion)
                VALUES (%s, %s, %s)
                RETURNING *
            """
            params = (
                gasto.id_usuario,
                gasto.monto,
                gasto.descripcion
            )
            resultado = conexion(query, params)
            
            if resultado:
                print(f"✅ Gasto registrado: ${gasto.monto:.2f} - {gasto.descripcion[:30]}")
                return GastoRepository._tupla_a_gasto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al guardar gasto: {e}")
            return None
    
    @staticmethod
    def listar_por_fecha(fecha_inicio: date, fecha_fin: date) -> List[Gasto]:
        """Lista gastos en un rango de fechas"""
        try:
            query = """
                SELECT * FROM GASTO 
                WHERE DATE(fecha) BETWEEN %s AND %s
                ORDER BY fecha DESC
            """
            resultados = conexion(query, (fecha_inicio, fecha_fin))
            if resultados:
                return [GastoRepository._tupla_a_gasto(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar gastos por fecha: {e}")
            return []
    
    @staticmethod
    def listar_todos(limite: int = 100) -> List[Gasto]:
        """Lista los últimos gastos"""
        try:
            query = """
                SELECT g.*, u.nombre as usuario_nombre
                FROM GASTO g
                JOIN USUARIO u ON g.id_usuario = u.id_usuario
                ORDER BY g.fecha DESC
                LIMIT %s
            """
            resultados = conexion(query, (limite,))
            if resultados:
                return [GastoRepository._tupla_a_gasto(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar gastos: {e}")
            return []
    
    @staticmethod
    def obtener_total_gastos(fecha_inicio: date, fecha_fin: date) -> float:
        """Obtiene el total de gastos en un período"""
        try:
            query = """
                SELECT COALESCE(SUM(monto), 0) as total
                FROM GASTO
                WHERE DATE(fecha) BETWEEN %s AND %s
            """
            resultado = conexion(query, (fecha_inicio, fecha_fin))
            if resultado and resultado[0][0] is not None:
                return float(resultado[0][0])
            return 0.0
        except Exception as e:
            print(f"❌ Error al obtener total de gastos: {e}")
            return 0.0