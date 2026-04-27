from datetime import date, timedelta
from typing import Dict, Optional
from models.venta_repository import VentaRepository
from models.gasto_repository import GastoRepository

class ReporteService:
    """Servicio para generar reportes del sistema"""
    
    @staticmethod
    def _obtener_total_ventas_periodo(fecha_inicio: date, fecha_fin: date) -> float:
        """Obtiene el total de ventas en un período"""
        try:
            from database.connection import conexion
            query = """
                SELECT COALESCE(SUM(total), 0) as total
                FROM VENTA
                WHERE DATE(fecha) BETWEEN %s AND %s
            """
            resultado = conexion(query, (fecha_inicio, fecha_fin))
            if resultado and resultado[0][0] is not None:
                return float(resultado[0][0])
            return 0.0
        except Exception as e:
            print(f"❌ Error al obtener total de ventas: {e}")
            return 0.0
    
    @staticmethod
    def obtener_reportes_diario(fecha: Optional[date] = None) -> Dict:
        """Genera un reporte completo del día"""
        if fecha is None:
            fecha = date.today()
        
        # Ventas del día
        ventas_dia = VentaRepository.obtener_ventas_hoy() if fecha == date.today() else \
                     VentaRepository.listar_por_fecha(fecha, fecha)
        
        total_ventas = sum(v.total for v in ventas_dia) if ventas_dia else 0.0
        cantidad_ventas = len(ventas_dia) if ventas_dia else 0
        
        # Gastos del día
        gastos_dia = GastoRepository.listar_por_fecha(fecha, fecha)
        total_gastos = sum(g.monto for g in gastos_dia) if gastos_dia else 0.0
        
        # Métodos de pago
        metodos_pago = {}
        for v in ventas_dia:
            metodos_pago[v.metodo_pago] = metodos_pago.get(v.metodo_pago, 0) + 1
        
        utilidad = total_ventas - total_gastos
        
        return {
            'fecha': fecha,
            'ventas': {
                'total': total_ventas,
                'cantidad': cantidad_ventas,
                'promedio': total_ventas / cantidad_ventas if cantidad_ventas > 0 else 0,
                'metodos_pago': metodos_pago
            },
            'gastos': {
                'total': total_gastos,
                'cantidad': len(gastos_dia)
            },
            'utilidad': utilidad,
            'margen_utilidad': (utilidad / total_ventas * 100) if total_ventas > 0 else 0
        }
    
    @staticmethod
    def obtener_reportes_mensual(anio: int, mes: int) -> Dict:
        """Genera un reporte completo del mes"""
        fecha_inicio = date(anio, mes, 1)
        if mes == 12:
            fecha_fin = date(anio + 1, 1, 1) - timedelta(days=1)
        else:
            fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)
        
        total_ventas = ReporteService._obtener_total_ventas_periodo(fecha_inicio, fecha_fin)
        total_gastos = GastoRepository.obtener_total_gastos(fecha_inicio, fecha_fin)
        
        return {
            'periodo': f"{mes:02d}/{anio}",
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ventas': {
                'total': total_ventas,
                'promedio_diario': total_ventas / fecha_fin.day if fecha_fin.day > 0 else 0
            },
            'gastos': {
                'total': total_gastos
            },
            'utilidad': total_ventas - total_gastos,
            'margen_utilidad': ((total_ventas - total_gastos) / total_ventas * 100) if total_ventas > 0 else 0
        }
    
    @staticmethod
    def mostrar_reporte_diario(fecha: Optional[date] = None):
        """Muestra en pantalla el reporte diario formateado"""
        reporte = ReporteService.obtener_reportes_diario(fecha)
        
        print(f"\n{'='*70}")
        print(f"📊 REPORTE DIARIO")
        print(f"📅 Fecha: {reporte['fecha'].strftime('%Y-%m-%d')}")
        print(f"{'='*70}")
        
        print(f"\n💰 VENTAS DEL DÍA")
        print(f"{'-'*50}")
        print(f"   Total de ventas:    ${reporte['ventas']['total']:>12.2f}")
        print(f"   Número de ventas:   {reporte['ventas']['cantidad']:>12}")
        print(f"   Promedio por venta: ${reporte['ventas']['promedio']:>12.2f}")
        
        if reporte['ventas']['metodos_pago']:
            print(f"\n   Métodos de pago:")
            for metodo, cantidad in reporte['ventas']['metodos_pago'].items():
                print(f"      • {metodo}: {cantidad} venta(s)")
        
        print(f"\n💸 GASTOS DEL DÍA")
        print(f"{'-'*50}")
        print(f"   Total de gastos:    ${reporte['gastos']['total']:>12.2f}")
        print(f"   Número de gastos:   {reporte['gastos']['cantidad']:>12}")
        
        print(f"\n📈 UTILIDAD DEL DÍA")
        print(f"{'-'*50}")
        print(f"   Utilidad:           ${reporte['utilidad']:>12.2f}")
        print(f"   Margen de utilidad: {reporte['margen_utilidad']:>11.1f}%")
        
        print(f"\n⚠️ INDICADORES")
        print(f"{'-'*50}")
        
        if reporte['margen_utilidad'] < 10 and reporte['ventas']['total'] > 0:
            print(f"   🔴 ALERTA: Margen de utilidad bajo ({reporte['margen_utilidad']:.1f}%)")
        elif reporte['margen_utilidad'] < 20 and reporte['ventas']['total'] > 0:
            print(f"   🟡 Margen de utilidad aceptable ({reporte['margen_utilidad']:.1f}%)")
        elif reporte['ventas']['total'] > 0:
            print(f"   🟢 Excelente margen de utilidad ({reporte['margen_utilidad']:.1f}%)")
        
        if reporte['ventas']['total'] == 0:
            print(f"   🔴 No hubo ventas en el día")
        
        print(f"{'='*70}")
        return reporte
    
    @staticmethod
    def mostrar_reporte_mensual(anio: int, mes: int):
        """Muestra en pantalla el reporte mensual formateado"""
        reporte = ReporteService.obtener_reportes_mensual(anio, mes)
        
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        print(f"\n{'='*70}")
        print(f"📊 REPORTE MENSUAL")
        print(f"📅 {meses[mes-1]} {anio}")
        print(f"{'='*70}")
        
        print(f"\n💰 VENTAS DEL MES")
        print(f"{'-'*50}")
        print(f"   Total de ventas:    ${reporte['ventas']['total']:>12.2f}")
        print(f"   Promedio diario:    ${reporte['ventas']['promedio_diario']:>12.2f}")
        
        print(f"\n💸 GASTOS DEL MES")
        print(f"{'-'*50}")
        print(f"   Total de gastos:    ${reporte['gastos']['total']:>12.2f}")
        
        print(f"\n📈 UTILIDAD DEL MES")
        print(f"{'-'*50}")
        print(f"   Utilidad:           ${reporte['utilidad']:>12.2f}")
        print(f"   Margen de utilidad: {reporte['margen_utilidad']:>11.1f}%")
        
        if mes > 1:
            reporte_anterior = ReporteService.obtener_reportes_mensual(anio, mes - 1)
            if reporte_anterior['ventas']['total'] > 0:
                variacion_ventas = ((reporte['ventas']['total'] - reporte_anterior['ventas']['total']) / 
                                   reporte_anterior['ventas']['total'] * 100)
                
                print(f"\n📈 COMPARATIVA VS MES ANTERIOR")
                print(f"{'-'*50}")
                if variacion_ventas > 0:
                    print(f"   Ventas aumentaron:  +{variacion_ventas:.1f}% 🟢")
                elif variacion_ventas < 0:
                    print(f"   Ventas disminuyeron: {variacion_ventas:.1f}% 🔴")
                else:
                    print(f"   Ventas se mantuvieron estables")
        
        print(f"{'='*70}")
        return reporte