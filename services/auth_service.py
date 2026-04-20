from typing import Optional, Any, Tuple
from middleware.auth_interface import AuthInterface
from models.usuario_repository import UsuarioRepository
from models.usuario import Usuario

class AuthService(AuthInterface):
    def login(self, nombre: str, contrasena: str) -> Optional[Usuario]:
        valores = UsuarioRepository.buscar(nombre, contrasena)
        
        if valores and len(valores) > 0:
            fila: Tuple[Any, ...] = valores[0]  
            
            if len(fila) < 7:
                print(f"❌ Error: La consulta retornó {len(fila)} columnas, se esperaban al menos 7")
                return None
            
            usuario = Usuario(
                _nombre=fila[1],
                _email=fila[2],
                _contrasena=fila[3],
                _rol=fila[6] if len(fila) > 6 else "",
                _fecha=fila[5] if len(fila) > 5 else "",
                _estado=fila[4]
            )
            return usuario
        else:
            print("❌ No se encontró usuario")
            return None