from database.connection import conexion
from typing import Optional, List

class CategoriaRepository:
    """Repositorio para operaciones con categorías"""
    
    @staticmethod
    def buscar_por_id(id_categoria: int) -> Optional[dict]:
        """Busca una categoría por su ID"""
        try:
            query = "SELECT * FROM CATEGORIAS WHERE id_categoria = %s"
            resultado = conexion(query, (id_categoria,))
            
            if resultado:
                return {
                    'id_categoria': resultado[0][0],
                    'nombre': resultado[0][1]
                }
            return None
        except Exception as e:
            print(f"❌ Error al buscar categoría: {e}")
            return None
    
    @staticmethod
    def listar_todas() -> List[dict]:
        """Lista todas las categorías"""
        try:
            query = "SELECT * FROM CATEGORIAS ORDER BY id_categoria"
            resultados = conexion(query, None)
            
            if resultados:
                return [{'id_categoria': r[0], 'nombre': r[1]} for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar categorías: {e}")
            return []