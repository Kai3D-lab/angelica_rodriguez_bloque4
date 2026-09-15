"""
================================================
       PSEUDOCODIGO - API CATALOGO KAI 3D
================================================

INICIO

    // --- 1. Preparacion del Sistema ---
    IMPORTAR FastAPI y HTTPException

    IMPORTAR funcion para crear la tabla de SQLite
    IMPORTAR clase Producto
    IMPORTAR funciones CRUD desde logic.py

    CREAR aplicacion FastAPI
    CREAR tabla productos SI NO EXISTE

    // --- 2. Ruta Principal ---
    CUANDO usuario acceda a GET "/" ENTONCES:
        DEVOLVER mensaje de bienvenida
    FIN

    // --- 3. Crear Producto ---
    CUANDO usuario envie POST "/items" ENTONCES:
        RECIBIR:
            nombre
            descripcion
            categoria
            precio

        CREAR objeto Producto con los datos recibidos
        ENVIAR producto a crear_producto()
        GUARDAR producto en SQLite
        DEVOLVER producto creado como JSON
    FIN

    // --- 4. Listar Productos ---
    CUANDO usuario acceda a GET "/items" ENTONCES:
        OBTENER todos los productos desde SQLite
        CONVERTIR productos a formato JSON
        DEVOLVER lista de productos
    FIN

    // --- 5. Buscar Producto por ID ---
    CUANDO usuario acceda a GET "/items/{id}" ENTONCES:
        BUSCAR producto por ID

        SI producto NO EXISTE ENTONCES:
            DEVOLVER error HTTP 404
            MOSTRAR "Producto no encontrado"
        
        SINO: 
            DEVOLVER producto como JSON 
        FIN SI
    FIN

    // --- 6. Actualizar Producto ---
    CUANDO usuario envie PUT "/items/{id}" ENTONCES:
        RECIBIR:
            nombre
            descripcion
            categoria
            precio

        CREAR objeto Producto con los nuevos datos
        BUSCAR producto por ID y ACTUALIZAR sus datos
        
        SI producto NO EXISTE ENTONCES:
            DEVOLVER error HTTP 404
            MOSTRAR "Producto no encontrado"
        
        SINO:
            GUARDAR cambios en SQLite
            DEVOLVER producto actualizado
        FIN SI
    FIN

    // --- 7. Eliminar Producto ---
    CUANDO usuario envie DELETE "/items/{id}" ENTONCES:
        BUSCAR producto por ID
        
        SI producto NO EXISTE ENTONCES:
            DEVOLVER error HTTP 404
            MOSTRAR "Producto no encontrado"
        
        SINO:
            ELIMINAR producto de SQLite 
            DEVOLVER mensaje "Producto eliminado correctamente"
        FIN SI
    FIN

    // --- 8. Persistencia ---
    GUARDAR todos los cambios inmediatamente en SQLite

    AL reiniciar el servidor:
        CONSERVAR los productos guardados anteriormente
FIN

"""

# =============================================================
# HOW TO RUN THIS API FROM THE VS CODE POWERSHELL TERMINAL
# =============================================================
# 1. Move to the project folder:
# cd "C:\Users\Angelica Rodriguez\Documents\CEI\CPY Python\Python\PEC_4"

# 2. Activate this project's virtual environment:
# .\venv\Scripts\Activate.ps1

# 3. Start the FastAPI server:
# python -m uvicorn main:app --reload

# 4. Open the interactive API documentation:
# http://127.0.0.1:8000/docs


# =============================================================
# GIT COMMANDS USED FOR THIS PROJECT
# =============================================================
# Check repository status:
# git status

# View commit history:
# git log --oneline

# Add all modified files:
# git add .

# Create a new commit:
# git commit -m "Descripcion del cambio"

# Push changes to GitHub:
# git push

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
                   descripcion: str, 
                   categoria: str, 
                   precio: float):
    """Create a new product in the catalog"""
# Create a Product object using the data received from the API
    producto = Producto(nombre, descripcion, categoria, precio)
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
