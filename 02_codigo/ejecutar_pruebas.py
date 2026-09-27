"""
ejecutar_pruebas.py
Corre BFS sobre los tres mapas de prueba (sin necesidad de la interfaz
gráfica) y guarda un resumen de métricas en 04_resultados/metricas.csv,
además de imprimir en pantalla una verificación manual para el caso
sencillo. Útil para incluir evidencia en el reporte técnico.
"""

import csv
from pathlib import Path

from bfs import bfs
from maze import cargar_mapa

CARPETA_MAPAS = Path(__file__).resolve().parent.parent / "03_mapas" #extrae la ruta de la carpeta de los mapas
CARPETA_RESULTADOS = Path(__file__).resolve().parent.parent / "04_resultados" #guarda la ruta de la carpeta de resultados

CASOS = [
    ("Mapa principal", "mapa_principal.json"),
    ("Mapa sencillo", "mapa_sencillo.json"),
    ("Mapa de estrés", "mapa_estres.json"),
]

def main():
    """Ejecuta BFS para cada mapa disponible y exporta las métricas.

    Recorre CASOS, omite con un aviso los archivos que no existan y carga los
    demás mapas. Ejecuta la búsqueda sin registrar pasos, imprime resultados
    y, si procesó al menos un mapa, escribe las filas en metricas.csv. La
    verificación del mapa sencillo que se imprime al final es informativa;
    no compara automáticamente la longitud calculada con 12.
    Dependencias del proyecto: importa bfs() desde bfs.py y cargar_mapa()
    desde maze.py. También usa csv y Path de la biblioteca estándar.
    """
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    filas_csv = []

    for nombre, archivo in CASOS:
        ruta = CARPETA_MAPAS / archivo
        if not ruta.exists():
            print(f"[Aviso] No existe {ruta}. Ejecute primero: python generar_mapas.py")
            continue

        mapa = cargar_mapa(str(ruta))
        grid = mapa["grid"]
        inicio = tuple(mapa["inicio"])
        meta = tuple(mapa["meta"])

        resultado = bfs(grid, inicio, meta, registrar_pasos=False)

        print(f"\n=== {nombre} ===")
        print(f"Tamaño: {len(grid)}x{len(grid[0])}  Inicio: {inicio}  Meta: {meta}")
        print(f"Solución encontrada: {resultado['camino'] is not None}")
        print(f"Longitud del camino: {resultado['profundidad']}")
        print(f"Generados: {resultado['generados']}  Expandidos: {resultado['expandidos']}  "
              f"Visitados: {resultado['visitados']}  Frontera máx.: {resultado['frontera_maxima']}")
        print(f"Tiempo: {resultado['tiempo_ejecucion']*1000:.3f} ms")

        filas_csv.append({
            "mapa": nombre,
            "filas": len(grid),
            "columnas": len(grid[0]),
            "solucion_encontrada": resultado["camino"] is not None,
            "longitud_camino": resultado["profundidad"],
            "nodos_generados": resultado["generados"],
            "nodos_expandidos": resultado["expandidos"],
            "estados_visitados": resultado["visitados"],
            "frontera_maxima": resultado["frontera_maxima"],
            "tiempo_ms": round(resultado["tiempo_ejecucion"] * 1000, 3),
        })

    if filas_csv:
        ruta_csv = CARPETA_RESULTADOS / "metricas.csv"
        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=list(filas_csv[0].keys()))
            escritor.writeheader()
            escritor.writerows(filas_csv)
        print(f"\nMétricas guardadas en: {ruta_csv}")

    # Verificación manual del caso sencillo (7x7, muro con un único hueco
    # en la fila 3): desde (0,0) hasta (6,6) sin nada más que rodear, la
    # distancia Manhattan es 6 + 6 = 12, y el hueco del muro cae justo
    # sobre esa diagonal directa, así que la ruta óptima esperada a mano
    # es de 12 movimientos.
    print("\nVerificación manual (mapa sencillo): ruta óptima esperada = 12 movimientos.")


if __name__ == "__main__":
    main()
