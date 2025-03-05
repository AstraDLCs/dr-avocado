from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
import sqlite3
import json

load_dotenv()

def create_database():
    """
    Crea la base de datos 'turismos.db' con las tablas: Ciudades, Lugares, Usuarios y Reservas.
    """
    conn = sqlite3.connect("turismos.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ciudades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Lugares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            moneda TEXT NOT NULL DEFAULT 'PEN',
            descripcion TEXT,
            FOREIGN KEY (ciudad_id) REFERENCES Ciudades(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL 
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            lugar_id INTEGER NOT NULL,
            fecha_reserva TEXT NOT NULL,  -- formato ISO 'YYYY-MM-DD'
            FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
            FOREIGN KEY (lugar_id) REFERENCES Lugares(id)
        );
    ''')

    conn.commit()
    conn.close()
    print("La base de datos 'turismos.db' se ha creado con éxito.")

if __name__ == "__main__":
    # Ejecutar la creación de la base de datos (esto se debe hacer solo una vez)
    create_database()
