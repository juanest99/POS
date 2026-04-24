from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Venta:
    """Modelo que representa una venta en el sistema"""
    
    _id_venta: Optional[int] = None
    _id_usuario: int = 0
    _metodo_pago: str = ""          # 'efectivo', 'tarjeta', 'transferencia'
    _total: float = 0.0
    _monto_recibido: float = 0.0
    _cambio: float = 0.0
    _fecha: Optional[date] = None
    
    @property
    def id_venta(self) -> Optional[int]:
        return self._id_venta
    
    @id_venta.setter
    def id_venta(self, valor: int):
        self._id_venta = valor
    
    @property
    def id_usuario(self) -> int:
        return self._id_usuario
    
    @id_usuario.setter
    def id_usuario(self, valor: int):
        self._id_usuario = valor
    
    @property
    def metodo_pago(self) -> str:
        return self._metodo_pago
    
    @metodo_pago.setter
    def metodo_pago(self, valor: str):
        self._metodo_pago = valor
    
    @property
    def total(self) -> float:
        return self._total
    
    @total.setter
    def total(self, valor: float):
        self._total = valor
    
    @property
    def monto_recibido(self) -> float:
        return self._monto_recibido
    
    @monto_recibido.setter
    def monto_recibido(self, valor: float):
        self._monto_recibido = valor
    
    @property
    def cambio(self) -> float:
        return self._cambio
    
    @cambio.setter
    def cambio(self, valor: float):
        self._cambio = valor
    
    @property
    def fecha(self) -> Optional[date]:
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor: date):
        self._fecha = valor
    
    def __str__(self) -> str:
        return f"Venta #{self._id_venta} | Total: ${self._total:.2f} | {self._fecha}"