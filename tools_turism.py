import json
import sqlite3
from agno.tools import Toolkit
from agno.utils.log import logger

class TurismToolkit(Toolkit):
    def __init__(self):
        # Se registra el toolkit con el nombre "tools_turism" y se añaden las funciones.
        super().__init__(name="tools_turism")
        self.register(self.get_ciudades)
        self.register(self.get_lugares_en_ciudad)
        self.register(self.registrar_usuario)
        self.register(self.crear_reserva)
        self.register(self.obtener_reservas_usuario)
        self.register(self.verificar_cuenta)

    def get_ciudades(self) -> str:
        """
        Retorna la lista de ciudades registradas en la base de datos en formato JSON.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion FROM Ciudades")
            rows = cursor.fetchall()
            ciudades = [
                {"id": row[0], "nombre": row[1], "descripcion": row[2]}
                for row in rows
            ]
            logger.info("Se obtuvieron las ciudades.")
            return json.dumps({"ciudades": ciudades})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener ciudades: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def get_lugares_en_ciudad(self, ciudad: str) -> str:
        """
        Retorna la lista de lugares de una ciudad específica en formato JSON.
        Realiza la búsqueda de forma insensible a mayúsculas para asegurar coincidencias
        independientemente del uso de mayúsculas o minúsculas en el nombre.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            query = """
                SELECT Lugares.id, Lugares.nombre, Lugares.precio, Lugares.moneda, Lugares.descripcion
                FROM Lugares
                INNER JOIN Ciudades ON Lugares.ciudad_id = Ciudades.id
                WHERE LOWER(Ciudades.nombre) = ?
            """
            cursor.execute(query, (ciudad.lower(),))
            rows = cursor.fetchall()
            lugares = [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "precio": row[2],
                    "moneda": row[3],
                    "descripcion": row[4],
                }
                for row in rows
            ]
            logger.info(f"Se obtuvieron lugares para la ciudad {ciudad}.")
            return json.dumps({"lugares": lugares})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener lugares para {ciudad}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def registrar_usuario(self, usuario: str, contrasena: str) -> str:
        """
        Registra un nuevo usuario en la base de datos y retorna el resultado en formato JSON.
        Se utiliza una consulta parametrizada para evitar inyecciones SQL.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            query = "INSERT INTO Usuarios (usuario, contrasena) VALUES (?, ?)"
            cursor.execute(query, (usuario, contrasena))
            conn.commit()
            logger.info(f"Usuario {usuario} registrado exitosamente.")
            return json.dumps({"mensaje": f"Usuario {usuario} registrado exitosamente."})
        except sqlite3.IntegrityError:
            logger.error("El usuario ya existe.")
            return json.dumps({"error": "El usuario ya existe."})
        except sqlite3.Error as e:
            logger.error(f"Error al registrar usuario {usuario}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def crear_reserva(self, usuario: str, lugar: str, fecha_reserva: str) -> str:
        """
        Crea una reserva para un usuario en un lugar dado.
        Se obtienen los IDs del usuario y del lugar a partir de sus nombres (usando búsqueda insensible a mayúsculas),
        y se inserta la reserva usando estos IDs.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            # Obtener el ID del usuario
            cursor.execute("SELECT id FROM Usuarios WHERE usuario = ?", (usuario,))
            user_row = cursor.fetchone()
            if not user_row:
                logger.error(f"El usuario {usuario} no existe.")
                return json.dumps({"error": f"El usuario {usuario} no existe."})
            usuario_id = user_row[0]
            
            # Obtener el ID del lugar usando el nombre (búsqueda insensible a mayúsculas)
            cursor.execute("SELECT id FROM Lugares WHERE LOWER(nombre) = ?", (lugar.lower(),))
            lugar_row = cursor.fetchone()
            if not lugar_row:
                logger.error(f"El lugar {lugar} no existe.")
                return json.dumps({"error": f"El lugar {lugar} no existe."})
            lugar_id = lugar_row[0]
            
            # Insertar la reserva
            query = "INSERT INTO Reservas (usuario_id, lugar_id, fecha_reserva) VALUES (?, ?, ?)"
            cursor.execute(query, (usuario_id, lugar_id, fecha_reserva))
            conn.commit()
            logger.info(f"Reserva creada para el usuario {usuario} en el lugar {lugar}.")
            return json.dumps({"mensaje": "Reserva creada exitosamente."})
        except sqlite3.Error as e:
            logger.error(f"Error al crear reserva para el usuario {usuario}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()


    def obtener_reservas_usuario(self, usuario: str) -> str:
        """
        Retorna las reservas realizadas por un usuario en formato JSON.
        Se obtiene el ID del usuario a partir del nombre y se unen las tablas Reservas y Lugares
        para obtener el nombre del lugar y la fecha de la reserva.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            # Obtener el ID del usuario
            cursor.execute("SELECT id FROM Usuarios WHERE usuario = ?", (usuario,))
            user_row = cursor.fetchone()
            if not user_row:
                logger.error(f"El usuario {usuario} no existe.")
                return json.dumps({"error": f"El usuario {usuario} no existe."})
            usuario_id = user_row[0]
            
            # Consultar las reservas del usuario uniendo con Lugares para obtener el nombre del lugar
            query = """
                SELECT Reservas.id, Lugares.nombre, Reservas.fecha_reserva
                FROM Reservas
                INNER JOIN Lugares ON Reservas.lugar_id = Lugares.id
                WHERE Reservas.usuario_id = ?
            """
            cursor.execute(query, (usuario_id,))
            rows = cursor.fetchall()
            reservas = [
                {"id": row[0], "lugar": row[1], "fecha_reserva": row[2]}
                for row in rows
            ]
            logger.info(f"Se obtuvieron reservas para el usuario {usuario}.")
            return json.dumps({"reservas": reservas})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener reservas para el usuario {usuario}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def verificar_cuenta(self, usuario: str, contrasena: str) -> str:
        """
        Verifica si una cuenta existe en la base de datos y retorna si es válida junto con el rol asignado.
        Si la cuenta no existe o la contraseña es incorrecta, retorna que la cuenta no existe.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            query = "SELECT rol FROM Usuarios WHERE usuario = ? AND contrasena = ?"
            cursor.execute(query, (usuario, contrasena))
            row = cursor.fetchone()
            if row:
                rol = row[0]
                logger.info(f"Cuenta {usuario} verificada exitosamente, rol: {rol}.")
                return json.dumps({"valido": True, "rol": rol})
            else:
                logger.info(f"La cuenta {usuario} no existe o la contraseña es incorrecta.")
                return json.dumps({"valido": False, "mensaje": "La cuenta no existe."})
        except sqlite3.Error as e:
            logger.error(f"Error al verificar la cuenta {usuario}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()
