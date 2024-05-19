# Description: Clase que se encarga de generar la distribución de probabilidad de un estado futuro dado un estado actual
from itertools import combinations, product
import numpy as np
from GUI import Gui
from logica.Data import Data
#from Data import Data
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.stats import wasserstein_distance
import re
from logica.LogArista import LogArista
from logica.LogGrafo import LogGrafo
from streamlit_agraph import agraph



class ProbabilidadEP:
    def datosMatrices(self):
        datos = Data().retornarDatosTresNodos()
        return datos
    
    def generarDistribucionProbabilidades(self, tabla, estadoActual, estadoFuturo, num, estados):
        indice = [estados.index(i) for i in estadoActual]
        probabilidadesDistribuidas = []
        for i in estadoFuturo:
            nuevaTabla = self.generarTablaComparativa(tabla[i])
            filtro2 = self.porcentajeDistribucion(nuevaTabla, indice, num)
            probabilidadesDistribuidas.append(filtro2)
        tabla = self.generarTabla(probabilidadesDistribuidas, num)
        tabla[0] = [f"{estadoActual} | {estadoFuturo}"] + tabla[0]
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
        #tabla1 = [fila for fila in tabla if all(i < len(fila[0]) and fila[0][pos] == num[i] for i, pos in enumerate(indice))]
        fila = None  # Valor por defecto
        try:
            tabla1 = [
                fila for fila in tabla if all(
                    i < len(num) and pos < len(fila[0]) and fila[0][pos] == num[i] for i, pos in enumerate(indice)
                )
            ]
        except IndexError as e:
            print(f"IndexError: {e}")
            raise

        nuevosValores = [0, 0]
        for i in tabla1:
            nuevosValores[0] += i[1]
            nuevosValores[1] += i[2]
        

        nuevosValores = [v / len(tabla1) for v in nuevosValores] 
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
    
    def retornarEstados(self):
        datos = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(datos)
        return estados
    
    def retornarDistribucion(self, eActual, eFuturo, valorActual, st):
        matrices = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(matrices)
        datos = self.generarDistribucionProbabilidades(matrices, eActual, eFuturo, valorActual, estados)
        lista = []
        lista.append(str(datos[0][0]))
            
        #lista.append(datos[0])
        for i in range(len(datos[0][1:])):
            lista.append(str(datos[0][1:][i]))
        
        df = pd.DataFrame(datos[1:], columns=lista)
        return df
    
    def retornarValorActual(self, c1):
        datos = self.datosMatrices()
        lista =[]
        if len(c1) == 1:
            lista.append((0,))
            lista.append((1,))
        elif len(c1) == 2:
            lista.append((0,0))
            lista.append((0,1))
            lista.append((1,0))
            lista.append((1,1))
        else:
            for k, v in datos.items():
                for k2, v2 in v.items():
                    lista.append(k2)
                break
        return lista
    
    def retornarEstadosFuturos(self):
        datos = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(datos)
        # agregarle a cada valor de los estados una '
        for i in range(len(estados)):
            estados[i] = estados[i] + "'"

        return estados
            
    def generarParticiones(self, conjunto1, conjunto2):
        particiones = []
               
        # Generar todas las combinaciones posibles de elementos del primer conjunto
        for i in range(len(conjunto1) + 1):
            combos1 = combinations(conjunto1, i)
            # Agregar la partición a la lista de particiones
            for c1 in combos1:
                particion1 = [list(c1), sorted(list(set(conjunto1) - set(c1)) + list(set(conjunto2)))]
                particiones.append(particion1)

        for i in range(len(conjunto2) + 1):
            combos2 = combinations(conjunto2, i)
            # Agregar la partición a la lista de particiones
            for c2 in combos2:
                particion2 = [list(c2), sorted(list(set(conjunto2) - set(c2)) + list(set(conjunto1)))]
                particiones.append(particion2)
        # eliminar si hay particiones vacias
        
        n = len(conjunto1)
        for i, particion in enumerate(particiones):
            particiones[i].append(tuple(j % 2 for j in range(n)))
            
        particiones = [tuple(p) for p in particiones]
        particiones = [p for p in particiones if p[0] and p[1]]
        df = pd.DataFrame(particiones, columns=['Conjunto 1', 'Conjunto 2', 'Estado'])
        return df, particiones
    
    def particiones(self, listaDistribuida, eAcual1, eActual2, eFuturo1, eFuturo2):
        p1 = tuple(listaDistribuida[1][0][i] for i in eAcual1 if i < len(listaDistribuida[1][0]))
        p2 = tuple(listaDistribuida[1][0][i] for i in eActual2 if i < len(listaDistribuida[1][0]))
        listaNueva1 =[]
        listaNueva2 =[]
        i1 ={}
        i2 ={}
        for num, fila in enumerate(listaDistribuida[0][1:], start=1):
            auxNuevaTabla1 = tuple(fila[i-1] for i in eFuturo1)
            auxNuevaTabla2 = tuple(fila[i-1] for i in eFuturo2)
            

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
    
    def retornarMejorParticion(self, c1, c2, estadoActual, nodes, edges,st):
        #df, particiones = self.generarParticiones(c1, c2)
        matrices = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(matrices)
       
        distribucionProbabilidad = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)# Original
        combinaciones = self.generarCombinaciones(c1, c2) # Combinaciones de particiones posibles de la original
        particioness = self.generarProbParticiones(distribucionProbabilidad, combinaciones)
        
        menor = float('inf')
        particion = []
        particionesMenores = {}
        part ={}
        for i in particioness:
            
            particion1 = particioness[i][0][1][1:]
            particion2 = particioness[i][1][1][1:]
            prodTensor = self.producto_tensor(particion1, particion2)
            diferencia = min(self.calcularEMD(distribucionProbabilidad[1][1:], prodTensor))
            part[i] = diferencia
        
        for i in part:
            if part[i] < menor:
                menor = part[i]
           
        for i in part:
            if part[i] == menor:
                particionesMenores[i] = part[i]
        lista_particiones = []
        for particion, probabilidad in particionesMenores.items():
            partes = particion.split('-')
            particion1 = re.findall(r'\((.*?)\)', partes[0].strip())
            particion2 = re.findall(r'\((.*?)\)', partes[1].strip())
            particion1 = [list(p.split()) if p else [""] for p in particion1]
            particion2 = [list(p.split()) if p else [""] for p in particion2]
            lista_particiones.append([particion1, particion2, probabilidad])
        
        for i in range(len(lista_particiones)):
            #lista_particiones[i][0] = [sublist for sublist in lista_particiones[i][0] if sublist]
            #lista_particiones[i][1] = [sublist for sublist in lista_particiones[i][1] if sublist]
            
            if [] in lista_particiones[i][0]:
                lista_particiones[i][0].remove([])
                lista_particiones[i][0][0].append("")
                if len(lista_particiones[i][0]) > 1:
                    a = lista_particiones[i][0][1]
                    print(a)
                

            print(lista_particiones[i][0])
            a = lista_particiones[i][0][0]
            #print(a)
            # eliminar aristas de la particion
            for arista in edges:
                if arista.source in lista_particiones[i][0][0] :
                    arista.dashes = True
                    arista.color = 'rgba(254, 20, 56, 0.5)'
                
         
        
               
        agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=Gui(False))
        
                
        return particion, diferencia, nodes, edges
    
    
    
    def calcularEMD(self, p1, p2):
        # Convertir las listas a arreglos de numpy si es necesario
        p1 = np.array(p1)
        p2 = np.array(p2)
        
        # Calcular la diferencia de probabilidad utilizando EMD
        diferencias = [wasserstein_distance(p1, p2_row) for p2_row in p2]
        
        return diferencias



    

    def productoTensor(self,vector_a, vector_b, i=0,vector_resultado = None):
    
        if vector_resultado is None:
            vector_resultado = []

        if i == len(vector_a):
            return vector_resultado
        else:
            aux2 = []
            for j in range(len(vector_b)):
                aux2.append(vector_a[i] * vector_b[j]) 
            self.productoTensor(vector_a, aux2, i + 1, vector_resultado)
            vector_resultado.append(aux2)
            return vector_resultado[0]
        
    def producto_tensor(self, p1, p2):
        """
        Calcula el producto tensor de dos particiones de probabilidades.
        
        Argumentos:
        p1 -- Lista o arreglo de numpy con la primera partición de probabilidades.
        p2 -- Lista o arreglo de numpy con la segunda partición de probabilidades.
        
        Retorna:
        Un arreglo de numpy con el producto tensor de las particiones de probabilidades.
        """
        # Convertir las listas a arreglos de numpy si es necesario
        p1 = np.array(p1)
        p2 = np.array(p2)
        
        # Calcular el producto tensor
        resultado = np.outer(p1, p2)
        
        return resultado
        
    
    
[['(', ')', '(', '1', ')'], ['(', '1', '2', ')', '(', '2', ')'], 0.1875]
[['()','(1)'],['(1, 2)','(2)'],0.1875]

[[' ', ' 1 '], [' 1 2 ', ' 2 '], 0.1875]
[[[''], ['1']], [['1','2'], ['2']], 0.1875]
        
        

a = ProbabilidadEP()
#print(a.retornarDistribucion(['1','2','3'], ['1','2','3'], (1, 0, 0)))


[(['1', '2', '2', '3', '3'], ['1'], [(0, 0, 0, 0, 0), (0, 0, 0, 0, 1), (0, 0, 0, 1, 0), (0, 0, 0, 1, 1), (0, 0, 1, 0, 0),
(0, 0, 1, 0, 1), (0, 0, 1, 1, 0), (0, 0, 1, 1, 1), (0, 1, 0, 0, 0), (0, 1, 0, 0, 1), (0, 1, 0, 1, 0), (0, 1, 0, 1, 1), 
(0, 1, 1, 0, 0), (0, 1, 1, 0, 1), (0, 1, 1, 1, 0), (0, 1, 1, 1, 1), (1, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 1, 0), 
(1, 0, 0, 1, 1), (1, 0, 1, 0, 0), (1, 0, 1, 0, 1), (1, 0, 1, 1, 0), (1, 0, 1, 1, 1), (1, 1, 0, 0, 0), (1, 1, 0, 0, 1), 
(1, 1, 0, 1, 0), (1, 1, 0, 1, 1), (1, 1, 1, 0, 0), (1, 1, 1, 0, 1), (1, 1, 1, 1, 0), (1, 1, 1, 1, 1)]), 
[(1, 0, 0), 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 
 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 
 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875, 0.046875]]   
