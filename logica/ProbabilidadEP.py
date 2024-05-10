from logica.LogGrafo import LogGrafo
from lector.LectorArchivo import LectorArchivo

class ProbabilidadEP:

    def datosMatrices(self):
        dato = LectorArchivo().cargarArchivo("Data/probabilidades/tresNodos.json")
        return dato
    
    def datos(self, nodes, edges):
        conjunto1, conjunto2, aristas = LogGrafo().obtenerConjuntosGrafoBipartito(nodes, edges)
        return conjunto1, conjunto2

    def retornarProbabilidad(self, nodes, edges, estadoActual):
        matrices = self.datosMatrices()
        conjunto1, conjunto2 = self.datos(nodes, edges)
        
        #ordenar el conjunto1
        conjunto1 = sorted(conjunto1)
        return self.probabilidadEstadoFuturo(matrices, estadoActual)
    
    def retornarEstadosActuales(self):
        matrices = self.datosMatrices()
        lista = []
        for k, v in matrices.items():
            for key, value in v.items():
                if key not in lista:
                    lista.append(key)
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
                    
        
             
        
        



    





        




