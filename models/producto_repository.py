from database.connection import conexion
from models.producto import Producto
from typing import List, Optional

class ProductoRepository:
    """Repositorio para operaciones CRUD de productos en la base de datos"""
    
    @staticmethod
    def _tupla_a_producto(tupla: tuple) -> Producto:
        """MÉTODO PRIVADO: Convierte una tupla de la BD en un objeto Producto"""
        return Producto(
            _id_producto=tupla[0],
            _id_categoria=tupla[1],
            _nombre=tupla[2],
            _stock=tupla[3],
            _precio=float(tupla[4]),
            _fecha=tupla[5]
        )
    
    @staticmethod
    def crear(producto: Producto) -> Optional[Producto]:
        """INSERT: Guarda un nuevo producto en la base de datos"""
        try:
            query = """
                INSERT INTO PRODUCTO (id_categoria, nombre, stock, precio)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """
            params = (producto.id_categoria, producto.nombre, producto.stock, producto.precio)
            resultado = conexion(query, params)
            
            if resultado:
                print(f"✅ Producto '{producto.nombre}' creado exitosamente")
                return ProductoRepository._tupla_a_producto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al crear producto: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(id_producto: int) -> Optional[Producto]:
        """SELECT: Busca un producto por su ID"""
        try:
            query = "SELECT * FROM PRODUCTO WHERE id_producto = %s"
            resultado = conexion(query, (id_producto,))
            
            if resultado:
                return ProductoRepository._tupla_a_producto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al buscar producto: {e}")
            return None
    
    @staticmethod
    def buscar_por_nombre(nombre: str) -> Optional[Producto]:
        """SELECT: Busca un producto por su nombre exacto"""
        try:
            query = "SELECT * FROM PRODUCTO WHERE nombre = %s"
            resultado = conexion(query, (nombre,))
            
            if resultado:
                return ProductoRepository._tupla_a_producto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al buscar producto: {e}")
            return None
    
    @staticmethod
    def listar_todos() -> List[Producto]:
        """SELECT: Obtiene todos los productos de la base de datos"""
        try:
            query = """
                SELECT p.*, c.nombre as categoria_nombre 
                FROM PRODUCTO p
                JOIN CATEGORIAS c ON p.id_categoria = c.id_categoria
                ORDER BY p.id_producto
            """
            resultados = conexion(query, None)
            
            if resultados:
                return [ProductoRepository._tupla_a_producto(r) for r in resultados]
            return []
        except Exception as e:
            print(f"❌ Error al listar productos: {e}")
            return []
    
    @staticmethod
    def actualizar(producto: Producto) -> Optional[Producto]:
        """UPDATE: Actualiza un producto existente"""
        try:
            query = """
                UPDATE PRODUCTO 
                SET id_categoria = %s, nombre = %s, stock = %s, precio = %s
                WHERE id_producto = %s
                RETURNING *
            """
            params = (producto.id_categoria, producto.nombre, 
                      producto.stock, producto.precio, producto.id_producto)
            resultado = conexion(query, params)
            
            if resultado:
                print(f"✅ Producto '{producto.nombre}' actualizado exitosamente")
                return ProductoRepository._tupla_a_producto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al actualizar producto: {e}")
            return None
    
    @staticmethod
    def eliminar(id_producto: int) -> bool:
        """DELETE: Elimina un producto de la base de datos"""
        try:
            producto = ProductoRepository.buscar_por_id(id_producto)
            if not producto:
                print(f"❌ Producto con ID {id_producto} no encontrado")
                return False
            
            query = "DELETE FROM PRODUCTO WHERE id_producto = %s"
            conexion(query, (id_producto,))
            print(f"✅ Producto '{producto.nombre}' eliminado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar producto: {e}")
            return False
    
    @staticmethod
    def actualizar_stock(id_producto: int, nueva_cantidad: int) -> Optional[Producto]:
        """UPDATE específico: Actualiza solo el stock de un producto"""
        try:
            query = """
                UPDATE PRODUCTO 
                SET stock = %s
                WHERE id_producto = %s
                RETURNING *
            """
            params = (nueva_cantidad, id_producto)
            resultado = conexion(query, params)
            
            if resultado:
                print(f"✅ Stock actualizado a {nueva_cantidad} unidades")
                return ProductoRepository._tupla_a_producto(resultado[0])
            return None
        except Exception as e:
            print(f"❌ Error al actualizar stock: {e}")
            return None