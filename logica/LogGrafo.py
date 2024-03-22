import json
import random
import copy
from typing import Dict, List
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista
import networkx as nx
from networkx.algorithms import bipartite
from streamlit_agraph import agraph
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_agraph import Config
import io
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.components import is_connected


class LogGrafo:
    def __init__(self):
        self.grafo = {}
        self.historial = []
    
    # ========================GENERACIÓN DE GRAFOS=============================================
   
    def generarGrafoDirigido (self, numNodos:int, tipoGrafo, Node, Edge):
        if tipoGrafo == "Grafo dirigido":
            G = nx.gnm_random_graph(numNodos, numNodos, directed=True)
        #else:
         #   G = nx.gnm_random_graph(numNodos, numNodos, directed=False)
        # Agregar etiquetas a los nodos
        for i in range(numNodos):
            G.nodes[i]['label'] = f'Nodo {i+1}'
        
        # Agregar pesos a las aristas
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 1000)
        
        nodes = [Node(str(i), 
                      label=G.nodes[i]['label'],
                      shape=None,
                        x=random.uniform(0, 900),  # Coordenada x aleatoria
                    y=random.uniform(0, 900)) for i in range(numNodos)]
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight']), weight=G.edges[u, v]['weight'],
                      width=3, directed=True) for u, v in G.edges()]        
        return nodes, edges
   
    def generarGrafoCompleto(self, numNodos:int, tipoGrafo, Node, Edge):
        if tipoGrafo == 'Completo':
            G = nx.complete_graph(numNodos)
        # Agregar etiquetas a los nodos
        for i in range(numNodos):
            G.nodes[i]['label'] = f'Nodo {i+1}'
        # Agregar pesos a las aristas
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 1000)
        
        nodes = [Node(str(i), 
                    label=G.nodes[i]['label'], 
                    shape=None,
                    x=random.uniform(0, 900),  # Coordenada x aleatoria
                    y=random.uniform(0, 900))  # Coordenada y aleatoria
                for i in range(numNodos)]
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight']), width=3, directed=False, 
                    type="dotted",weight=G.edges[u, v]['weight']) for u, v in G.edges()]
        return nodes, edges

        # Funcion para crear un grafo bipartito, donde se puede elegir el numero de nodos de cada conjunto
    def generarGrafoBipartito(self, numNodosConjunto1: int, numNodosConjunto2: int, Node, Edge):
        # Crear un grafo bipartito
        G = nx.complete_bipartite_graph(numNodosConjunto1, numNodosConjunto2)

        # Agregar etiquetas a los nodos
        for i in range(numNodosConjunto1 + numNodosConjunto2):
            G.nodes[i]['label'] = f'Nodo {i+1}'

        # Agregar pesos a las aristas
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 1000)

        # Crear una lista de nodos
        nodes = [Node(str(i), 
                    label=G.nodes[i]['label'],
                    shape=None,
                    x=random.uniform(0, 900),  # Coordenada x aleatoria
                    y=random.uniform(0, 900),  # Coordenada y aleatoria
                    color='blue' if i < numNodosConjunto1 else 'red')  # Color de nodo
                for i in range(numNodosConjunto1 + numNodosConjunto2)]

        # Crear una lista de aristas
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight']), width=3, directed=False, 
                    type="dotted", weight=G.edges[u, v]['weight']) for u, v in G.edges()]

        return nodes, edges
    
    # ========================OPERACIONES CON GRAFOS=============================================
    
    def esCompleto(self, numNodos: int, numAristas: int) -> bool:
        return numAristas == (numNodos * (numNodos - 1)) / 2
    
    def esDirigido(self, numNodos: int, numAristas: int) -> bool:
        return numAristas == numNodos * numNodos
    
    # Función para serializar los nodos
    def serialize_nodes(self,obj, Node):
        if isinstance(obj, Node):
            return obj.__dict__
        return obj
    
    def serialize_edges(self,obj, Edge):
        if isinstance(obj, Edge):
            return obj.__dict__
        return obj
    
    # funcion para descargar manual de usuario desde pdf
    def descargarManualUsuario(self, archivo, st):
        # Leer el archivo PDF como un objeto BytesIO
        with open(archivo, 'rb') as f:
            pdf_data = f.read()

        # Botón de descarga
        st.download_button(
            label="Descargar archivo PDF",
            data=pdf_data,
            file_name="Archivo.pdf",
            mime="application/pdf"
        )

    # funcion para determinar si un grafo es bipartito o no
    def esBipartito(self, nodes, edges) -> bool:
        # Crear el grafo con networkx
        salida = False
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)
        
        # verificar si en el grafo hay una arista de color 'rgba(254, 20, 56, 0.5)'
        for edge in edges:
            if edge.color == 'rgba(254, 20, 56, 0.5)':
                salida = True
            else:
                salida = bipartite.is_bipartite(G)
        return salida  
    def esBipartitoConexoOdisconexo(self, nodes, edges) -> str:
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            if edge.color != 'rgba(254, 20, 56, 0.5)':  # Solo agregar las aristas que no tienen este color
                G.add_edge(edge.source, edge.to, weight=edge.label)

        # verificar si el grafo es bipartito
        if not bipartite.is_bipartite(G):
            return "El grafo no es bipartito"

        # verificar si el grafo es conexo o disconexo
        if is_connected(G):
            return "El grafo es bipartito y conexo"
        else:
            return "El grafo es bipartito y disconexo"



    
    """def guardar_estado(self):
        # Guardar una copia del estado actual del grafo en el historial
        self.historial.append(copy.deepcopy(self.grafo))
        print(len(self.historial))

    def deshacer_cambio(self):
        if self.historial:
            # Si hay estados en el historial, establecer el estado actual del grafo al estado más reciente
            self.grafo = self.historial.pop()
            return True
        else:
            # Si no hay estados en el historial, retornar False
            return False"""
    

    # ========================EXPORTACIÓN DE GRAFOS=============================================

    def exportarGrafoJson(self, nombre_archivo: str, nodes, edges, Node, st):
        # Convertir la lista de nodos a una lista de diccionarios usando el método to_dict
        listaNodos = [node.to_dict() for node in nodes]
        listaAristas = [edge.to_dict() for edge in edges if edge.color=='gray']

        # Determinar si el grafo es dirigido o no
        #dirigido = any("directed" in edge for edge in listaAristas)
        dirigido = any(edge.get("directed", False) for edge in listaAristas)

        # Crear un diccionario con nodos y aristas
        grafo = {"nodes": listaNodos, "edges": listaAristas, "directed": dirigido}

        # Guardar el grafo en un archivo JSON
        with open(nombre_archivo, 'w') as archivo:
            json.dump(grafo, archivo, default=self.serialize_nodes(nodes, Node))

        # Leer el archivo JSON
        with open(nombre_archivo, "r") as json_file:
            json_data = json_file.read()

        # Botón de descarga
        st.download_button(
            label="Guardar JSON",
            data=json_data,
            file_name=nombre_archivo,
            mime="application/json"
        )

    def exportarGrafoImagen(self, st, nombre_archivo: str, formato: str = 'png'):
        # Crear el grafo desde la caché de la sesión
        nodes = st.session_state.nodes
        #edges =  st.session_state.edges
        edges = [edge for edge in st.session_state.edges if edge.color=='gray']
        #edges = st.session_state.edges
       
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)

        # Dibujar el grafo con matplotlib
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G,scale=2)#
        nx.draw(G,pos , with_labels=True, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')#
        nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels, ax=ax)#
        # Mostrar la figura en Streamlit
        st.pyplot(fig)

        # Capturar la imagen en formato PIL
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format=formato, bbox_inches='tight', pad_inches=0)
        img_buffer.seek(0)  # Regresar al inicio del buffer

        # Descargar la imagen
        st.download_button(
            label=f"Descargar {nombre_archivo}.{formato}",
            data=img_buffer.getvalue(),
            file_name=f"{nombre_archivo}.{formato}",
            mime=f"image/{formato}"
        )
    # Función para exportar el grafo en formato de excel
    def exportarGrafoExcel(self, nombre_archivo: str, nodes, edges, st):
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)

        # Crear un DataFrame con los nodos
        df_nodes = pd.DataFrame(columns=['Node', 'Label'])
        for node, data in G.nodes(data=True):
            df_nodes = pd.concat([df_nodes, pd.DataFrame({'Node': [node], 'Label': [data['label']]})], ignore_index=True)

        # Crear un DataFrame con las aristas
        df_edges = pd.DataFrame(columns=['Source', 'Target', 'Weight'])
        for u, v, w in G.edges(data='weight'):
            df_edges = pd.concat([df_edges, pd.DataFrame({'Source': [u], 'Target': [v], 'Weight': [w]})], ignore_index=True)

        # Guardar los DataFrames en un archivo de Excel
        with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
            df_nodes.to_excel(writer, sheet_name='Nodes', index=False)
            #df_edges.to_excel(writer, sheet_name='Edges', index=False)

            # Obtener los objetos workbook y worksheet
            workbook  = writer.book
            worksheet = writer.sheets['Nodes']

            # Definir un formato para las celdas del encabezado
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1})

            # Aplicar el formato a las celdas del encabezado
            for col_num, value in enumerate(df_nodes.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Hacer lo mismo para la hoja 'Edges'
            worksheet = writer.sheets['Edges']
            for col_num, value in enumerate(df_edges.columns.values):
                worksheet.write(0, col_num, value, header_format)

        # Leer el archivo Excel como un objeto BytesIO
        with open(nombre_archivo, 'rb') as f:
            excel_data = f.read()

        # Botón de descarga
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ========================MOSTRAR DATOS DE GRAFOS=============================================

    def mostrarDatosGrafoTabla(self, nodes, edges, st):
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)

        # Crear un DataFrame con los nodos
        df_nodes = pd.DataFrame(columns=['Node', 'Label'])
        for node, data in G.nodes(data=True):
            df_nodes = pd.concat([df_nodes, pd.DataFrame({'Node': [node], 'Label': [data['label']]})], ignore_index=True)

        # Crear un DataFrame con las aristas
        df_edges = pd.DataFrame(columns=['Source', 'Target', 'Weight'])
        for u, v, w in G.edges(data='weight'):
            df_edges = pd.concat([df_edges, pd.DataFrame({'Source': [u], 'Target': [v], 'Weight': [w]})], ignore_index=True)

        # Mostrar los DataFrames en Streamlit
        st.title('Datos de grafo en tabla')
        st.write('Nodos')
        st.write(df_nodes)
        st.write('Aristas')
        st.write(df_edges)  
            
    # Funcion para mostrar el grafo en un formato de matriz de adyacencia
    def mostrarMatrizAdyacencia(self, nodes, edges, st):
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)

        # Crear una matriz de adyacencia
        matriz_adyacencia = nx.to_pandas_adjacency(G)

        # Mostrar la matriz de adyacencia en Streamlit
        st.write("Matriz de adyacencia")
        st.write(matriz_adyacencia)

    # Funcion para deshacer los cambios que se hayan hecho en el grafo, por ejemplo eliminar una arista volver a dejarla como estaba hasta antes de eliminarla, etc...
    def deshacerCambios(self,  st):
        # Crear una copia de los nodos y aristas originales
        original_nodes = copy.deepcopy(st.session_state.nodes)
        original_edges = copy.deepcopy(st.session_state.edges)

        # Restaurar los nodos y aristas originales
        st.session_state.nodes = original_nodes
        st.session_state.edges = original_edges

        # Mostrar un mensaje de éxito
        st.success("Cambios deshechos con éxito")
    
    # Funcion para determinar si un es bipartito conexo o disconexto
    def esBipartitoConexo(self, nodes, edges) -> bool:
        # Crear el grafo con networkx
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.id, label=node.label)
        for edge in edges:
            G.add_edge(edge.source, edge.to, weight=edge.label)
        for edge in edges:
            if edge.color == 'rgba(254, 20, 56, 0.5)':
                return False
            else:
                return bipartite.is_bipartite(G)
    
    
   