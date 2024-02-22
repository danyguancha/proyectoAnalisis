import json

class LectorArchivo:

    def cargarArchivo(nombreArchivo):
        #with open(nombreArchivo, "r") as archivo:
        return json.load(nombreArchivo)
        
    def guardarArchivo(nombreArchivo, datos):
        with open(nombreArchivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
        