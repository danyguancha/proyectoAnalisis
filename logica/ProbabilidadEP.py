# Description: Clase que se encarga de generar la distribución de probabilidad de un estado futuro dado un estado actual
from logica.Data import Data
#from Data import Data
import pandas as pd
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
        tabla[0] = estadoActual, estadoFuturo ,tabla[0]
        tabla[1]= [num]+tabla[1]
        return tabla
    
    def generarTabla(self, distribucion, num, i=0, numBinario ='', nuevoValor=1):
        if i == len(distribucion):
            numBinario = '0'*(len(distribucion)-len(numBinario))+numBinario
            nuevoDato = tuple(int(i) for i in numBinario)
            return [[nuevoDato], [nuevoValor]]
        else:
            tabla = self.generarTabla(distribucion, num, i+1, numBinario+'0', nuevoValor*distribucion[i][1][2])
            tabla2 = self.generarTabla(distribucion, num, i+1, numBinario+'1', nuevoValor*distribucion[i][1][1])
            return [tabla[0]+tabla2[0], tabla[1]+tabla2[1]]
        
    def porcentajeDistribucion(self, tabla, indice, num):
        tablaNueva = [tabla[0]]
        #tabla1 = [i for i in tabla if all(j < len(i[0]) and i[0][pos] == num[j] for j, pos in enumerate(indice))]
        tabla1 = [fila for fila in tabla if all(i < len(fila[0]) and fila[0][pos] == num[i] for i, pos in enumerate(indice))]

        nuevosValores = [0,0]
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
    
    def generarEstadoTransicion(self, matrices):
        estados = list(matrices.keys())
        transiciones ={}
        estadoActual = [0] * len(estados)

        def aux (indice):
            if indice == len(estados):
                estadoAc = tuple(estadoActual)
                estadoFuturo = tuple(matrices[estado][estadoAc] for estado in estados)
                transiciones[estadoAc] = estadoFuturo
            else:
                estadoActual[indice] = 0
                aux(indice+1)
                estadoActual[indice] = 1
                aux(indice+1)
        aux(0)
        return transiciones, estados
    
    def retornarEstados(self):
        datos = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(datos)
        return estados
    
    def retornarDistribucion(self, eActual, eFuturo, valorActual):
        matrices = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(matrices)
        datos = self.generarDistribucionProbabilidades(matrices, eActual, eFuturo, valorActual, estados)
        return datos
    
    def retornarValorActual(self):
        datos = self.datosMatrices()
        lista =[]
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
            

    def mostrarDatos (self):
        datos = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(datos) # estados = ["1", "2", "3"]
        # self.generarDistribucionProbabilidades(matrices, eActual, eFuturo, valorActual, estados)
        distribucionProbabilidades = self.generarDistribucionProbabilidades(datos, ["1", "2", "3"], ["1","2","3"], (1, 0, 0), estados)
        print(distribucionProbabilidades)

a = ProbabilidadEP()
print(a.retornarDistribucion(['1','2','3'], ['1','2','3'], (1, 0, 0)))


        