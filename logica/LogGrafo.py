import json
import random
from typing import Dict, List
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista
import networkx as nx

class LogGrafo:
    def __init__(self):
        self.grafo = {}

    #funcion para generar el grafo aleatorio
    def generarGrafo(self, num_nodes: int, num_edges: int, Node, Edge, gui):
        G = nx.gnm_random_graph(num_nodes, num_edges)
        
        # Agregar etiquetas a los nodos
        for i in range(num_nodes):
            G.nodes[i]['label'] = f'Nodo {i+1}'
        
        # Agregar pesos a las aristas
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 10)
        
        nodes = [Node(str(i), label=G.nodes[i]['label']) for i in range(num_nodes)]
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight'])) for u, v in G.edges()]
        
        #config = Config(width=500, height=500, directed=False, nodeHighlightBehavior=True, highlightColor="#F7A7A6")
        return nodes, edges, gui

    def exportarGrafoJson(self,nombre_archivo: str, nodes, edges, Node, st):
        # Convertir la lista de nodos a una lista de diccionarios usando el método to_dict
        listaNodos = [node.to_dict() for node in nodes]
        listaAristas = [edge.to_dict() for edge in edges]

        # Crear un diccionario con nodos y aristas
        grafo = {"nodes": listaNodos, "edges": listaAristas}

        # Crear un botón para la descarga
        if st.button("Exportar grafo"):
            with open(nombre_archivo, 'w') as archivo:
                json.dump(grafo, archivo, default=self.serialize_nodes(nodes, Node))
            st.success(f"El archivo se ha exportado correctamente")
            # Leer el contenido del archivo y crear el botón de descarga
            #with open(nombre_archivo, "r") as json_file:
             #   json_data = json_file.read()
              #  st.download_button(
               #     label="Descargar archivo JSON",
                #    data=json_data,
                 #   file_name=nombre_archivo,
                  #  mime="application/json"
                #)
        




    # Función para serializar los nodos
    def serialize_nodes(self,obj, Node):
        if isinstance(obj, Node):
            return obj.__dict__
        return obj
    
    def serialize_edges(self,obj, Edge):
        if isinstance(obj, Edge):
            return obj.__dict__
        return obj


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

    def exportarGJson(self, nodos, aristas):
        grafo = {}
        grafo['nodos'] = nodos
        grafo['aristas'] = aristas
        return grafo