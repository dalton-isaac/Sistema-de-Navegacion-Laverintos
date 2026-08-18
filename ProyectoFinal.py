"""
===============================================================================
PROYECTO FINAL: SISTEMA INTELIGENTE DE BÚSQUEDA Y NAVEGACIÓN EN LABERINTOS
Fundamentos de Inteligencia Artificial - Pontificia Universidad Católica del Ecuador
Autor: Isaac Oña
Docente: Ing. Patricio Alvear
NRC: 1371
===============================================================================
Lanzador de compatibilidad directa hacia la arquitectura modular en src/
===============================================================================
"""

import sys
from src.core import (
    MOVIMIENTOS,
    NOMBRES_MOVIMIENTOS,
    heuristica_manhattan,
    encontrar_inicio_meta,
    es_celda_transitable,
    calcular_costo_ruta,
    bfs,
    dfs,
    ucs,
    greedy,
    a_star,
    ALGORITMOS,
    PRESETS_LABERINTOS,
    generar_laberinto_aleatorio,
    ejecutar_todos
)
from src.gui import InterfazLaberinto, iniciar_interfaz_grafica
from src.utils import generar_graficos_comparativos, construir_informe
from main import main, ejecutar_benchmark_consola

if __name__ == "__main__":
    main()