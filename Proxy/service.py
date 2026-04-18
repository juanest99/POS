from abc import ABC, abstractmethod

from Objects.Usuario import Usuario


class service:
    @abstractmethod
    def acceder(self, persona:Usuario, nombre,contrasena, rol):
        pass
