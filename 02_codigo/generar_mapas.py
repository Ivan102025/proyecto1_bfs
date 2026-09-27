"""
generar_mapas.py
Genera y guarda en 03_mapas/ los tres mapas de prueba exigidos por el
proyecto: el mapa principal (semilla de ambas matrículas), un caso
sencillo verificable a mano y un caso de estrés con mayor porcentaje de
obstáculos. Con la misma semilla siempre se genera el mismo mapa
principal, sin importar cuántas veces se ejecute este script.
"""
from pathlib import Path
from maze import generar_mapa, generar_mapa_sencillo, generar_mapa_estres, guardar_mapa
MATRICULA_1 = "20241110"
MATRICULA_2 = "20241018"
CARPETA = Path(__file__).resolve().parent.parent / "03_mapas"

def main():
    """Genera y guarda los tres mapas de prueba del proyecto.

    Crea el mapa principal a partir de las matrículas, además de los casos
    sencillo y de estrés; imprime sus datos relevantes y guarda cada uno en
    CARPETA como archivo JSON.
    Dependencias del proyecto: importa desde maze.py las funciones
    generar_mapa(), generar_mapa_sencillo(), generar_mapa_estres() y
    guardar_mapa(). Usa las matrículas y la ruta definidas en este archivo.
    """
    print("Generando mapa principal (25x25, semilla de ambas matrículas)...")
    principal = generar_mapa(MATRICULA_1, MATRICULA_2)
    guardar_mapa(principal, str(CARPETA / "mapa_principal.json"))
    print(f"  Semilla: {principal['semilla']}")
    print(f"  Ruta óptima: {principal['longitud_optima']} movimientos")

    print("Generando mapa sencillo (verificable a mano)...")
    sencillo = generar_mapa_sencillo()
    guardar_mapa(sencillo, str(CARPETA / "mapa_sencillo.json"))
    print(f"  {sencillo['descripcion']}")

    print("Generando mapa de estrés (35% de obstáculos)...")
    estres = generar_mapa_estres(MATRICULA_1, MATRICULA_2)
    guardar_mapa(estres, str(CARPETA / "mapa_estres.json"))
    print(f"  Ruta óptima: {estres['longitud_optima']} movimientos")

    print(f"\nMapas guardados en: {CARPETA}")


if __name__ == "__main__":
    main()
