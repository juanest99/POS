from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class MovimientoInventario:
    """Modelo que representa un movimiento de inventario"""
    
    # Atributos privados
    _id_movimiento: Optional[int] = None
    _id_producto: int = 0
    _id_usuario: int = 0
    _tipo: str = ""          # 'entrada', 'salida', 'ajuste'
    _cantidad: int = 0
    _motivo: str = ""        # 'compra', 'venta', 'merma', 'ajuste_fisico'
    _fecha: Optional[date] = None
    
    # Propiedades (Getters y Setters)
    @property
    def id_movimiento(self) -> Optional[int]:
        return self._id_movimiento
    
    @id_movimiento.setter
    def id_movimiento(self, valor: int):
        self._id_movimiento = valor
    
    @property
    def id_producto(self) -> int:
        return self._id_producto
    
    @id_producto.setter
    def id_producto(self, valor: int):
        self._id_producto = valor
    
    @property
    def id_usuario(self) -> int:
        return self._id_usuario
    
    @id_usuario.setter
    def id_usuario(self, valor: int):
        self._id_usuario = valor
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor: str):
        self._tipo = valor
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, valor: int):
        self._cantidad = valor
    
    @property
    def motivo(self) -> str:
        return self._motivo
    
    @motivo.setter
    def motivo(self, valor: str):
        self._motivo = valor
    
    @property
    def fecha(self) -> Optional[date]:
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor: date):
        self._fecha = valor
    
    def __str__(self) -> str:
        return f"{self._id_movimiento} | Prod:{self._id_producto} | {self._tipo} | {self._cantidad} | {self._motivo}"