"""
===============================================================================
PROYECTO FINAL: SISTEMA INTELIGENTE DE BÚSQUEDA Y NAVEGACIÓN EN LABERINTOS
Fundamentos de Inteligencia Artificial - Pontificia Universidad Católica del Ecuador
Autor: Isaac Oña
Docente: Ing. Patricio Alvear
NRC: 1371
===============================================================================
Descripción:
Este software implementa y compara de manera exhaustiva algoritmos de búsqueda
no informada (BFS, DFS, Costo Uniforme - UCS) y búsqueda informada (Greedy Best-First,
A*) aplicados al problema de navegación y rescate robótico en laberintos con obstáculos.

Costos de Movimiento:
  - Movimiento Horizontal (Izquierda / Derecha): Costo = 1
  - Movimiento Vertical   (Arriba / Abajo)    : Costo = 2

Heurística Informada:
  - Distancia Manhattan: h(n) = |x1 - x2| + |y1 - y2|
===============================================================================
"""

import time
import heapq
import random
import copy
import sys
import os
from collections import deque
from typing import List, Tuple, Dict, Optional, Any, Set

# --- CONFIGURACIÓN DE MOVIMIENTOS Y COSTOS ---
# Fila (x) = Movimiento Vertical (Costo 2) | Columna (y) = Movimiento Horizontal (Costo 1)
MOVIMIENTOS: Dict[Tuple[int, int], int] = {
    (0, 1): 1,   # Derecha (Horizontal)
    (0, -1): 1,  # Izquierda (Horizontal)
    (1, 0): 2,   # Abajo (Vertical)
    (-1, 0): 2   # Arriba (Vertical)
}

NOMBRES_MOVIMIENTOS = {
    (0, 1): "Derecha",
    (0, -1): "Izquierda",
    (1, 0): "Abajo",
    (-1, 0): "Arriba"
}


# =============================================================================
# FUNCIONES AUXILIARES Y HEURÍSTICAS
# =============================================================================

def heuristica_manhattan(actual: Tuple[int, int], meta: Tuple[int, int]) -> int:
    """
    Calcula la distancia Manhattan entre el nodo actual y el objetivo.
    h(n) = |x_actual - x_meta| + |y_actual - y_meta|
    """
    return abs(actual[0] - meta[0]) + abs(actual[1] - meta[1])


def encontrar_inicio_meta(laberinto: List[List[str]]) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """
    Encuentra las coordenadas del nodo de inicio ('S') y de la meta ('G').
    """
    inicio: Optional[Tuple[int, int]] = None
    meta: Optional[Tuple[int, int]] = None
    
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            val = str(laberinto[i][j]).strip().upper()
            if val == 'S':
                inicio = (i, j)
            elif val == 'G':
                meta = (i, j)
                
    return inicio, meta


def es_celda_transitable(laberinto: List[List[str]], fila: int, col: int) -> bool:
    """
    Verifica si una celda dentro del laberinto es válida y no es una pared/obstáculo.
    '1' representa una pared. '0', 'S', 'G' son celdas transitables.
    """
    filas = len(laberinto)
    cols = len(laberinto[0])
    if 0 <= fila < filas and 0 <= col < cols:
        val = str(laberinto[fila][col]).strip()
        return val != '1'
    return False


def calcular_costo_ruta(ruta: List[Tuple[int, int]]) -> int:
    """
    Calcula el costo total acumulado de una ruta dada con base en los costos
    diferenciados: horizontal = 1, vertical = 2.
    """
    if not ruta or len(ruta) <= 1:
        return 0
    costo_total = 0
    for i in range(1, len(ruta)):
        nodo_anterior = ruta[i - 1]
        nodo_actual = ruta[i]
        dx = nodo_actual[0] - nodo_anterior[0]
        dy = nodo_actual[1] - nodo_anterior[1]
        costo_total += MOVIMIENTOS.get((dx, dy), 1)
    return costo_total


# =============================================================================
# 1. BÚSQUEDA EN ANCHURA (BFS - BREADTH FIRST SEARCH)
# =============================================================================

def bfs(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo de Búsqueda en Anchura (BFS).
    Estrategia no informada basada en cola FIFO.
    Garantiza el camino con el menor número de pasos (longitud).
    
    Retorna: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
    """
    inicio, meta = encontrar_inicio_meta(laberinto)
    if not inicio or not meta:
        return None, 0, 0.0, 0, 0, []
        
    inicio_tiempo = time.perf_counter()
    cola = deque([(inicio, [inicio])])
    visitados: Set[Tuple[int, int]] = {inicio}
    orden_exploracion: List[Tuple[int, int]] = []
    nodos_explorados = 0
    
    while cola:
        actual, ruta = cola.popleft()
        nodos_explorados += 1
        if registrar_exploracion:
            orden_exploracion.append(actual)
            
        if actual == meta:
            tiempo_ejecucion = time.perf_counter() - inicio_tiempo
            costo = calcular_costo_ruta(ruta)
            return ruta, nodos_explorados, tiempo_ejecucion, costo, len(ruta) - 1, orden_exploracion
            
        for (dx, dy), _ in MOVIMIENTOS.items():
            vecino = (actual[0] + dx, actual[1] + dy)
            if es_celda_transitable(laberinto, vecino[0], vecino[1]) and vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, ruta + [vecino]))
                
    tiempo_ejecucion = time.perf_counter() - inicio_tiempo
    return None, nodos_explorados, tiempo_ejecucion, 0, 0, orden_exploracion


# =============================================================================
# 2. BÚSQUEDA EN PROFUNDIDAD (DFS - DEPTH FIRST SEARCH)
# =============================================================================

def dfs(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo de Búsqueda en Profundidad (DFS).
    Estrategia no informada basada en pila LIFO.
    Explora lo más profundo de cada rama antes de retroceder. No garantiza optimalidad.
    
    Retorna: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
    """
    inicio, meta = encontrar_inicio_meta(laberinto)
    if not inicio or not meta:
        return None, 0, 0.0, 0, 0, []
        
    inicio_tiempo = time.perf_counter()
    pila = [(inicio, [inicio])]
    visitados: Set[Tuple[int, int]] = set()
    orden_exploracion: List[Tuple[int, int]] = []
    nodos_explorados = 0
    
    while pila:
        actual, ruta = pila.pop()
        
        if actual not in visitados:
            visitados.add(actual)
            nodos_explorados += 1
            if registrar_exploracion:
                orden_exploracion.append(actual)
                
            if actual == meta:
                tiempo_ejecucion = time.perf_counter() - inicio_tiempo
                costo = calcular_costo_ruta(ruta)
                return ruta, nodos_explorados, tiempo_ejecucion, costo, len(ruta) - 1, orden_exploracion
                
            for (dx, dy), _ in MOVIMIENTOS.items():
                vecino = (actual[0] + dx, actual[1] + dy)
                if es_celda_transitable(laberinto, vecino[0], vecino[1]) and vecino not in visitados:
                    pila.append((vecino, ruta + [vecino]))
                    
    tiempo_ejecucion = time.perf_counter() - inicio_tiempo
    return None, nodos_explorados, tiempo_ejecucion, 0, 0, orden_exploracion


# =============================================================================
# 3. BÚSQUEDA DE COSTO UNIFORME (UCS - UNIFORM COST SEARCH)
# =============================================================================

def ucs(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo de Búsqueda de Costo Uniforme (UCS / Dijkstra).
    Estrategia no informada basada en cola de prioridad por costo acumulado g(n).
    Garantiza encontrar la ruta con el menor costo total en grafos ponderados.
    
    Retorna: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
    """
    inicio, meta = encontrar_inicio_meta(laberinto)
    if not inicio or not meta:
        return None, 0, 0.0, 0, 0, []
        
    inicio_tiempo = time.perf_counter()
    # Cola de prioridad: (costo_acumulado, contador_desempate, nodo_actual, ruta)
    contador = 0
    cola = [(0, contador, inicio, [inicio])]
    visitados: Dict[Tuple[int, int], int] = {}
    orden_exploracion: List[Tuple[int, int]] = []
    nodos_explorados = 0
    
    while cola:
        costo_actual, _, actual, ruta = heapq.heappop(cola)
        
        if actual in visitados and visitados[actual] <= costo_actual:
            continue
            
        visitados[actual] = costo_actual
        nodos_explorados += 1
        if registrar_exploracion:
            orden_exploracion.append(actual)
            
        if actual == meta:
            tiempo_ejecucion = time.perf_counter() - inicio_tiempo
            return ruta, nodos_explorados, tiempo_ejecucion, costo_actual, len(ruta) - 1, orden_exploracion
            
        for (dx, dy), costo_mov in MOVIMIENTOS.items():
            vecino = (actual[0] + dx, actual[1] + dy)
            if es_celda_transitable(laberinto, vecino[0], vecino[1]):
                nuevo_costo = costo_actual + costo_mov
                if vecino not in visitados or nuevo_costo < visitados[vecino]:
                    contador += 1
                    heapq.heappush(cola, (nuevo_costo, contador, vecino, ruta + [vecino]))
                    
    tiempo_ejecucion = time.perf_counter() - inicio_tiempo
    return None, nodos_explorados, tiempo_ejecucion, 0, 0, orden_exploracion


# =============================================================================
# 4. BÚSQUEDA GREEDY (AVARA / HEURÍSTICA PURA)
# =============================================================================

def greedy(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo de Búsqueda Avara (Greedy Best-First Search).
    Estrategia informada que prioriza exclusivamente la heurística h(n) = Distancia Manhattan a la meta.
    Rápido y focalizado hacia la meta, pero no garantiza la ruta de costo óptimo.
    
    Retorna: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
    """
    inicio, meta = encontrar_inicio_meta(laberinto)
    if not inicio or not meta:
        return None, 0, 0.0, 0, 0, []
        
    inicio_tiempo = time.perf_counter()
    contador = 0
    h_inicio = heuristica_manhattan(inicio, meta)
    # Cola de prioridad: (heuristica_h, contador_desempate, nodo_actual, ruta)
    cola = [(h_inicio, contador, inicio, [inicio])]
    visitados: Set[Tuple[int, int]] = set()
    orden_exploracion: List[Tuple[int, int]] = []
    nodos_explorados = 0
    
    while cola:
        h_val, _, actual, ruta = heapq.heappop(cola)
        
        if actual in visitados:
            continue
            
        visitados.add(actual)
        nodos_explorados += 1
        if registrar_exploracion:
            orden_exploracion.append(actual)
            
        if actual == meta:
            tiempo_ejecucion = time.perf_counter() - inicio_tiempo
            costo = calcular_costo_ruta(ruta)
            return ruta, nodos_explorados, tiempo_ejecucion, costo, len(ruta) - 1, orden_exploracion
            
        for (dx, dy), _ in MOVIMIENTOS.items():
            vecino = (actual[0] + dx, actual[1] + dy)
            if es_celda_transitable(laberinto, vecino[0], vecino[1]) and vecino not in visitados:
                h_vecino = heuristica_manhattan(vecino, meta)
                contador += 1
                heapq.heappush(cola, (h_vecino, contador, vecino, ruta + [vecino]))
                
    tiempo_ejecucion = time.perf_counter() - inicio_tiempo
    return None, nodos_explorados, tiempo_ejecucion, 0, 0, orden_exploracion


# =============================================================================
# 5. ALGORITMO A* (A-STAR)
# =============================================================================

def a_star(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo A* (A-Star).
    Estrategia informada óptima que evalúa f(n) = g(n) + h(n), donde:
      g(n) = costo acumulado real desde el inicio.
      h(n) = distancia Manhattan estimada hasta la meta.
    Garantiza encontrar la ruta de menor costo explorando significativamente menos nodos que UCS.
    
    Retorna: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
    """
    inicio, meta = encontrar_inicio_meta(laberinto)
    if not inicio or not meta:
        return None, 0, 0.0, 0, 0, []
        
    inicio_tiempo = time.perf_counter()
    contador = 0
    h_inicio = heuristica_manhattan(inicio, meta)
    # Cola de prioridad: (f_cost, g_cost, contador_desempate, nodo_actual, ruta)
    cola = [(h_inicio, 0, contador, inicio, [inicio])]
    visitados: Dict[Tuple[int, int], int] = {}
    orden_exploracion: List[Tuple[int, int]] = []
    nodos_explorados = 0
    
    while cola:
        f_cost, g_cost, _, actual, ruta = heapq.heappop(cola)
        
        if actual in visitados and visitados[actual] <= g_cost:
            continue
            
        visitados[actual] = g_cost
        nodos_explorados += 1
        if registrar_exploracion:
            orden_exploracion.append(actual)
            
        if actual == meta:
            tiempo_ejecucion = time.perf_counter() - inicio_tiempo
            return ruta, nodos_explorados, tiempo_ejecucion, g_cost, len(ruta) - 1, orden_exploracion
            
        for (dx, dy), costo_mov in MOVIMIENTOS.items():
            vecino = (actual[0] + dx, actual[1] + dy)
            if es_celda_transitable(laberinto, vecino[0], vecino[1]):
                nuevo_g_cost = g_cost + costo_mov
                if vecino not in visitados or nuevo_g_cost < visitados[vecino]:
                    h_cost = heuristica_manhattan(vecino, meta)
                    nuevo_f_cost = nuevo_g_cost + h_cost
                    contador += 1
                    heapq.heappush(cola, (nuevo_f_cost, nuevo_g_cost, contador, vecino, ruta + [vecino]))
                    
    tiempo_ejecucion = time.perf_counter() - inicio_tiempo
    return None, nodos_explorados, tiempo_ejecucion, 0, 0, orden_exploracion


# =============================================================================
# LABERINTOS PRECONFIGURADOS Y GENERADOR
# =============================================================================

PRESETS_LABERINTOS = {
    "1. Ejemplo Oficial PDF (5x5)": [
        ['S', '0', '0', '1', '0'],
        ['1', '1', '0', '1', '0'],
        ['0', '0', '0', '0', '0'],
        ['0', '1', '1', '1', '0'],
        ['0', '0', '0', 'G', '0']
    ],
    "2. Rescate Urbano / Alternativas (10x10)": [
        ['S', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
        ['0', '1', '1', '0', '1', '0', '1', '1', '1', '0'],
        ['0', '1', '0', '0', '0', '0', '0', '0', '1', '0'],
        ['0', '1', '0', '1', '1', '1', '1', '0', '1', '0'],
        ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0'],
        ['1', '1', '0', '1', '0', '1', '1', '1', '1', '0'],
        ['0', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
        ['0', '1', '1', '1', '0', '1', '0', '1', '1', '0'],
        ['0', '0', '0', '1', '0', '0', '0', '1', 'G', '0'],
        ['0', '1', '0', '0', '0', '1', '0', '0', '0', '0']
    ],
    "3. Trampa Cóncava en U (12x12)": [
        ['S', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0'],
        ['0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '0', 'G', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
        ['0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    ],
    "4. Complejo Gran Escala (16x16)": [
        ['S', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
        ['0', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '1', '1', '0'],
        ['1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0'],
        ['0', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '0', '1', '0'],
        ['0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        ['0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0'],
        ['1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '0', '1', '0', '1', '0'],
        ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
        ['0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0'],
        ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        ['0', '1', '0', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '0'],
        ['0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0'],
        ['1', '1', '0', '1', '0', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '0'],
        ['0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0'],
        ['0', '1', '1', '1', '0', '1', '0', '1', '1', '0', '1', '1', '1', '0', '0', '0'],
        ['0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', 'G', '0']
    ]
}


def generar_laberinto_aleatorio(filas: int = 12, columnas: int = 12, densidad_muros: float = 0.25) -> List[List[str]]:
    """
    Genera un laberinto aleatorio garantizando la existencia de al menos un camino
    solucionable entre el inicio ('S') y la meta ('G').
    """
    while True:
        matriz = [['0' for _ in range(columnas)] for _ in range(filas)]
        
        # Colocar muros aleatorios según la densidad
        for r in range(filas):
            for c in range(columnas):
                if random.random() < densidad_muros:
                    matriz[r][c] = '1'
                    
        inicio = (0, 0)
        meta = (filas - 1, columnas - 1)
        matriz[inicio[0]][inicio[1]] = 'S'
        matriz[meta[0]][meta[1]] = 'G'
        
        # Validar si tiene solución mediante BFS
        ruta, _, _, _, _, _ = bfs(matriz, registrar_exploracion=False)
        if ruta is not None:
            return matriz


# =============================================================================
# MOTOR DE BENCHMARK Y GENERACIÓN DE GRÁFICOS
# =============================================================================

ALGORITMOS = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("UCS", ucs),
    ("Greedy", greedy),
    ("A*", a_star)
]


def ejecutar_todos(laberinto: List[List[str]]) -> Dict[str, Dict[str, Any]]:
    """
    Ejecuta los 5 algoritmos sobre el laberinto dado y recopila todas las métricas.
    """
    resultados = {}
    for nombre, fn in ALGORITMOS:
        ruta, nodos, t_exec, costo, longitud, exploracion = fn(laberinto, registrar_exploracion=True)
        resultados[nombre] = {
            "resuelto": ruta is not None,
            "ruta": ruta,
            "nodos_explorados": nodos,
            "tiempo_ms": t_exec * 1000.0,
            "costo_total": costo,
            "longitud_ruta": longitud,
            "orden_exploracion": exploracion
        }
    return resultados


def generar_graficos_comparativos(resultados: Dict[str, Dict[str, Any]], guardar_path: Optional[str] = None, mostrar: bool = False):
    """
    Genera una figura de 2x2 con gráficos de barras de alta calidad comparando:
      1. Nodos Explorados
      2. Tiempo de Ejecución (ms)
      3. Costo Total de la Ruta
      4. Longitud de la Ruta (pasos)
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[ADVERTENCIA] matplotlib no está instalado. No se pueden generar gráficos.")
        return None

    nombres = list(resultados.keys())
    colores = ['#2b5c8f', '#d95f02', '#7570b3', '#e7298a', '#1b9e77']
    
    nodos = [resultados[n]["nodos_explorados"] for n in nombres]
    tiempos = [resultados[n]["tiempo_ms"] for n in nombres]
    costos = [resultados[n]["costo_total"] for n in nombres]
    longitudes = [resultados[n]["longitud_ruta"] for n in nombres]

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Comparación Integral del Desempeño de Algoritmos de Búsqueda', fontsize=15, fontweight='bold', y=0.98)
    
    # 1. Nodos Explorados
    bars1 = axs[0, 0].bar(nombres, nodos, color=colores, edgecolor='black', alpha=0.85)
    axs[0, 0].set_title('1. Nodos Explorados (Menor es mejor)', fontsize=11, fontweight='bold')
    axs[0, 0].set_ylabel('Cantidad de Nodos')
    axs[0, 0].grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars1:
        yval = bar.get_height()
        axs[0, 0].text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{int(yval)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 2. Tiempo de Ejecución (ms)
    bars2 = axs[0, 1].bar(nombres, tiempos, color=colores, edgecolor='black', alpha=0.85)
    axs[0, 1].set_title('2. Tiempo de Ejecución (ms) (Menor es mejor)', fontsize=11, fontweight='bold')
    axs[0, 1].set_ylabel('Milisegundos (ms)')
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars2:
        yval = bar.get_height()
        axs[0, 1].text(bar.get_x() + bar.get_width()/2.0, yval + (max(tiempos)*0.02 if max(tiempos) > 0 else 0.001), f'{yval:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 3. Costo Total de la Ruta
    bars3 = axs[1, 0].bar(nombres, costos, color=colores, edgecolor='black', alpha=0.85)
    axs[1, 0].set_title('3. Costo Total (H=1, V=2) (Menor es mejor)', fontsize=11, fontweight='bold')
    axs[1, 0].set_ylabel('Costo Acumulado')
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars3:
        yval = bar.get_height()
        axs[1, 0].text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{int(yval)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 4. Longitud de la Ruta
    bars4 = axs[1, 1].bar(nombres, longitudes, color=colores, edgecolor='black', alpha=0.85)
    axs[1, 1].set_title('4. Longitud de la Ruta (Pasos) (Menor es mejor)', fontsize=11, fontweight='bold')
    axs[1, 1].set_ylabel('Cantidad de Pasos')
    axs[1, 1].grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars4:
        yval = bar.get_height()
        axs[1, 1].text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{int(yval)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    if guardar_path:
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"[INFO] Gráfico comparativo guardado exitosamente en: {guardar_path}")
        
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
        
    return fig


# =============================================================================
# INTERFAZ GRÁFICA INTERACTIVA (TKINTER MODERNA)
# =============================================================================

def iniciar_interfaz_grafica():
    """
    Inicia la interfaz gráfica moderna desarrollada en Tkinter.
    """
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog

    class InterfazLaberinto:
        def __init__(self, root: tk.Tk):
            self.root = root
            self.root.title("Sistema Inteligente de Búsqueda y Navegación en Laberintos - PUCE")
            self.root.geometry("1200x820")
            self.root.minsize(1050, 700)
            
            # Paleta de colores UI
            self.COLOR_FONDO = "#f4f6f9"
            self.COLOR_PANEL = "#ffffff"
            self.COLOR_PRIMARIO = "#1a365d"
            self.COLOR_SECUNDARIO = "#2b6cb0"
            self.COLOR_INICIO = "#38a169"     # Verde
            self.COLOR_META = "#e53e3e"       # Rojo
            self.COLOR_MURO = "#2d3748"       # Gris Oscuro / Muro
            self.COLOR_LIBRE = "#edf2f7"      # Gris muy claro / Celda Libre
            self.COLOR_EXPLORADO = "#fefcbf"  # Amarillo pastel suave
            self.COLOR_FRONTERA = "#bee3f8"   # Azul pastel
            self.COLOR_RUTA = "#3182ce"       # Azul brillante / Solución
            self.COLOR_TEXTO = "#1a202c"
            
            self.root.configure(bg=self.COLOR_FONDO)
            
            # Estado del laberinto
            self.laberinto = copy.deepcopy(PRESETS_LABERINTOS["1. Ejemplo Oficial PDF (5x5)"])
            self.modo_edicion = tk.StringVar(value="muro")
            self.algoritmo_seleccionado = tk.StringVar(value="A*")
            self.preset_seleccionado = tk.StringVar(value="1. Ejemplo Oficial PDF (5x5)")
            self.velocidad_animacion = tk.IntVar(value=30)
            self.animacion_activa = False
            self.cancelar_animacion = False
            self.resultados_comparacion: Optional[Dict[str, Dict[str, Any]]] = None
            
            self._configurar_estilos()
            self._construir_interfaz()
            self._dibujar_laberinto_completo()

        def _configurar_estilos(self):
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('.', font=('Segoe UI', 10))
            style.configure('TFrame', background=self.COLOR_FONDO)
            style.configure('Panel.TFrame', background=self.COLOR_PANEL, relief='flat')
            style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.COLOR_PRIMARIO, background=self.COLOR_PANEL)
            style.configure('SubHeader.TLabel', font=('Segoe UI', 11, 'bold'), foreground=self.COLOR_SECUNDARIO, background=self.COLOR_PANEL)
            style.configure('Normal.TLabel', background=self.COLOR_PANEL, foreground=self.COLOR_TEXTO)
            style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), background=self.COLOR_SECUNDARIO, foreground='#ffffff')
            style.map('Accent.TButton', background=[('active', '#2b5282')])

        def _construir_interfaz(self):
            # Barra de encabezado
            header_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARIO, height=55)
            header_frame.pack(fill=tk.X, side=tk.TOP)
            
            lbl_title = tk.Label(
                header_frame, 
                text="🤖 Sistema Inteligente de Búsqueda y Navegación en Laberintos", 
                font=('Segoe UI', 14, 'bold'), 
                fg='#ffffff', 
                bg=self.COLOR_PRIMARIO,
                padx=15, 
                pady=10
            )
            lbl_title.pack(side=tk.LEFT)
            
            lbl_author = tk.Label(
                header_frame, 
                text="PUCE | Fundamentos de IA | Isaac Oña", 
                font=('Segoe UI', 10), 
                fg='#cbd5e0', 
                bg=self.COLOR_PRIMARIO,
                padx=15
            )
            lbl_author.pack(side=tk.RIGHT)

            # Contenedor Principal (Panel Izquierdo de Controles + Panel Central de Canvas y Métricas)
            main_container = tk.Frame(self.root, bg=self.COLOR_FONDO, padx=10, pady=10)
            main_container.pack(fill=tk.BOTH, expand=True)

            # === PANEL IZQUIERDO: CONTROLES ===
            panel_izq = tk.Frame(main_container, bg=self.COLOR_PANEL, bd=1, relief=tk.SOLID, padx=12, pady=12, width=340)
            panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            panel_izq.pack_propagate(False)

            # 1. Presets de Laberinto
            lbl_p = tk.Label(panel_izq, text="1. Configuración del Laberinto", font=('Segoe UI', 11, 'bold'), bg=self.COLOR_PANEL, fg=self.COLOR_PRIMARIO)
            lbl_p.pack(anchor=tk.W, pady=(0, 4))
            
            cb_presets = ttk.Combobox(panel_izq, textvariable=self.preset_seleccionado, values=list(PRESETS_LABERINTOS.keys()), state="readonly", width=30)
            cb_presets.pack(fill=tk.X, pady=(0, 6))
            cb_presets.bind("<<ComboboxSelected>>", self._on_preset_cambiado)

            btn_rnd = tk.Button(panel_izq, text="🎲 Generar Laberinto Aleatorio", bg="#4a5568", fg="#ffffff", font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, cursor="hand2", command=self._generar_aleatorio)
            btn_rnd.pack(fill=tk.X, pady=(0, 8))

            # 2. Herramientas de Edición Interactiva
            lbl_herramientas = tk.Label(panel_izq, text="2. Editor Interactivo (Clic en Rejilla)", font=('Segoe UI', 11, 'bold'), bg=self.COLOR_PANEL, fg=self.COLOR_PRIMARIO)
            lbl_herramientas.pack(anchor=tk.W, pady=(6, 4))

            frame_radios = tk.Frame(panel_izq, bg=self.COLOR_PANEL)
            frame_radios.pack(fill=tk.X, pady=(0, 8))
            
            rb_muro = tk.Radiobutton(frame_radios, text="Pared (1)", variable=self.modo_edicion, value="muro", bg=self.COLOR_PANEL)
            rb_libre = tk.Radiobutton(frame_radios, text="Libre (0)", variable=self.modo_edicion, value="libre", bg=self.COLOR_PANEL)
            rb_inicio = tk.Radiobutton(frame_radios, text="Inicio (S)", variable=self.modo_edicion, value="inicio", bg=self.COLOR_PANEL, fg="#22543d", font=('Segoe UI', 9, 'bold'))
            rb_meta = tk.Radiobutton(frame_radios, text="Meta (G)", variable=self.modo_edicion, value="meta", bg=self.COLOR_PANEL, fg="#742a2a", font=('Segoe UI', 9, 'bold'))
            
            rb_muro.grid(row=0, column=0, sticky=tk.W, padx=2)
            rb_libre.grid(row=0, column=1, sticky=tk.W, padx=2)
            rb_inicio.grid(row=1, column=0, sticky=tk.W, padx=2)
            rb_meta.grid(row=1, column=1, sticky=tk.W, padx=2)

            # 3. Selección de Algoritmo y Ejecución
            lbl_alg = tk.Label(panel_izq, text="3. Algoritmo de Búsqueda", font=('Segoe UI', 11, 'bold'), bg=self.COLOR_PANEL, fg=self.COLOR_PRIMARIO)
            lbl_alg.pack(anchor=tk.W, pady=(6, 4))

            cb_algoritmos = ttk.Combobox(panel_izq, textvariable=self.algoritmo_seleccionado, values=["BFS (Anchura)", "DFS (Profundidad)", "UCS (Costo Uniforme)", "Greedy (Avara)", "A* (A-Estrella)"], state="readonly")
            cb_algoritmos.pack(fill=tk.X, pady=(0, 6))

            # Velocidad de animación
            lbl_speed = tk.Label(panel_izq, text="Velocidad de Animación (ms):", font=('Segoe UI', 9), bg=self.COLOR_PANEL)
            lbl_speed.pack(anchor=tk.W)
            scale_speed = tk.Scale(panel_izq, from_=1, to=150, orient=tk.HORIZONTAL, variable=self.velocidad_animacion, bg=self.COLOR_PANEL, highlightthickness=0)
            scale_speed.pack(fill=tk.X, pady=(0, 8))

            # Botones de Acción
            btn_animar = tk.Button(panel_izq, text="▶ Resolver con Animación", bg="#2b6cb0", fg="#ffffff", font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor="hand2", command=self._resolver_con_animacion)
            btn_animar.pack(fill=tk.X, pady=3)

            btn_instant = tk.Button(panel_izq, text="⚡ Resolver Instantáneo", bg="#319795", fg="#ffffff", font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor="hand2", command=self._resolver_instantaneo)
            btn_instant.pack(fill=tk.X, pady=3)

            btn_comparar = tk.Button(panel_izq, text="📊 Comparar Todos (Benchmark)", bg="#805ad5", fg="#ffffff", font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, cursor="hand2", command=self._comparar_todos_algoritmos)
            btn_comparar.pack(fill=tk.X, pady=3)

            btn_limpiar = tk.Button(panel_izq, text="🔄 Limpiar Ruta / Exploración", bg="#718096", fg="#ffffff", font=('Segoe UI', 9), relief=tk.FLAT, cursor="hand2", command=self._limpiar_visualizacion)
            btn_limpiar.pack(fill=tk.X, pady=3)

            # Leyenda
            lbl_leyenda = tk.Label(panel_izq, text="Leyenda de Costos y Nodos:", font=('Segoe UI', 9, 'bold'), bg=self.COLOR_PANEL, fg=self.COLOR_PRIMARIO)
            lbl_leyenda.pack(anchor=tk.W, pady=(10, 2))
            
            txt_leyenda = "• Inicio: Verde (S) | Meta: Rojo (G)\n• Pared: Muro gris (1) | Libre: Blanco (0)\n• Costo Horizontal = 1 | Costo Vertical = 2\n• Heurística: Manhattan | f(n)=g(n)+h(n)"
            lbl_desc_leyenda = tk.Label(panel_izq, text=txt_leyenda, justify=tk.LEFT, font=('Segoe UI', 8), bg=self.COLOR_PANEL, fg="#4a5568")
            lbl_desc_leyenda.pack(anchor=tk.W)

            # === PANEL CENTRAL: CANVAS DEL LABERINTO + MÉTRICAS ===
            panel_central = tk.Frame(main_container, bg=self.COLOR_PANEL, bd=1, relief=tk.SOLID, padx=10, pady=10)
            panel_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Canvas del Laberinto
            self.canvas_laberinto = tk.Canvas(panel_central, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#cbd5e0")
            self.canvas_laberinto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.canvas_laberinto.bind("<Button-1>", self._on_canvas_click)
            self.canvas_laberinto.bind("<B1-Motion>", self._on_canvas_drag)

            # Tarjetas de Métricas en Tiempo Real (Inferior)
            self.frame_metricas = tk.Frame(panel_central, bg=self.COLOR_PANEL, pady=5)
            self.frame_metricas.pack(fill=tk.X, side=tk.BOTTOM)

            self.card_alg = self._crear_tarjeta_metrica(self.frame_metricas, "Algoritmo", "-", "#2b6cb0")
            self.card_nodos = self._crear_tarjeta_metrica(self.frame_metricas, "Nodos Explorados", "0", "#d95f02")
            self.card_tiempo = self._crear_tarjeta_metrica(self.frame_metricas, "Tiempo Ejecución", "0.00 ms", "#7570b3")
            self.card_costo = self._crear_tarjeta_metrica(self.frame_metricas, "Costo Total (H=1, V=2)", "0", "#e7298a")
            self.card_longitud = self._crear_tarjeta_metrica(self.frame_metricas, "Longitud Ruta", "0 pasos", "#1b9e77")

            self.card_alg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
            self.card_nodos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
            self.card_tiempo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
            self.card_costo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
            self.card_longitud.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

            # Barra de Estado
            self.status_var = tk.StringVar(value="Sistema listo. Seleccione un algoritmo o preset para comenzar.")
            status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Segoe UI', 9), bg="#e2e8f0", fg="#2d3748", padx=10, pady=3)
            status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        def _crear_tarjeta_metrica(self, parent, titulo, valor_inicial, color_acento):
            card = tk.Frame(parent, bg="#edf2f7", bd=1, relief=tk.GROOVE, padx=8, pady=6)
            lbl_t = tk.Label(card, text=titulo, font=('Segoe UI', 8, 'bold'), fg=color_acento, bg="#edf2f7")
            lbl_t.pack(anchor=tk.CENTER)
            lbl_v = tk.Label(card, text=valor_inicial, font=('Segoe UI', 11, 'bold'), fg="#1a202c", bg="#edf2f7")
            lbl_v.pack(anchor=tk.CENTER)
            card.lbl_valor = lbl_v  # Guardar referencia
            return card

        def _actualizar_tarjetas_metricas(self, nombre_alg: str, nodos: int, tiempo_ms: float, costo: int, longitud: int):
            self.card_alg.lbl_valor.config(text=nombre_alg)
            self.card_nodos.lbl_valor.config(text=str(nodos))
            self.card_tiempo.lbl_valor.config(text=f"{tiempo_ms:.3f} ms")
            self.card_costo.lbl_valor.config(text=str(costo))
            self.card_longitud.lbl_valor.config(text=f"{longitud} pasos")

        def _dibujar_laberinto_completo(self, ruta: Optional[List[Tuple[int, int]]] = None, explorados: Optional[List[Tuple[int, int]]] = None):
            self.canvas_laberinto.delete("all")
            filas = len(self.laberinto)
            cols = len(self.laberinto[0])
            
            c_width = self.canvas_laberinto.winfo_width()
            c_height = self.canvas_laberinto.winfo_height()
            
            if c_width <= 1 or c_height <= 1:
                c_width = 750
                c_height = 550
                
            cell_size = min((c_width - 40) // cols, (c_height - 40) // filas)
            cell_size = max(18, min(cell_size, 65))
            
            offset_x = (c_width - (cols * cell_size)) // 2
            offset_y = (c_height - (filas * cell_size)) // 2
            
            self.cell_size = cell_size
            self.offset_x = offset_x
            self.offset_y = offset_y
            
            set_ruta = set(ruta) if ruta else set()
            set_explorados = set(explorados) if explorados else set()
            
            inicio, meta = encontrar_inicio_meta(self.laberinto)

            for r in range(filas):
                for c in range(cols):
                    x1 = offset_x + c * cell_size
                    y1 = offset_y + r * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    
                    val = str(self.laberinto[r][c]).strip().upper()
                    
                    # Determinar color de relleno
                    if (r, c) == inicio:
                        fill_color = self.COLOR_INICIO
                        txt = "S"
                        txt_color = "#ffffff"
                    elif (r, c) == meta:
                        fill_color = self.COLOR_META
                        txt = "G"
                        txt_color = "#ffffff"
                    elif (r, c) in set_ruta:
                        fill_color = self.COLOR_RUTA
                        txt = "●"
                        txt_color = "#ffffff"
                    elif (r, c) in set_explorados:
                        fill_color = self.COLOR_EXPLORADO
                        txt = ""
                        txt_color = "#000000"
                    elif val == '1':
                        fill_color = self.COLOR_MURO
                        txt = ""
                        txt_color = "#000000"
                    else:
                        fill_color = self.COLOR_LIBRE
                        txt = ""
                        txt_color = "#a0aec0"
                        
                    tag = f"cell_{r}_{c}"
                    self.canvas_laberinto.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#cbd5e0", width=1, tags=tag)
                    
                    if txt:
                        font_size = max(9, int(cell_size * 0.45))
                        self.canvas_laberinto.create_text((x1 + x2)/2, (y1 + y2)/2, text=txt, fill=txt_color, font=('Segoe UI', font_size, 'bold'), tags=f"txt_{r}_{c}")

            # Dibujar línea trazadora de la ruta si existe
            if ruta and len(ruta) > 1:
                coords_linea = []
                for (r, c) in ruta:
                    cx = offset_x + c * cell_size + cell_size / 2
                    cy = offset_y + r * cell_size + cell_size / 2
                    coords_linea.extend([cx, cy])
                self.canvas_laberinto.create_line(coords_linea, fill="#ecc94b", width=max(3, int(cell_size * 0.18)), capstyle=tk.ROUND, joinstyle=tk.ROUND, tags="path_line")

        def _on_canvas_click(self, event):
            self._aplicar_edicion_celda(event.x, event.y)

        def _on_canvas_drag(self, event):
            if self.modo_edicion.get() in ["muro", "libre"]:
                self._aplicar_edicion_celda(event.x, event.y)

        def _aplicar_edicion_celda(self, x: int, y: int):
            if not hasattr(self, 'cell_size') or self.animacion_activa:
                return
                
            c = (x - self.offset_x) // self.cell_size
            r = (y - self.offset_y) // self.cell_size
            
            filas = len(self.laberinto)
            cols = len(self.laberinto[0])
            
            if 0 <= r < filas and 0 <= c < cols:
                modo = self.modo_edicion.get()
                
                if modo == "muro":
                    if self.laberinto[r][c] not in ['S', 'G']:
                        self.laberinto[r][c] = '1'
                elif modo == "libre":
                    if self.laberinto[r][c] not in ['S', 'G']:
                        self.laberinto[r][c] = '0'
                elif modo == "inicio":
                    # Limpiar inicio previo
                    for i in range(filas):
                        for j in range(cols):
                            if self.laberinto[i][j] == 'S':
                                self.laberinto[i][j] = '0'
                    self.laberinto[r][c] = 'S'
                elif modo == "meta":
                    # Limpiar meta previa
                    for i in range(filas):
                        for j in range(cols):
                            if self.laberinto[i][j] == 'G':
                                self.laberinto[i][j] = '0'
                    self.laberinto[r][c] = 'G'
                    
                self._dibujar_laberinto_completo()

        def _on_preset_cambiado(self, event=None):
            seleccion = self.preset_seleccionado.get()
            if seleccion in PRESETS_LABERINTOS:
                self.laberinto = copy.deepcopy(PRESETS_LABERINTOS[seleccion])
                self._limpiar_visualizacion()
                self.status_var.set(f"Preset cargado: {seleccion}")

        def _generar_aleatorio(self):
            filas = len(self.laberinto)
            cols = len(self.laberinto[0])
            self.laberinto = generar_laberinto_aleatorio(filas, cols, densidad_muros=0.28)
            self._limpiar_visualizacion()
            self.status_var.set(f"Laberinto aleatorio solvable generado ({filas}x{cols}).")

        def _limpiar_visualizacion(self):
            self.cancelar_animacion = True
            self.animacion_activa = False
            self._dibujar_laberinto_completo()
            self._actualizar_tarjetas_metricas("-", 0, 0.0, 0, 0)
            self.status_var.set("Visualización limpia.")

        def _obtener_funcion_algoritmo(self):
            alg_str = self.algoritmo_seleccionado.get()
            if "BFS" in alg_str:
                return "BFS", bfs
            elif "DFS" in alg_str:
                return "DFS", dfs
            elif "UCS" in alg_str:
                return "UCS", ucs
            elif "Greedy" in alg_str:
                return "Greedy", greedy
            elif "A*" in alg_str:
                return "A*", a_star
            return "A*", a_star

        def _resolver_instantaneo(self):
            nombre_alg, fn = self._obtener_funcion_algoritmo()
            ruta, nodos, t_exec, costo, longitud, exploracion = fn(self.laberinto, registrar_exploracion=True)
            
            if ruta is None:
                messagebox.showwarning("Sin Solución", f"El algoritmo {nombre_alg} determinó que no existe una ruta transitable hacia la meta.")
                self.status_var.set(f"{nombre_alg}: No se encontró solución.")
                return
                
            self._actualizar_tarjetas_metricas(nombre_alg, nodos, t_exec * 1000.0, costo, longitud)
            self._dibujar_laberinto_completo(ruta=ruta, explorados=exploracion)
            self.status_var.set(f"✅ {nombre_alg} resuelto exitosamente | Costo: {costo} | Nodos: {nodos} | Tiempo: {t_exec*1000:.3f} ms")

        def _resolver_con_animacion(self):
            if self.animacion_activa:
                return
                
            nombre_alg, fn = self._obtener_funcion_algoritmo()
            ruta, nodos, t_exec, costo, longitud, exploracion = fn(self.laberinto, registrar_exploracion=True)
            
            if ruta is None:
                messagebox.showwarning("Sin Solución", f"El algoritmo {nombre_alg} determinó que no existe una ruta transitable hacia la meta.")
                return
                
            self.animacion_activa = True
            self.cancelar_animacion = False
            self.status_var.set(f"Animando exploración de {nombre_alg}...")
            
            # Limpiar canvas inicial
            self._dibujar_laberinto_completo()
            
            inicio, meta = encontrar_inicio_meta(self.laberinto)
            idx_exp = 0
            
            def paso_exploracion():
                nonlocal idx_exp
                if self.cancelar_animacion:
                    self.animacion_activa = False
                    return
                    
                if idx_exp < len(exploracion):
                    nodo = exploracion[idx_exp]
                    if nodo != inicio and nodo != meta:
                        r, c = nodo
                        x1 = self.offset_x + c * self.cell_size
                        y1 = self.offset_y + r * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        self.canvas_laberinto.create_rectangle(x1, y1, x2, y2, fill=self.COLOR_EXPLORADO, outline="#cbd5e0", width=1)
                    idx_exp += 1
                    self.root.after(self.velocidad_animacion.get(), paso_exploracion)
                else:
                    # Animar la ruta final paso a paso
                    idx_ruta = 0
                    def paso_ruta():
                        nonlocal idx_ruta
                        if self.cancelar_animacion:
                            self.animacion_activa = False
                            return
                        if idx_ruta < len(ruta):
                            r, c = ruta[idx_ruta]
                            if (r, c) != inicio and (r, c) != meta:
                                x1 = self.offset_x + c * self.cell_size
                                y1 = self.offset_y + r * self.cell_size
                                x2 = x1 + self.cell_size
                                y2 = y1 + self.cell_size
                                self.canvas_laberinto.create_rectangle(x1, y1, x2, y2, fill=self.COLOR_RUTA, outline="#cbd5e0", width=1)
                                self.canvas_laberinto.create_text((x1+x2)/2, (y1+y2)/2, text="●", fill="#ffffff", font=('Segoe UI', int(self.cell_size*0.45), 'bold'))
                            idx_ruta += 1
                            self.root.after(self.velocidad_animacion.get() * 2, paso_ruta)
                        else:
                            # Dibujar línea final completa
                            self._dibujar_laberinto_completo(ruta=ruta, explorados=exploracion)
                            self._actualizar_tarjetas_metricas(nombre_alg, nodos, t_exec * 1000.0, costo, longitud)
                            self.animacion_activa = False
                            self.status_var.set(f"✅ Animación completada: {nombre_alg} | Costo: {costo} | Nodos: {nodos} | Tiempo: {t_exec*1000:.3f} ms")
                            
                    paso_ruta()
                    
            paso_exploracion()

        def _comparar_todos_algoritmos(self):
            self.resultados_comparacion = ejecutar_todos(self.laberinto)
            
            # Ventana emergente de reporte y comparación
            win = tk.Toplevel(self.root)
            win.title("📊 Comparación Integral de Desempeño - Algoritmos de Búsqueda")
            win.geometry("880x560")
            win.configure(bg=self.COLOR_FONDO)
            win.transient(self.root)
            
            lbl_title = tk.Label(win, text="Tabla Comparativa de Métricas de Desempeño", font=('Segoe UI', 13, 'bold'), bg=self.COLOR_FONDO, fg=self.COLOR_PRIMARIO, pady=10)
            lbl_title.pack()

            # Tabla Treeview
            columns = ("Métrica", "BFS", "DFS", "UCS", "Greedy", "A*")
            tree = ttk.Treeview(win, columns=columns, show="headings", height=6)
            
            tree.heading("Métrica", text="Métrica Evaluada")
            for col in ["BFS", "DFS", "UCS", "Greedy", "A*"]:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.CENTER, width=120)
            tree.column("Métrica", anchor=tk.W, width=220)

            # Insertar filas
            res = self.resultados_comparacion
            tree.insert("", tk.END, values=("Nodos explorados", res["BFS"]["nodos_explorados"], res["DFS"]["nodos_explorados"], res["UCS"]["nodos_explorados"], res["Greedy"]["nodos_explorados"], res["A*"]["nodos_explorados"]))
            tree.insert("", tk.END, values=("Tiempo ejecución (ms)", f"{res['BFS']['tiempo_ms']:.4f}", f"{res['DFS']['tiempo_ms']:.4f}", f"{res['UCS']['tiempo_ms']:.4f}", f"{res['Greedy']['tiempo_ms']:.4f}", f"{res['A*']['tiempo_ms']:.4f}"))
            tree.insert("", tk.END, values=("Costo total (H=1, V=2)", res["BFS"]["costo_total"], res["DFS"]["costo_total"], res["UCS"]["costo_total"], res["Greedy"]["costo_total"], res["A*"]["costo_total"]))
            tree.insert("", tk.END, values=("Longitud ruta (pasos)", res["BFS"]["longitud_ruta"], res["DFS"]["longitud_ruta"], res["UCS"]["longitud_ruta"], res["Greedy"]["longitud_ruta"], res["A*"]["longitud_ruta"]))
            tree.insert("", tk.END, values=("¿Ruta Óptima en Costo?", "No (salvo coincidencia)", "No", "Sí (Garantizado)", "No (Heurística pura)", "Sí (Garantizado)"))
            tree.pack(fill=tk.X, padx=20, pady=10)

            # Botón para generar y guardar gráficos Matplotlib
            def ver_graficos():
                generar_graficos_comparativos(self.resultados_comparacion, guardar_path="grafico_comparativo.png", mostrar=True)
                messagebox.showinfo("Gráfico Generado", "El gráfico comparativo de alta resolución se ha guardado como 'grafico_comparativo.png'.")

            frame_btn = tk.Frame(win, bg=self.COLOR_FONDO)
            frame_btn.pack(pady=15)
            
            btn_ver_graf = tk.Button(frame_btn, text="📈 Ver y Exportar Gráficos Comparativos (Matplotlib)", bg="#2b6cb0", fg="#ffffff", font=('Segoe UI', 10, 'bold'), padx=15, pady=6, relief=tk.FLAT, cursor="hand2", command=ver_graficos)
            btn_ver_graf.pack(side=tk.LEFT, padx=10)

            btn_cerrar = tk.Button(frame_btn, text="Cerrar", bg="#718096", fg="#ffffff", font=('Segoe UI', 10), padx=15, pady=6, relief=tk.FLAT, cursor="hand2", command=win.destroy)
            btn_cerrar.pack(side=tk.LEFT, padx=10)

    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()


# =============================================================================
# EJECUCIÓN PRINCIPAL / CLI / BENCHMARK
# =============================================================================

def ejecutar_benchmark_consola():
    """
    Ejecuta el benchmark en consola sobre todos los presets disponibles y muestra tablas formateadas.
    """
    print("=" * 80)
    print("SISTEMA INTELIGENTE DE BÚSQUEDA Y NAVEGACIÓN EN LABERINTOS")
    print("PUCE - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL")
    print("Autor: Isaac Oña | Docente: Ing. Patricio Alvear | NRC: 1371")
    print("=" * 80)

    for nombre_mapa, matriz in PRESETS_LABERINTOS.items():
        print(f"\n>>> EVALUANDO: {nombre_mapa} ({len(matriz)}x{len(matriz[0])})")
        print("-" * 80)
        res = ejecutar_todos(matriz)
        
        print(f"{'Métrica':<25} | {'BFS':<10} | {'DFS':<10} | {'UCS':<10} | {'Greedy':<10} | {'A*':<10}")
        print("-" * 80)
        print(f"{'Nodos explorados':<25} | {res['BFS']['nodos_explorados']:<10} | {res['DFS']['nodos_explorados']:<10} | {res['UCS']['nodos_explorados']:<10} | {res['Greedy']['nodos_explorados']:<10} | {res['A*']['nodos_explorados']:<10}")
        print(f"{'Tiempo ejecución (ms)':<25} | {res['BFS']['tiempo_ms']:<10.4f} | {res['DFS']['tiempo_ms']:<10.4f} | {res['UCS']['tiempo_ms']:<10.4f} | {res['Greedy']['tiempo_ms']:<10.4f} | {res['A*']['tiempo_ms']:<10.4f}")
        print(f"{'Costo total (H=1, V=2)':<25} | {res['BFS']['costo_total']:<10} | {res['DFS']['costo_total']:<10} | {res['UCS']['costo_total']:<10} | {res['Greedy']['costo_total']:<10} | {res['A*']['costo_total']:<10}")
        print(f"{'Longitud ruta (pasos)':<25} | {res['BFS']['longitud_ruta']:<10} | {res['DFS']['longitud_ruta']:<10} | {res['UCS']['longitud_ruta']:<10} | {res['Greedy']['longitud_ruta']:<10} | {res['A*']['longitud_ruta']:<10}")
        print("-" * 80)

    # Generar gráfico para el ejemplo oficial
    mapa_oficial = PRESETS_LABERINTOS["1. Ejemplo Oficial PDF (5x5)"]
    res_oficial = ejecutar_todos(mapa_oficial)
    generar_graficos_comparativos(res_oficial, guardar_path="grafico_comparativo_oficial.png", mostrar=False)
    print("\n[INFO] Gráfico comparativo generado: grafico_comparativo_oficial.png")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--benchmark", "--cli", "-b"]:
        ejecutar_benchmark_consola()
    else:
        # Por defecto, iniciar interfaz gráfica si está en entorno de escritorio
        try:
            iniciar_interfaz_grafica()
        except Exception as e:
            print(f"[AVISO] No se pudo inicializar la GUI ({e}). Ejecutando en modo consola...")
            ejecutar_benchmark_consola()