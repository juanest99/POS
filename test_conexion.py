from database.connection import conexion

# Probar conexión consultando usuarios
query = "SELECT nombre, rol FROM USUARIO"
resultados = conexion(query, None)

if resultados:
    print("✅ Conexión exitosa!")
    print("\n📋 Usuarios en la base de datos:")
    for usuario in resultados:
        print(f"   👤 {usuario[0]} - {usuario[1]}")
else:
    print("❌ No se pudieron obtener usuarios")