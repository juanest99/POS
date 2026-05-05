from database.connection import conexion
from models.gasto import Gasto
from typing import List, Optional

class GastoRepository:
    """Repositorio para operaciones CRUD de gastos"""
    
    @staticmethod
    def _tupla_a_gasto(tupla: tuple) -> Gasto:
        # Orden esperado: id_gasto, id_usuario, categoria, monto, descripcion, fecha
        return Gasto(
            _id_gasto=tupla[0],
            _id_usuario=tupla[1],
            _categoria=tupla[2],
            _monto=float(tupla[3]),
            _descripcion=tupla[4],
            _fecha=tupla[5]
        )
    
    @staticmethod
    def crear(gasto: Gasto) -> Optional[Gasto]:
        try:
            query = """
                INSERT INTO GASTO (id_usuario, categoria, monto, descripcion)
                VALUES (%s, %s, %s, %s)
                RETURNING id_gasto, id_usuario, categoria, monto, descripcion, fecha
            """
            params = (gasto.id_usuario, gasto.categoria, gasto.monto, gasto.descripcion)
            resultado = conexion(query, params)
            if resultado:
                print(f"✅ Gasto registrado: {gasto.categoria} - ${gasto.monto:.2f}")
                return GastoRepository._tupla_a_gasto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al crear gasto: {e}")
            return None
    
    @staticmethod
    def listar_todos(limite: int = 100) -> List[Gasto]:
        try:
            query = """
                SELECT g.id_gasto, g.id_usuario, g.categoria, g.monto, g.descripcion, g.fecha
                FROM GASTO g
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
    def listar_por_periodo(fecha_desde: str, fecha_hasta: str) -> List[Gasto]:
        try:
            query = """
                SELECT id_gasto, id_usuario, categoria, monto, descripcion, fecha
                FROM GASTO
                WHERE fecha BETWEEN %s AND %s
                ORDER BY fecha DESC
            """
            resultados = conexion(query, (fecha_desde, fecha_hasta))
            if resultados:
                return [GastoRepository._tupla_a_gasto(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar gastos por periodo: {e}")
            return []
    
    @staticmethod
    def obtener_total_por_categoria(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> dict:
        try:
            if fecha_desde is not None and fecha_hasta is not None:
                query = """
                    SELECT categoria, SUM(monto) as total
                    FROM GASTO
                    WHERE fecha BETWEEN %s AND %s
                    GROUP BY categoria
                """
                resultados = conexion(query, (fecha_desde, fecha_hasta))
            else:
                query = """
                    SELECT categoria, SUM(monto) as total
                    FROM GASTO
                    GROUP BY categoria
                """
                resultados = conexion(query, None)
            
            totales = {}
            if resultados:
                for r in resultados:
                    totales[r[0]] = float(r[1])
            return totales
        except Exception as e:
            print(f"❌ Error al obtener total por categoría: {e}")
            return {}
    
    @staticmethod
    def obtener_total_gastos(fecha_desde: Optional[str] = None, fecha_hasta: Optional[str] = None) -> float:
        try:
            if fecha_desde is not None and fecha_hasta is not None:
                query = "SELECT COALESCE(SUM(monto), 0) FROM GASTO WHERE fecha BETWEEN %s AND %s"
                resultado = conexion(query, (fecha_desde, fecha_hasta))
            else:
                query = "SELECT COALESCE(SUM(monto), 0) FROM GASTO"
                resultado = conexion(query, None)
            
            if resultado and resultado[0][0]:
                return float(resultado[0][0])
            return 0.0
        except Exception as e:
            print(f"❌ Error al obtener total gastos: {e}")
            return 0.0