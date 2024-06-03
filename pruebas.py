def retornarMejorParticion(self, c1, c2, estadoActual):
        matrices = self.datosMatrices()
        resultado, estados = self.generarEstadoTransicion(matrices)
        distribucionProbabilidadOriginal = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
        lista =[]
        def busqueda_voraz(c1, c2, estadoActual):
            mejor_particion = []
            menor_diferencia = float('inf')
            listaParticionesEvaluadas = []
            for i in range(len(c1) + 1):
                c1_izq = c1[:i]
                c1_der = c1[i:]
                c2_izq = []
                c2_der = list(c2)

                for j in range(len(c2)):
                    c2_izq.append(c2_der.pop(0))
                
                    inicio = time.time()
                    distribucion_izq = self.generarDistribucionProbabilidades(matrices, tuple(c1_izq), tuple(c2_izq), estadoActual, estados)
                    distribucion_der = self.generarDistribucionProbabilidades(matrices, tuple(c1_der), tuple(c2_der), estadoActual, estados)
                    print(distribucion_izq)
                    print(distribucion_der)
                    p1 = distribucion_izq[1][1:]
                    p2 = distribucion_der[1][1:]
                    prodTensor = self.producto_tensor(p1, p2)
                    diferencia = self.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)
                    fin = time.time()
                    tiempoEjecucion = fin - inicio
                    aux = []
                    if c2_der == [] and c1_der == []:
                        continue
                    elif diferencia < menor_diferencia:
                        menor_diferencia = diferencia
                        mejor_particion = [(tuple(c2_izq),(tuple(c1_izq))),(tuple(c2_der), tuple(c1_der))]
                    aux = [(tuple(c2_izq),(tuple(c1_izq))),(tuple(c2_der), tuple(c1_der)),str(diferencia), str(tiempoEjecucion)]
                    listaParticionesEvaluadas.append(aux)
                
            return mejor_particion, menor_diferencia, tiempoEjecucion, listaParticionesEvaluadas

        particion, diferencia, tiempo, lista = busqueda_voraz(list(c1), list(c2), estadoActual)
        return particion, diferencia,tiempo, lista

"""def retornarMejorParticion(self, c1, c2, estadoActual, nodes, edges,st):
        tabla = {}
        matrices = self.datosMatrices()

        def helper(c1, c2, estadoActual):
            # Check if the result is already computed
            if estadoActual in tabla:
                return tabla[estadoActual]
            resultado, estados = self.generarEstadoTransicion(matrices)
            distribucionProbabilidadOriginal = self.generarDistribucionProbabilidades(matrices, c1, c2, estadoActual, estados)
            combinaciones = self.generarCombinaciones(distribucionProbabilidadOriginal[0][1], distribucionProbabilidadOriginal[1][0])

            particioness = self.generarProbParticiones(distribucionProbabilidadOriginal, combinaciones)
            probabilidades = {}
            for i in particioness:
                aux = self.convertir_a_listas(i)
                for j in aux:
                    distribucion1 = self.generarDistribucionProbabilidades(matrices, j[0][0], j[0][1], estadoActual, estados)
                    distribucion2 = self.generarDistribucionProbabilidades(matrices, j[1][0], j[1][1], estadoActual, estados)
                probabilidades[i]= distribucion1 + distribucion2
            menor = float('inf')
            mejor_particion = None
            aux={}
            for i in probabilidades:
                p1 = probabilidades[i][1][1:]
                p2 = probabilidades[i][3][1:]
                prodTensor = self.producto_tensor(p1, p2)
                diferencia = self.calcularEMD(distribucionProbabilidadOriginal[1][1:], prodTensor)
                aux2 = self.convertir_a_listas(i)
                for j in aux2:
                    if diferencia < menor and (j[0][0] != c1 and j[0][1]!=c2):
                        menor = diferencia
                        mejor_particion = i
                print(i, ': ', diferencia)
            tabla[estadoActual] = (menor, mejor_particion)
            return tabla[estadoActual]
        
        return helper(c1, c2, estadoActual)"""