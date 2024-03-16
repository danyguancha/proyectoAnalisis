import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
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
        dirigido = grafo['directed']
        for nodeData in grafo["graph"][0]["data"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, size=nodeData["radius"], 
                            label=nodeData["label"], 
                            #label='👾', 
                            type=nodeData["type"], data=nodeData["data"], color="green", shape=None))

        for nodeData in grafo["graph"][0]["data"]:
            node_id = nodeData["id"]
            for link in nodeData["linkedTo"]:
                linked_node_id = link["nodeId"]
                # Asignar un color diferente a cada arista basado en el peso
                edge_color = LogArista().asignarColorArista(link["weight"])
                edges.append(Edge(source=node_id, target=linked_node_id, 
                                weight=link["weight"], label=str(link["weight"]), 
                                width=3, color=edge_color, directed=False))
                if not any(node.id == linked_node_id for node in nodes):
                    nodes.append(Node(id=linked_node_id, size=20, 
                                      label=str(linked_node_id), 
                                      #label='👾',
                                      type="circle", color="blue", shape=None))
            
    else:
        dirigido = grafo["directed"]
        for nodeData in grafo["nodes"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, title=nodeData["title"],
                              label=nodeData["label"],
                              #label='👾',
                              shape=None,size=nodeData["size"],color=nodeData["color"]))
            
        for edgeData in grafo["edges"]:
            source_node_id = edgeData["from"]
            target_node_id = edgeData["to"]
            #edge_color = LogArista().asignarColorArista(edgeData["source"])

            directed = edgeData["directed"] if 'directed' in edgeData else False

            edges.append(Edge(source=source_node_id, target=target_node_id, label=str(edgeData["label"]), 
                            width=3, color=edgeData["color"], directed=directed))
    return nodes, edges, dirigido


def cargarGrafo():
    file = st.file_uploader("Cargar archivo JSON", type=["json"])
    if file is not None:
        st.session_state.nodes, st.session_state.edges, st.session_state.directed = cargarArchivo(file)
        st.session_state.grafo_cargado = True
      
def main():
    logNodo = LogNodo()
    logArista = LogArista()
    logGrafo = LogGrafo()
    bandera = False
    with st.sidebar:
        st.session_state.directed = None
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
                                                                                "Completo",])
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
                            if st.session_state.directed == None:
                                nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                                st.session_state.nodes = nodes
                                st.session_state.edges = edges
                                st.session_state.directed = True
                            if st.session_state.directed:
                                bandera = True
                        elif nuevaOp == "Grafo no dirigido":
                            nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                            st.session_state.nodes = nodes
                            st.session_state.edges = edges

                elif selected_sub_option == "Personalizado":
                    st.sidebar.header("Grafo Personalizado")
                    logNodo.agregarNodo(Node, st)
                    logArista.agregarArista(Edge, st)
                    
                                
                    
                       
            elif selected_option == "Abrir":
                
                if st.session_state.directed == None:
                    cargarGrafo()
                if st.session_state.directed:
                    bandera = True
                
            elif selected_option == "Salir":
                st.session_state.nodes = []
                st.session_state.edges = []
                st.session_state.grafo_cargado = False
            elif selected_option == "Exportar Datos":
                if logGrafo.esCompleto(len(st.session_state.nodes), len(st.session_state.edges)):
                    bandera = True
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
            
        if selected == "Editar":
            
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Deshacer", "Nodo", "Arista", "Guardar", "Guardar Como", "Importar Datos", "Salir"]
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
            elif selected_option == "Arista":
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
                config = Gui(False)
                agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=config)

if __name__ == "__main__":
    main()
