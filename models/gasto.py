from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Gasto:
    """Modelo que representa un gasto del negocio"""
    
    _id_gasto: Optional[int] = None
    _id_usuario: int = 0
    _categoria: str = ""        # 'compra_productos', 'servicios', 'salarios', 'otros'
    _monto: float = 0.0
    _descripcion: str = ""
    _fecha: Optional[date] = None
    
    @property
    def id_gasto(self) -> Optional[int]:
        return self._id_gasto
    
    @id_gasto.setter
    def id_gasto(self, valor: int):
        self._id_gasto = valor
    
    @property
    def id_usuario(self) -> int:
        return self._id_usuario
    
    @id_usuario.setter
    def id_usuario(self, valor: int):
        self._id_usuario = valor
    
    @property
    def categoria(self) -> str:
        return self._categoria
    
    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor
    
    @property
    def monto(self) -> float:
        return self._monto
    
    @monto.setter
    def monto(self, valor: float):
        self._monto = valor
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor
    
    @property
    def fecha(self) -> Optional[date]:
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor: date):
        self._fecha = valor
    
    def __str__(self) -> str:
        return f"Gasto #{self._id_gasto} | {self._categoria} | ${self._monto:.2f} | {self._fecha}"