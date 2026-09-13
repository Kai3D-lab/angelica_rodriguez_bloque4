import sqlite3

# SQLite database filename
DB_NAME = "catalogo_kai3d.db"

def conectar():
    """Creates and returns a connection to the SQLite database. """
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    """Create the products table if it does not already exist."""
    conexion = conectar()
    cursor = conexion.cursor()
# Create the main catalog table
# The ID is automatically generated for each new product
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL)""")
# Save the changes and close the connection
    conexion.commit()
    conexion.close()

