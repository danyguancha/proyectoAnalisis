from logica.LogGrafo import LogGrafo
from lector.LectorArchivo import LectorArchivo
from logica.MarginalizarEP import MarginalizarEP

class ProbabilidadEP:

    def datosMatrices(self):
        dato = LectorArchivo().cargarArchivo("Data/probabilidades/tresNodos.json")
        return dato
    
    def datos(self, nodes, edges):
        conjunto1, conjunto2, aristas = LogGrafo().obtenerConjuntosGrafoBipartito(nodes, edges)
        return conjunto1, conjunto2

    def retornarProbabilidad(self, nodes, edges,estadoActual, marginalizar=None):
        matrices = self.datosMatrices()
        #est = MarginalizarEP().marginalizar(nodes, edges, ['0'], marginalizar)
        est = self.probabilidadEstadoFuturo(matrices, estadoActual)
        return est
    
    def retornarEstadosActuales(self):
        matrices = self.datosMatrices()
        lista = ['']
        listaEstados = []
        for k, v in matrices.items():
            listaEstados.append(k)
            for key, value in v.items():
                if key not in lista:
                    lista.append(key)
        lista.append('0')
        lista.append('1')
        lista.append('00')
        lista.append('01')
        lista.append('10')
        lista.append('11')
        
        return listaEstados, lista
    def retornarEstadosFuturos(self):
        matrices = self.datosMatrices()
        lista = []
        mayor = 0
        # Asignar las claves de matrices a una lista
        claves = list(matrices.keys())
        for i in claves:
            if int(i) > mayor:
                mayor = int(i)
        hasta = mayor + len(claves) +1
        for i in range(mayor+1, hasta):
            lista.append(i)
        return lista
    
    def probabilidadEstadoFuturo(self, matrices, estadoActual):
        probabilidad ={}
        s =''
        for k, v in matrices.items():
            for key, value in v.items():
                if key == estadoActual:
                    s += str(value[1])
                probabilidad[key]=0
        probabilidad[s]=1
        return probabilidad
                    




    





        




