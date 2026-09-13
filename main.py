from fastapi import FastAPI, HTTPException

from app.database import crear_tabla
from app.modelos import Producto
from app.logic import (crear_producto, 
                       listar_productos, 
                       obtener_producto, 
                       actualizar_producto,
                       eliminar_producto)

# Create FastAPI aplication
app = FastAPI()

# Create the products table when the application starts
# If it does not yet exist in the database
crear_tabla()

#--------------
# HOME - GET /
#--------------
@app.get("/")
def inicio():
    """Muestra un mensaje de bienvenida a la API"""
    return {"mensaje": "Bienvenido al catalogo KAI 3D"}

#----------------------
# CREATE - POST /items
#----------------------
@app.post("/items")
def nuevo_producto(nombre: str,
                   description: str, 
                   categoria: str, 
                   precio: float):
    """Create a new product in the catalog"""
# Create a Product object using the data received from the API
    producto = Producto(nombre, description, categoria, precio)
# Send the object to logic.py to save it in SQLite
    producto_creado = crear_producto(producto)
# Convert the object to a dictionary to return it as JSON
    return producto_creado.to_dict()

#-------------------
# READ - GET /items
#-------------------
@app.get("/items")
def obtener_productos():
    """Devuelve todos los productos guardados en el catalogo"""
    return listar_productos()

#-------------------------
# READ - GET /items /{id}
#-------------------------
@app.get("/items/{id}")
def obtener_producto_por_id(id: int):
    """Devuelve un producto especifico utilizando su ID"""
# Search for the product using the function defined in logic.py
    producto = obtener_producto(id)
# If logic.py returns None, the product does not exist
    if producto is None: 
        raise HTTPException(status_code=404,
                            detail="Producto no encontrado")
    return producto

#---------------------------
# UPDATE - PUT /items /{id}
#---------------------------
@app.put("/items/{id}")
def modificar_producto(id: int,
                       nombre: str, 
                       descripcion: str,
                       categoria: str,
                       precio: float):
    """Actualiza los datos de un producto existente"""
# Create a Product object with the new data received
    producto = Producto(nombre, descripcion, categoria, precio)
# Send the new data to logic.py along with the ID
    producto_actualizado = actualizar_producto(id, producto)
# If the ID does not exist, it returns an HTTP 404 error
    if producto_actualizado is None:
        raise HTTPException(status_code=404,
                            detail="Producto no encontrado")
    return producto_actualizado

#------------------------------
# DELETE - DELETE /items /{id}
#------------------------------
@app.delete("/items/{id}")
def borrar_producto(id: int):
    """Elimina un producto existente pos su ID"""
# logic.py returns True if the product was deleted
# and False if the ID does not exist
    eliminado = eliminar_producto(id)

    if not eliminado:
        raise HTTPException(status_code=404,
                            detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}
