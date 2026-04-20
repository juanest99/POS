from typing import List, Optional
from models.producto import Producto
from models.producto_repository import ProductoRepository
from models.categoria_repository import CategoriaRepository

class ProductoService:
    """Servicio con la lógica de negocio para productos"""
    
    @staticmethod
    def crear_producto(id_categoria: int, nombre: str, stock: int, precio: float) -> Optional[Producto]:
        """
        REGLAS DE NEGOCIO para crear un producto:
        1. El nombre no puede estar vacío
        2. El precio debe ser mayor a 0
        3. El stock no puede ser negativo
        4. No puede haber otro producto con el mismo nombre
        5. La categoría debe existir
        """
        
        # Regla 1: Validar nombre
        if not nombre or nombre.strip() == "":
            print("❌ Error: El nombre del producto no puede estar vacío")
            return None
        
        # Regla 2: Validar precio
        if precio <= 0:
            print("❌ Error: El precio debe ser mayor a 0")
            return None
        
        # Regla 3: Validar stock
        if stock < 0:
            print("❌ Error: El stock no puede ser negativo")
            return None
        
        # Regla 4: Validar que no exista producto con mismo nombre
        existente = ProductoRepository.buscar_por_nombre(nombre)
        if existente:
            print(f"❌ Error: Ya existe un producto con el nombre '{nombre}'")
            return None
        
        # Regla 5: Validar que la categoría existe
        categoria = CategoriaRepository.buscar_por_id(id_categoria)
        if not categoria:
            print(f"❌ Error: La categoría con ID {id_categoria} no existe")
            print("   Categorías disponibles: 1-Electrónicos, 2-Ropa, 3-Alimentos, 4-Hogar, 5-Deportes")
            return None
        
        # Crear objeto Producto
        nuevo_producto = Producto(
            _id_categoria=id_categoria,
            _nombre=nombre.strip(),
            _stock=stock,
            _precio=precio
        )
        
        # Guardar en la base de datos
        return ProductoRepository.crear(nuevo_producto)
    
    @staticmethod
    def listar_productos() -> List[Producto]:
        """Retorna todos los productos ordenados"""
        productos = ProductoRepository.listar_todos()
        
        if not productos:
            print("📦 No hay productos registrados en el sistema")
        else:
            print(f"📦 Total de productos encontrados: {len(productos)}")
        
        return productos
    
    @staticmethod
    def buscar_producto(id_producto: int) -> Optional[Producto]:
        """Busca un producto por su ID"""
        producto = ProductoRepository.buscar_por_id(id_producto)
        
        if not producto:
            print(f"❌ No se encontró producto con ID {id_producto}")
        
        return producto
    
    @staticmethod
    def actualizar_producto(id_producto: int, id_categoria: int, nombre: str, stock: int, precio: float) -> Optional[Producto]:
        """
        REGLAS DE NEGOCIO para actualizar:
        1. El producto debe existir
        2. El nombre no puede estar vacío
        3. El precio debe ser mayor a 0
        4. El stock no puede ser negativo
        """
        
        # Regla 1: Verificar que existe
        producto_existente = ProductoRepository.buscar_por_id(id_producto)
        if not producto_existente:
            print(f"❌ Error: No existe producto con ID {id_producto}")
            return None
        
        # Regla 2: Validar nombre
        if not nombre or nombre.strip() == "":
            print("❌ Error: El nombre del producto no puede estar vacío")
            return None
        
        # Regla 3: Validar precio
        if precio <= 0:
            print("❌ Error: El precio debe ser mayor a 0")
            return None
        
        # Regla 4: Validar stock
        if stock < 0:
            print("❌ Error: El stock no puede ser negativo")
            return None
        
        # Crear objeto con los nuevos datos
        producto_actualizado = Producto(
            _id_producto=id_producto,
            _id_categoria=id_categoria,
            _nombre=nombre.strip(),
            _stock=stock,
            _precio=precio
        )
        
        return ProductoRepository.actualizar(producto_actualizado)
    
    @staticmethod
    def eliminar_producto(id_producto: int) -> bool:
        """
        REGLAS DE NEGOCIO para eliminar:
        1. El producto debe existir
        """
        
        producto = ProductoRepository.buscar_por_id(id_producto)
        if not producto:
            print(f"❌ Error: No existe producto con ID {id_producto}")
            return False
        
        return ProductoRepository.eliminar(id_producto)
    
    @staticmethod
    def mostrar_producto(producto: Producto):
        """Formatea la información de un producto para mostrarla"""
        print(f"""
┌─────────────────────────────────────────┐
│ ID:       {producto.id_producto}
│ Nombre:   {producto.nombre}
│ Categoría: {producto.id_categoria}
│ Stock:    {producto.stock} unidades
│ Precio:   ${producto.precio:.2f}
│ Fecha:    {producto.fecha}
└─────────────────────────────────────────┘
        """)
    
    @staticmethod
    def mostrar_lista_productos(productos: List[Producto]):
        """Muestra una lista de productos en formato tabla"""
        if not productos:
            print("📦 No hay productos para mostrar")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<6} {'NOMBRE':<30} {'STOCK':<10} {'PRECIO':<12}")
        print("="*80)
        
        for p in productos:
            print(f"{p.id_producto:<6} {p.nombre:<30} {p.stock:<10} ${p.precio:<12.2f}")
        
        print("="*80)
        print(f"Total: {len(productos)} productos\n")