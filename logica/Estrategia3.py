from itertools import combinations, product
import time
import numpy as np
from GUI import Gui
from logica.Data import Data
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.stats import wasserstein_distance
import streamlit_agraph as stag
import random
import math
from logica.ProbabilidadEP import ProbabilidadEP

class Estrategia3:
    def datosMatriz(self):
        p = ProbabilidadEP()
        datos = p.datosMatrices()
        return datos
    
    def generarDistribucionProbabilidades(self, tabla, estadoActual, estadoFuturo, num, estados):
        indice = [estados.index(i) for i in estadoActual]
        probabilidadesDistribuidas = []
        for i in estadoFuturo:
            if "'" in i:
                i = i[:-1]
            nuevaTabla = self.generarTablaComparativa(tabla[i])
            filtro2 = self.porcentajeDistribucion(nuevaTabla, indice, num)
            probabilidadesDistribuidas.append(filtro2)
        tabla = self.generarTabla(probabilidadesDistribuidas, num)
        tabla[0] = [[estadoFuturo, estadoActual]] + tabla[0]
        tabla[1] = [num] + tabla[1]
        return tabla
    
    def generarTabla(self, distribucion, num, i=0, numBinario ='', nuevoValor=1):
        if i == len(distribucion):
            numBinario = '0' * (len(distribucion)-len(numBinario)) + numBinario
            nuevoDato = tuple(int(bit) for bit in numBinario)
            return [[nuevoDato], [nuevoValor]]
        else:
            tabla = self.generarTabla(distribucion, num, i+1, numBinario+'0', nuevoValor*distribucion[i][1][2])
            tabla2 = self.generarTabla(distribucion, num, i+1, numBinario+'1', nuevoValor*distribucion[i][1][1])
            return [tabla[0]+tabla2[0], tabla[1]+tabla2[1]]
        
    def porcentajeDistribucion(self, tabla, indice, num):
        tablaNueva = [tabla[0]]
        fila = None
        try:
            tabla1 = [fila for fila in tabla[1:] if all(i < len(num) and pos < len(fila[0]) and fila[0][pos] == num[i] for i, pos in enumerate(indice))]
        except IndexError as e:
            print(f"IndexError: {e}")
            raise

        nuevosValores = [0, 0]
        for i in tabla1:
            nuevosValores[0] += i[1]
            nuevosValores[1] += i[2]

        total = sum(nuevosValores)
        nuevosValores = [v / total if total != 0 else v for v in nuevosValores]
        nuevaFila = [num, *nuevosValores]
        tablaNueva.append(nuevaFila)
        return tablaNueva
    
    def generarTablaComparativa(self, diccionario):
        lista = [['key', (1,), (0,)]]
        for k, v in diccionario.items():
            lista.append([k, v, 1 - v])
        return lista
    
    def generarEstadoTransicion(self, subconjuntos):
        estados = list(subconjuntos.keys())
        transiciones = {}
        estado_actual = [0] * len(estados)

        def aux(i):
            if i == len(estados):
                estado_actual_tuple = tuple(estado_actual)
                estado_futuro = tuple(subconjuntos[estado][estado_actual_tuple] for estado in estados)
                transiciones[estado_actual_tuple] = estado_futuro
            else:
                estado_actual[i] = 0
                aux(i + 1)
                estado_actual[i] = 1
                aux(i + 1)
        aux(0)
        return transiciones, estados  
    
    def retornarMejorParticion(self, c1, c2, estadoActual):
        matrices = self.datosMatriz()
        resultado, estados = self.generarEstadoTransicion(matrices)
        distribucionProbabilidadOriginal = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
        lista = []
        particion, diferencia, tiempo, lista = self.recocidoSimulado(matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        return particion, diferencia, tiempo, lista

    def recocidoSimulado(self, matrices, estados, disProbdOriginal, c1, c2, estadoActual):
        mejor_particion = None
        menor_diferencia = float('inf')
        listaParticionesEvaluadas = []
        temperatura = 1000
        factor_enfriamiento = 0.99
        iteraciones_por_temperatura = 2
        tiempo = 0
        
        while temperatura > 1:
            for _ in range(iteraciones_por_temperatura):
                inicio = time.time()
                c1_izq, c2_izq, c1_der, c2_der = self.generar_vecino(c1, c2)
                diferencia = self.obtener_diferencia(c1_izq, c2_izq, c1_der, c2_der, matrices, estadoActual, disProbdOriginal, estados)
                aux = [(tuple(c2_izq), tuple(c1_izq)), (tuple(c2_der), tuple(c1_der)), str(diferencia), str(time.time())]
                listaParticionesEvaluadas.append(aux)
                
                if diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    mejor_particion = [(tuple(c2_izq), tuple(c1_izq)), (tuple(c2_der), tuple(c1_der))]
                else:
                    probabilidad_aceptacion = math.exp((menor_diferencia - diferencia) / temperatura)
                    if random.random() < probabilidad_aceptacion:
                        menor_diferencia = diferencia
                        mejor_particion = [(tuple(c2_izq), tuple(c1_izq)), (tuple(c2_der), tuple(c1_der))]
                fin = time.time()
                tiempo = fin - inicio
            temperatura *= factor_enfriamiento

        return mejor_particion, menor_diferencia, tiempo, listaParticionesEvaluadas

    def obtener_diferencia(self, c1_izq, c2_izq, c1_der, c2_der, matrices, estadoActual,disOriginal, estados):
        distribucion_izq = self.generarDistribucionProbabilidades(matrices, c1_izq, c2_izq, estadoActual, estados)
        distribucion_der = self.generarDistribucionProbabilidades(matrices, c1_der, c2_der, estadoActual, estados)
        p1 = distribucion_izq[1][1:]
        p2 = distribucion_der[1][1:]
        prodTensor = self.producto_tensor(p1, p2)
        diferencia = self.calcularEMD(disOriginal[1][1:], prodTensor)
        return diferencia

    def generar_vecino(self, c1, c2):
        mitad_c1 = len(c1) // 2
        mitad_c2 = len(c2) // 2
        c1_izq = random.sample(c1, mitad_c1)
        c1_der = list(set(c1) - set(c1_izq))
        c2_izq = random.sample(c2, mitad_c2)
        c2_der = list(set(c2) - set(c2_izq))
        return c1_izq, c2_izq, c1_der, c2_der
   
    def pintarGrafoGenerado(self, c1, c2, estadoActual, nodes, edges, st):
        particion, diferencia, tiempo, lista = self.retornarMejorParticion(c1, c2, estadoActual)
        p1, p2 = particion
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
        st.write(str(particion), diferencia, tiempo)
        graph = stag.agraph(nodes=nodes, edges=edges, config=Gui(True))

    def calcularEMD(self, p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)

        if p1.ndim != 1 or p2.ndim != 1:
            raise ValueError("p1 y p2 deben ser arrays unidimensionales")

        if len(p1) != len(p2):
            p2 = np.interp(np.linspace(0, 1, len(p1)), np.linspace(0, 1, len(p2)), p2)
        
        cost_matrix = np.abs(np.subtract.outer(p1, p2))
        salida = np.sum(np.min(cost_matrix, axis=1) * p1)
        return salida
    
    def producto_tensor(self, p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.outer(p1, p2).flatten()
