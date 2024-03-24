import random
class LogArista:
    def __init__(self):
        self.aux = False
        self.color_dict = {}
    def agregarArista(self, Edge,tipo, st):
        if 'edges' not in st.session_state:
            st.session_state.edges = []
        aux = False
        source_node_id = st.sidebar.selectbox("Nodo de inicio", [node.id for node in st.session_state.nodes])
        target_node_id = st.sidebar.selectbox("Nodo de destino", [node.id for node in st.session_state.nodes])
        weight = st.sidebar.number_input("Peso", min_value=1, max_value=1000)
        if st.sidebar.button("Agregar Arista"):
            for edge in st.session_state.edges:
                if edge.color == 'rgba(254, 20, 56, 0.5)':
                    st.session_state.edges.remove(edge)
            nueva_arista = Edge(source=source_node_id, target=target_node_id, weight=weight, 
                            label=str(weight), width=3, directed=tipo)
            st.session_state.edges.append(nueva_arista)
           

            
    def asignarColorArista(self, peso):
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
        
    
    def cambiarPesoArista(self, st):
        selected_edge_label = st.sidebar.selectbox("Seleccionar Arista:", [edge.label for edge in st.session_state.edges])
        selected_weight = st.sidebar.number_input("Nuevo Peso", min_value=1, max_value=1000, value=1)
        if st.sidebar.button("Editar Peso"):
            selected_edge = next((edge for edge in st.session_state.edges if edge.label == selected_edge_label), None)
            if selected_edge:
                selected_edge.weight = selected_weight
                selected_edge.label = str(selected_weight)
            else:
                st.warning("No se ha seleccionado ninguna arista.")
        
    def eliminarArista(self, st):
        # seleccionar arista a eliminar con nodo inicio y nodo destino
        st.write('I: Nodo Inicio')
        st.write('D: Nodo Destino')
        st.write('P: Peso de la arista')
        selectedAristaEliminar = st.sidebar.selectbox("Eliminar Arista:",['Arista. '+str({'I':edge.source, 'D':edge.to, 'P':edge.weight}) for edge in st.session_state.edges])
        
        # Si ya se seleccionó una arista anteriormente, cambiar su color al original
        if hasattr(st.session_state, 'last_selected_edge') and st.session_state.last_selected_edge:
            st.session_state.last_selected_edge.color = 'gray'
        
        if st.sidebar.button("Eliminar Arista"):
            aristaEliminar = next((edge for edge in st.session_state.edges if 'Arista. '+str({'I':edge.source, 'D':edge.to, 'P':edge.weight}) == selectedAristaEliminar), None)
            
            if aristaEliminar:
                aristaEliminar.dashes = True
                aristaEliminar.color = 'rgba(254, 20, 56, 0.5)'  # Cambiar el color de la arista a rgba cuando se elimina
                st.session_state.last_selected_edge = None  # Resetear la última arista seleccionada
            else:
                st.warning("No se ha seleccionado ninguna arista.")
        
    def cambiarColorArista(self, st):
        selectedAristaColor = st.sidebar.selectbox("Cambiar Color Arista:", [edge.label for edge in st.session_state.edges])
        selected_color = st.sidebar.color_picker("Seleccionar Color", "#ff0000")
        if st.sidebar.button("Cambiar Color Arista"):
            selected_arista = next((edge for edge in st.session_state.edges if edge.label == selectedAristaColor), None)
            if selected_arista:
                selected_arista.color = selected_color
            else:
                st.warning("No se ha seleccionado ninguna arista.")
            
            


    

