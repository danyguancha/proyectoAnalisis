class LogArista:
    def agregarArista(self, Edge, st):
        if 'edges' not in st.session_state:
            st.session_state.edges = []
            
        source_node_id = st.sidebar.selectbox("Nodo de inicio", [node.id for node in st.session_state.nodes])
        target_node_id = st.sidebar.selectbox("Nodo de destino", [node.id for node in st.session_state.nodes])
        weight = st.sidebar.number_input("Peso", min_value=1, max_value=1000)
        if st.sidebar.button("Agregar Arista"):
            color = self.asignarColorArista(weight)
            nueva_arista = Edge(source=source_node_id, target=target_node_id, weight=weight, label=str(weight), width=3, color=color)
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
        
    
    def editarArista(self, st):
        selected_edge_label = st.sidebar.selectbox("Seleccionar Arista:", [edge.label for edge in st.session_state.edges])
        selected_weight = st.sidebar.number_input("Nuevo Peso", min_value=1, max_value=100, value=1)
        if st.sidebar.button("Editar Peso"):
            selected_edge = next((edge for edge in st.session_state.edges if edge.label == selected_edge_label), None)
            if selected_edge:
                selected_edge.weight = selected_weight
                selected_edge.label = str(selected_weight)
            else:
                st.warning("No se ha seleccionado ninguna arista.")
    
    def eliminarArista(self, st):
        selectedAristaEliminar = st.sidebar.selectbox("Eliminar Arista:", [edge.label for edge in st.session_state.edges])
        
        if st.sidebar.button("Eliminar Arista"):
            aristaEliminar = next((edge for edge in st.session_state.edges if edge.label == selectedAristaEliminar), None)
            
            if aristaEliminar:
                color = 'rgba(254, 20, 56, 0.2)'
                if aristaEliminar.color == color and aristaEliminar.width==4:
                    st.warning('Esta arista ya fue eliminada anteriormente')
                else:
                    aristaEliminar.width = 5
                    aristaEliminar.color = color
                
                #aristaEliminar.label = f'[ X, {aristaEliminar.label} ]'  # Encerramos el peso en un cuadro
                #st.session_state.edges = st.session_state.edges  # Actualizamos las aristas
                #st.session_state.graph = {'edges': st.session_state.edges}  # Inicializamos o actualizamos el grafo
            else:
                st.warning("No se ha seleccionado ninguna arista.")
            
            


    

