from models.usuario import Usuario
from middleware.service_interface import ServiceInterface 

class RealService(ServiceInterface):  
    def acceder(self, persona: Usuario, *args, **kwargs):
        nombre = kwargs.get('nombre', persona.nombre)
        contrasena = kwargs.get('contrasena', '')
        rol = kwargs.get('rol', persona.rol)
        
        print(f"✅ Ejecutando servicio real para: {persona.nombre}")
        
        if rol.lower() == 'admin':
            print("👑 Acceso de Administrador concedido")
            print("   - Gestión de productos")
            print("   - Reportes financieros")
            print("   - Gestión de usuarios")
            self._menu_admin(persona)
        elif rol.lower() == 'cajero':
            print("💵 Acceso de Cajero concedido")
            print("   - Registrar ventas")
            print("   - Buscar productos")
            print("   - Procesar pagos")
            self._menu_cajero(persona)
        else:
            print(f"❌ Rol desconocido: {rol}")
    
    def _menu_admin(self, usuario):
        print(f"\n=== PANEL ADMINISTRADOR - {usuario.nombre} ===")
        print("1. Gestionar productos")
        print("2. Gestionar inventario")
        print("3. Ver reportes")
        print("4. Gestionar usuarios")
        print("5. Cerrar sesión")
    
    def _menu_cajero(self, usuario):
        print(f"\n=== PANEL CAJERO - {usuario.nombre} ===")
        print("1. Nueva venta")
        print("2. Buscar producto")
        print("3. Historial de ventas")
        print("4. Cerrar sesión")