from Proxy.Login import Login
from Objects.registroUser import RegistroUser
from Objects.Usuario import Usuario
class LoginVerificar(Login):
    def login(self, nombre,contrasena):
        valores = RegistroUser.buscar(nombre,contrasena)
        if valores:
            fila = valores[0]
            usuario = Usuario(
                fila[1],
                fila[2],
                fila[3],
                fila[6],
                fila[5],
                fila[4]
            )
            return usuario

        else:
            print("no se encontro usuario")
            return None
