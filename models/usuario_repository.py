from database.connection import conexion
from models.usuario import Usuario
from typing import Optional, Any

class UsuarioRepository:
    
    @staticmethod
    def guardar(usuario: Usuario) -> bool:
        try:
            query = """INSERT INTO USUARIO(nombre, email, contrasena, estado, rol)
                       VALUES (%s, %s, %s, %s, %s)"""
            params = (usuario.nombre, usuario.email,
                      usuario.contrasena, usuario.estado, usuario.rol)
            conexion(query, params)
            print("✅ Usuario guardado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            return False
    
    @staticmethod
    def buscar(nombre: str, contrasena: str) -> Optional[list]:
        try:
            query = "SELECT * FROM USUARIO WHERE nombre = %s AND contrasena = %s"
            resultados = conexion(query, (nombre, contrasena))
            return resultados
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return None
    
    @staticmethod
    def buscar_por_nombre(nombre: str) -> Optional[list]:
        try:
            query = "SELECT * FROM USUARIO WHERE nombre = %s"
            resultados = conexion(query, (nombre,))
            return resultados
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id_usuario: int) -> Optional[Usuario]:
        """Busca usuario por ID"""
        try:
            from models.usuario import Usuario
            query = "SELECT * FROM USUARIO WHERE id_usuario = %s"
            resultados = conexion(query, (id_usuario,))
            if resultados:
                # Convertir a lista para acceder por índice fácilmente
                fila = list(resultados[0])
                
                # Asegurar que la lista tenga suficientes elementos
                while len(fila) < 7:
                    fila.append("")  # Rellenar con valores vacíos si faltan
                
                return Usuario(
                    _nombre=fila[1],
                    _email=fila[2],
                    _contrasena=fila[3],
                    _rol=fila[6] if len(fila) > 6 else "",
                    _fecha=fila[5] if len(fila) > 5 else "",
                    _estado=fila[4]
                )
            return None
        except Exception as e:
            print(f"❌ Error en búsqueda por ID: {e}")
            return None