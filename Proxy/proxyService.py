from dataclasses import dataclass
from Objects.Usuario import Usuario
from Proxy.realService import servicioReal
from Proxy.service import service  # asumiendo que existe

@dataclass
class Proxy(service):

    servicioReal: servicioReal

    def acceder(self, persona: Usuario, nombre, contrasena, rol):
        if persona is None:
            print("usuario no existe")

        elif (persona.nombre == nombre) and (persona.contrasena == contrasena):
            print("usuario existe")
            self.servicioReal.acceder(persona, nombre, contrasena, rol)