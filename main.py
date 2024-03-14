import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pyautogui
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



# Función para cargar el grafo desde el archivo y almacenar en la caché
@st.cache_data()
def cargarArchivo(file):
    grafo = LectorArchivo.cargarArchivo(file)
    nodes = []
    edges = []
    # verificar si el grafo tiene la clave graph
    if "graph" in grafo:

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
    else:
        for nodeData in grafo["nodes"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, title=nodeData["title"],label=nodeData["label"],
                              shape=nodeData["shape"],size=nodeData["size"],color=nodeData["color"]))
            
        for edgeData in grafo["edges"]:
            source_node_id = edgeData["from"]
            target_node_id = edgeData["to"]
            #edge_color = LogArista().asignarColorArista(edgeData["source"])
            edges.append(Edge(source=source_node_id, target=target_node_id, label=str(edgeData["label"]), 
                            width=3, color=edgeData["color"]))
            #if not any(node.id == target_node_id for node in nodes):
             #   nodes.append(Node(id=edgeData["source"], size=20, label=str(target_node_id),shape=nodeData["shape"], type="circle"))
    return nodes, edges


def cargarGrafo():
    file = st.file_uploader("Cargar archivo JSON", type=["json"])
    if file is not None:
        st.session_state.nodes, st.session_state.edges = cargarArchivo(file)
        st.session_state.grafo_cargado = True
        # Verificar si el grafo es dirigido y actualizar el estado de Gui()
      






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
    bandera = False
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
                        num_nodes = st.sidebar.number_input('Ingrese el número de nodos', min_value=0, value=0)
                        selectTipo = st.selectbox("Seleccione el tipo de grafo", [" ",
                                                                                  "Grafo dirigido", 
                                                                                  "Completo", 
                                                                                  "Bipartito"])
                        if selectTipo == "Grafo dirigido":
                            nodes, edges = logGrafo.generarGrafoDirigido(num_nodes, selectTipo, Node, Edge)
                            st.session_state.nodes = nodes
                            st.session_state.edges = edges
                            bandera = True
                            
                        elif selectTipo == "Completo":
                            nuevaOp = st.selectbox("Seleccione el tipo de grafo", [" ",
                                                                                  "Grafo dirigido", 
                                                                                  "Grafo no dirigido", 
                                                                                  ])
                            if nuevaOp == "Grafo dirigido":
                                nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                                st.session_state.nodes = nodes
                                st.session_state.edges = edges
                                bandera = True
                            elif nuevaOp == "Grafo no dirigido":
                                nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                                st.session_state.nodes = nodes
                                st.session_state.edges = edges
                                
                            
                        elif selectTipo == "Bipartito":
                            nodes, edges = logGrafo.generarGrafoBipartito(num_nodes, selectTipo, Node, Edge)
                            st.session_state.nodes = nodes
                            st.session_state.edges = edges
                       
            elif selected_option == "Abrir":
                cargarGrafo()
            elif selected_option == "Cerrar":
                st.session_state.nodes = []
                st.session_state.edges = []
                st.session_state.grafo_cargado = False
            
            
                
            elif selected_option == "Exportar Datos":
                selected_sub_option = st.selectbox(
                    "Formato a exportar:",
                    [" ","JSON", "CSV", "Excel", "Imagen"]
                )
                if selected_sub_option == "JSON":
                    ruta = './Data/'
                    nombreArchivo = 'grafo_exportado.json'
                    nombreCompleto = ruta + nombreArchivo
                    logGrafo.exportarGrafoJson(nombreCompleto, st.session_state.nodes, st.session_state.edges,Node, st)
                elif selected_sub_option == "Excel":
                    logGrafo.exportarGrafoExcel('excel',st.session_state.nodes, st.session_state.edges, st)
                elif selected_sub_option == "Imagen":
                    logGrafo.exportarGrafoImagen(st,'grafo_img')


            
        elif selected == "Editar":

            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Deshacer", "Nodo", "Arco", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
            )
            #=======================Seccion de nodos=======================
            if selected_option == "Deshacer":
                pass
            elif selected_option == "Nodo":
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
        if bandera == True:
            with st.container(border=True):
                agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui(True))
        else:
            with st.container(border=True):
                agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui(False))

if __name__ == "__main__":
    main()
