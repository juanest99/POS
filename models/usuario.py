from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    """Modelo que representa un usuario del sistema"""
    
    # Atributos privados
    _id_usuario: Optional[int] = None
    _nombre: str = ""
    _email: str = ""
    _contrasena: str = ""
    _rol: str = ""
    _fecha: str = ""
    _estado: bool = False

    @property
    def id_usuario(self) -> Optional[int]:
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor: int):
        self._id_usuario = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        self._email = valor

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str):
        self._contrasena = valor

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str):
        self._rol = valor

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str):
        self._fecha = valor

    @property
    def estado(self) -> bool:
        return self._estado

    @estado.setter
    def estado(self, valor: bool):
        self._estado = valor

    def __str__(self) -> str:
        return f"{self._id_usuario} | {self._nombre} | {self._rol}"