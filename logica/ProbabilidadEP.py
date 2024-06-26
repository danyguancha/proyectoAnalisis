# Description: Clase que se encarga de generar la distribución de probabilidad de un estado futuro dado un estado actual
import functools
from itertools import combinations, product
import time
import numpy as np
from GUI import Gui
from logica.Data import Data
#from Data import Data
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.stats import wasserstein_distance
import streamlit_agraph as stag
from logica.sustentacion import Sustentacion
from logica.LogGrafo import LogGrafo

class ProbabilidadEP:
    def datosMatrices(self, opcion):
        tres = Data().retornarDatosTresNodos()
        cuatro = Data().retornarDatosCuatroNodos()
        cinco = Data().retornarDatosCincoNodos()
        seis = Data().retornarDatosSeisNodos()
        ocho = Data().retornarDatosMatrizOchoNodos()
        diez = Data().retornarDatosMatrizDiezNodos()
        salida = None
        if opcion == "Tres Nodos":
            salida = tres
        if opcion == "Cuatro Nodos":
            salida = cuatro
        if opcion == "Cinco Nodos":
            salida =  cinco
        if opcion == "Seis Nodos":
            salida = seis  
        if opcion == "Ocho Nodos":
            salida = ocho
        if opcion == "Diez Nodos":
            salida = diez
        return salida
    def listaMatrices(self):
        opcion = ["Tres Nodos", "Cuatro Nodos", "Cinco Nodos", "Seis Nodos", "Ocho Nodos", "Diez Nodos"]          
        return opcion
      
    def mostrarMatriz(self, st):
        tres = Data().retornarDatosTresNodos()
        cuatro = Data().retornarDatosCuatroNodos()
        cinco = Data().retornarDatosCincoNodos()
        seis = Data().retornarDatosSeisNodos()
        #datos = Data().retornarDatosMatrizPrueba()  
        #datos = Data().retornarDatosCuatro() 
        opcion = st.radio("",["Tres Nodos", "Cuatro Nodos"], key="matriz")
        if opcion == "Tres Nodos":
            return tres

    
    def generarDistribucionProbabilidades(self, tabla, estadoActual, estadoFuturo, num, estados):
        #indice = [estados.index(i) for i in estadoActual]
        try:
            indice = [estados.index(i) for i in estadoActual]
        except ValueError as e:
            print(f"Error: {e}")
            print("estadoActual:", estadoActual)
            print("estados:", estados)
            raise

        probabilidadesDistribuidas = []
        for i in estadoFuturo:
            # verificar si i tiene "'", si es así, se elimina la comilla
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
    
    def retornarEstados(self, datos):
        
        resultado, estados = self.generarEstadoTransicion(datos)
        return estados
    
    def retornarDistribucion(self, c1, c2, valorActual, opcion):
        matrices = self.datosMatrices(opcion)
        resultado, estados = self.generarEstadoTransicion(matrices)
        datos = self.generarDistribucionProbabilidades(matrices, c1, c2, valorActual, estados)
        lista = []
        lista.append(str(datos[0][0]))
            
        #lista.append(datos[0])
        for i in range(len(datos[0][1:])):
            lista.append(str(datos[0][1:][i]))
        
        df = pd.DataFrame(datos[1:], columns=lista)
        return df
    
    def retornarDistribucionSustentacion(self, c1, c2, valorActual, candidato, opcion):
        matrices = self.datosMatrices(opcion)
        matricesP = self.retornarMatrizCondicionada(matrices, c1, valorActual, candidato)
        c1 = self.retornarEstados(matricesP)
        c2 = self.retornarEstadosFuturos(matricesP)
        resultado, estados = self.generarEstadoTransicion(matricesP)
        datos = self.generarDistribucionProbabilidades(matricesP, c1, c2, valorActual, estados)
        lista = []
        lista.append(str(datos[0][0]))
            
        #lista.append(datos[0])
        for i in range(len(datos[0][1:])):
            lista.append(str(datos[0][1:][i]))
        
        df = pd.DataFrame(datos[1:], columns=lista)
        return df
    
    
    def retornarValorActual(self, c1, c2, opcion):
        lista = []
        matrices = self.datosMatrices(opcion)
        
        for j in matrices['A']:
            lista.append(j)
        
        return lista
    
    def retornarEstadosFuturos(self, datos):
        
        resultado, estados = self.generarEstadoTransicion(datos)
        # agregarle a cada valor de los estados una '
        for i in range(len(estados)):
            estados[i] = estados[i] + "'"

        return estados

    
    def generarParticiones(self, c1, c2, estadoActual, candidato, opcion):
        matrices = self.datosMatrices(opcion)
        particiones = []
        a, b,c, lista = self.retornarMejorParticion(c1, c2, estadoActual, candidato)
        #print(lista)
        df = pd.DataFrame(lista, columns=['Conjunto 1', 'Conjunto 2','Diferencia'])
        return df, particiones
    
    def particiones(self, listaDistribuida, eAcual1, eActual2, eFuturo1, eFuturo2):
        p1 = tuple(listaDistribuida[1][0][i] for i in eAcual1 if i < len(listaDistribuida[1][0]))
        p2 = tuple(listaDistribuida[1][0][i] for i in eActual2 if i < len(listaDistribuida[1][0]))
        listaNueva1 =[]
        listaNueva2 =[]
        i1 ={}
        i2 ={}
        for num, fila in enumerate(listaDistribuida[0][1:], start=1):
            auxNuevaTabla1 = tuple(fila[i] for i in eFuturo1)
            auxNuevaTabla2 = tuple(fila[i] for i in eFuturo2)
            self.actualizarTabla(i1, auxNuevaTabla1, listaNueva1, num)
            self.actualizarTabla(i2, auxNuevaTabla2, listaNueva2, num)
        listaAux1 = [p1] + self.calcularPromedio(i1, listaDistribuida)
        listaAux2 = [p2] + self.calcularPromedio(i2, listaDistribuida)
        listaSalida1 = [['Key'] + listaNueva1, listaAux1]
        listaSalida2 = [['Key'] + listaNueva2, listaAux2]
        return listaSalida1, listaSalida2
    
    def calcularPromedio(self, indices, listaDistribuida):
        return [sum(listaDistribuida[1][j] for j in indices[i])/len(indices[i]) if indices[i] else 0 for i in indices]
    
    def actualizarTabla(self, indices, auxNuevaLista, listaNueva, num):
        if auxNuevaLista not in indices:
            indices[auxNuevaLista] = [num]
            listaNueva.append(auxNuevaLista)
        else:
            indices[auxNuevaLista].append(num) 

    def generarCombinaciones(self, c1, c2):
        conjunto1 = [comb for i in range(len(c1)+1) for comb in combinations(range(len(c1)), i)]
        conjunto2 = [comb for i in range(len(c2)+1) for comb in combinations(range(len(c2)), i)]
        todasLasCombinaciones = [(cc1, cc2) for cc1 in conjunto1 for cc2 in conjunto2]
        listaCombinaciones = []
        for comb in todasLasCombinaciones:
            parteContador = (tuple(set(range(len(c1))) - set(comb[0])), tuple(set(range(len(c2))) - set(comb[1])))

            if (parteContador, comb) not in listaCombinaciones and (comb, parteContador) not in listaCombinaciones:
                listaCombinaciones.append([comb, parteContador])
        return listaCombinaciones
    
    def generarProbParticiones(self, distribuciones, combinaciones):
        tablaDeparticiones ={}
        # Cadena que representa la operación de diferencia entre listas
        cadena = distribuciones[0][0]
        lista1, lista2 = [eval(subcadena) for subcadena in cadena.split('|')]
        
        for i in combinaciones[1:]:
            lista = self.particiones(distribuciones, i[0][0], i[1][0], i[0][1], i[1][1])
            nombre = "("
            for j in i[0][0]:
                if j < len(lista1):
                    nombre += f" {lista1[j]}"
            nombre += " ) ("
            for j in i[0][1]:
                if j < len(lista2):
                    nombre += f" {lista2[j]}"
            nombre += " ) - ("

            for j in i[1][0]:
                if j < len(lista1):
                    nombre += f" {lista1[j]}"
            nombre += " ) ("
            for j in i[1][1]:
                if j < len(lista2):
                    nombre += f" {lista2[j]}"
                    pass
            nombre += " )"
            tablaDeparticiones[nombre] = lista
        return tablaDeparticiones
    
    def retornarMejorParticion(self, c1, c2, estadoActual, candidato, opcion):
        matrices = self.datosMatrices(opcion)
        matricesP = self.retornarMatrizCondicionada(matrices, c1, estadoActual, candidato)
        c1 = self.retornarEstados(matricesP)
        c2 = self.retornarEstadosFuturos(matricesP)
        resultado, estados = self.generarEstadoTransicion(matricesP)
        distribucionProbabilidadOriginal = self.generarDistribucionProbabilidades(matricesP, c1, c2, estadoActual, estados)
        lista = []
        particion, diferencia, tiempo, lista = self.busqueda_voraz(matricesP, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        return particion, diferencia, tiempo, lista

    def retornarMejorParticionE1(self, c1, c2, estadoActual, opcion):
        matrices = self.datosMatrices(opcion)
        resultado, estados = self.generarEstadoTransicion(matrices)
        distribucionProbabilidadOriginal = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
        lista = []
        inicio = time.time()
        particion, diferencia, tiempo, lista = self.busqueda_voraz(matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        fin = time.time()
        tiempoEjecucion = fin - inicio
        return particion, diferencia, tiempoEjecucion, lista
  
    
    def retornarMatrizCondicionada(self, matrices, c1, estadoActual, candidato):
        s = Sustentacion()
        matrices_condicionadas = s.condiciona_matriz(matrices, estadoActual, candidato,c1)
        probabilidades_finales = s.calcula_probabilidades(matrices_condicionadas, estadoActual, candidato,c1)
        return probabilidades_finales
    
    def estrategiaUno(self, matrices, c1, c2, estadoActual, estados):
        tabla = {}
        key = (tuple(c1), tuple(c2), estadoActual)  # Creamos una llave única para la tabla
        if key not in tabla:
            tabla[key] = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
        return tabla[key]

    def busqueda_voraz(self, matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual):
        mejor_particion = []
        menor_diferencia = float('inf')
        listaParticionesEvaluadas = []
        
        for i in range(len(c1)):
            
            c1_izq = c1[:i]
            c1_der = c1[i:]
            c2_izq = []
            c2_der = list(c2)
            
            for j in range(len(c2)):
                c2_izq.append(c2_der.pop(0))

                
                distribucion_izq = self.estrategiaUno(matrices, c1_izq, c2_izq, estadoActual, estados)
                distribucion_der = self.estrategiaUno(matrices, c1_der, c2_der, estadoActual, estados)
                p1 = distribucion_izq[1][1:]
                p2 = distribucion_der[1][1:]
                prodTensor = self.producto_tensor(p1, p2)
                diferencia = self.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)
                
                aux = []
                if c2_der == [] and c1_der == []:
                    continue
                elif diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    mejor_particion = [(tuple(c2_izq), (tuple(c1_izq))), (tuple(c2_der), tuple(c1_der))]
                aux = [(tuple(c2_izq), (tuple(c1_izq))), (tuple(c2_der), tuple(c1_der)), str(diferencia)]
                listaParticionesEvaluadas.append(aux)
        
        return mejor_particion, menor_diferencia,0, listaParticionesEvaluadas
   
    def pintarGrafoGeneradoE1(self, c1, c2, estadoActual, nodes, edges, opcion):
        mP, a, b, c = self.retornarMejorParticionE1(c1, c2, estadoActual, opcion)
        p1, p2 = mP
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
        
        # Graficamos el grafo con las aristas eliminadas
        graph = stag.agraph(nodes=nodes, edges=edges, config=Gui(True))

    def pintarGrafoGenerado(self, c1, c2, estadoActual, edges, candidato, Node, Edge, opcion):
        
        mP, a, b, c = self.retornarMejorParticion(c1, c2, estadoActual, candidato, opcion)
        matrices = self.datosMatrices(opcion)
        matricesP = self.retornarMatrizCondicionada(matrices, c1, estadoActual, candidato)
        c1 = self.retornarEstados(matricesP)
        c2 = self.retornarEstadosFuturos(matricesP)
        nodes, edges = LogGrafo().generar_grafoBipartito(c1, c2, Node, Edge)
        p1, p2 = mP
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
        
        # Graficamos el grafo con las aristas eliminadas
        graph = stag.agraph(nodes=nodes, edges=edges, config=Gui(True))     

    
    def convertir_a_listas(self, datos):
        lineas = datos.split('\n')
        listas = []
        for linea in lineas:
            grupos = linea.split(' - ')
            grupos_listas = []
            for grupo in grupos:
                subgrupos = grupo.split(') (')
                subgrupos = [subgrupo.replace("(", "").replace(")", "").strip() for subgrupo in subgrupos]
                subgrupos_listas = [subgrupo.split() if subgrupo else [] for subgrupo in subgrupos]
                grupos_listas.append(subgrupos_listas)
            listas.append(grupos_listas)
        return listas

    def calcularEMD(self, p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)

        # Asegúrate de que p1 y p2 sean unidimensionales
        if p1.ndim != 1 or p2.ndim != 1:
            raise ValueError("p1 y p2 deben ser arrays unidimensionales")

        # Ajusta p2 para que tenga la misma longitud que p1
        if len(p1) != len(p2):
            p2 = np.interp(np.linspace(0, 1, len(p1)), np.linspace(0, 1, len(p2)), p2)
        
        cost_matrix = np.abs(np.subtract.outer(p1, p2))
        salida = np.sum(np.min(cost_matrix, axis=1) * p1)
        return salida
            
    def producto_tensor(self, p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.outer(p1, p2).flatten()
        
