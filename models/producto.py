from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Producto:
    """Modelo que representa un producto en el sistema"""
    
    # Atributos privados
    _id_producto: Optional[int] = None
    _id_categoria: int = 0
    _nombre: str = ""
    _stock: int = 0
    _precio: float = 0.0
    _fecha: Optional[date] = None
    
    # Propiedades (Getters y Setters)
    @property
    def id_producto(self) -> Optional[int]:
        return self._id_producto
    
    @id_producto.setter
    def id_producto(self, valor: int):
        self._id_producto = valor
    
    @property
    def id_categoria(self) -> int:
        return self._id_categoria
    
    @id_categoria.setter
    def id_categoria(self, valor: int):
        self._id_categoria = valor
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @stock.setter
    def stock(self, valor: int):
        self._stock = valor
    
    @property
    def precio(self) -> float:
        return self._precio
    
    @precio.setter
    def precio(self, valor: float):
        self._precio = valor
    
    @property
    def fecha(self) -> Optional[date]:
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor: date):
        self._fecha = valor
    
    def __str__(self) -> str:
        """Representación en texto del producto"""
        return f"{self._id_producto} | {self._nombre} | Stock: {self._stock} | ${self._precio:.2f}"