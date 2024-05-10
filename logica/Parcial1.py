import numpy as np
from itertools import chain, combinations
import networkx as nx
import random
from logica.LogGrafo import LogGrafo
import matplotlib.pyplot as plt

class Parcial1:
    def conjunto(self, listaNodos):
        s = list(listaNodos)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    """  
    def generarConjuntosConPeso(self, nodes, edges): # Generar todas las particiones posibles de ambos lados de los grupos
        todas_las_particiones = []
        for subconjunto in self.conjunto(nodes):
            S1 = set(subconjunto)  # Convertir a conjunto, conjunto 1
            S2 = set(nodes) - S1  # Conjunto 2
            s11 = [nodo.id for nodo in S1]
            s22 = [nodo.id for nodo in S2]
            if S1 and S2:  # Evitar particiones vacías
                peso_total = 0
                for arista in edges:
                    if (arista.source in s11 and arista.to in s22) or (arista.source in s22 and arista.to in s11):
                        peso_total += arista.weight
                todas_las_particiones.append(((S1, S2), peso_total))
               
        return todas_las_particiones
    """

    def generarConjuntosConPeso(self, nodes, edges):
        todas_las_particiones = []
        n = len(nodes)
        
        for i in range(1, 2**n // 2):  # mostrar solo la mitad de las particiones por ser dirigido
            indicesS1 = [j for j in range(n) if (i >> j) & 1]
            S1 = set([nodes[idx] for idx in indicesS1])
            S2 = set(nodes) - S1
            s11 = [nodo.id for nodo in S1]
            s22 = [nodo.id for nodo in S2]
            ss1 = [str(nodo.id) for nodo in S1]
            ss2 = [str(nodo.id) for nodo in S2]
            aristasEliminadas = []
            total_weight = 0
            for edge in edges:
                if (edge.source in s11 and edge.to in s22) or (edge.source in s22 and edge.to in s11) or (edge.source in ss1 and edge.to in ss2) or (edge.source in ss2 and edge.to in ss1):
                    total_weight += float(edge.weight)
                    aristasEliminadas.append(str(edge.source)+' '+ '=> '+ str(edge.to))
            # Agregar la partición, el peso total y las aristas no contadas a la lista
            todas_las_particiones.append(((S1, S2), total_weight, aristasEliminadas))
        return todas_las_particiones

    
    def mostrarParticiones(self, numNodosConjunto1, numNodosConjunto2, Node, Edge):
        nodes, edges = LogGrafo().generarGrafoBipartito(numNodosConjunto1, numNodosConjunto2, Node, Edge)
        peso_menor = float('inf')  # Inicializar con infinito para encontrar el mínimo
        todosLosSubgrafos = self.generarConjuntosConPeso(nodes, edges)
        # Imprimir todas las particiones
        resultados = {
            "subgrafos": [],
            "mejorSubGrafo": {},
            "AristasNoConsideradas": {}
        }
        for particion, peso_total, listaAristas in todosLosSubgrafos:
            datosSubgrafos = {
                "G1": [nodo.id for nodo in particion[0]],
                "G2": [nodo.id for nodo in particion[1]],
                "peso_minimo_aristas_eliminadas": peso_total,
                "AristasNoConsideradas": listaAristas
            }
            resultados["subgrafos"].append(datosSubgrafos)
            if peso_total < peso_menor:
                peso_menor = peso_total
                mejorSubgrafoFinal = {
                    "G1": [nodo.id for nodo in particion[0]],
                    "G2": [nodo.id for nodo in particion[1]],
                    "peso_minimo_aristas_eliminadas": peso_menor,
                    "AristasNoConsideradas": listaAristas
                }
                resultados["mejorSubGrafo"] = mejorSubgrafoFinal
        return nodes, edges, resultados
    
    def mostrarParticiones2(self, nodes, edges):
        todosLosSubgrafos = self.generarConjuntosConPeso(nodes, edges)
        peso_menor = float('inf')  # Inicializar con infinito para encontrar el mínimo
        # Imprimir todas las particiones
        resultados = {
            "subgrafos": [],
            "mejorSubGrafo": {},
            "AristasNoConsideradas": {}
        }
        for particion, peso_total, listaAristas in todosLosSubgrafos:
            datosSubgrafos = {
                "G1": [nodo.id for nodo in particion[0]],
                "G2": [nodo.id for nodo in particion[1]],
                "peso_minimo_aristas_eliminadas": peso_total,
                "AristasNoConsideradas": listaAristas
            }
            resultados["subgrafos"].append(datosSubgrafos)
            if peso_total < peso_menor:
                peso_menor =peso_total
                mejorSubgrafoFinal = {
                    "G1": [nodo.id for nodo in particion[0]],
                    "G2": [nodo.id for nodo in particion[1]],
                    "peso_minimo_aristas_eliminadas": peso_menor,
                    "AristasNoConsideradas": listaAristas
                }
                resultados["mejorSubGrafo"] = mejorSubgrafoFinal
        return resultados
    

    def mostrarParticiones3(self, nodes, edges, st):
        todosLosSubgrafos = self.generarConjuntosConPeso(nodes, edges)
        """G = nx.Graph()
        G.add_nodes_from(subgrafo["G1"])
        G.add_nodes_from(subgrafo["G2"])
        for arista in subgrafo["AristasNoConsideradas"]:
            nodo1, nodo2 = arista.split("=>")
            G.add_edge(nodo1.strip(), nodo2.strip())

        pos = nx.spring_layout(G)  # Posiciones para todos los nodos
        nx.draw_networkx_nodes(G, pos, nodelist=subgrafo["G1"], node_color="r", label="Conjunto 1")
        nx.draw_networkx_nodes(G, pos, nodelist=subgrafo["G2"], node_color="b", label="Conjunto 2")
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=8)

        plt.title("Subgrafo")
        plt.axis("off")
        plt.legend()
        st.pyplot(plt)"""
        """G = nx.Graph()
        for node in mejorGrafo.nodes():
            G.add_node(node.id, label=node.label)
        for edge in mejorGrafo.edges():
            G.add_edge(edge.source, edge.to, weight=edge.label)
        # Dibujar el grafo con matplotlib
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G,scale=2)#
        nx.draw(G,pos , with_labels=True, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')#
        nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels, ax=ax)#
        # Mostrar la figura en Streamlit
        st.pyplot(fig)"""
            
            

        


