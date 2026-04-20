import csv
import psycopg2
import sys
import os

def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        database="pos",
        user="postgres",
        password="postgres"
    )

# Mapeo de categorías según tu imagen
MAPEO_CATEGORIAS = {
    'VARIOS': 0,
    'CONGELADOS': 2,
    'LACTEOS Y REFRIGERADOS': 3,
    'PANADERIA Y PASTELERIA': 4,
    'FRUTAS Y VEGETALES': 5,
    'DULCERIA Y SNACKS': 6,
    'CUIDADO PERSONAL': 7,
    'ASEO DEL HOGAR': 8,
    'BEBIDAS': 9,
    'ABARROTES': 10,
}

def importar_productos(archivo_csv):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    importados = 0
    errores = 0
    duplicados = 0
    
    print(f"📂 Leyendo archivo: {archivo_csv}")
    
    with open(archivo_csv, 'r', encoding='utf-8-sig') as file:
        # Detectar el delimitador automáticamente
        muestra = file.read(1024)
        file.seek(0)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(muestra)
        reader = csv.DictReader(file, dialect=dialect)
        
        print(f"📋 Columnas encontradas: {reader.fieldnames}")
        print(f"📊 Iniciando importación...\n")
        
        for row in reader:
            categoria = row.get('categoria', '').strip()
            codigo = row.get('codigo', '').strip()
            nombre = row.get('nombre', '').strip()
            barras = row.get('barras', '').strip()
            precio_str = row.get('precio', '0').strip()
            
            if not nombre:
                errores += 1
                continue
            
            # Convertir precio
            try:
                precio = float(precio_str.replace(',', '.'))
            except:
                precio = 0
            
            # Mapear categoría
            id_categoria = MAPEO_CATEGORIAS.get(categoria, 0)
            
            # Si no hay código de producto, usar el nombre como referencia
            if not codigo:
                codigo = nombre[:50]  # Máximo 50 caracteres
            
            query = """
                INSERT INTO PRODUCTO (id_categoria, codigo_producto, nombre, codigo_barras, stock, precio)
                VALUES (%s, %s, %s, %s, 0, %s)
            """
            
            try:
                cursor.execute(query, (id_categoria, codigo, nombre, barras, precio))
                importados += 1
                if importados % 100 == 0:
                    print(f"✅ Procesados {importados} productos...")
            except psycopg2.errors.UniqueViolation:
                duplicados += 1
                print(f"⚠️ Producto duplicado (código de barras): {nombre}")
                conn.rollback()
                conn = conectar_bd()
                cursor = conn.cursor()
            except Exception as e:
                errores += 1
                print(f"❌ Error en '{nombre}': {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"📊 RESUMEN DE IMPORTACIÓN")
    print(f"{'='*50}")
    print(f"✅ Productos importados: {importados}")
    print(f"⚠️ Duplicados omitidos: {duplicados}")
    print(f"❌ Errores: {errores}")
    print(f"{'='*50}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python importar_productos.py productos.csv")
        sys.exit(1)
    
    if not os.path.exists(sys.argv[1]):
        print(f"❌ Archivo no encontrado: {sys.argv[1]}")
        sys.exit(1)
    
    importar_productos(sys.argv[1])