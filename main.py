import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import os
from streamlit_agraph import agraph, Node, Edge
from streamlit_option_menu import option_menu
from GUI import Gui
from lector.LectorArchivo import LectorArchivo
from logica.LogNodo import LogNodo
from logica.LogArista import LogArista
from logica.LogGrafo import LogGrafo
from logica.Parcial1 import Parcial1
from logica.ProbabilidadEP import ProbabilidadEP
from logica.Estrategia2 import Estrategia2
from logica.Estrategia3 import Estrategia3
import random
from logica.pruebas import PruebasEstrategias

st.set_page_config(
    page_title="Project ADA",
    page_icon="./Data/iconos/icon1.webp",
    layout="wide"
)

# Función para cargar el grafo desde el archivo y almacenar en la caché
@st.cache_data()
def cargarArchivo(file):
    grafo = LectorArchivo.cargarArchivo(file)
    nodes = []
    edges = []

    # establecer un valor predeterminado para 'directed'
    dirigido = grafo.get('directed', False)

    if "graph" in grafo:
        for nodeData in grafo["graph"][0]["data"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, size=nodeData["radius"], 
                            label=nodeData["label"], 
                            type=nodeData["type"], data=nodeData["data"], color="green", shape=None))

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
                                      type="circle", color="blue", shape=None))
            
    else:
        for nodeData in grafo["nodes"]:
            node_id = nodeData["id"]
            nodes.append(Node(id=node_id, title=nodeData["title"],
                              label=nodeData["label"],
                              size=nodeData["size"],color=nodeData["color"], shape=None,
                              x=random.uniform(0, 900),  # Coordenada x aleatoria
                              y=random.uniform(0, 900)))
            
        for edgeData in grafo["edges"]:
            source_node_id = edgeData["from"]
            target_node_id = edgeData["to"]

            # usar el valor de 'directed' si está presente, de lo contrario usar el valor predeterminado
            directed = edgeData.get('directed', dirigido)

            edges.append(Edge(source=source_node_id, target=target_node_id, label=str(edgeData["weight"]), 
                            weight=edgeData["weight"], width=3, color=edgeData["color"], directed=directed))
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
    parcial = Parcial1()
    probEP = ProbabilidadEP()
    estra2 = Estrategia2()
    estra3 = Estrategia3()
    pruebas = PruebasEstrategias()

    bandera = False
    conexoOdisconexo = False
    boolParcial = False
    mostrarProbabilidad = False
    estrategia2 = False
    estrategia3 = False
    mostrarSustentacion = False
    salida = {}
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
                    [" ","Personalizado", "Aleatorio","Bipartito"]
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
                                st.session_state.directed = True
                            if st.session_state.directed:
                                bandera = True
                                
                        elif nuevaOp == "Grafo no dirigido":
                            if st.session_state.directed == None:
                                nodes, edges = logGrafo.generarGrafoCompleto(num_nodes, selectTipo, Node, Edge)
                                st.session_state.nodes = nodes
                                st.session_state.edges = edges
                            if st.session_state.directed==True:
                                bandera = False
                           

                    elif selectTipo == "Ponderado":
                        st.text("Opción con fallos, estará disponible muy pronto")

                elif selected_sub_option == "Personalizado":
                    st.sidebar.header("Grafo Personalizado")
                    st.sidebar.header("Tipo de Grafo") 
                    tipo_grafo = st.radio("",["Dirigido", "No dirigido"], key="tipoGrafo")
                    if tipo_grafo == "Dirigido":
                        bandera = True
                    elif tipo_grafo == "No dirigido":
                        bandera = False
                    st.sidebar.header("Agrega Nodo") 
                    logNodo.agregarNodo(Node, st)
                    st.sidebar.header(" Cambiar Color Nodo")
                    logNodo.cambiarColorNodo(st)
                    st.sidebar.header("Agrega Aristas") 
                    if tipo_grafo == "Dirigido":
                        logArista.agregarArista(Edge,True, st)
                    elif tipo_grafo == "No dirigido":
                        logArista.agregarArista(Edge,False, st)
                    
                    st.sidebar.header(" Cambiar Color Arista")
                    logArista.cambiarColorArista(st)
                    st.sidebar.header("Cambiar Peso Arista")
                    logArista.cambiarPesoArista(st)
                elif selected_sub_option == "Bipartito":
                    numNodosG1 = st.sidebar.number_input("Número de nodos conjunto 1", min_value=0, max_value=100)
                    numNodosG2 = st.sidebar.number_input("Número de nodos conjunto 2", min_value=0, max_value=100)
                    st.session_state.nodes, st.session_state.edges = logGrafo.generarGrafoBipartito(numNodosG1, numNodosG2,Node, Edge)
                    
                                        
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
                
                selected_sub_option = st.selectbox(
                    "Formato a exportar:",
                    [" ", "Excel", "Imagen"]
                )
                if selected_sub_option == "JSON":
                    ruta = './Data/'
                    nombreArchivo = 'grafo_exportado.json'
                    nombreCompleto = ruta + nombreArchivo
                    logGrafo.exportarGrafoJson(nombreCompleto, st.session_state.nodes, st.session_state.edges,Node, st)
                
                    
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
                [" ", "Nodo", "Arista"]
            )
            #=======================Seccion de nodos=======================
            
            
            logGrafo.guardarEstadoAntesDeCambio(st.session_state.nodes, st.session_state.edges)
            if selected_option == "Nodo":
                st.sidebar.header("Nodos")
                st.header("Agregar Nodo")
                logNodo.agregarNodo(Node, st)
                st.header("Cambiar Etiqueta Nodo")
                logNodo.cambiarEtiquetaNodo(st)
                st.header("Cambiar Color Nodo")
                logNodo.cambiarColorNodo(st)
                st.header("Eliminar Nodo")
                logNodo.eliminarNodo(st)
                hizoCambio = True
                
             
                 
            #=======================Seccion de arcos=======================
            if selected_option == "Arista":
                st.sidebar.header("Aristas")
                #listaEstadoAnterior=logGrafo.guardarEstadoAntesDeCambio(st.session_state.nodes, st.session_state.edges)
                st.header("Agregar Arista")
                if st.session_state.directed:  # Si el grafo es dirigido
                    bandera=True
                    logArista.agregarArista(Edge, True, st)  # Establece la dirección en True
                    cambio = True
                    
                else:
                    logArista.agregarArista(Edge, False, st)
                    cambio = True
                st.header("Cambiar Peso Arista")
                logArista.cambiarPesoArista(st)
                cambio = True
                st.header("Cambiar Color Arista")
                logArista.cambiarColorArista(st)
                cambio = True
                st.header("Eliminar Arista")
                logArista.eliminarArista(st)
                cambio = True
            
                
   
        if selected == "Ejecutar":
            selected_option = option_menu(
                menu_title=None,
                options=[" ","Procesos", "Parcial1 Analisis","Primera estrategia", "Segunda estrategia", "Tercera estrategia", "Sustentación Proyecto Dany"]
            )

            if selected_option == "Procesos":
                selected_sub_option = st.selectbox(
                    "Seleccionar un proceso:",
                    ["¿El grafo es bipartito?", "¿El grafo es bipartito conexo ó disconexo?"]
                )
                if selected_sub_option == "¿El grafo es bipartito?":
                    if logGrafo.esBipartito(st.session_state.nodes, st.session_state.edges):
                        st.text("El grafo es bipartito")
                    else:
                        st.text("El grafo no es bipartito")
                elif selected_sub_option == "¿El grafo es bipartito conexo ó disconexo?":
                    try:
                        salida, grafo = logGrafo.esBipartitoConexoOdisconexo(st.session_state.nodes, st.session_state.edges)
                        st.write(salida)
                        conexoOdisconexo = True
                    except Exception as e:
                        st.write("El grafo no es bipartito")
            elif selected_option == "Parcial1 Analisis":
                st.header("Algoritmo Parcial 1 Dany")
                op = st.selectbox("Seleccione una opción", [" ", "Ejecutar parcial analisis creandro grafo", "Ejecutar parcial"])
                if op == "Ejecutar parcial analisis creandro grafo":
                    bandera = True
                    numNodosG1 = st.sidebar.number_input("Número de nodos conjunto 1", min_value=0, max_value=100)
                    numNodosG2 = st.sidebar.number_input("Número de nodos conjunto 2", min_value=0, max_value=100)
                    nodes, edges, salida = parcial.mostrarParticiones(numNodosG1, numNodosG2, Node, Edge)
                    st.session_state.nodes = nodes
                    st.session_state.edges = edges
                    boolParcial = True
                elif op == "Ejecutar parcial":
                    bandera = True
                    salida= parcial.mostrarParticiones2(st.session_state.nodes, st.session_state.edges)                   
                    boolParcial=True
            elif selected_option == "Primera estrategia":
                futuros  = probEP.retornarEstadosFuturos(probEP.datosMatrices()) 
                estados = probEP.retornarEstados(probEP.datosMatrices())
                # Permitir al usuario seleccionar los nodos
                nodosG1 = st.multiselect("Seleccione los nodos del estado presente",estados)
                nodosG2 = st.multiselect('Seleccione los nodos del estado futuro:', futuros)
                estadoActual = st.selectbox("Seleccione el estado actual", probEP.retornarValorActual(nodosG1, nodosG2))
                st.session_state.nodes, st.session_state.edges = logGrafo.generar_grafoBipartito(nodosG1, nodosG2, Node, Edge)
                
                bandera = True
                aux2 =[]
                for i in nodosG2:
                    # verificar si el dato tiene ' al final por ejemplo "1'"
                    if "'" in i:
                        aux2.append(i[:-1])
                
                if st.button("Calcular probabilidad"):
                    mostrarProbabilidad = True
                    
            elif selected_option == "Segunda estrategia":
                c1 = st.multiselect("Seleccione los nodos del conjunto 1", probEP.retornarEstados(probEP.datosMatrices()))
                c2 = st.multiselect("Seleccione los nodos del conjunto 2", probEP.retornarEstadosFuturos(probEP.datosMatrices()))
                estadoActual = st.selectbox("Seleccione el estado actual", probEP.retornarValorActual(c1, c2))
                st.session_state.nodes, st.session_state.edges = logGrafo.generar_grafoBipartito(c1, c2, Node, Edge)
                bandera = True
                aux3 =[]
                for i in c2:
                    # verificar si el dato tiene ' al final por ejemplo "1'"
                    if "'" in i:
                        aux3.append(i[:-1])
                if st.button("Calcular segunda estrategia"):
                    estrategia2 = True
            elif selected_option == "Tercera estrategia":
                c11 = st.multiselect("Seleccione los nodos del conjunto 1", probEP.retornarEstados(probEP.datosMatrices()))
                c22 = st.multiselect("Seleccione los nodos del conjunto 2", probEP.retornarEstadosFuturos(probEP.datosMatrices()))
                estadoActual = st.selectbox("Seleccione el estado actual", probEP.retornarValorActual(c11, c22))
                st.session_state.nodes, st.session_state.edges = logGrafo.generar_grafoBipartito(c11, c22, Node, Edge)
                bandera = True
                aux4 =[]
                for i in c22:
                    # verificar si el dato tiene ' al final por ejemplo "1'"
                    if "'" in i:
                        aux4.append(i[:-1])
                if st.button("Calcular tercera estrategia"):
                    estrategia3 = True
            elif selected_option == "Sustentación Proyecto Dany":
                futuros  = probEP.retornarEstadosFuturos(probEP.datosMatrices()) 
                estados = probEP.retornarEstados(probEP.datosMatrices())
                # Permitir al usuario seleccionar los nodos
                nodosG1 = st.multiselect("Seleccione los nodos del estado presente",estados)
                nodosG2 = st.multiselect('Seleccione los nodos del estado futuro:', futuros)
                estadoActual = st.selectbox("Seleccione el estado actual", probEP.retornarValorActual(nodosG1, nodosG2))
                st.session_state.nodes, st.session_state.edges = logGrafo.generar_grafoBipartito(nodosG1, nodosG2, Node, Edge)
                candidato = st.multiselect("Seleccione los nodos del sistema candidato", estados)
                bandera = True
                aux2 =[]
                for i in nodosG2:
                    # verificar si el dato tiene ' al final por ejemplo "1'"
                    if "'" in i:
                        aux2.append(i[:-1])
                
                if st.button("Calcular probabilidad"):
                    mostrarSustentacion = True
       
        elif selected == "Ventana":
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Gráfica", "Tabla"]
            )

            if selected_option == "Gráfica":
                st.text(" Opción no dipsonible")

            elif selected_option == "Tabla":
                logGrafo.mostrarDatosGrafoTabla(st.session_state.nodes, st.session_state.edges,st)

        elif selected == "Ayuda":
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Manual de usuario", "Documentación", "Acerca de Grafos"]
            )
            if selected_option == "Manual de usuario":
                ruta = './Data/Manual de Usuario - Proyecto ADA.pdf'
                logGrafo.descargarManualUsuario(ruta, st)
            elif selected_option == "Documentación":
                ruta = './Data/Documentación_Proyecto_Final.pdf'
                logGrafo.descargarManualUsuario(ruta, st)
            elif selected_option == "Acerca de Grafos":
                ruta = './Data/grafos.pdf'
                logGrafo.descargarManualUsuario(ruta, st)
            
    
        
    # Navbar
    st.title("Proyecto de Análisis de Algoritmos")
    
    if "nodes" not in st.session_state:
        st.warning("No se ha cargado ningún archivo.")
    else:
        # Renderizar el grafo en el cuerpo principal
        
        configuracion = Gui(bandera)
        with st.container(border=True):
            agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=configuracion)
        if conexoOdisconexo:
            st.header("Componentes del grafo")
            salida, grafo = logGrafo.esBipartitoConexoOdisconexo(st.session_state.nodes, st.session_state.edges)
            logGrafo.dibujarGrafo(grafo,st)
        if boolParcial:
            st.header("Mejor SubGrafo con el coste minimo de aristas eliminadas:")
            st.write(salida["mejorSubGrafo"])
            st.header("Posibles SubGrafos:")
            st.write(salida["subgrafos"])   
            st.header("Mas datos")
            s = parcial.mostrarParticiones3(st.session_state.nodes, st.session_state.edges, st)
            
        
        if mostrarProbabilidad:
            aux = probEP.retornarDistribucion(nodosG1, nodosG2, estadoActual)
            # Convierte las listas a cadenas
            nodosG1_str = ', '.join(nodosG1)
            aux2_str = ', '.join(nodosG2)
            # Muestra la fórmula de probabilidad condicional con los valores de las variables
            st.latex(r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
            st.header("Distribución de probabilidad")
            st.table(aux)
            #st.header("Particiones del grafo")
            #df, particiones  = probEP.generarParticiones(nodosG1, nodosG2, estadoActual, candidato)
            #st.table(df)
            st.header("Mejor particion estrategia 1")
            particion, d, tiempo, lista = probEP.retornarMejorParticionE1(nodosG1, nodosG2, estadoActual)
            st.write('Partición: ',str(particion))
            st.write('Perdida: ', d)
            st.write('Tiempo: ', tiempo)
            #probEP.pintarGrafoGeneradoE1(nodosG1, nodosG2,estadoActual, st.session_state.nodes, st.session_state.edges)
            #tablapruebas = pruebas.calcularPrueba(nodosG1, nodosG2, estadoActual, st.session_state.edges)
            #st.table(tablapruebas)
            
        if estrategia2:
            aux = probEP.retornarDistribucion(c1, c2, estadoActual)
            st.header("Distribución de probabilidad")
            st.table(aux)
            st.header("Mejor particion estrategia 2")
            particionn, diferencia, tiempo, lista,l = estra2.estrategia2(c1, c2, estadoActual, st.session_state.edges)
            st.write('Partición: ',str(particionn))
            st.write('Perdida: ', diferencia)
            st.write('Tiempo: ', tiempo)
            #st.header("Particiones del grafo")
            #df  = estra2.generarParticiones(c1, c2, estadoActual, st.session_state.edges)
            #estra2.pintarGrafoGenerado(c1, c2,estadoActual, st.session_state.nodes, st.session_state.edges,Node, Edge)
            #st.table(df)
        if estrategia3:
            st.header("Mejor particion estrategia 3")
            estra3.pintarGrafoGenerado(c11, c22,estadoActual, st.session_state.nodes, st.session_state.edges,st)
        
        if mostrarSustentacion:
            aux = probEP.retornarDistribucion(nodosG1, nodosG2, estadoActual)
            # Convierte las listas a cadenas
            nodosG1_str = ', '.join(nodosG1)
            aux2_str = ', '.join(nodosG2)
            # Muestra la fórmula de probabilidad condicional con los valores de las variables
            st.latex(r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
            st.header("Distribución de probabilidad")
            st.table(aux)
            st.header("Mejor particion Sustentación Proyecto")
            particion, d, tiempo, lista = probEP.retornarMejorParticion(nodosG1, nodosG2, estadoActual, candidato)
            st.write(str(particion), d)
            probEP.pintarGrafoGenerado(nodosG1, nodosG2,estadoActual, st.session_state.edges,candidato,Node, Edge)
            
           
            
           


           
            
            
    st.write("© 2024 Proyecto ADA. Todos los derechos reservados.") 
        
if __name__ == "__main__":
    main()
