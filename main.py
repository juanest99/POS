#para probar nada mas
from Objects.Usuario import Usuario
from Objects.registroUser import RegistroUser
from Proxy.LoginVerificar import Login, LoginVerificar
from Proxy.proxyService import Proxy
from Proxy.realService import servicioReal

#TODO simulacion crear cliente
"""
nombre = input("ingresa tu nombre: ")
email = input("ingresa tu email: ")
contrasena = input("ingresa tu contraseña: ")
estado = input("ingresa tu estado (True/False): ") == "True"
rol = input("ingresa tu rol: ")

print(nombre, email, contrasena, estado, rol)

usuario = Usuario(nombre, email, contrasena, rol, "", estado)
registrar = RegistroUser(usuario)
registrar.guardar()
"""

# TODO simulacion de login de usuario

nombre = input("ingresa tu nombre: ")
contrasena = input("ingresa tu contraseña: ")


login = LoginVerificar()
usuario = login.login(nombre, contrasena)

print(usuario)
if usuario:
    servicio_real = servicioReal()
    proxy = Proxy(servicio_real)
    proxy.acceder(usuario, nombre, contrasena, usuario.rol)

else:
    print("pues como se va a ingrear sin usuarios jsjsjs ")

