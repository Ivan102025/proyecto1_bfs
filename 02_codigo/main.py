"""
main.py - Explorador visual con Búsqueda en Amplitud (BFS) - Proyecto 1

Interfaz gráfica en Tkinter (sin dependencias externas) que permite:
- elegir uno de los mapas de prueba (principal, sencillo, estrés) o cargar
  un mapa .json guardado previamente,
- ejecutar BFS en modo automático o paso a paso,
- iniciar, pausar, avanzar, reiniciar y cambiar la velocidad,
- ver en todo momento: obstáculos, celdas libres, inicio, meta, nodo
  actual, frontera abierta, estados visitados y camino final, con leyenda,
- consultar la frontera en orden FIFO (truncada si es muy grande),
- consultar al finalizar las métricas exigidas por la rúbrica.
"""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from bfs import bfs
from maze import (
    generar_mapa, generar_mapa_sencillo, generar_mapa_estres,
    guardar_mapa, cargar_mapa, construir_semilla,
)

# ----- Semilla del equipo: matrículas de ambos integrantes -----
MATRICULA_1 = "20241110"  # IVÁN
MATRICULA_2 = "20241018"  # ISAÍ PASCUAL CRUZ

CARPETA_MAPAS = Path(__file__).resolve().parent.parent / "03_mapas"

COLORES = {
    "obstaculo": "#201F1F",
    "libre": "#fefefe",
    "inicio": "#05fb11",
    "meta": "#ff0404",
    "actual": "#fb8c00",
    "frontera": "#fff177",
    "visitado": "#1e94f5",
    "camino": "#8e24aa",
    "rejilla": "#d9d9d9",
}

MAX_FRONTERA_MOSTRADA = 12  # elementos que se listan antes de resumir el resto


class ExploradorBFS(tk.Tk):
    def __init__(self):
        """Inicializa la ventana, el estado de la búsqueda y la interfaz."""
        super().__init__()
        self.title("Explorador visual con Búsqueda en Amplitud (BFS)")
        self.geometry("1150x760")
        self.minsize(950, 650)

        self.mapa_actual = None
        self.resultado = None
        self.pasos = []
        self.indice_paso = -1
        self.reproduciendo = False
        self.velocidad_ms = tk.IntVar(value=120)

        self._construir_layout()
        self._cargar_mapa_por_nombre("Mapa principal")

    # ---------------------------------------------------------------
    # Construcción de la interfaz
    # ---------------------------------------------------------------
    def _construir_layout(self):
        """Arma el lienzo del mapa, la barra de controles y el panel derecho."""
        contenedor = tk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=0, minsize=320)
        contenedor.rowconfigure(0, weight=1)

        panel_izquierdo = tk.Frame(contenedor)
        panel_izquierdo.grid(row=0, column=0, sticky="nsew")

        panel_derecho = tk.Frame(contenedor, width=320)
        panel_derecho.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        panel_derecho.grid_propagate(False)

        self.canvas = tk.Canvas(panel_izquierdo, bg="white", highlightthickness=1,
                                 highlightbackground="#999999")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._dibujar())

        barra = tk.Frame(panel_izquierdo)
        barra.pack(fill="x", pady=(8, 0))

        self.combo_mapa = tk.StringVar(value="Mapa principal")
        opciones = ["Mapa principal", "Mapa sencillo", "Mapa de estrés", "Cargar archivo..."]
        menu_mapa = tk.OptionMenu(barra, self.combo_mapa, *opciones,
                                   command=self._cargar_mapa_por_nombre)
        menu_mapa.config(width=16)
        menu_mapa.pack(side="left", padx=(0, 8))

        tk.Button(barra, text="▶ Iniciar", width=10, command=self.iniciar).pack(side="left", padx=2)
        tk.Button(barra, text="⏸ Pausar", width=10, command=self.pausar).pack(side="left", padx=2)
        tk.Button(barra, text="⏭ Avanzar", width=10, command=self.avanzar_paso).pack(side="left", padx=2)
        tk.Button(barra, text="⟲ Reiniciar", width=10, command=self.reiniciar).pack(side="left", padx=2)

        tk.Label(barra, text="Velocidad:").pack(side="left", padx=(15, 2))
        tk.Scale(barra, from_=400, to=10, orient="horizontal", showvalue=False,
                 variable=self.velocidad_ms, length=140).pack(side="left")

        self._construir_leyenda(panel_derecho)
        self._construir_estado(panel_derecho)
        self._construir_metricas(panel_derecho)

    def _construir_leyenda(self, padre):
        """Muestra una etiqueta de color por cada estado del mapa."""
        marco = tk.LabelFrame(padre, text="Leyenda", padx=8, pady=8)
        marco.pack(fill="x", pady=(0, 10))
        elementos = [
            ("obstaculo", "Obstáculo"),
            ("libre", "Celda libre"),
            ("inicio", "Inicio"),
            ("meta", "Meta"),
            ("actual", "Nodo actual"),
            ("frontera", "Frontera abierta"),
            ("visitado", "Estados visitados"),
            ("camino", "Camino final"),
        ]
        for clave, etiqueta in elementos:
            fila = tk.Frame(marco)
            fila.pack(fill="x", pady=1)
            tk.Canvas(fila, width=16, height=16, bg=COLORES[clave],
                      highlightthickness=1, highlightbackground="#666666")\
                .pack(side="left", padx=(0, 6))
            tk.Label(fila, text=etiqueta, anchor="w").pack(side="left")

    def _construir_estado(self, padre):
        """Crea las etiquetas de frontera FIFO y número de paso."""
        marco = tk.LabelFrame(padre, text="Frontera (orden FIFO)", padx=8, pady=8)
        marco.pack(fill="x", pady=(0, 10))
        self.texto_frontera = tk.Label(marco, text="—", justify="left", anchor="w",
                                        wraplength=280)
        self.texto_frontera.pack(fill="x")
        self.texto_paso = tk.Label(marco, text="Paso: 0 / 0", anchor="w")
        self.texto_paso.pack(fill="x", pady=(6, 0))

    def _construir_metricas(self, padre):
        """Crea el panel donde se presentan las métricas al finalizar."""
        marco = tk.LabelFrame(padre, text="Métricas al finalizar", padx=8, pady=8)
        marco.pack(fill="both", expand=True)
        self.texto_metricas = tk.Label(marco, text="Ejecute la búsqueda para ver métricas.",
                                        justify="left", anchor="nw", wraplength=280)
        self.texto_metricas.pack(fill="both", expand=True)

    # ---------------------------------------------------------------
    # Carga de mapas
    # ---------------------------------------------------------------
    def _cargar_mapa_por_nombre(self, nombre):
        """Carga el mapa elegido en el menú, o abre un JSON personalizado."""
        self.combo_mapa.set(nombre)
        if nombre == "Mapa principal":
            semilla = construir_semilla(MATRICULA_1, MATRICULA_2)
            ruta = CARPETA_MAPAS / "mapa_principal.json"
            self.mapa_actual = self._cargar_o_generar(
                ruta, lambda: generar_mapa(MATRICULA_1, MATRICULA_2), semilla)
        elif nombre == "Mapa sencillo":
            ruta = CARPETA_MAPAS / "mapa_sencillo.json"
            self.mapa_actual = self._cargar_o_generar(ruta, generar_mapa_sencillo, None)
        elif nombre == "Mapa de estrés":
            semilla = construir_semilla(MATRICULA_1, MATRICULA_2)
            ruta = CARPETA_MAPAS / "mapa_estres.json"
            self.mapa_actual = self._cargar_o_generar(
                ruta, lambda: generar_mapa_estres(MATRICULA_1, MATRICULA_2), semilla)
        elif nombre == "Cargar archivo...":
            ruta = filedialog.askopenfilename(filetypes=[("Mapas JSON", "*.json")])
            if not ruta:
                return
            self.mapa_actual = cargar_mapa(ruta)
        self.reiniciar()

    def _cargar_o_generar(self, ruta: Path, generador, semilla_esperada):
        """Reutiliza el JSON si existe y su semilla coincide; si no, genera y guarda uno nuevo."""
        if ruta.exists():
            mapa = cargar_mapa(str(ruta))
            if semilla_esperada is None or mapa.get("semilla") == semilla_esperada:
                return mapa
        mapa = generador()
        guardar_mapa(mapa, str(ruta))
        return mapa

    # ---------------------------------------------------------------
    # Control de la búsqueda
    # ---------------------------------------------------------------
    def reiniciar(self):
        """Corre BFS de nuevo sobre el mapa actual y reinicia la animación."""
        self.reproduciendo = False
        if self.mapa_actual is None:
            return
        grid = self.mapa_actual["grid"]
        inicio = tuple(self.mapa_actual["inicio"])
        meta = tuple(self.mapa_actual["meta"])
        self.resultado = bfs(grid, inicio, meta, registrar_pasos=True)
        self.pasos = self.resultado["pasos"]
        self.indice_paso = -1
        self.texto_metricas.config(text="Ejecute la búsqueda para ver métricas.")
        self._dibujar()
        self._actualizar_panel_paso()
        if not self.pasos:
            # Inicio o meta no transitables: no hay ni un solo paso que dar.
            self._mostrar_metricas_finales()

    def iniciar(self):
        """Inicia la reproducción automática si hay pasos por recorrer."""
        if not self.pasos:
            return
        self.reproduciendo = True
        self._reproducir()

    def pausar(self):
        """Detiene la reproducción automática sin perder el paso actual."""
        self.reproduciendo = False

    def _reproducir(self):
        """Avanza un paso y programa el siguiente mientras esté reproduciendo."""
        if not self.reproduciendo:
            return
        hay_mas = self.avanzar_paso()
        if hay_mas:
            self.after(self.velocidad_ms.get(), self._reproducir)
        else:
            self.reproduciendo = False

    def avanzar_paso(self):
        """Avanza un paso de BFS. Devuelve True si quedan más pasos."""
        if self.indice_paso + 1 >= len(self.pasos):
            return False
        self.indice_paso += 1
        self._dibujar()
        self._actualizar_panel_paso()

        es_ultimo = self.indice_paso == len(self.pasos) - 1
        if self.pasos[self.indice_paso]["meta_encontrada"] or es_ultimo:
            self._mostrar_metricas_finales()
            return False
        return True

    # ---------------------------------------------------------------
    # Dibujo
    # ---------------------------------------------------------------
    def _dibujar(self):
        """Pinta el mapa y el estado de BFS correspondiente al paso actual."""
        self.canvas.delete("all")
        if self.mapa_actual is None:
            return

        grid = self.mapa_actual["grid"]
        filas, columnas = len(grid), len(grid[0])
        ancho = self.canvas.winfo_width() or 700
        alto = self.canvas.winfo_height() or 700
        tam = max(3, min(ancho // columnas, alto // filas))

        inicio = tuple(self.mapa_actual["inicio"])
        meta = tuple(self.mapa_actual["meta"])

        visitados, frontera_actual, actual, camino_final = set(), [], None, set()
        if 0 <= self.indice_paso < len(self.pasos):
            paso = self.pasos[self.indice_paso]
            visitados = set(paso["visitados"])
            frontera_actual = paso["frontera"]
            actual = paso["expandido"]
            if paso["meta_encontrada"] and self.resultado["camino"]:
                camino_final = set(self.resultado["camino"])

        frontera_set = set(frontera_actual)

        for f in range(filas):
            for c in range(columnas):
                x0, y0 = c * tam, f * tam
                x1, y1 = x0 + tam, y0 + tam
                celda = (f, c)

                if grid[f][c] == 1:
                    color = COLORES["obstaculo"]
                elif celda in camino_final:
                    color = COLORES["camino"]
                elif celda == actual:
                    color = COLORES["actual"]
                elif celda in frontera_set:
                    color = COLORES["frontera"]
                elif celda in visitados:
                    color = COLORES["visitado"]
                else:
                    color = COLORES["libre"]

                if celda == inicio:
                    color = COLORES["inicio"]
                elif celda == meta:
                    color = COLORES["meta"]

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                                              outline=COLORES["rejilla"])

    def _actualizar_panel_paso(self):
        """Actualiza el contador de paso y la frontera mostrada (truncada)."""
        total = len(self.pasos)
        actual = self.indice_paso + 1
        self.texto_paso.config(text=f"Paso: {actual} / {total}")

        frontera = self.pasos[self.indice_paso]["frontera"] if 0 <= self.indice_paso < len(self.pasos) else []

        if len(frontera) > MAX_FRONTERA_MOSTRADA:
            visibles = frontera[:MAX_FRONTERA_MOSTRADA]
            texto = f"{visibles}\n… (+{len(frontera) - MAX_FRONTERA_MOSTRADA} más)\nTamaño total: {len(frontera)}"
        else:
            texto = f"{frontera}\nTamaño total: {len(frontera)}"
        self.texto_frontera.config(text=texto)

    def _mostrar_metricas_finales(self):
        """Muestra el resultado y las 8 métricas exigidas por la rúbrica."""
        r = self.resultado
        estado = "Solución encontrada" if r["camino"] else "Sin solución (frontera agotada)"
        texto = (
            f"{estado}\n\n"
            f"Longitud del camino: {r['profundidad']}\n"
            f"Nodos generados: {r['generados']}\n"
            f"Nodos expandidos: {r['expandidos']}\n"
            f"Estados visitados: {r['visitados']}\n"
            f"Profundidad de la solución: {r['profundidad']}\n"
            f"Tamaño máximo de frontera: {r['frontera_maxima']}\n"
            f"Tiempo de ejecución: {r['tiempo_ejecucion']*1000:.3f} ms"
        )
        self.texto_metricas.config(text=texto)


if __name__ == "__main__":
    app = ExploradorBFS()
    app.mainloop()
