from Objects.Usuario import Usuario
from Proxy.service import service

class servicioReal(service):

    def acceder(self, persona:Usuario, nombre,contrasena, rol):
        if rol.lower() == 'admin':
            print('eres admin')
        else:
            print('eres usuario')