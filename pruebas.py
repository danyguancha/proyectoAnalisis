def producto_tensor_vector_recursivo(vector_a, vector_b, i=0,vector_resultado = None):
    
    if vector_resultado is None:
        vector_resultado = []

    if i == len(vector_a):
        return vector_resultado
    else:
        aux2 = []
        for j in range(len(vector_b)):
            aux2.append(vector_a[i] * vector_b[j]) 
        producto_tensor_vector_recursivo(vector_a, aux2, i + 1, vector_resultado)
        vector_resultado.append(aux2)
        return vector_resultado[0]

        
    

# Ejemplo de uso
particion1 = [0.5, 0.5]
particion2 = [0.5, 0.0]

resultado = producto_tensor_vector_recursivo(particion1, particion2)

print(resultado)
