"""
maze.py-Generación y validación de mapas

Contiene:
- construcción determinista de la semilla a partir de ambas matrículas
- generación del mapa principal cumpliendo todas las restricciones
- generación de los casos de prueba adicionales
"""

import json
import random
from pathlib import Path

from bfs import bfs  # se reutiliza el BFS propio para medir la ruta óptima

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)] #puntos cardinales

LIBRE = 0 #celda libre
OBSTACULO = 1 #celda con obstáculo

"""Construye la semilla a partir de las matrículas
    En main.py  comprueba la semilla de un mapa guardado"""

def construir_semilla(matricula_1: str, matricula_2: str) -> int:
    m1 = str(matricula_1).strip() #Asigna la matrícula 1 a m1 y elimina espacios en blanco
    m2 = str(matricula_2).strip()
    ordenadas = sorted([m1, m2]) #Ordena las matrículas
    return int("".join(ordenadas))#devuelve la semilla como un entero concatenando las matrículas ordenadas


def _conectados_desde(grid, inicio):
    """ ----Devuelve las celdas libres alcanzables desde inicio. llama generar_mapa()"""
    filas, columnas = len(grid), len(grid[0])
    visitados = {inicio}
    pila = [inicio]
    while pila:
        f, c = pila.pop()
        for df, dc in DIRECCIONES:
            vecino = (f + df, c + dc)
            nf, nc = vecino
            if 0 <= nf < filas and 0 <= nc < columnas and vecino not in visitados:
                if grid[nf][nc] == LIBRE:
                    visitados.add(vecino)
                    pila.append(vecino)
    return visitados


def _tiene_callejones(grid):
    """Indica si el mapa contiene una celda libre tipo callejón sin salida"""
    filas, columnas = len(grid), len(grid[0])
    for f in range(filas):
        for c in range(columnas):
            if grid[f][c] != LIBRE:
                continue
            libres = 0
            for df, dc in DIRECCIONES:
                nf, nc = f + df, c + dc
                if 0 <= nf < filas and 0 <= nc < columnas and grid[nf][nc] == LIBRE:
                    libres += 1
            if libres == 1:
                return True
    return False


def _generar_intento(rng, filas, columnas, pct_obstaculos, inicio, meta):
    """Construye un candidato colocando obstáculos en posiciones mezcladas
    Mantiene libres el inicio y la meta, calcula la cantidad de obstáculos a
    partir del porcentaje"""
    grid = [[LIBRE for _ in range(columnas)] for _ in range(filas)]
    total = filas * columnas
    n_obstaculos = int(total * pct_obstaculos)

    celdas = [(f, c) for f in range(filas) for c in range(columnas)
              if (f, c) not in (inicio, meta)]
    rng.shuffle(celdas)

    for (f, c) in celdas[:n_obstaculos]:
        grid[f][c] = OBSTACULO

    return grid


def generar_mapa(matricula_1, matricula_2, filas=25, columnas=25,
                  pct_obstaculos=0.28, longitud_minima=25, max_intentos=1000):
    """
    General el mapa principal, con el 28% de obstáculos y la ruta óptima de al menos 25 movimientos.
    """
    if filas < 25 or columnas < 25:
        raise ValueError("El mapa debe tener al menos 25 filas y 25 columnas.")
    if not (0.20 <= pct_obstaculos <= 0.35):
        raise ValueError("El porcentaje de obstáculos debe estar entre 20% y 35%.")

    semilla_base = construir_semilla(matricula_1, matricula_2)
    inicio, meta = (0, 0), (filas - 1, columnas - 1)

    for intento in range(max_intentos):
        rng = random.Random(semilla_base + intento) #agrega el intento a la semilla para variar la generación
        #inicializador matriz vacia 
        grid = _generar_intento(rng, filas, columnas, pct_obstaculos, inicio, meta)

        if meta not in _conectados_desde(grid, inicio):
            continue

        resultado = bfs(grid, inicio, meta, registrar_pasos=False)
        if resultado["camino"] is None or resultado["profundidad"] < longitud_minima:
            continue

        if not _tiene_callejones(grid):
            continue
        #Estructura JSON que contiene los datos del mapa generado para su exportacion
        return {
            "semilla": semilla_base,
            "intento": intento,
            "filas": filas,
            "columnas": columnas,
            "pct_obstaculos": pct_obstaculos,
            "inicio": list(inicio),
            "meta": list(meta),
            "grid": grid,
            "longitud_optima": resultado["profundidad"],
        }

    raise RuntimeError(
        f"No se logró generar un mapa válido tras {max_intentos} intentos; "
        "ajuste los parámetros (tamaño, % de obstáculos o longitud mínima)."
    )


def generar_mapa_sencillo():
    """Genera un mapa pequeño y verificable a mano, con un único callejón """
    filas, columnas = 7, 7
    grid = [[LIBRE for _ in range(columnas)] for _ in range(filas)]
    for f in range(filas):
        if f != 3:  # hueco único en la fila 3
            grid[f][3] = OBSTACULO
    inicio, meta = (0, 0), (6, 6)
    return {
        "semilla": None,
        "filas": filas,
        "columnas": columnas,
        "pct_obstaculos": None,
        "inicio": list(inicio),
        "meta": list(meta),
        "grid": grid,
        "descripcion": "Caso sencillo verificable a mano (ruta óptima esperada: 12 movimientos)",
    }


def generar_mapa_estres(matricula_1, matricula_2, filas=30, columnas=30,
                         pct_obstaculos=0.35):
    """Genera un mapa grande con el porcentaje máximo de obstáculos. Reutiliza las funciones de generar_mapa() y construir_semilla() para mantener la consistencia."""
    return generar_mapa(
        matricula_1, matricula_2,
        filas=filas, columnas=columnas,
        pct_obstaculos=pct_obstaculos,
        longitud_minima=1,
    )


def guardar_mapa(mapa: dict, ruta: str):
    """guarda el mapa en un archivo JSON"""
    #verifica si la carpeta existe, si no la crea
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    ##Guarda el mapa en formato JSON
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(mapa, f, ensure_ascii=False, indent=2)


def cargar_mapa(ruta: str) -> dict:
    """Lee un archivo JSON de mapa y devuelve sus datos como diccionario.

    Dependencias del proyecto: usa json de la biblioteca estándar. La llaman
    main.py y ejecutar_pruebas.py; no requiere otro módulo del proyecto.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)
