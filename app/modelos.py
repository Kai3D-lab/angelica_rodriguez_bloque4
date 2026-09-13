class Producto:
    """Representa un producto del catálogo KAI 3D."""

    def __init__(self, 
            nombre, 
            descripcion, 
            categoria, 
            precio,
            id=None):

# Store the received data as attributes of the object
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio

    def to_dict(self):
        """Convierte el producto en un diccionario."""

        return{"id": self.id, 
               "nombre": self.nombre,
               "descripcion": self.descripcion,
               "categoria": self.categoria,
               "precio": self.precio}
    