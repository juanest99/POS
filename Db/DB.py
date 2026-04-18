import psycopg2
def conexion(query,params):

    conexion = psycopg2.connect(
        host="localhost",
        database="POS",
        user="postgres",
        password="postgres",
        port="5432"
    )

    cursor = conexion.cursor()

    cursor.execute(query,params)

    try:
      resultados = cursor.fetchall()
    except:
        resultados= None


    conexion.commit()
    cursor.close()
    conexion.close()

    return resultados