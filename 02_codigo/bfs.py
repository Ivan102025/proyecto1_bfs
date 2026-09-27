"""bfs.py - Implementación de Búsqueda en Amplitud (BFS)"""
import time
from collections import deque

# movimientos permitidos arriba, abajo, izquierda, derecha (no diagonales)
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def vecinos(grid, celda):
    """crea las celdas libres en el orden de direciones
    comprueba que cada coordenada esté dentro del mapa y que su valor sea 0 (libre)"""
    filas, columnas = len(grid), len(grid[0])
    f, c = celda
    for df, dc in DIRECCIONES:
        nf, nc = f + df, c + dc
        if 0 <= nf < filas and 0 <= nc < columnas and grid[nf][nc] == 0:
            yield (nf, nc)


def reconstruir_camino(parent, meta):
    """Reconstruye el camino siguiendo los padres desde la meta"""
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = parent[actual] #estoa ayuda a evitar duplicados
    camino.reverse()
    return camino


def bfs(grid, inicio, meta, registrar_pasos=True):
    """
    Ejecuta BFS desde inicio hasta meta(0->libre, 1->obstáculo)

    Convierte las coordenadas a tuplas, valida que inicio y meta sean libres,
    y recorre la cuadrícula con una cola FIFO. El parent registra
    tanto los estados descubiertos como el padre de cada uno, evitando que un
    estado entre más de una vez. Al retirar un estado de la cola comprueba si
    es la meta; al encontrarla, reconstruye el camino de profundidad mínima.
    Si registrar_pasos es True, guarda instantáneas de la búsqueda para la
    animación; en False evita ese almacenamiento adicional.

    Dependencias del proyecto: usa vecinos() y reconstruir_camino() de este
    archivo. maze.py, main.py y ejecutar_pruebas.py importan esta función.

    Devuelve un diccionario con:
      camino            -> lista de celdas desde inicio hasta meta, o None
      profundidad       -> longitud del camino en movimientos (len(camino)-1)
      generados         -> número de estados registrados en 'parent'
      expandidos        -> número de estados retirados y procesados
      visitados         -> número de estados distintos alcanzados
      frontera_maxima   -> mayor tamaño que alcanzó la cola
      tiempo_ejecucion  -> segundos que tardó la búsqueda
      pasos             -> snapshots para animar (si registrar_pasos=True):
                           cada uno es {"expandido", "frontera", "visitados",
                           "meta_encontrada"}
    """
    inicio, meta = tuple(inicio), tuple(meta)
    t0 = time.perf_counter()

    if grid[inicio[0]][inicio[1]] != 0 or grid[meta[0]][meta[1]] != 0:
        # Estado inicial o meta no transitables: fracaso inmediato.
        return {
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
                continue  #ya visistado(no se agrega de nuevo a la frontera)
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
