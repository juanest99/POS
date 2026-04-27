from models.gasto import Gasto
from models.gasto_repository import GastoRepository
from models.usuario_repository import UsuarioRepository
from typing import Optional, List
from datetime import date, timedelta

class GastoService:
    """Servicio con la lógica de negocio para gastos"""
    
    @staticmethod
    def registrar_gasto(id_usuario: int, descripcion: str, monto: float) -> Optional[Gasto]:
        """Registra un nuevo gasto con validaciones"""
        
        # Validar usuario
        usuario = UsuarioRepository.buscar_por_id(id_usuario)
        if not usuario:
            print(f"❌ Error: Usuario con ID {id_usuario} no existe")
            return None
        
        # Validar monto
        if monto <= 0:
            print("❌ Error: El monto debe ser mayor a 0")
            return None
        
        # Validar descripción
        if not descripcion or descripcion.strip() == "":
            print("❌ Error: La descripción no puede estar vacía")
            return None
        
        # Crear gasto
        gasto = Gasto(
            _id_usuario=id_usuario,
            _descripcion=descripcion.strip(),
            _monto=monto
        )
        
        return GastoRepository.guardar(gasto)
    
    @staticmethod
    def obtener_gastos_dia(fecha: Optional[date] = None) -> List[Gasto]:
        """Obtiene los gastos de un día específico"""
        if fecha is None:
            fecha = date.today()
        return GastoRepository.listar_por_fecha(fecha, fecha)
    
    @staticmethod
    def obtener_gastos_mes(anio: int, mes: int) -> List[Gasto]:
        """Obtiene los gastos de un mes específico"""
        fecha_inicio = date(anio, mes, 1)
        if mes == 12:
            fecha_fin = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)
        return GastoRepository.listar_por_fecha(fecha_inicio, fecha_fin)
    
    @staticmethod
    def obtener_total_gastos_periodo(fecha_inicio: date, fecha_fin: date) -> float:
        """Obtiene el total de gastos en un período"""
        return GastoRepository.obtener_total_gastos(fecha_inicio, fecha_fin)
    
    @staticmethod
    def mostrar_resumen_gastos(fecha_inicio: date, fecha_fin: date):
        """Muestra un resumen de gastos"""
        total_general = GastoRepository.obtener_total_gastos(fecha_inicio, fecha_fin)
        gastos = GastoRepository.listar_por_fecha(fecha_inicio, fecha_fin)
        
        print(f"\n{'='*70}")
        print(f"📊 RESUMEN DE GASTOS")
        print(f"📅 Período: {fecha_inicio} al {fecha_fin}")
        print(f"{'='*70}")
        
        if not gastos:
            print("   No hay gastos registrados en este período")
        else:
            print(f"\n📋 TOTAL DE GASTOS: ${total_general:>12.2f}")
            print(f"📋 NÚMERO DE GASTOS: {len(gastos)}")
        
        print(f"{'='*70}")
        return total_general
    
    @staticmethod
    def mostrar_lista_gastos(gastos: List[Gasto], titulo: str = "LISTA DE GASTOS"):
        """Muestra la lista detallada de gastos"""
        if not gastos:
            print("\n📭 No hay gastos para mostrar")
            return
        
        print(f"\n{'='*90}")
        print(f"📋 {titulo}")
        print(f"{'='*90}")
        print(f"{'ID':<6} {'FECHA':<12} {'MONTO':<12} {'DESCRIPCIÓN'}")
        print(f"{'-'*90}")
        
        for g in gastos:
            fecha_str = g.fecha.strftime("%Y-%m-%d") if g.fecha else "N/A"
            print(f"{g.id_gasto:<6} {fecha_str:<12} ${g.monto:<11.2f} {g.descripcion[:60]}")
        
        total = sum(g.monto for g in gastos)
        print(f"{'-'*90}")
        print(f"{'TOTAL':<6} {'':<12} ${total:<11.2f}")
        print(f"{'='*90}")