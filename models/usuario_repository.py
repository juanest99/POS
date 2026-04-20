from database.connection import conexion
from models.usuario import Usuario
from dataclasses import dataclass
from typing import Optional  

@dataclass
class UsuarioRepository:
    usuario: Optional[Usuario] = None  

    def guardar(self):
        if self.usuario is None:
            print("❌ No hay usuario para guardar")
            return False
        
        try:
            query = """INSERT INTO USUARIO(nombre, email, contrasena, estado, rol)
                       VALUES (%s, %s, %s, %s, %s)"""
            params = (self.usuario.nombre, self.usuario.email,
                      self.usuario.contrasena, self.usuario.estado, self.usuario.rol)
            conexion(query, params)
            print("✅ Usuario guardado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            return False
    
    @staticmethod
    def buscar(nombre, contrasena):
        try:
            query = "SELECT * FROM USUARIO WHERE nombre = %s AND contrasena = %s"
            resultados = conexion(query, (nombre, contrasena))
            return resultados
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return None
    
    @staticmethod
    def buscar_por_nombre(nombre):
        try:
            query = "SELECT * FROM USUARIO WHERE nombre = %s"
            resultados = conexion(query, (nombre,))
            return resultados
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return None