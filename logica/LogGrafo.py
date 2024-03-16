import json
import random
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


class LogGrafo:
    def __init__(self):
        self.grafo = {}
    
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
                      shape=None) for i in range(numNodos)]
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight']), width=3, directed=True) for u, v in G.edges()]        
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
                      shape=None) for i in range(numNodos)]
        edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight']), width=3, directed=False) for u, v in G.edges()]
        return nodes, edges
    

    def esCompleto(self, numNodos: int, numAristas: int) -> bool:
        return numAristas == (numNodos * (numNodos - 1)) / 2
    
    def esDirigido(self, numNodos: int, numAristas: int) -> bool:
        return numAristas == numNodos * numNodos

    """def exportarGrafoJson(self, nombre_archivo: str, nodes, edges, Node, st):
        # Convertir la lista de nodos a una lista de diccionarios usando el método to_dict
        listaNodos = [node.to_dict() for node in nodes]
        listaAristas = [edge.to_dict() for edge in edges]

        # Crear un diccionario con nodos y aristas
        grafo = {"nodes": listaNodos, "edges": listaAristas}

        # Guardar el grafo en un archivo JSON
        with open(nombre_archivo, 'w') as archivo:
            json.dump(grafo, archivo, default=self.serialize_nodes(nodes, Node), ident=4)

        # Leer el archivo JSON
        with open(nombre_archivo, "r") as json_file:
            json_data = json_file.read()

        # Botón de descarga
        st.download_button(
            label="Descargar JSON",
            data=json_data,
            file_name=nombre_archivo,
            mime="application/json"
        )"""
    def exportarGrafoJson(self, nombre_archivo: str, nodes, edges, Node, st):
        # Convertir la lista de nodos a una lista de diccionarios usando el método to_dict
        listaNodos = [node.to_dict() for node in nodes]
        listaAristas = [edge.to_dict() for edge in edges]

        # Determinar si el grafo es dirigido o no
        dirigido = any("directed" in edge for edge in listaAristas)

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
            label="Descargar JSON",
            data=json_data,
            file_name=nombre_archivo,
            mime="application/json"
        )

   

    # Función para serializar los nodos
    def serialize_nodes(self,obj, Node):
        if isinstance(obj, Node):
            return obj.__dict__
        return obj
    
    def serialize_edges(self,obj, Edge):
        if isinstance(obj, Edge):
            return obj.__dict__
        return obj

    def exportarGrafoImagen(self, st, nombre_archivo: str, formato: str = 'png'):
        # Crear el grafo desde la caché de la sesión
        nodes = st.session_state.nodes
        edges = st.session_state.edges
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
            df_edges.to_excel(writer, sheet_name='Edges', index=False)

        # Botón de descarga
        st.download_button(
            label="Descargar Excel",
            data=pd.concat([df_nodes, df_edges], axis=1).to_csv(index=False).encode('utf-8'),
            file_name=nombre_archivo + '.xls',
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    # funcion para mostrar los datos del grafo en una tabla.. por ejemplo dataframe
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



        
        