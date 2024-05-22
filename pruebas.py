import numpy as np

def calcularEMD(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    
    cost_matrix = np.abs(np.subtract.outer(p1, p2))
    return np.sum(np.min(cost_matrix, axis=1) * p1)

def producto_tensor(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.outer(p1, p2)

p1 = [0, 0, 0, 0, 1, 0, 0, 0]
p2 = [0.25, 0.25]

print(f"Producto tensor de {p1} y {p2}:")
print(producto_tensor(p1, p2))
print(f"EMD entre {p1} y {p2}: {calcularEMD(p1, p2)}")