import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import json
import pyautogui
import random
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_option_menu import option_menu
from GUI import Gui
from lector.LectorArchivo import LectorArchivo
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista
from logica.LogGrafo import LogGrafo
from PIL import Image
#import io
#import csv


# Función para cargar el grafo desde el archivo y almacenar en la caché
@st.cache_data()
def cargarArchivo(file):
    grafo = LectorArchivo.cargarArchivo(file)
    nodes = []
    edges = []

    for nodeData in grafo["graph"][0]["data"]:
        node_id = nodeData["id"]
        nodes.append(Node(id=node_id, size=nodeData["radius"], label=nodeData["label"], 
                          type=nodeData["type"], data=nodeData["data"], color="green"))

    for nodeData in grafo["graph"][0]["data"]:
        node_id = nodeData["id"]
        for link in nodeData["linkedTo"]:
            linked_node_id = link["nodeId"]
            # Asignar un color diferente a cada arista basado en el peso
            edge_color = LogArista().asignarColorArista(link["weight"])
            edges.append(Edge(source=node_id, target=linked_node_id, 
                              weight=link["weight"], label=str(link["weight"]), 
                              width=3, color=edge_color))
            if not any(node.id == linked_node_id for node in nodes):
                nodes.append(Node(id=linked_node_id, size=20, label=str(linked_node_id), type="circle", color="blue"))

    return nodes, edges


def cargarGrafo():
    file = st.file_uploader("Cargar archivo JSON", type=["json"])
    if file is not None:
        st.session_state.nodes, st.session_state.edges = cargarArchivo(file)
        st.session_state.grafo_cargado = True


#funcion para generar el grafo aleatorio
def generarGrafo(num_nodes: int, num_edges: int):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    
    # Agregar etiquetas a los nodos
    for i in range(num_nodes):
        G.nodes[i]['label'] = f'Nodo {i+1}'
    
    # Agregar pesos a las aristas
    for u, v in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 10)
    
    nodes = [Node(str(i), label=G.nodes[i]['label']) for i in range(num_nodes)]
    edges = [Edge(str(u), str(v), label=str(G.edges[u, v]['weight'])) for u, v in G.edges()]
    
    config = Config(width=500, height=500, directed=False, nodeHighlightBehavior=True, highlightColor="#F7A7A6")
    return nodes, edges, config



def exportarGrafoJPG():
    # Capturar la posición de la ventana de Streamlit
    streamlit_window = pyautogui.getWindowsWithTitle("Streamlit")[0]
    streamlit_x, streamlit_y = streamlit_window.topleft

    # Capturar un pantallazo del área de la ventana de Streamlit
    img = pyautogui.screenshot(region=(streamlit_x, streamlit_y, streamlit_window.width, streamlit_window.height))

    # Guardar la captura de pantalla en un archivo temporal
    img_path = "grafo_pantallazo.png"
    img.save(img_path)
    st.success("Captura de pantalla del grafo exportada como 'grafo_pantallazo.png'")

    return img_path


def main():
    logNodo = LogNodo()
    logArista = LogArista()
    logGrafo = LogGrafo()
    with st.sidebar:
        
        selected = option_menu(
            menu_title="App Algoritmos",
            options=["Archivo", "Editar", "Ejecutar", "Herramientas", "Ventana", "Ayuda"],
        )
        
        if selected == "Archivo":

            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Nuevo Grafo", "Abrir", "Buscar Nodo", "Cerrar", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
            )
            
            if selected_option == "Buscar Nodo":
                logNodo.buscarNodo(st)
        
        
            if selected_option == "Nuevo Grafo":
                selected_sub_option = st.selectbox(
                    "Seleccionar sub-opción:",
                    [" ","Personalizado", "Aleatorio"]
                )
                if selected_sub_option == "Aleatorio":
                    st.session_state.nodes = []
                    st.session_state.edges = []
                    numNodos = st.number_input("Número de nodos", min_value=0, max_value=500, value=0)
                    numAristas = st.number_input("Número de aristas", min_value=0, max_value=1000, value=0)
                    
                    s = logGrafo.generarGrafoAleatorio(numNodos, numAristas)
                    ruta_archivo = "./Data/"
                    nombre_archivo = "nuevoGrafo.json"
                    nombre_completo_archivo = ruta_archivo + nombre_archivo
                    logGrafo.guardar_grafo_json(nombre_completo_archivo)
                    
                    st.session_state.grafo_cargado = True
                    for c, v in s.items():
                        for i in v:
                            st.session_state.edges.append(Edge(source=c, target=i, weight=3))
                        st.session_state.nodes.append(Node(id=c, size=20, label=c, type="circle", color="blue"))
                        
            
                elif selected_sub_option == "Personalizado":
                    cargarGrafo()
                
                if selected_sub_option == "Aleatorio":
                        num_nodes = st.sidebar.number_input('Ingrese el número de nodos', min_value=1, value=5)
                        num_edges = st.sidebar.number_input('Ingrese el número de aristas', min_value=1, value=5)
                        nodes, edges, config = generarGrafo(num_nodes, num_edges)
                        st.session_state.nodes = nodes
                        st.session_state.edges = edges
                        st.session_state.config = config

            elif selected_option == "Abrir":
                cargarGrafo()
            elif selected_option == "Cerrar":
                st.session_state.nodes = []
                st.session_state.edges = []
                st.session_state.grafo_cargado = False
            
            
                
            elif selected_option == "Exportar Datos":
                selected_sub_option = st.selectbox(
                    "Formato a exportar:",
                    ["JSON", "CSV", "Excel", "Imagen"]
                )
                if selected_sub_option == "JSON":
                    logGrafo.exportarGrafoJSON(st.session_state.nodes, st.session_state.edges)
                    with open("grafo_exportado.json", "r") as json_file:
                        json_data = json_file.read()
                    st.download_button(
                        label="Descargar archivo JSON",
                        data=json_data,
                        file_name="grafo_exportado.json",
                        mime="application/json"
                    )
                elif selected_sub_option == "Imagen":
                    img_path = exportarGrafoJPG()
                    # Crear un botón de descarga
                    with open(img_path, "rb") as img_file:
                        st.download_button(
                            label="Descargar Pantallazo",
                            data=img_file,
                            file_name="grafo_pantallazo.png",
                            mime="image/png"
                        )

           
            
        elif selected == "Editar":

            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Deshacer", "Nodo", "Arco", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
            )
            #=======================Seccion de nodos=======================
            if selected_option == "Nodo":
                st.sidebar.header("Nodos")
                logNodo.agregarNodo(Node, st)
                logNodo.cambiarColorNodo(st)
                logNodo.eliminarNodo(st)
                    
            #=======================Seccion de arcos=======================
            elif selected_option == "Arco":
                st.sidebar.header("Aristas")
                logArista.agregarArista(Edge, st)
                logArista.editarArista(st)
                logArista.eliminarArista(st)
            
        
        elif selected == "Ejecutar":
            selected_option = option_menu(
                menu_title=None,
                options=["Procesos"]
            )

            if selected_option == "Procesos":
                selected_sub_option = st.selectbox(
                    "Seleccionar un proceso:",
                    ["Proceso 1", "Proceso 2"]
                )

        elif selected == "Ventana":
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Gráfica", "Tabla"]
            )

        elif selected == "Ayuda":
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Ayuda", "Acerca de Grafos"]
            )
            
    
        
    # Navbar
    st.title("Proyecto de Análisis de Algoritmos")
    if "nodes" not in st.session_state:
        st.warning("No se ha cargado ningún archivo.")
    else:
        # Renderizar el grafo en el cuerpo principal
        with st.container(border=True):
            #agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui())
        # Renderizar el grafo en el cuerpo principal
        graph_clicked = st.graph(agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui()))

        # Obtener el nodo clickeado
        clicked_node_id = graph_clicked["selectedNodes"][0] if graph_clicked else None

        # Mostrar información del nodo clickeado
        if clicked_node_id:
            selected_node = next((node for node in st.session_state.nodes if node.id == clicked_node_id), None)
            if selected_node:
                st.sidebar.markdown(f"### Información del Nodo {selected_node.id}")
                st.sidebar.write(f"**Label:** {selected_node.label}")
                st.sidebar.write(f"**Tipo:** {selected_node.type}")
                st.sidebar.write(f"**Data:** {selected_node.data}")
                st.sidebar.write(f"**Color:** {selected_node.color}")

if __name__ == "__main__":
    main()
