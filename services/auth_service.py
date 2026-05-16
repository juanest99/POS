from typing import Optional
from middleware.auth_interface import AuthInterface
from models.usuario_repository import UsuarioRepository
from models.usuario import Usuario

class AuthService(AuthInterface):
    def login(self, nombre: str, contrasena: str) -> Optional[Usuario]:
        valores = UsuarioRepository.buscar(nombre, contrasena)
        
        if valores:
            fila = valores[0]
            # La estructura: id_usuario, nombre, email, contrasena, estado, fecha, rol
            usuario = Usuario(
                _id_usuario=fila[0],
                _nombre=fila[1],
                _email=fila[2],
                _contrasena=fila[3],
                _estado=fila[4] if len(fila) > 4 else True,
                _fecha=fila[5] if len(fila) > 5 else None,
                _rol=fila[6].lower() if len(fila) > 6 and fila[6] else "cajero"
            )
            return usuario
        else:
            return None