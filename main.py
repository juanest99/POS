from services.auth_service import AuthService
from middleware.real_service import RealService
from middleware.access_proxy import AccessProxy

def main():
    print("=== SISTEMA POS ===\n")
    
    nombre = input("Ingresa tu nombre: ")
    contrasena = input("Ingresa tu contraseña: ")
    
    # 1. Autenticar usuario
    auth_service = AuthService()
    usuario = auth_service.login(nombre, contrasena)
    
    # 2. Usar el Proxy para controlar acceso
    if usuario:
        servicio_real = RealService()
        proxy = AccessProxy(servicio_real)
        proxy.acceder(usuario, nombre=nombre, contrasena=contrasena, rol=usuario.rol)
    else:
        print("❌ No se pudo iniciar sesión")

if __name__ == "__main__":
    main()