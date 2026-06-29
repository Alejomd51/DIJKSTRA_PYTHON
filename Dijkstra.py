import heapq

def dijkstra(grafo, origen):
    """
    Calcula la distancia mínima desde el nodo origen
    hacia todos los demás nodos usando Dijkstra.
    """

    # Inicializar distancias
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0

    # Diccionario para reconstruir la ruta
    anteriores = {nodo: None for nodo in grafo}

    # Cola de prioridad
    cola = [(0, origen)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si ya existe una distancia mejor, ignorar
        if distancia_actual > distancias[nodo_actual]:
            continue

        # Recorrer vecinos
        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, anteriores


def obtener_ruta(anteriores, origen, destino):
    """
    Reconstruye la ruta desde el origen hasta el destino.
    """

    ruta = []
    actual = destino

    while actual is not None:
        ruta.append(actual)
        actual = anteriores[actual]

    ruta.reverse()

    if ruta[0] == origen:
        return ruta
    else:
        return []


# ===============================
# EJEMPLO DE USO
# ===============================

grafo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('D', 6), ('E', 3)]
}

origen = 'A'
destino = 'F'

distancias, anteriores = dijkstra(grafo, origen)
ruta = obtener_ruta(anteriores, origen, destino)

print("Distancia mínima:", distancias[destino])
print("Ruta:", " -> ".join(ruta))