"""
ejecutar_pruebas.py - Corre BFS sobre los tres mapas de prueba (sin
necesidad de la interfaz gráfica), guarda un resumen de métricas en
04_resultados/metricas.csv, y compara la longitud calculada para el
mapa sencillo contra el valor esperado a mano (verificación real, no
solo un mensaje informativo).
"""

import csv
from pathlib import Path

from bfs import bfs
from maze import cargar_mapa

# Este archivo vive en 02_codigo/modulos_y_notebooks/, dos niveles bajo la
# raíz del proyecto: de ahí los tres ".parent" para llegar a la raíz.
CARPETA_MAPAS = Path(__file__).resolve().parent.parent.parent / "03_mapas" / "mapa_principal_y_pruebas"
CARPETA_RESULTADOS = Path(__file__).resolve().parent.parent.parent / "04_resultados"

CASOS = [
    ("Mapa principal", "1_mapa_principal.json"),
    ("Mapa sencillo", "2_mapa_sencillo.json"),
    ("Mapa de estrés", "3_mapa_estres.json"),
]

RUTA_OPTIMA_ESPERADA_SENCILLO = 12  # calculada a mano: distancia Manhattan (0,0)->(6,6)


def main():
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

    # Verificación real (no solo un mensaje informativo): compara la
    # longitud que BFS calculó para el mapa sencillo contra el valor
    # esperado a mano. Si algún cambio futuro rompe el resultado, esto
    # lo hace visible de inmediato en vez de imprimir un texto fijo.
    resultado_sencillo = next((f for f in filas_csv if f["mapa"] == "Mapa sencillo"), None)
    if resultado_sencillo:
        obtenido = resultado_sencillo["longitud_camino"]
        coincide = obtenido == RUTA_OPTIMA_ESPERADA_SENCILLO
        print(f"\nVerificación manual (mapa sencillo): esperado={RUTA_OPTIMA_ESPERADA_SENCILLO}, "
              f"obtenido={obtenido}, coincide={coincide}")
        assert coincide, "La longitud calculada no coincide con la verificación manual."


if __name__ == "__main__":
    main()
