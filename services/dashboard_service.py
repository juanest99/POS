# services/dashboard_service.py
from database.connection import conexion
from datetime import datetime, timedelta
from typing import Dict, List, Any

class DashboardService:
    
    @staticmethod
    def get_today_sales() -> Dict[str, Any]:
        """Obtiene ventas del día actual"""
        hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT COUNT(*) as transactions, SUM(total) as total_sales
            FROM VENTA
            WHERE DATE(fecha) = %s
        """
        result = conexion(query, (hoy,))
        if result and result[0]:
            return {
                'transactions': result[0][0] or 0,
                'total_sales': float(result[0][1] or 0)
            }
        return {'transactions': 0, 'total_sales': 0.0}
    
    @staticmethod
    def get_products_sold_today() -> int:
        """Total de unidades vendidas hoy"""
        hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT COALESCE(SUM(dv.cantidad), 0)
            FROM DETALLE_VENTA dv
            JOIN VENTA v ON dv.id_venta = v.id_venta
            WHERE DATE(v.fecha) = %s
        """
        result = conexion(query, (hoy,))
        return result[0][0] if result else 0
    
    @staticmethod
    def get_top_product_week() -> Dict[str, Any]:
        """Producto más vendido en los últimos 7 días"""
        fecha_limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query = """
            SELECT p.nombre, p.id_categoria, SUM(dv.cantidad) as total
            FROM DETALLE_VENTA dv
            JOIN PRODUCTO p ON dv.id_producto = p.id_producto
            JOIN VENTA v ON dv.id_venta = v.id_venta
            WHERE DATE(v.fecha) >= %s
            GROUP BY p.id_producto
            ORDER BY total DESC
            LIMIT 1
        """
        result = conexion(query, (fecha_limite,))
        if result:
            return {
                'product': result[0][0],
                'category_id': result[0][1],
                'sold': result[0][2]
            }
        return {'product': 'N/A', 'category_id': 0, 'sold': 0}
    
    @staticmethod
    def get_unsold_product_week() -> Dict[str, Any]:
        """Producto con stock > 0 pero sin ventas en los últimos 7 días"""
        fecha_limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query = """
            SELECT p.nombre, p.id_categoria
            FROM PRODUCTO p
            WHERE p.stock > 0
            AND NOT EXISTS (
                SELECT 1 FROM DETALLE_VENTA dv
                JOIN VENTA v ON dv.id_venta = v.id_venta
                WHERE dv.id_producto = p.id_producto
                AND DATE(v.fecha) >= %s
            )
            LIMIT 1
        """
        result = conexion(query, (fecha_limite,))
        if result:
            return {'product': result[0][0], 'category_id': result[0][1]}
        return {'product': 'N/A', 'category_id': 0}
    
    @staticmethod
    def get_payment_methods_today() -> Dict[str, float]:
        """Monto por método de pago hoy"""
        hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT metodo_pago, SUM(total) as total
            FROM VENTA
            WHERE DATE(fecha) = %s
            GROUP BY metodo_pago
        """
        results = conexion(query, (hoy,))
        payment_data = {}
        if results:
            for row in results:
                payment_data[row[0]] = float(row[1])
        return payment_data
    
    @staticmethod
    def get_average_sale_value_today() -> float:
        """Valor promedio de venta hoy"""
        hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT AVG(total) FROM VENTA WHERE DATE(fecha) = %s
        """
        result = conexion(query, (hoy,))
        if result and result[0][0]:
            return float(result[0][0])
        return 0.0
    
    @staticmethod
    def get_sales_by_hour_today() -> Dict[int, float]:
        """Ventas agrupadas por hora del día (para gráfico)"""
        hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT EXTRACT(HOUR FROM fecha) as hour, SUM(total) as total
            FROM VENTA
            WHERE DATE(fecha) = %s
            GROUP BY hour
            ORDER BY hour
        """
        results = conexion(query, (hoy,))
        sales_by_hour = {}
        if results:
            for row in results:
                sales_by_hour[int(row[0])] = float(row[1])
        # Completar horas sin ventas (0)
        for h in range(24):
            if h not in sales_by_hour:
                sales_by_hour[h] = 0
        return sales_by_hour
    
    @staticmethod
    def get_peak_hour_today() -> str:
        """Hora pico de ventas hoy"""
        sales_by_hour = DashboardService.get_sales_by_hour_today()
        if not sales_by_hour:
            return "N/A"
        peak_hour = max(sales_by_hour, key=sales_by_hour.get) # type: ignore
        return f"{peak_hour}:00 - {peak_hour+1}:00"
    
    @staticmethod
    def get_preferred_payment_method_today() -> str:
        """Método de pago con mayor monto hoy"""
        payments = DashboardService.get_payment_methods_today()
        if not payments:
            return "N/A"
        return max(payments, key=payments.get) # type: ignore