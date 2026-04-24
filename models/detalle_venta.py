from dataclasses import dataclass
from typing import Optional

@dataclass
class DetalleVenta:
    """Modelo que representa el detalle de una venta (productos vendidos)"""
    
    _id_producto: int = 0
    _id_venta: int = 0
    _cantidad: int = 0
    _precio_unitario: float = 0.0
    _subtotal: float = 0.0
    
    @property
    def id_producto(self) -> int:
        return self._id_producto
    
    @id_producto.setter
    def id_producto(self, valor: int):
        self._id_producto = valor
    
    @property
    def id_venta(self) -> int:
        return self._id_venta
    
    @id_venta.setter
    def id_venta(self, valor: int):
        self._id_venta = valor
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, valor: int):
        self._cantidad = valor
        self._calcular_subtotal()
    
    @property
    def precio_unitario(self) -> float:
        return self._precio_unitario
    
    @precio_unitario.setter
    def precio_unitario(self, valor: float):
        self._precio_unitario = valor
        self._calcular_subtotal()
    
    @property
    def subtotal(self) -> float:
        return self._subtotal
    
    def _calcular_subtotal(self):
        """Calcula el subtotal automáticamente"""
        self._subtotal = self._cantidad * self._precio_unitario
    
    def __str__(self) -> str:
        return f"Producto: {self._id_producto} | {self._cantidad} x ${self._precio_unitario:.2f} = ${self._subtotal:.2f}"