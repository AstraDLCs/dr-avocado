import sqlite3

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
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'usuario'
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

    # Insertar el usuario administrador si no existe
    cursor.execute("""
        INSERT OR IGNORE INTO Usuarios (usuario, contrasena, rol) 
        VALUES ('admin', 'admin', 'administrador')
    """)

    conn.commit()
    conn.close()
    print("La base de datos 'turismos.db' se ha creado con éxito.")


def insert_test_data():
    """
    Inserta datos de prueba de ciudades y lugares turísticos de Perú en la base de datos.
    """
    conn = sqlite3.connect("turismos.db")
    cursor = conn.cursor()

    # Insertar datos de ciudades
    ciudades = [
        ("Lima", "Capital de Perú, centro político y cultural."),
        ("Cusco", "Ciudad histórica y puerta de entrada al Imperio Inca."),
        ("Arequipa", "Ciudad de sillar y arquitectura colonial."),
        ("Piura", "Ciudad en el norte de Perú, con hermosas playas."),
        ("Trujillo", "Ciudad con rica cultura precolombina.")
    ]
    cursor.executemany("INSERT INTO Ciudades (nombre, descripcion) VALUES (?, ?)", ciudades)

    # Obtener los IDs asignados a cada ciudad
    cursor.execute("SELECT id, nombre FROM Ciudades")
    ciudades_dict = {nombre: id for (id, nombre) in cursor.fetchall()}

    # Datos de prueba para lugares turísticos
    lugares = [
        # Lugares en Lima
        (ciudades_dict["Lima"], "Plaza Mayor", 0.0, "Plaza principal de Lima, rodeada de edificios históricos."),
        (ciudades_dict["Lima"], "Museo Larco", 15.0, "Museo con una extensa colección de arte precolombino."),
        (ciudades_dict["Lima"], "Parque Kennedy", 0.0, "Parque popular en el corazón de Miraflores."),
        
        # Lugares en Cusco
        (ciudades_dict["Cusco"], "Sacsayhuamán", 40.0, "Ruinas incas cercanas a la ciudad de Cusco."),
        (ciudades_dict["Cusco"], "Valle Sagrado", 50.0, "Hermoso valle con mercados y sitios arqueológicos."),
        (ciudades_dict["Cusco"], "Machu Picchu", 70.0, "La ciudadela inca ubicada en lo alto de los Andes."),
        
        # Lugares en Arequipa
        (ciudades_dict["Arequipa"], "Monasterio de Santa Catalina", 20.0, "Complejo religioso con arquitectura colonial."),
        (ciudades_dict["Arequipa"], "Cañón del Colca", 30.0, "Impresionante cañón, hogar del cóndor andino."),
        
        # Lugares en Piura
        (ciudades_dict["Piura"], "Playa Los Órganos", 10.0, "Hermosa playa en la costa de Piura."),
        (ciudades_dict["Piura"], "Reserva Natural de Piura", 5.0, "Reserva natural con biodiversidad costera."),
        
        # Lugares en Trujillo
        (ciudades_dict["Trujillo"], "Chan Chan", 20.0, "Ciudad precolombina de adobe, la más grande de su tipo en América."),
        (ciudades_dict["Trujillo"], "Huacas del Sol y de la Luna", 25.0, "Complejo arqueológico en la región de La Libertad, cerca de Trujillo.")
    ]
    cursor.executemany(
        "INSERT INTO Lugares (ciudad_id, nombre, precio, descripcion) VALUES (?, ?, ?, ?)", 
        lugares
    )

    conn.commit()
    conn.close()
    print("Datos de prueba insertados exitosamente en 'turismos.db'.")


if __name__ == "__main__":
    create_database()
    insert_test_data()
