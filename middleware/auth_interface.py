from abc import ABC, abstractmethod
from typing import Optional
from models.usuario import Usuario

class AuthInterface(ABC):
    @abstractmethod
    def login(self, nombre: str, contrasena: str) -> Optional[Usuario]:
        """Retorna un objeto Usuario si existe, None si no"""
        pass