from dataclasses import dataclass
from models.usuario import Usuario
from middleware.service_interface import ServiceInterface  
from middleware.real_service import RealService

@dataclass
class AccessProxy(ServiceInterface):  
    servicio_real: RealService

    def acceder(self, persona: Usuario, *args, **kwargs):
        if persona is None:
            print("❌ Acceso denegado: usuario no existe")
            return None
        
        nombre = kwargs.get('nombre', '')
        contrasena = kwargs.get('contrasena', '')
        
        if (persona.nombre == nombre) and (persona.contrasena == contrasena):
            print(f"🔐 Proxy: Usuario '{nombre}' autenticado correctamente")
            
            if not persona.estado:
                print("❌ Acceso denegado: usuario inactivo")
                return None
            
            return self.servicio_real.acceder(persona, *args, **kwargs)
        else:
            print("❌ Acceso denegado: credenciales incorrectas")
            return None