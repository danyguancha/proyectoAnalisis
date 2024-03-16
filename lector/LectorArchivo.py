import json
import streamlit as st
import PyPDF2
from PyPDF2 import PdfFileReader

class LectorArchivo:

    def cargarArchivo(nombreArchivo):
        #with open(nombreArchivo, "r") as archivo:
        return json.load(nombreArchivo)
        
    def guardarArchivo(nombreArchivo, datos):
        with open(nombreArchivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
    
    def leerArchivoPdf(self, rutaArchivo):
        # Abre el archivo en modo lectura binaria
        with open(rutaArchivo, 'rb') as archivo:
            # Crea un objeto PdfReader
            lector_pdf = PyPDF2.PdfReader(archivo)
            # Inicializa una cadena vacía para almacenar el contenido
            contenido = ""
            # Itera sobre cada página del PDF
            for pagina in lector_pdf.pages:
                # Añade el contenido de la página al contenido total
                contenido += pagina.extract_text()
            contenido = contenido.replace('\n', ' ')
            # Usa streamlit para mostrar el contenido
            st.markdown(contenido)
            

            
        