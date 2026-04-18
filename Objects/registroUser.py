#solo es de prueba, tiene que funcioanr con el front
from Db.DB import conexion
from Objects.Usuario import Usuario
from dataclasses import dataclass

@dataclass
class RegistroUser:
    usuario:Usuario

    def guardar(self):
        try:
            query = f"""INSERT INTO USUARIO(nombre,email,contrasena, estado,rol)
            VALUES ('{self.usuario.nombre}', '{self.usuario.email}',
            '{self.usuario.contrasena}', {self.usuario.estado}, '{self.usuario.rol}');"""
            conexion(query,None)
        except Exception as e:
            print(e)
    @staticmethod
    def buscar(nombre,contrasena):
        try:
            query = f"""SELECT * FROM USUARIO U 
            WHERE (U.nombre = '{nombre}') AND (U.contrasena ='{contrasena}');"""
            return conexion(query,None)
        except Exception as e:
            print(e)
            return None

