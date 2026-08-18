"""
===============================================================================
MÓDULO: ALGORITMOS DE BÚSQUEDA EN ESPACIOS DE ESTADOS
Sistema Inteligente de Búsqueda y Navegación en Laberintos - PUCE
===============================================================================
Descripción:
Implementa 5 estrategias fundamentales de búsqueda:
  1. Búsqueda en Anchura (BFS) - No informada (Garantiza menor longitud)
  2. Búsqueda en Profundidad (DFS) - No informada (Exploración profunda)
  3. Búsqueda de Costo Uniforme (UCS) - No informada (Garantiza costo óptimo)
  4. Búsqueda Avara / Greedy - Informada por Manhattan (Rápida hacia la meta)
  5. Algoritmo A* (A-Star) - Informada óptima f(n) = g(n) + h(n)
===============================================================================
"""

import time
import heapq
from collections import deque
from typing import List, Tuple, Dict, Optional, Any, Set

from .heuristics import (
    MOVIMIENTOS,
    heuristica_manhattan,
    encontrar_inicio_meta,
    es_celda_transitable,
    calcular_costo_ruta
)


# =============================================================================
# 1. BÚSQUEDA EN ANCHURA (BFS - BREADTH FIRST SEARCH)
# =============================================================================

def bfs(laberinto: List[List[str]], registrar_exploracion: bool = True):
    """
    Algoritmo de Búsqueda en Anchura (BFS).
    Estrategia no informada basada en cola FIFO.
    Garantiza el camino con el menor número de pasos (longitud).
    
    Retorna:
        Tuple: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
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
    
    Retorna:
        Tuple: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
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
    
    Retorna:
        Tuple: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
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
    
    Retorna:
        Tuple: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
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
    
    Retorna:
        Tuple: (ruta, nodos_explorados, tiempo_ejecucion, costo_total, longitud_ruta, orden_exploracion)
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
# REGISTRO Y EJECUCIÓN COLECTIVA DE ALGORITMOS
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
    Ejecuta los 5 algoritmos de búsqueda sobre la matriz dada y recopila
    todas las métricas para análisis comparativo y benchmarking.
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
