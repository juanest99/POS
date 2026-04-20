from dataclasses import dataclass

@dataclass
class Usuario:
    _nombre: str = ""
    _email: str = ""
    _contrasena: str = ""
    _rol: str = ""
    _fecha: str = ""
    _estado: bool = False

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        self._email = valor
    
    @property
    def contrasena(self):
        return self._contrasena
    
    @contrasena.setter
    def contrasena(self, valor):
        self._contrasena = valor
    
    @property
    def rol(self):
        return self._rol
    
    @rol.setter
    def rol(self, valor):
        self._rol = valor
    
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        self._estado = valor