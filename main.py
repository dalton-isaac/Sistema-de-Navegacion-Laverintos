"""
===============================================================================
PUNTO DE ENTRADA PRINCIPAL (MAIN)
Sistema Inteligente de Búsqueda y Navegación en Laberintos
Pontificia Universidad Católica del Ecuador (PUCE)
Fundamentos de Inteligencia Artificial - NRC: 1371
Autor: Isaac Oña
Docente: Ing. Patricio Alvear
===============================================================================
Uso:
  python main.py                     # Inicia la Interfaz Gráfica (GUI Tkinter)
  python main.py --benchmark         # Ejecuta el Benchmark en Consola y genera gráficos
  python main.py --cli               # Modo Consola interactivo
  python main.py --report            # Compila el Informe Técnico APA 7 en Word
===============================================================================
"""

import sys
import os

# Configurar encoding UTF-8 en consola Windows si es necesario
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.core import (
    PRESETS_LABERINTOS,
    ejecutar_todos,
    bfs,
    dfs,
    ucs,
    greedy,
    a_star
)
from src.gui import iniciar_interfaz_grafica
from src.utils import generar_graficos_comparativos, construir_informe


def ejecutar_benchmark_consola():
    """
    Ejecuta el protocolo de pruebas experimental sobre todos los presets
    mostrando tablas de métricas formateadas y generando gráficos de alta resolución.
    """
    print("=" * 85)
    print(" SISTEMA INTELIGENTE DE BUSQUEDA Y NAVEGACION EN LABERINTOS")
    print(" Pontificia Universidad Catolica del Ecuador (PUCE)")
    print(" Autor: Isaac Ona | Docente: Ing. Patricio Alvear | NRC: 1371")
    print("=" * 85)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    for idx, (nombre_mapa, matriz) in enumerate(PRESETS_LABERINTOS.items(), start=1):
        print(f"\n>>> EVALUANDO: {nombre_mapa} ({len(matriz)}x{len(matriz[0])})")
        print("-" * 85)
        res = ejecutar_todos(matriz)
        
        print(f"{'Metrica Evaluada':<25} | {'BFS':<10} | {'DFS':<10} | {'UCS':<10} | {'Greedy':<10} | {'A*':<10}")
        print("-" * 85)
        print(f"{'Nodos explorados':<25} | {res['BFS']['nodos_explorados']:<10} | {res['DFS']['nodos_explorados']:<10} | {res['UCS']['nodos_explorados']:<10} | {res['Greedy']['nodos_explorados']:<10} | {res['A*']['nodos_explorados']:<10}")
        print(f"{'Tiempo ejecucion (ms)':<25} | {res['BFS']['tiempo_ms']:<10.4f} | {res['DFS']['tiempo_ms']:<10.4f} | {res['UCS']['tiempo_ms']:<10.4f} | {res['Greedy']['tiempo_ms']:<10.4f} | {res['A*']['tiempo_ms']:<10.4f}")
        print(f"{'Costo total (H=1, V=2)':<25} | {res['BFS']['costo_total']:<10} | {res['DFS']['costo_total']:<10} | {res['UCS']['costo_total']:<10} | {res['Greedy']['costo_total']:<10} | {res['A*']['costo_total']:<10}")
        print(f"{'Longitud ruta (pasos)':<25} | {res['BFS']['longitud_ruta']:<10} | {res['DFS']['longitud_ruta']:<10} | {res['UCS']['longitud_ruta']:<10} | {res['Greedy']['longitud_ruta']:<10} | {res['A*']['longitud_ruta']:<10}")
        print("-" * 85)

        # Generar gráfico para el preset
        guardar_fig = os.path.join(assets_dir, f"grafico_preset_{idx}.png")
        generar_graficos_comparativos(res, guardar_path=guardar_fig, mostrar=False)

    # Generar gráfico oficial adicional
    res_oficial = ejecutar_todos(PRESETS_LABERINTOS["1. Ejemplo Oficial PDF (5x5)"])
    graf_oficial = os.path.join(assets_dir, "grafico_comparativo_oficial.png")
    generar_graficos_comparativos(res_oficial, guardar_path=graf_oficial, mostrar=False)
    print(f"\n[INFO] Graficos estadisticos exportados en: {assets_dir}")


def main():
    """Función principal que procesa argumentos CLI e inicia el sistema."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--benchmark", "-b", "--cli", "-c"]:
            ejecutar_benchmark_consola()
            return
        elif arg in ["--report", "-r", "--informe"]:
            print("[INFO] Generando informe tecnico en Word...")
            construir_informe()
            return
        elif arg in ["--help", "-h"]:
            print(__doc__)
            return

    # Iniciar GUI por defecto
    try:
        iniciar_interfaz_grafica()
    except Exception as e:
        print(f"[AVISO] No se pudo inicializar el entorno grafico ({e}).")
        print("[INFO] Ejecutando benchmark en consola de respaldo...")
        ejecutar_benchmark_consola()


if __name__ == "__main__":
    main()
