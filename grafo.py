class Grafo:

    def __init__(self):
        # Diccionario que almacena el grafo
        self.grafo = {}
        
    # NODOS


    def agregar_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = {}

    def eliminar_nodo(self, nodo):
        if nodo in self.grafo:

            # Elimina las conexiones hacia ese nodo
            for vecino in list(self.grafo[nodo]):
                del self.grafo[vecino][nodo]

            # Elimina el nodo
            del self.grafo[nodo]

    # ARISTAS

    def agregar_arista(self, origen, destino, peso):

        if origen not in self.grafo:
            self.agregar_nodo(origen)

        if destino not in self.grafo:
            self.agregar_nodo(destino)

        # Grafo no dirigido
        self.grafo[origen][destino] = peso
        self.grafo[destino][origen] = peso

    def eliminar_arista(self, origen, destino):

        if origen in self.grafo and destino in self.grafo[origen]:
            del self.grafo[origen][destino]

        if destino in self.grafo and origen in self.grafo[destino]:
            del self.grafo[destino][origen]

    # CONSULTAS

    def obtener_nodos(self):
        return list(self.grafo.keys())

    def obtener_vecinos(self, nodo):
        if nodo in self.grafo:
            return self.grafo[nodo]
        return {}

    def obtener_grafo(self):
        return self.grafo

    # MOSTRAR

    def mostrar_grafo(self):

        if not self.grafo:
            print("El grafo está vacío.")
            return

        print("\n----- GRAFO -----")

        for nodo, vecinos in self.grafo.items():
            print(f"{nodo} -> {vecinos}")