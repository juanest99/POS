from database.connection import conexion
from typing import List, Dict, Optional
import csv
from datetime import datetime

class ReporteService:
    
    @staticmethod
    def ventas_por_dia(fecha: Optional[str] = None) -> List[Dict]:
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        query = """
            SELECT v.id_venta, u.nombre as cajero, v.total, v.metodo_pago, v.fecha
            FROM VENTA v
            JOIN USUARIO u ON v.id_usuario = u.id_usuario
            WHERE DATE(v.fecha) = %s
            ORDER BY v.fecha DESC
        """
        resultados = conexion(query, (fecha,))
        ventas = []
        if resultados:
            for r in resultados:
                ventas.append({
                    'id': r[0],
                    'cajero': r[1],
                    'total': float(r[2]),
                    'metodo_pago': r[3],
                    'fecha': r[4]
                })
        return ventas
    
    @staticmethod
    def ventas_por_mes(anio: int, mes: int) -> List[Dict]:
        query = """
            SELECT v.id_venta, u.nombre as cajero, v.total, v.metodo_pago, v.fecha
            FROM VENTA v
            JOIN USUARIO u ON v.id_usuario = u.id_usuario
            WHERE EXTRACT(YEAR FROM v.fecha) = %s AND EXTRACT(MONTH FROM v.fecha) = %s
            ORDER BY v.fecha DESC
        """
        resultados = conexion(query, (anio, mes))
        ventas = []
        if resultados:
            for r in resultados:
                ventas.append({
                    'id': r[0],
                    'cajero': r[1],
                    'total': float(r[2]),
                    'metodo_pago': r[3],
                    'fecha': r[4]
                })
        return ventas
    
    @staticmethod
    def total_ventas_periodo(fecha_desde: str, fecha_hasta: str) -> float:
        query = "SELECT COALESCE(SUM(total), 0) FROM VENTA WHERE DATE(fecha) BETWEEN %s AND %s"
        resultado = conexion(query, (fecha_desde, fecha_hasta))
        if resultado and resultado[0][0]:
            return float(resultado[0][0])
        return 0.0
    
    @staticmethod
    def productos_mas_vendidos(limite: int = 10) -> List[Dict]:
        query = """
            SELECT p.id_producto, p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as total_ingresos
            FROM DETALLE_VENTA dv
            JOIN PRODUCTO p ON dv.id_producto = p.id_producto
            GROUP BY p.id_producto, p.nombre
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        resultados = conexion(query, (limite,))
        productos = []
        if resultados:
            for r in resultados:
                productos.append({
                    'id': r[0],
                    'nombre': r[1],
                    'total_vendido': r[2],
                    'total_ingresos': float(r[3])
                })
        return productos
    
    @staticmethod
    def productos_con_menor_stock(limite: int = 10) -> List[Dict]:
        query = "SELECT id_producto, nombre, stock FROM PRODUCTO ORDER BY stock ASC LIMIT %s"
        resultados = conexion(query, (limite,))
        productos = []
        if resultados:
            for r in resultados:
                productos.append({
                    'id': r[0],
                    'nombre': r[1],
                    'stock': r[2]
                })
        return productos
    
    @staticmethod
    def exportar_ventas_csv(ventas: List[Dict], nombre_archivo: Optional[str] = None) -> str:
        if not nombre_archivo:
            nombre_archivo = f"reporte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
            if not ventas:
                print("No hay datos para exportar")
                return ""
            fieldnames = ventas[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ventas)
        print(f"✅ Reporte exportado a {nombre_archivo}")
        return nombre_archivo

    @staticmethod
    def total_ventas_hoy():
        """Retorna (total_dinero, total_transacciones) del día actual"""
        query = """
            SELECT COALESCE(SUM(total), 0), COUNT(*)
            FROM VENTA
            WHERE DATE(fecha) = CURRENT_DATE
        """
        resultado = conexion(query, None)
        if resultado:
            return float(resultado[0][0]), resultado[0][1]
        return 0.0, 0

    @staticmethod
    def unidades_vendidas_hoy():
        """Suma de cantidades de detalle_venta de ventas del día actual"""
        query = """
            SELECT COALESCE(SUM(dv.cantidad), 0)
            FROM DETALLE_VENTA dv
            JOIN VENTA v ON dv.id_venta = v.id_venta
            WHERE DATE(v.fecha) = CURRENT_DATE
        """
        resultado = conexion(query, None)
        if resultado:
            return resultado[0][0]
        return 0

    @staticmethod
    def ventas_por_hora():
        """Retorna un diccionario {hora: total_vendido} para hoy, rango 0-23"""
        query = """
            SELECT EXTRACT(HOUR FROM v.fecha)::int as hora, COALESCE(SUM(v.total), 0)
            FROM VENTA v
            WHERE DATE(v.fecha) = CURRENT_DATE
            GROUP BY hora
            ORDER BY hora
        """
        resultados = conexion(query, None)
        ventas_hora = {h: 0 for h in range(24)}
        if resultados:
            for r in resultados:
                hora = int(r[0])
                ventas_hora[hora] = float(r[1])  # type: ignore
        return ventas_hora

    @staticmethod
    def producto_mas_vendido_semana():
        """Retorna (nombre, categoria, unidades) del producto más vendido en últimos 7 días"""
        query = """
            SELECT p.nombre, c.nombre, SUM(dv.cantidad) as total
            FROM DETALLE_VENTA dv
            JOIN PRODUCTO p ON dv.id_producto = p.id_producto
            JOIN CATEGORIAS c ON p.id_categoria = c.id_categoria
            JOIN VENTA v ON dv.id_venta = v.id_venta
            WHERE v.fecha >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY p.id_producto, p.nombre, c.nombre
            ORDER BY total DESC
            LIMIT 1
        """
        resultado = conexion(query, None)
        if resultado:
            return resultado[0][0], resultado[0][1], resultado[0][2]
        return "Ninguno", "", 0

    @staticmethod
    def producto_menos_vendido_semana():
        """Producto con menos ventas (puede ser cero ventas)"""
        query = """
            SELECT p.nombre, c.nombre, COALESCE(SUM(dv.cantidad), 0) as total
            FROM PRODUCTO p
            JOIN CATEGORIAS c ON p.id_categoria = c.id_categoria
            LEFT JOIN DETALLE_VENTA dv ON p.id_producto = dv.id_producto
            LEFT JOIN VENTA v ON dv.id_venta = v.id_venta AND v.fecha >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY p.id_producto, p.nombre, c.nombre
            ORDER BY total ASC
            LIMIT 1
        """
        resultado = conexion(query, None)
        if resultado:
            return resultado[0][0], resultado[0][1], resultado[0][2]
        return "Ninguno", "", 0

    @staticmethod
    def total_por_metodo_pago_hoy():
        """Retorna diccionario {metodo_pago: total_dinero}"""
        query = """
            SELECT metodo_pago, COALESCE(SUM(total), 0)
            FROM VENTA
            WHERE DATE(fecha) = CURRENT_DATE
            GROUP BY metodo_pago
        """
        resultados = conexion(query, None)
        totales = {}
        if resultados:
            for r in resultados:
                totales[r[0]] = float(r[1])
        return totales

    @staticmethod
    def promedio_venta_hoy():
        total, transacciones = ReporteService.total_ventas_hoy()
        if transacciones == 0:
            return 0.0
        return total / transacciones

    @staticmethod
    def hora_pico_hoy():
        ventas_hora = ReporteService.ventas_por_hora()
        if not ventas_hora or all(v == 0 for v in ventas_hora.values()):
            return "No hay datos"
        max_hora = max(ventas_hora, key=ventas_hora.get)  # type: ignore
        return f"{max_hora}:00 - {max_hora+1}:00"

    @staticmethod
    def metodo_pago_preferido_hoy():
        por_metodo = ReporteService.total_por_metodo_pago_hoy()
        if not por_metodo:
            return "Ninguno"
        preferido = max(por_metodo, key=por_metodo.get)  # type: ignore
        return preferido.capitalize()