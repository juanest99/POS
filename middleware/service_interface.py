from abc import ABC, abstractmethod
from models.usuario import Usuario

class ServiceInterface(ABC): 
    @abstractmethod
    def acceder(self, persona: Usuario, *args, **kwargs):
        pass