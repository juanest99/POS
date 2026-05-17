from typing import List, Optional
from models.gasto import Gasto
from models.gasto_repository import GastoRepository
from models.usuario_repository import UsuarioRepository

class GastoService:
    """Lógica de negocio para gastos"""
    
    @staticmethod
    def registrar_gasto(id_usuario: int, categoria: str, monto: float, descripcion: str) -> Optional[Gasto]:
        """
        Reglas:
        1. El usuario debe existir
        2. Monto debe ser > 0
        3. Categoría válida
        """
        # Validar usuario
        usuario = UsuarioRepository.buscar_por_id(id_usuario)
        if not usuario:
            print(f"❌ Usuario ID {id_usuario} no existe")
            return None
        
        # Validar monto
        if monto <= 0:
            print("❌ El monto debe ser mayor a 0")
            return None
        
        # Validar categoría
        categorias_validas = ['compra_productos', 'servicios', 'salarios', 'otros']
        if categoria not in categorias_validas:
            print(f"❌ Categoría inválida. Use: {categorias_validas}")
            return None
        
        gasto = Gasto(
            _id_usuario=id_usuario,
            _categoria=categoria,
            _monto=monto,
            _descripcion=descripcion
        )
        return GastoRepository.crear(gasto)
    
    @staticmethod
    def listar_gastos() -> List[Gasto]:
        return GastoRepository.listar_todos()
    
    @staticmethod
    def ver_resumen_gastos() -> dict:
        """Retorna resumen de gastos por categoría y total"""
        total = GastoRepository.obtener_total_gastos()
        por_categoria = GastoRepository.obtener_total_por_categoria()
        return {
            'total': total,
            'por_categoria': por_categoria
        }
    
    @staticmethod
    def mostrar_gastos_recientes():
        gastos = GastoRepository.listar_todos(limite=20)
        if not gastos:
            print("📋 No hay gastos registrados")
            return
        
        print("\n" + "="*70)
        print("ÚLTIMOS GASTOS REGISTRADOS")
        print("="*70)
        print(f"{'ID':<4} {'FECHA':<12} {'CATEGORÍA':<18} {'MONTO':<12} {'DESCRIPCIÓN'}")
        print("-"*70)
        for g in gastos:
            fecha_str = g.fecha.strftime("%Y-%m-%d") if g.fecha else "N/A"
            print(f"{g.id_gasto:<4} {fecha_str:<12} {g.categoria:<18} ${g.monto:<12.2f} {g.descripcion[:30]}")
        print("="*70)