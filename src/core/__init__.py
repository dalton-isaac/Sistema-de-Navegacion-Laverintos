"""
Módulo Núcleo (Core) de Inteligencia Artificial
==============================================
Exporta heurísticas, algoritmos y laberintos para fácil importación.
"""

from .heuristics import (
    MOVIMIENTOS,
    NOMBRES_MOVIMIENTOS,
    heuristica_manhattan,
    encontrar_inicio_meta,
    es_celda_transitable,
    calcular_costo_ruta
)

from .algorithms import (
    bfs,
    dfs,
    ucs,
    greedy,
    a_star,
    ejecutar_todos,
    ALGORITMOS
)

from .maze import (
    PRESETS_LABERINTOS,
    generar_laberinto_aleatorio
)

__all__ = [
    "MOVIMIENTOS",
    "NOMBRES_MOVIMIENTOS",
    "heuristica_manhattan",
    "encontrar_inicio_meta",
    "es_celda_transitable",
    "calcular_costo_ruta",
    "bfs",
    "dfs",
    "ucs",
    "greedy",
    "a_star",
    "ejecutar_todos",
    "ALGORITMOS",
    "PRESETS_LABERINTOS",
    "generar_laberinto_aleatorio"
]
