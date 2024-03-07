import json
import random
from typing import Dict, List
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista

class LogGrafo:
    def __init__(self):
        self.grafo = {}

    def generarGrafoAleatorio(self, num_nodos: int, num_aristas: int) -> Dict[str, List[str]]:
        grafo = {str(i): [] for i in range(num_nodos)}
        for _ in range(num_aristas):
            nodo_inicio = str(random.randint(0, num_nodos - 1))
            nodo_fin = str(random.randint(0, num_nodos - 1))
            if nodo_fin not in grafo[nodo_inicio]:
                grafo[nodo_inicio].append(nodo_fin)
        self.grafo = grafo
        return self.grafo

    def guardar_grafo_json(self, nombre_archivo: str):
        with open(nombre_archivo, 'w') as archivo:
            json.dump(self.grafo, archivo)
    

    def guardar_grafo_txt(self, nombre_archivo: str):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(str(self.grafo))

    def cargar_grafo_json(self, nombre_archivo: str) -> Dict[str, List[str]]:
        with open(nombre_archivo, 'r') as archivo:
            self.grafo = json.load(archivo)
        return self.grafo

    def cargar_grafo_txt(self, nombre_archivo: str) -> Dict[str, List[str]]:
        with open(nombre_archivo, 'r') as archivo:
            self.grafo = eval(archivo.read())
        return self.grafo
