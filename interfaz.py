import customtkinter as ctk
from tkinter import messagebox

from grafo import Grafo
from dijkstra import Dijkstra


class Interfaz:

    def __init__(self):

        self.grafo = Grafo()

        # ======== Datos de prueba ========
        self.grafo.agregar_arista("A", "B", 4)
        self.grafo.agregar_arista("A", "C", 2)
        self.grafo.agregar_arista("B", "C", 1)
        self.grafo.agregar_arista("B", "D", 5)
        self.grafo.agregar_arista("C", "D", 8)
        self.grafo.agregar_arista("C", "E", 10)
        self.grafo.agregar_arista("D", "E", 2)
        self.grafo.agregar_arista("D", "F", 6)
        self.grafo.agregar_arista("E", "F", 3)

        # ======== Ventana ========

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()
        self.ventana.title("Algoritmo de Dijkstra")
        self.ventana.geometry("500x450")

        titulo = ctk.CTkLabel(
            self.ventana,
            text="Ruta más corta - Dijkstra",
            font=("Arial", 22, "bold")
        )

        titulo.pack(pady=20)

        ctk.CTkLabel(self.ventana, text="Origen").pack()

        self.origen = ctk.CTkEntry(self.ventana)
        self.origen.pack(pady=5)

        ctk.CTkLabel(self.ventana, text="Destino").pack()

        self.destino = ctk.CTkEntry(self.ventana)
        self.destino.pack(pady=5)

        boton = ctk.CTkButton(
            self.ventana,
            text="Calcular Ruta",
            command=self.calcular
        )

        boton.pack(pady=20)

        self.resultado = ctk.CTkTextbox(
            self.ventana,
            width=420,
            height=150
        )

        self.resultado.pack()

        self.ventana.mainloop()

    def calcular(self):

        origen = self.origen.get().strip()
        destino = self.destino.get().strip()

        ruta, distancia = Dijkstra.calcular(
            self.grafo,
            origen,
            destino
        )

        self.resultado.delete("1.0", "end")

        if ruta is None:

            messagebox.showerror(
                "Error",
                "No existe una ruta."
            )

            return

        self.resultado.insert(
            "end",
            f"Ruta encontrada:\n{' -> '.join(ruta)}\n\n"
        )

        self.resultado.insert(
            "end",
            f"Distancia total: {distancia}"
        )


if __name__ == "__main__":
    Interfaz()