import itertools
from GUI import Gui
import pandas as pd
from logica.Data import Data
from logica.ProbabilidadEP import ProbabilidadEP
import time
import streamlit_agraph as stag

class Estrategia2:
    def estrategia2(self, c1, c2, estadoActual, edges):
        p = ProbabilidadEP()
        matrices = p.datosMatrices()
        resultado, estados = p.generarEstadoTransicion(matrices)
        distribucionProbabilidadOriginal = p.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
        mejor_particion = []
        menor_diferencia = float('inf')
        listaParticionesEvaluadas = []
        eliminadas = []
        tiempoEjecucion = 0
        
        # Calcular la pérdida de información para cada arista
        perdidas_aristas = {arista: self.calcular_perdida(matrices, estados, distribucionProbabilidadOriginal, c1.copy(), c2.copy(), estadoActual, arista, p) for arista in edges}

        # Filtrar las aristas con pérdida != 0
        aristas_con_perdida = [arista for arista, perdida in perdidas_aristas.items() if perdida != 0]

        # Si no hay aristas con pérdida distinta de cero, generar la partición trivial
        if not aristas_con_perdida:
            mejor_particion = [(tuple(c2), ()), ((), tuple(c1))]
            
            distribucion_izq = p.generarDistribucionProbabilidades(matrices, (), tuple(c2), estadoActual, estados)
            distribucion_der = p.generarDistribucionProbabilidades(matrices, tuple(c1), (), estadoActual, estados)
            p1 = distribucion_izq[1][1:]
            p2 = distribucion_der[1][1:]
            prodTensor = p.producto_tensor(p1, p2)
            diferencia = p.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)
            
            aux = [(tuple(c2), ()), ((), tuple(c1)), str(diferencia)]
            listaParticionesEvaluadas.append(aux)
            return mejor_particion, diferencia, tiempoEjecucion, listaParticionesEvaluadas, eliminadas
        inicio = time.time()
        # Ordenar las aristas de menor a mayor pérdida
        aristas_con_perdida.sort(key=lambda arista: perdidas_aristas[arista])

        while aristas_con_perdida:
            arista_min_perdida = aristas_con_perdida.pop(0)
            eliminadas.append(arista_min_perdida)

            c1_izq = []
            c1_der = list(c1)
            c2_izq = []
            c2_der = list(c2)

            if arista_min_perdida.source in c1_der:
                c1_der.remove(arista_min_perdida.source)
                c1_izq.append(arista_min_perdida.source)
            if arista_min_perdida.to in c2_der:
                c2_der.remove(arista_min_perdida.to)
                c2_izq.append(arista_min_perdida.to)
            distribucion_izq = p.generarDistribucionProbabilidades(matrices, tuple(c1_izq), tuple(c2_izq), estadoActual, estados)
            distribucion_der = p.generarDistribucionProbabilidades(matrices, tuple(c1_der), tuple(c2_der), estadoActual, estados)
            p1 = distribucion_izq[1][1:]
            p2 = distribucion_der[1][1:]
            prodTensor = p.producto_tensor(p1, p2)
            diferencia = p.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)

            if diferencia < menor_diferencia:
                menor_diferencia = diferencia
                mejor_particion = [(tuple(c2_izq), tuple(c1_izq)), (tuple(c2_der), tuple(c1_der))]

            aux = [(tuple(c2_izq), tuple(c1_izq)), (tuple(c2_der), tuple(c1_der)), str(diferencia)]
            listaParticionesEvaluadas.append(aux)
        fin = time.time()
        tiempoEjecucion = fin - inicio 
        return mejor_particion, menor_diferencia, tiempoEjecucion, listaParticionesEvaluadas, eliminadas
    
   

    def calcular_perdida(self, matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual, arista, p):
        c1_copy = c1.copy()
        c2_copy = c2.copy()

        if arista.source in c1_copy and arista.to in c2_copy:
            c1_copy.remove(arista.source)
            c2_copy.remove(arista.to)
        elif arista.source in c2_copy and arista.to in c1_copy:
            c2_copy.remove(arista.source)
            c1_copy.remove(arista.to)
        else:
            return float('inf')

        distribucion_izq = p.generarDistribucionProbabilidades(matrices, c1_copy, c2_copy, estadoActual, estados)
        prodTensor = p.producto_tensor(distribucion_izq[1][1:], distribucion_izq[1][1:])
        diferencia = p.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)
        return diferencia
    
    def generarParticiones(self, c1, c2, estadoActual, edges):
        a, b, c, lista, l = self.estrategia2(c1, c2, estadoActual, edges)
        df = pd.DataFrame(lista, columns=['Conjunto 1', 'Conjunto 2', 'Diferencia'])
        return df
    
    def pintarGrafoGenerado(self, c1, c2, estadoActual, nodes, edges, Node, Edge):
        p = ProbabilidadEP()
        mp, menorD, tiempo, lpEvaluadas, eliminadas = self.estrategia2(c1, c2, estadoActual, edges)
        m = p.datosMatrices()
        s, e = p.generarEstadoTransicion(m)
        dpo = p.generarDistribucionProbabilidades(m, c1, c2, estadoActual, e)

        aristas_eliminadas_perdida_cero = set()
        arista_minima_perdida = None
        minima_perdida = float('inf')

        # Identificar aristas con pérdida cero y la arista con la pérdida mínima
        for arista in edges:
            perdida = self.calcular_perdida(m, e, dpo, c1.copy(), c2.copy(), estadoActual, arista, p)
            if perdida == 0:
                aristas_eliminadas_perdida_cero.add((arista.source, arista.to))
            elif perdida < minima_perdida:
                arista_minima_perdida = (arista.source, arista.to)
                minima_perdida = perdida

        # Pintar las aristas según las condiciones especificadas
        for arista in edges:
            if (arista.source, arista.to) in aristas_eliminadas_perdida_cero:
                arista.color = 'yellow'
                arista.dashes = True
            elif (arista.source, arista.to) == arista_minima_perdida:
                arista.color = 'violet'
                arista.dashes = True
        p1, p2 = mp
        for i in p1[1]:
            if i not in p2[1]:
                for arista in edges:
                    if  arista.source == i and arista.to in p2[0]:
                        arista.dashes = True
                        arista.color = 'rgba(254, 20, 56, 0.5)'
        for i in p2[1]:
            if i not in p1[1]:
                for arista in edges:
                    if  arista.source == i and arista.to in p1[0]:
                        arista.dashes = True
                        arista.color = 'rgba(254, 20, 56, 0.5)'

        # Generar y mostrar el grafo
        graph = stag.agraph(nodes=nodes, edges=edges, config=Gui(True))

