from typing import Optional
from middleware.auth_interface import AuthInterface
from models.usuario_repository import UsuarioRepository
from models.usuario import Usuario

class AuthService(AuthInterface):
    def login(self, nombre: str, contrasena: str) -> Optional[Usuario]:
        valores = UsuarioRepository.buscar(nombre, contrasena)
        
        if valores:
            fila = valores[0]
            # Crear objeto Usuario con todos los campos incluyendo id_usuario
            usuario = Usuario(
                _id_usuario=fila[0],  # ← AGREGAR id_usuario
                _nombre=fila[1],
                _email=fila[2],
                _contrasena=fila[3],
                _estado=fila[4],
                _fecha=fila[5],
                _rol=fila[6] if len(fila) > 6 else ""
            )
            return usuario
        else:
            print("❌ No se encontró usuario")
            return None