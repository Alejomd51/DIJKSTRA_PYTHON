import math
import customtkinter as ctk
from tkinter import messagebox, Canvas

from grafo import Grafo
from dijkstra import Dijkstra


class Interfaz:

    def __init__(self):

        self.grafo = Grafo()
        self.ruta_actual = []

        # ======== Ventana ========

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()
        self.ventana.title("Algoritmo de Dijkstra")
        self.ventana.geometry("1000x650")
        self.ventana.minsize(900, 600)

        contenedor = ctk.CTkFrame(self.ventana, fg_color="transparent")
        contenedor.pack(fill="both", expand=True, padx=15, pady=15)

        panel_izq = ctk.CTkFrame(contenedor, width=300)
        panel_izq.pack(side="left", fill="y", padx=(0, 10))

        panel_der = ctk.CTkFrame(contenedor)
        panel_der.pack(side="left", fill="both", expand=True)

        # ======== Panel izquierdo: controles ========

        ctk.CTkLabel(
            panel_izq,
            text="Dijkstra",
            font=("Arial", 22, "bold")
        ).pack(pady=(15, 20))

        # ---- Agregar nodo ----

        ctk.CTkLabel(panel_izq, text="Agregar Nodo", font=("Arial", 14, "bold")).pack(pady=(5, 5))

        self.entry_nodo = ctk.CTkEntry(panel_izq, placeholder_text="Nombre del nodo")
        self.entry_nodo.pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(
            panel_izq,
            text="Agregar Nodo",
            command=self.agregar_nodo
        ).pack(pady=5, padx=15, fill="x")

        # ---- Agregar arista ----

        ctk.CTkLabel(panel_izq, text="Agregar Arista", font=("Arial", 14, "bold")).pack(pady=(20, 5))

        self.entry_origen_a = ctk.CTkEntry(panel_izq, placeholder_text="Nodo origen")
        self.entry_origen_a.pack(pady=3, padx=15, fill="x")

        self.entry_destino_a = ctk.CTkEntry(panel_izq, placeholder_text="Nodo destino")
        self.entry_destino_a.pack(pady=3, padx=15, fill="x")

        self.entry_peso = ctk.CTkEntry(panel_izq, placeholder_text="Peso")
        self.entry_peso.pack(pady=3, padx=15, fill="x")

        ctk.CTkButton(
            panel_izq,
            text="Agregar Arista",
            command=self.agregar_arista
        ).pack(pady=5, padx=15, fill="x")

        # ---- Calcular ruta ----

        ctk.CTkLabel(panel_izq, text="Calcular Ruta", font=("Arial", 14, "bold")).pack(pady=(20, 5))

        self.entry_origen = ctk.CTkEntry(panel_izq, placeholder_text="Origen")
        self.entry_origen.pack(pady=3, padx=15, fill="x")

        self.entry_destino = ctk.CTkEntry(panel_izq, placeholder_text="Destino")
        self.entry_destino.pack(pady=3, padx=15, fill="x")

        ctk.CTkButton(
            panel_izq,
            text="Calcular Ruta",
            command=self.calcular
        ).pack(pady=5, padx=15, fill="x")

        # ---- Limpiar ----

        ctk.CTkButton(
            panel_izq,
            text="Limpiar Grafo",
            fg_color="#8B2020",
            hover_color="#6B1515",
            command=self.limpiar_grafo
        ).pack(pady=(20, 5), padx=15, fill="x")

        # ---- Resultado ----

        self.resultado = ctk.CTkTextbox(panel_izq, height=120)
        self.resultado.pack(pady=(15, 10), padx=15, fill="x")

        # ======== Panel derecho: grafo ========

        ctk.CTkLabel(
            panel_der,
            text="Visualización del Grafo",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))

        self.canvas = Canvas(panel_der, bg="#242424", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas.bind("<Configure>", lambda e: self.dibujar_grafo())

        self.ventana.mainloop()

    # ======== Acciones ========

    def agregar_nodo(self):

        nodo = self.entry_nodo.get().strip()

        if not nodo:
            messagebox.showwarning("Aviso", "Escribe un nombre de nodo.")
            return

        self.grafo.agregar_nodo(nodo)
        self.entry_nodo.delete(0, "end")
        self.dibujar_grafo()

    def agregar_arista(self):

        origen = self.entry_origen_a.get().strip()
        destino = self.entry_destino_a.get().strip()
        peso_texto = self.entry_peso.get().strip()

        if not origen or not destino or not peso_texto:
            messagebox.showwarning("Aviso", "Completa origen, destino y peso.")
            return

        if origen == destino:
            messagebox.showerror("Error", "El origen y destino no pueden ser iguales.")
            return

        try:
            peso = float(peso_texto)
            if peso == int(peso):
                peso = int(peso)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número.")
            return

        self.grafo.agregar_arista(origen, destino, peso)

        self.entry_origen_a.delete(0, "end")
        self.entry_destino_a.delete(0, "end")
        self.entry_peso.delete(0, "end")

        self.dibujar_grafo()

    def limpiar_grafo(self):
        self.grafo = Grafo()
        self.ruta_actual = []
        self.resultado.delete("1.0", "end")
        self.dibujar_grafo()

    def calcular(self):

        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()

        if not origen or not destino:
            messagebox.showwarning("Aviso", "Completa origen y destino.")
            return

        ruta, distancia = Dijkstra.calcular(self.grafo, origen, destino)

        self.resultado.delete("1.0", "end")

        if ruta is None:
            messagebox.showerror("Error", "No existe una ruta.")
            self.ruta_actual = []
            self.dibujar_grafo()
            return

        self.resultado.insert("end", f"Ruta encontrada:\n{' -> '.join(ruta)}\n\n")
        self.resultado.insert("end", f"Distancia total: {distancia}")

        self.ruta_actual = ruta
        self.dibujar_grafo()

    # ======== Dibujo del grafo ========

    def dibujar_grafo(self):

        self.canvas.delete("all")

        nodos = self.grafo.obtener_nodos()

        if not nodos:
            return

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho < 10 or alto < 10:
            return

        cx, cy = ancho / 2, alto / 2
        radio = min(ancho, alto) / 2 - 60
        n = len(nodos)

        # Posiciones en círculo
        posiciones = {}

        for i, nodo in enumerate(nodos):
            angulo = 2 * math.pi * i / n
            x = cx + radio * math.cos(angulo)
            y = cy + radio * math.sin(angulo)
            posiciones[nodo] = (x, y)

        # Pares de nodos que forman la ruta resaltada
        pares_ruta = set()

        if self.ruta_actual:
            for i in range(len(self.ruta_actual) - 1):
                par = frozenset((self.ruta_actual[i], self.ruta_actual[i + 1]))
                pares_ruta.add(par)

        # Aristas
        for origen, destino, peso in self.grafo.obtener_aristas():

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]

            es_ruta = frozenset((origen, destino)) in pares_ruta
            color = "#F5A623" if es_ruta else "#5A5A5A"
            grosor = 3 if es_ruta else 2

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor)

            mx, my = (x1 + x2) / 2, (y1 + y2) / 2

            self.canvas.create_text(
                mx, my,
                text=str(peso),
                fill="#DDDDDD",
                font=("Arial", 10, "bold")
            )

        # Nodos
        r = 22

        for nodo in nodos:

            x, y = posiciones[nodo]
            es_ruta = nodo in self.ruta_actual
            color = "#F5A623" if es_ruta else "#1F6AA5"

            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline="white", width=2
            )

            self.canvas.create_text(
                x, y,
                text=nodo,
                fill="white",
                font=("Arial", 12, "bold")
            )


if __name__ == "__main__":
    Interfaz()