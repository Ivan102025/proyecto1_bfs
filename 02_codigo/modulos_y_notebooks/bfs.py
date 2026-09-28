import time
from collections import deque

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha


def vecinos(grid, celda):
    """Devuelve las celdas libres adyacentes a 'celda' (sin diagonales)."""
    filas, columnas = len(grid), len(grid[0])
    f, c = celda
    for df, dc in DIRECCIONES:
        nf, nc = f + df, c + dc
        if 0 <= nf < filas and 0 <= nc < columnas and grid[nf][nc] == 0:
            yield (nf, nc)


def reconstruir_camino(parent, meta):
    """Sigue los padres desde la meta hasta el inicio y devuelve el camino."""
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = parent[actual]
    camino.reverse()
    return camino


def bfs(grid, inicio, meta, registrar_pasos=True):
    """
    Ejecuta BFS desde 'inicio' hasta 'meta' (grid: 0 = libre, 1 = obstáculo).

    Devuelve un diccionario con:
      camino, profundidad, generados, expandidos, visitados,
      frontera_maxima, tiempo_ejecucion, pasos (snapshots para animar,
      cada uno con expandido/frontera/visitados/meta_encontrada).
    """
    inicio, meta = tuple(inicio), tuple(meta)
    t0 = time.perf_counter()

    if grid[inicio[0]][inicio[1]] != 0 or grid[meta[0]][meta[1]] != 0:
        return {  # inicio o meta no transitables: fracaso inmediato
            "camino": None, "profundidad": None,
            "generados": 0, "expandidos": 0, "visitados": 0,
            "frontera_maxima": 0,
            "tiempo_ejecucion": time.perf_counter() - t0,
            "pasos": [],
        }

    frontera = deque([inicio])
    parent = {inicio: None}
    expandidos = 0
    frontera_maxima = len(frontera)
    pasos = []
    camino = None

    while frontera:
        estado = frontera.popleft()
        expandidos += 1
        es_meta = (estado == meta)

        if registrar_pasos:
            pasos.append({
                "expandido": estado,
                "frontera": list(frontera),
                "visitados": list(parent.keys()),
                "meta_encontrada": es_meta,
            })

        if es_meta:
            camino = reconstruir_camino(parent, meta)
            break

        for vecino in vecinos(grid, estado):
            if vecino in parent:
                continue  # ya alcanzado antes: no se agrega de nuevo
            parent[vecino] = estado
            frontera.append(vecino)

        frontera_maxima = max(frontera_maxima, len(frontera))

    return {
        "camino": camino,
        "profundidad": (len(camino) - 1) if camino else None,
        "generados": len(parent),
        "expandidos": expandidos,
        "visitados": len(parent),
        "frontera_maxima": frontera_maxima,
        "tiempo_ejecucion": time.perf_counter() - t0,
        "pasos": pasos,
    }
