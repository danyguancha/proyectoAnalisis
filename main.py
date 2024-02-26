import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_option_menu import option_menu
from GUI import Gui
from lector.LectorArchivo import LectorArchivo

# Función para cargar el grafo desde el archivo y almacenar en la caché
@st.cache_data()
def cargarArchivo(file):
    #grafo = LectorArchivo.cargarArchivo("E:/proyectosU/semestres/semestre-2024-1/Analisis/JSON Example.json")
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
            edge_color = asignarColorArista(link["weight"])
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

def asignarColorArista(peso):
    if peso >= 0 and peso <= 50:
        return "red"
    elif peso > 50 and peso <= 100:
        return "blue"
    elif peso > 100 and peso <= 150:
        return "green"
    elif  peso > 150 and peso <= 200:
        return "orange"
    elif peso > 200 and peso <= 250:
        return "purple"
    else:
        return "gray"

def agregarNodo():
    all_possible_ids = set(range(1, 1000))
    existing_ids = set([node.id for node in st.session_state.nodes])
    available_ids = list(all_possible_ids - existing_ids)
    idNodo = st.sidebar.selectbox("ID del nodo", available_ids)
    if st.sidebar.button("Agregar Nodo"):
        nuevo_nodo = Node(id=idNodo, size=20, label=str(idNodo), type="circle", color="purple")
        st.session_state.nodes.append(nuevo_nodo)
        
def cambiarColorNodo():
    # Crear un selectbox para seleccionar el nodo
    selected_node_label = st.sidebar.selectbox("Seleccionar Nodo:", [node.label for node in st.session_state.nodes])

    #Se obtiene el color seleccionado por el usuario
    selected_color = st.sidebar.color_picker("Seleccionar Color", "#ff0000") #Color por defecto

    # Crear un botón para cambiar el color del nodo seleccionado
    if st.sidebar.button("Cambiar Color"):
        selected_node = next((node for node in st.session_state.nodes if node.label == selected_node_label), None)
        if selected_node:
            selected_node.color = selected_color
        else:
            st.warning("No se ha seleccionado ningún nodo.")

def eliminarNodo():
    selectedNodoEliminar = st.sidebar.selectbox("Eliminar Nodo:", [node.label for node in st.session_state.nodes])
            
    if st.sidebar.button("Eliminar Nodo"):
        # Lógica para eliminar el nodo seleccionado
        nodoEliminar = next((node for node in st.session_state.nodes if node.label == selectedNodoEliminar), None)
        if nodoEliminar:
            st.session_state.nodes.remove(nodoEliminar)
        else:
            st.warning("No se ha seleccionado ningún nodo.")
            
# =================Aristas=================
def agregarArista():
    source_node_id = st.sidebar.selectbox("Nodo de inicio", [node.id for node in st.session_state.nodes])
    target_node_id = st.sidebar.selectbox("Nodo de destino", [node.id for node in st.session_state.nodes])
    weight = st.sidebar.number_input("Peso", min_value=1, max_value=100, value=1)
    if st.sidebar.button("Agregar Arista"):
        
        nueva_arista = Edge(source=source_node_id, target=target_node_id, weight=weight, label=str(weight), width=3, color="orange")
        st.session_state.edges.append(nueva_arista)

def main():

    with st.sidebar:
        
        selected = option_menu(
            menu_title="App",
            options=["Archivo", "Editar", "Ejecutar", "Herramientas", "Ventana", "Ayuda"],
        )

        if selected == "Archivo":

            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Nuevo Grafo", "Abrir", "Cerrar", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
        )
        
        
            if selected_option == "Nuevo Grafo":
                selected_sub_option = st.selectbox(
                    "Seleccionar sub-opción:",
                    ["Personalizado", "Aleatorio"]
                )
            elif selected_option == "Abrir":
                cargarGrafo()
                
            elif selected_option == "Exportar Datos":
                selected_sub_option = st.selectbox(
                    "Formato a exportar:",
                    ["JSON", "CSV", "Excel", "Imagen"]
                )


            
        elif selected == "Editar":

            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Deshacer", "Nodo", "Arco", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
            )
            #=======================Seccion de nodos=======================
            if selected_option == "Nodo":
                st.sidebar.header("Nodos")
                agregarNodo()
                cambiarColorNodo()
                eliminarNodo()
                    
            #=======================Seccion de arcos=======================
            elif selected_option == "Arco":
                st.sidebar.header("Aristas")
                agregarArista()
            
        
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
        agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui())

if __name__ == "__main__":
    main()
