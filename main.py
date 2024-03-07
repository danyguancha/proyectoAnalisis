import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_option_menu import option_menu
from GUI import Gui
from lector.LectorArchivo import LectorArchivo
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista
from logica.LogGrafo import LogGrafo
import json


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


def main():
    logNodo = LogNodo()
    logArista = LogArista()
    logGrafo = LogGrafo()
    with st.sidebar:
        
        selected = option_menu(
            menu_title="App",
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
                st.sidebar.button("Exportar")
           
            
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
