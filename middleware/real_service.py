from models.usuario import Usuario
from middleware.service_interface import ServiceInterface
from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from models.categoria_repository import CategoriaRepository
from models.usuario_repository import UsuarioRepository
from models.movimiento_repository import MovimientoRepository
from services.venta_service import VentaService

class RealService(ServiceInterface):
    def acceder(self, persona: Usuario, *args, **kwargs):
        nombre = kwargs.get('nombre', persona.nombre)
        contrasena = kwargs.get('contrasena', '')
        rol = kwargs.get('rol', persona.rol)
        
        print(f"✅ Ejecutando servicio real para: {persona.nombre}")
        
        if rol.lower() == 'admin':
            print("👑 Acceso de Administrador concedido")
            print("   - Gestión de productos")
            print("   - Gestión de inventario")
            print("   - Reportes financieros")
            print("   - Gestión de usuarios")
            self._menu_admin(persona)
        elif rol.lower() == 'cajero':
            print("💵 Acceso de Cajero concedido")
            print("   - Registrar ventas")
            print("   - Buscar productos")
            print("   - Procesar pagos")
            self._menu_cajero(persona)
        else:
            print(f"❌ Rol desconocido: {rol}")
    
    # ==================== MENÚ PRINCIPAL ADMIN ====================
    
    def _menu_admin(self, usuario):
        while True:
            print(f"\n{'='*50}")
            print(f"   PANEL ADMINISTRADOR - {usuario.nombre}")
            print(f"{'='*50}")
            print("1. Gestionar Productos")
            print("2. Gestionar Inventario")
            print("3. Ver Reportes")
            print("4. Gestionar Usuarios")
            print("5. Salir")
            print(f"{'='*50}")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self._menu_gestion_productos()
            elif opcion == "2":
                self._menu_gestion_inventario(usuario)
            elif opcion == "3":
                self._menu_reportes()
            elif opcion == "4":
                self._menu_gestion_usuarios()
            elif opcion == "5":
                print("👋 Sesión cerrada")
                break
            else:
                print("❌ Opción inválida")
    
    # ==================== MENÚ CAJERO ====================
    
    def _menu_cajero(self, usuario):
        venta_service = VentaService()
        while True:
            print(f"\n{'='*50}")
            print(f"   PANEL CAJERO - {usuario.nombre}")
            print(f"{'='*50}")
            print("1. Nueva venta")
            print("2. Buscar producto")
            print("3. Ver historial de ventas")
            print("4. Ver estadísticas del día")
            print("5. Salir")
            print(f"{'='*50}")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self._nueva_venta(usuario, venta_service)
            elif opcion == "2":
                self._buscar_producto()
            elif opcion == "3":
                self._historial_ventas(usuario)
            elif opcion == "4":
                self._estadisticas_ventas()
            elif opcion == "5":
                print("👋 Sesión cerrada")
                break
            else:
                print("❌ Opción inválida")

    def _nueva_venta(self, usuario, venta_service):
        print("\n🛒 NUEVA VENTA")
        print("="*40)
        
        while True:
            # Mostrar carrito actual
            venta_service.ver_carrito()
            
            print("\n📋 OPCIONES:")
            print("   1. Agregar producto")
            print("   2. Modificar cantidad")
            print("   3. Quitar producto")
            print("   4. Vaciar carrito")
            print("   5. Procesar pago")
            print("   6. Cancelar venta")
            
            opcion = input("\nSeleccione: ")
            
            if opcion == "1":
                try:
                    id_producto = int(input("ID del producto: "))
                    cantidad = int(input("Cantidad: "))
                    venta_service.agregar_al_carrito(id_producto, cantidad)
                except ValueError:
                    print("❌ Ingrese números válidos")
            
            elif opcion == "2":
                try:
                    id_producto = int(input("ID del producto: "))
                    nueva_cantidad = int(input("Nueva cantidad: "))
                    venta_service.modificar_cantidad(id_producto, nueva_cantidad)
                except ValueError:
                    print("❌ Ingrese números válidos")
            
            elif opcion == "3":
                try:
                    id_producto = int(input("ID del producto a quitar: "))
                    venta_service.quitar_del_carrito(id_producto)
                except ValueError:
                    print("❌ Ingrese número válido")
            
            elif opcion == "4":
                venta_service.vaciar_carrito()
            
            elif opcion == "5":
                if not venta_service.carrito:
                    print("❌ El carrito está vacío")
                    continue
                
                _, total = venta_service.ver_carrito()
                print(f"\n💰 TOTAL A PAGAR: ${total:.2f}")
                
                print("\n💳 Métodos de pago:")
                print("   1. Efectivo")
                print("   2. Tarjeta débito/crédito")
                print("   3. Transferencia")
                
                metodo_opcion = input("Seleccione método de pago: ")
                metodos = {"1": "efectivo", "2": "tarjeta", "3": "transferencia"}
                metodo_pago = metodos.get(metodo_opcion, "efectivo")
                
                try:
                    monto_recibido = float(input("Monto recibido: "))
                    id_venta = venta_service.procesar_pago(usuario.id_usuario, metodo_pago, monto_recibido)
                    
                    if id_venta:
                        print("\n¿Desea ver la factura? (s/n): ", end="")
                        if input().lower() == 's':
                            VentaService.mostrar_factura(id_venta)
                        break
                except ValueError:
                    print("❌ Ingrese un monto válido")
            
            elif opcion == "6":
                venta_service.vaciar_carrito()
                print("❌ Venta cancelada")
                break
            
            else:
                print("❌ Opción inválida")

    def _historial_ventas(self, usuario):
        from models.venta_repository import VentaRepository
        
        print("\n📜 HISTORIAL DE VENTAS")
        print("="*40)
        
        ventas = VentaRepository.listar_por_usuario(usuario.id_usuario)
        
        if not ventas:
            print("No hay ventas registradas")
        else:
            print(f"\n{'ID':<6} {'FECHA':<12} {'TOTAL':<12} {'MÉTODO':<12}")
            print("-"*50)
            for v in ventas:
                fecha_str = v.fecha.strftime("%Y-%m-%d") if v.fecha else "N/A"
                print(f"{v.id_venta:<6} {fecha_str:<12} ${v.total:<12.2f} {v.metodo_pago:<12}")
        
        input("\nPresione Enter para continuar...")

    def _estadisticas_ventas(self):
        from services.venta_service import VentaService
        
        stats = VentaService.obtener_estadisticas_rapidas()
        
        print("\n📊 ESTADÍSTICAS DEL DÍA")
        print("="*40)
        print(f"💰 Ventas del día: {stats['ventas_hoy']}")
        print(f"💵 Total recaudado: ${stats['total_hoy']:.2f}")
        print(f"📈 Promedio por venta: ${stats['promedio_hoy']:.2f}")
        print("="*40)
        
        input("\nPresione Enter para continuar...")
    
    # ==================== GESTIÓN DE PRODUCTOS ====================
    
    def _menu_gestion_productos(self):
        while True:
            print(f"\n{'='*50}")
            print("   GESTIÓN DE PRODUCTOS")
            print(f"{'='*50}")
            print("1. Listar productos")
            print("2. Crear producto")
            print("3. Buscar producto")
            print("4. Actualizar producto")
            print("5. Eliminar producto")
            print("6. Volver al menú principal")
            print(f"{'='*50}")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self._listar_productos()
            elif opcion == "2":
                self._crear_producto()
            elif opcion == "3":
                self._buscar_producto()
            elif opcion == "4":
                self._actualizar_producto()
            elif opcion == "5":
                self._eliminar_producto()
            elif opcion == "6":
                break
            else:
                print("❌ Opción inválida")
    
    def _listar_productos(self):
        print("\n📋 LISTANDO PRODUCTOS...")
        productos = ProductoService.listar_productos()
        ProductoService.mostrar_lista_productos(productos)
        input("Presione Enter para continuar...")
    
    def _crear_producto(self):
        print("\n➕ CREAR NUEVO PRODUCTO")
        print("="*40)
        
        # Mostrar categorías disponibles
        categorias = CategoriaRepository.listar_todas()
        if not categorias:
            print("❌ No hay categorías registradas.")
            print("   Ejecute en PostgreSQL:")
            print("   INSERT INTO CATEGORIAS VALUES (1, 'Electrónicos');")
            input("Presione Enter para continuar...")
            return
        
        print("\n📁 Categorías disponibles:")
        for cat in categorias:
            print(f"   {cat['id_categoria']} - {cat['nombre']}")
        
        try:
            id_categoria = int(input("\nID de categoría: "))
            nombre = input("Nombre del producto: ")
            stock = int(input("Cantidad en stock: "))
            precio = float(input("Precio: "))
            
            producto = ProductoService.crear_producto(id_categoria, nombre, stock, precio)
            
            if producto:
                print("\n✅ PRODUCTO CREADO EXITOSAMENTE")
                ProductoService.mostrar_producto(producto)
            else:
                print("\n❌ No se pudo crear el producto")
        except ValueError:
            print("❌ Error: Debe ingresar números válidos")
        
        input("\nPresione Enter para continuar...")
    
    def _buscar_producto(self):
        print("\n🔍 BUSCAR PRODUCTO")
        print("="*40)
        
        try:
            id_producto = int(input("Ingrese el ID del producto: "))
            producto = ProductoService.buscar_producto(id_producto)
            
            if producto:
                ProductoService.mostrar_producto(producto)
            else:
                print(f"❌ No se encontró producto con ID {id_producto}")
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
        
        input("\nPresione Enter para continuar...")
    
    def _actualizar_producto(self):
        print("\n✏️ ACTUALIZAR PRODUCTO")
        print("="*40)
        
        try:
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))
            
            producto_existente = ProductoService.buscar_producto(id_producto)
            if not producto_existente:
                print(f"❌ No existe producto con ID {id_producto}")
                input("Presione Enter para continuar...")
                return
            
            print("\n📌 DATOS ACTUALES:")
            ProductoService.mostrar_producto(producto_existente)
            
            print("\n📝 INGRESE NUEVOS DATOS (deje vacío para mantener el actual):")
            
            categorias = CategoriaRepository.listar_todas()
            print("\n📁 Categorías disponibles:")
            for cat in categorias:
                print(f"   {cat['id_categoria']} - {cat['nombre']}")
            
            id_categoria_input = input(f"ID de categoría [{producto_existente.id_categoria}]: ")
            id_categoria = int(id_categoria_input) if id_categoria_input else producto_existente.id_categoria
            
            nombre = input(f"Nombre [{producto_existente.nombre}]: ")
            nombre = nombre if nombre else producto_existente.nombre
            
            stock_input = input(f"Stock [{producto_existente.stock}]: ")
            stock = int(stock_input) if stock_input else producto_existente.stock
            
            precio_input = input(f"Precio [{producto_existente.precio}]: ")
            precio = float(precio_input) if precio_input else producto_existente.precio
            
            producto = ProductoService.actualizar_producto(id_producto, id_categoria, nombre, stock, precio)
            
            if producto:
                print("\n✅ PRODUCTO ACTUALIZADO EXITOSAMENTE")
                ProductoService.mostrar_producto(producto)
            else:
                print("\n❌ No se pudo actualizar el producto")
                
        except ValueError:
            print("❌ Error: Debe ingresar números válidos")
        
        input("\nPresione Enter para continuar...")
    
    def _eliminar_producto(self):
        print("\n🗑️ ELIMINAR PRODUCTO")
        print("="*40)
        
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            
            producto = ProductoService.buscar_producto(id_producto)
            if not producto:
                print(f"❌ No existe producto con ID {id_producto}")
                input("Presione Enter para continuar...")
                return
            
            print("\n⚠️  PRODUCTO A ELIMINAR:")
            ProductoService.mostrar_producto(producto)
            
            confirmacion = input("\n¿Está SEGURO de eliminar este producto? (s/n): ")
            
            if confirmacion.lower() == 's':
                if ProductoService.eliminar_producto(id_producto):
                    print("✅ Producto eliminado exitosamente")
                else:
                    print("❌ No se pudo eliminar el producto")
            else:
                print("❌ Eliminación cancelada")
                
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
        
        input("\nPresione Enter para continuar...")
    
    # ==================== GESTIÓN DE INVENTARIO ====================
    
    def _menu_gestion_inventario(self, usuario):
        while True:
            print(f"\n{'='*50}")
            print("   GESTIÓN DE INVENTARIO")
            print(f"{'='*50}")
            print("1. Registrar entrada de productos (compra)")
            print("2. Registrar salida de productos (venta/merma)")
            print("3. Ajustar stock (corrección física)")
            print("4. Consultar stock actual")
            print("5. Ver historial de movimientos")
            print("6. Ver resumen general")
            print("7. Volver al menú principal")
            print(f"{'='*50}")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self._registrar_entrada(usuario)
            elif opcion == "2":
                self._registrar_salida(usuario)
            elif opcion == "3":
                self._ajustar_stock(usuario)
            elif opcion == "4":
                self._consultar_stock()
            elif opcion == "5":
                self._ver_historial()
            elif opcion == "6":
                self._ver_resumen_inventario()
            elif opcion == "7":
                break
            else:
                print("❌ Opción inválida")
    
    def _registrar_entrada(self, usuario):
        print("\n📦 REGISTRAR ENTRADA DE PRODUCTOS (COMPRA)")
        print("="*40)
        
        try:
            # Mostrar productos existentes
            productos = ProductoService.listar_productos()
            if not productos:
                print("❌ No hay productos registrados. Cree productos primero.")
                input("Presione Enter para continuar...")
                return
            
            ProductoService.mostrar_lista_productos(productos)
            
            id_producto = int(input("\nID del producto: "))
            cantidad = int(input("Cantidad que entra: "))
            
            print("\n📝 Motivo de la entrada:")
            print("   1. Compra a proveedor")
            print("   2. Devolución de cliente")
            print("   3. Ajuste de inventario")
            
            motivo_opcion = input("Seleccione (1-3): ")
            
            motivos = {
                "1": "compra",
                "2": "devolucion_cliente",
                "3": "ajuste_inventario"
            }
            
            motivo = motivos.get(motivo_opcion, "compra")
            
            # Obtener ID del usuario (necesitas obtenerlo de la BD)
            # Por ahora usamos un ID fijo (1) - en producción deberías obtener el real
            resultado = InventarioService.registrar_entrada(
                id_producto=id_producto,
                id_usuario=1,  # Temporal, deberías obtener el ID real del usuario
                cantidad=cantidad,
                motivo=motivo
            )
            
            if resultado:
                print("\n✅ Entrada registrada exitosamente")
            else:
                print("\n❌ Error al registrar entrada")
                
        except ValueError:
            print("❌ Error: Debe ingresar números válidos")
        
        input("\nPresione Enter para continuar...")
    
    def _registrar_salida(self, usuario):
        print("\n📤 REGISTRAR SALIDA DE PRODUCTOS")
        print("="*40)
        
        try:
            productos = ProductoService.listar_productos()
            if not productos:
                print("❌ No hay productos registrados.")
                input("Presione Enter para continuar...")
                return
            
            ProductoService.mostrar_lista_productos(productos)
            
            id_producto = int(input("\nID del producto: "))
            cantidad = int(input("Cantidad que sale: "))
            
            print("\n📝 Motivo de la salida:")
            print("   1. Venta")
            print("   2. Merma (producto dañado)")
            print("   3. Devolución a proveedor")
            print("   4. Ajuste de inventario")
            
            motivo_opcion = input("Seleccione (1-4): ")
            
            motivos = {
                "1": "venta",
                "2": "merma",
                "3": "devolucion_proveedor",
                "4": "ajuste_inventario"
            }
            
            motivo = motivos.get(motivo_opcion, "venta")
            
            resultado = InventarioService.registrar_salida(
                id_producto=id_producto,
                id_usuario=1,  # Temporal
                cantidad=cantidad,
                motivo=motivo
            )
            
            if resultado:
                print("\n✅ Salida registrada exitosamente")
            else:
                print("\n❌ Error al registrar salida")
                
        except ValueError:
            print("❌ Error: Debe ingresar números válidos")
        
        input("\nPresione Enter para continuar...")
    
    def _ajustar_stock(self, usuario):
        print("\n🔧 AJUSTAR STOCK (CORRECCIÓN FÍSICA)")
        print("="*40)
        print("Este ajuste compara el stock del sistema con el conteo físico")
        print("y crea automáticamente el movimiento necesario.\n")
        
        try:
            id_producto = int(input("ID del producto a ajustar: "))
            
            # Mostrar stock actual
            stock_actual, nombre = InventarioService.consultar_stock(id_producto)
            
            if stock_actual is None:
                print(f"❌ Producto con ID {id_producto} no existe")
                input("Presione Enter para continuar...")
                return
            
            print(f"\n📊 Producto: {nombre}")
            print(f"📦 Stock actual en sistema: {stock_actual} unidades")
            
            nueva_cantidad = int(input("Nueva cantidad (conteo físico): "))
            
            print("\n📝 Motivo del ajuste:")
            print("   1. Ajuste físico (conteo de inventario)")
            print("   2. Corrección de error")
            
            motivo_opcion = input("Seleccione (1-2): ")
            motivo = "ajuste_fisico" if motivo_opcion == "1" else "correccion_error"
            
            resultado = InventarioService.registrar_ajuste(
                id_producto=id_producto,
                id_usuario=1,  # Temporal
                nueva_cantidad=nueva_cantidad,
                motivo=motivo
            )
            
            if resultado:
                print("\n✅ Ajuste completado exitosamente")
            else:
                print("\n⚠️ No se realizó ningún ajuste")
                
        except ValueError:
            print("❌ Error: Debe ingresar números válidos")
        
        input("\nPresione Enter para continuar...")
    
    def _consultar_stock(self):
        print("\n🔍 CONSULTAR STOCK")
        print("="*40)
        
        try:
            id_producto = int(input("ID del producto: "))
            stock, nombre = InventarioService.consultar_stock(id_producto)
            
            if stock is None:
                print(f"❌ Producto con ID {id_producto} no existe")
            else:
                print(f"\n📊 Producto: {nombre}")
                print(f"📦 Stock actual: {stock} unidades")
                
                if stock < 10:
                    print("⚠️ ALERTA: Stock bajo (menos de 10 unidades)")
                    
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_historial(self):
        print("\n📜 VER HISTORIAL DE MOVIMIENTOS")
        print("="*40)
        
        try:
            id_producto = int(input("ID del producto (0 para todos): "))
            
            if id_producto == 0:
                print("\n📋 MOSTRANDO TODOS LOS MOVIMIENTOS...")
                movimientos = MovimientoRepository.listar_todos(limite=30)
                
                if not movimientos:
                    print("📦 No hay movimientos registrados")
                else:
                    print(f"\n{'='*80}")
                    print(f"{'ID':<6} {'PRODUCTO':<25} {'TIPO':<10} {'CANTIDAD':<10} {'MOTIVO':<15} {'FECHA':<12}")
                    print(f"{'='*80}")
                    for m in movimientos:
                        fecha_str = m.fecha.strftime("%Y-%m-%d") if m.fecha else "N/A"
                        signo = "+" if m.tipo == "entrada" else "-"
                        print(f"{m.id_movimiento:<6} {'Producto':<25} {m.tipo:<10} {signo}{m.cantidad:<9} {m.motivo:<15} {fecha_str:<12}")
                    print(f"{'='*80}")
            else:
                InventarioService.ver_historial_producto(id_producto)
                
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_resumen_inventario(self):
        InventarioService.ver_resumen_general()
        input("\nPresione Enter para continuar...")
    
    # ==================== REPORTES ====================
    
    def _menu_reportes(self):
        print("\n📊 MÓDULO DE REPORTES (Próximamente)")
        input("Presione Enter para continuar...")
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def _menu_gestion_usuarios(self):
        print("\n👥 GESTIÓN DE USUARIOS (Próximamente)")
        input("Presione Enter para continuar...")