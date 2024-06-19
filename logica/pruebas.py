from logica.ProbabilidadEP import ProbabilidadEP
from logica.Estrategia2 import Estrategia2
from logica.Estrategia3 import Estrategia3
import pandas as pd

class PruebasEstrategias:
    def calcularPrueba(self,c1, c2, estadoActual, edges):
        e1 = ProbabilidadEP()
        e2 = Estrategia2()
        e3 = Estrategia3()
        #particionE1, diferenciaE1, tiempoE1, listaE1 = e1.retornarMejorParticionE1(c1, c2, estadoActual)
        particionE2, diferenciaE2, tiempoE2, listaE2, e = e2.estrategia2(c1, c2, estadoActual, edges)
        #particionE3, diferenciaE3, tiempoE3, listaE3 = e3.retornarMejorParticion(c1, c2, estadoActual)

        # Crear un DataFrame de pandas para mostrar los resultados
        """data = {
            'Estrategia': ['Estrategia 1', 'Estrategia 2', 'Estrategia 3'],
            'Partición': [particionE1, particionE2, particionE3],
            'Diferencia': [diferenciaE1, diferenciaE2, diferenciaE3],
            'Tiempo': [tiempoE1, tiempoE2, tiempoE3]
        }"""
        data = {
            'Estrategia': ['Estrategia 2'],
            'Partición': [particionE2],
            'Diferencia': [diferenciaE2],
            'Tiempo': [tiempoE2]
        }
        
        df = pd.DataFrame(data)
        return df
    
