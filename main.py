import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import os
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
    dirigido = grafo.get('directed', False)

    # establecer un valor predeterminado para 'directed'
    dirigido = grafo.get('directed', False)

    if "graph" in grafo:
        for nodeData in grafo["graph"][0]["data"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, size=nodeData["radius"], 
                            label=nodeData["label"], 
                            type=nodeData["type"], data=nodeData["data"], color="green"))

        for nodeData in grafo["graph"][0]["data"]:
            node_id = nodeData["id"]
            for link in nodeData["linkedTo"]:
                linked_node_id = link["nodeId"]
                edge_color = LogArista().asignarColorArista(link["weight"])
                edges.append(Edge(source=node_id, target=linked_node_id, 
                                weight=link["weight"], label=str(link["weight"]), 
                                width=3, color=edge_color, directed=dirigido))
                if not any(node.id == linked_node_id for node in nodes):
                    nodes.append(Node(id=linked_node_id, size=20, 
                                      label=str(linked_node_id), 
                                      type="circle", color="blue"))
            
    else:
        for nodeData in grafo["nodes"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, title=nodeData["title"],
                              label=nodeData["label"],
                              size=nodeData["size"],color=nodeData["color"]))
            
        for edgeData in grafo["edges"]:
            source_node_id = edgeData["from"]
            target_node_id = edgeData["to"]

            # usar el valor de 'directed' si está presente, de lo contrario usar el valor predeterminado
            directed = edgeData.get('directed', dirigido)

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
    estado = False
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
                                                                                "Completo",
                                                                                "Ponderado"])
                    if selectTipo == "Grafo dirigido":
                        nodes, edges = logGrafo.generarGrafoDirigido(num_nodes, selectTipo, Node, Edge)
                        st.session_state.nodes = nodes
                        st.session_state.edges = edges
                        bandera = True
                        estado = True
                        
                        
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
                                bandera = False
                                estado = True
                        elif nuevaOp == "Grafo no dirigido":
                            if st.session_state.directed == None:
                                nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                                st.session_state.nodes = nodes
                                st.session_state.edges = edges
                            if st.session_state.directed==True:
                                bandera = False
                            estado = True

                    elif selectTipo == "Ponderado":
                        st.text("Opción con fallos, estará disponible muy pronto")

                elif selected_sub_option == "Personalizado":
                    st.sidebar.header("Grafo Personalizado")
                    logNodo.agregarNodo(Node, st, logGrafo)
                    st.sidebar.header("Agrega Aristas")
                    logArista.agregarArista(Edge, st)
                    st.sidebar.header(" Cambiar Color")
                    logNodo.cambiarColorNodo(st)
                    st.sidebar.header("Cambiar Peso")
                    logArista.editarArista(st)
                                
                    
                       
            elif selected_option == "Abrir":
                
                if st.session_state.directed == None:
                    cargarGrafo()
                    estado = True
                if st.session_state.directed:
                    bandera = True
                
            elif selected_option == "Salir":
                st.session_state.nodes = []
                st.session_state.edges = []
                st.session_state.grafo_cargado = False
            elif selected_option == "Exportar Datos":
                
                selected_sub_option = st.selectbox(
                    "Formato a exportar:",
                    [" ", "Excel", "Imagen"]
                )
                if selected_sub_option == "JSON":
                    ruta = './Data/'
                    nombreArchivo = 'grafo_exportado.json'
                    nombreCompleto = ruta + nombreArchivo
                    logGrafo.exportarGrafoJson(nombreCompleto, st.session_state.nodes, st.session_state.edges,Node, st)
                elif selected_sub_option == "CSV":
                    estado = True
                    
                elif selected_sub_option == "Excel":
                    logGrafo.exportarGrafoExcel('datos_grafo.xlsx',st.session_state.nodes, st.session_state.edges, st)
                elif selected_sub_option == "Imagen":
                    logGrafo.exportarGrafoImagen(st,'grafo_img')

            elif selected_option == "Guardar":
                    ruta = './Data/'
                    nombreArchivo = 'grafo_exportado.json'
                    nombreCompleto = ruta + nombreArchivo
                    logGrafo.exportarGrafoJson(nombreCompleto, st.session_state.nodes, st.session_state.edges,Node, st)

            elif selected_option == "Guardar Como":
                ruta = './Data/'
                nombreArchivo = 'grafo_exportado.json'
                nombreUsuario = st.text_input("Nombre del archivo", value=nombreArchivo)

                if not nombreUsuario.endswith('.json'):
                    nombreUsuario += '.json'
                    
                nombreCompleto = os.path.join(ruta, nombreUsuario)

                logGrafo.exportarGrafoJson(nombreCompleto, st.session_state.nodes, st.session_state.edges, Node, st)

            
        if selected == "Editar":
            
            selected_option = st.selectbox(
                "Seleccionar opción:",
                [" ", "Deshacer", "Nodo", "Arista"]
            )
            #=======================Seccion de nodos=======================
            if selected_option == "Deshacer":
                cambio = logGrafo.deshacer_cambio()
                if cambio:
                    st.text("Se ha deshecho el cambio")
                else:
                    st.text("No hay cambios que deshacer")
            elif selected_option == "Nodo":
                st.sidebar.header("Nodos")
                logNodo.agregarNodo(Node, st, logGrafo)
                logNodo.cambiarEtiquetaNodo(st)
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
            if selected_option == "Ayuda":
                ayuda = True
            
    
        
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
        if estado:
            logGrafo.mostrarDatosGrafoTabla(st.session_state.nodes, st.session_state.edges,st)
        

if __name__ == "__main__":
    main()
