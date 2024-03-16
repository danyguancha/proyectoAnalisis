import time
from streamlit_agraph import agraph
from GUI import Gui

class LogNodo:
    
    
    def agregarNodo(self, Node, st):
        all_possible_ids = set(range(1, 1000))

        if 'nodes' not in st.session_state:
        # Si no existe, inicializarlo como una lista vacía
            st.session_state.nodes = []

        existing_ids = set([node.id for node in st.session_state.nodes])
        available_ids = list(all_possible_ids - existing_ids)
        idNodo = st.sidebar.selectbox("ID del nodo", available_ids)
        if st.sidebar.button("Agregar Nodo"):
            nuevo_nodo = Node(id=idNodo, size=20, label=str(idNodo), type="circle", color="purple")
            st.session_state.nodes.append(nuevo_nodo)
            st.success("Nodo agregado exitosamente!")
    
    def cambiarColorNodo(self, st):
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
                
    def eliminarNodo(self, st):
        selectedNodoEliminar = st.sidebar.selectbox("Eliminar Nodo:", [node.label for node in st.session_state.nodes])
                
        if st.sidebar.button("Eliminar Nodo"):
            # Lógica para eliminar el nodo seleccionado
            nodoEliminar = next((node for node in st.session_state.nodes if node.label == selectedNodoEliminar), None)
            if nodoEliminar:
                st.session_state.nodes.remove(nodoEliminar)
            else:
                st.warning("No se ha seleccionado ningún nodo.")
            
    def buscarNodo(self, st):
        selectedNodoBuscar = st.sidebar.selectbox("Buscar Nodo:", [node.label for node in st.session_state.nodes])
                
        if st.sidebar.button("Buscar Nodo"):
            # Lógica para buscar el nodo seleccionado
            nodoBuscar = next((node for node in st.session_state.nodes if node.label == selectedNodoBuscar), None)
            
            if nodoBuscar:
                # si lo encuentra, cambia el color del nodo a verde
                #clr = nodoBuscar.color
                nodoBuscar.color = "green"
                st.success("Nodo encontrado!")
                #nodoBuscar.color = clr
                
            else:
                st.warning("No se ha seleccionado ningún nodo.")
    