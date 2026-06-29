import heapq

class Dijkstra:

    @staticmethod
    def calcular(grafo, origen, destino):
        """
        grafo: objeto de la clase Grafo
        origen: nodo inicial
        destino: nodo final
        """

        datos = grafo.obtener_grafo()

        # Verificar que existan los nodos
        if origen not in datos or destino not in datos:
            return None, None

        # Inicializar distancias
        distancias = {
            nodo: float("inf")
            for nodo in datos
        }

        distancias[origen] = 0

        # Nodo anterior para reconstruir la ruta
        anteriores = {
            nodo: None
            for nodo in datos
        }

        # Cola de prioridad
        cola = [(0, origen)]

        while cola:

            distancia_actual, nodo_actual = heapq.heappop(cola)

            # Ignorar si existe una mejor distancia
            if distancia_actual > distancias[nodo_actual]:
                continue

            # Recorrer vecinos
            for vecino, peso in datos[nodo_actual].items():

                nueva_distancia = distancia_actual + peso

                if nueva_distancia < distancias[vecino]:

                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

                    heapq.heappush(
                        cola,
                        (nueva_distancia, vecino)
                    )

        # Reconstruir la ruta
        ruta = []

        actual = destino

        while actual is not None:
            ruta.append(actual)
            actual = anteriores[actual]

        ruta.reverse()

        if not ruta or ruta[0] != origen:
            return None, None

        return ruta, distancias[destino]