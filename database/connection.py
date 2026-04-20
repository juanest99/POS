import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="pos",
            user="postgres",
            password="postgres",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def conexion(query, params=None):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        try:
            resultados = cursor.fetchall()
        except psycopg2.ProgrammingError:
            resultados = None
        
        conn.commit()
        cursor.close()
        conn.close()
        return resultados
        
    except Exception as e:
        print(f"❌ Error en consulta: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None