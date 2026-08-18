"""
===============================================================================
MÓDULO: HEURÍSTICAS Y MODELO DE COSTOS
Sistema Inteligente de Búsqueda y Navegación en Laberintos - PUCE
===============================================================================
Descripción:
Define las constantes de movimiento, costos diferenciados (H=1, V=2),
la función heurística Manhattan admisible y consistente, y funciones de
validación de transitabilidad sobre la matriz del laberinto.
===============================================================================
"""

from typing import List, Tuple, Dict, Optional

# --- CONFIGURACIÓN DE MOVIMIENTOS Y COSTOS ASIMÉTRICOS ---
# Movimiento Horizontal (Izquierda / Derecha): Costo = 1
# Movimiento Vertical (Arriba / Abajo): Costo = 2 (resistencia gravitacional / física)
MOVIMIENTOS: Dict[Tuple[int, int], int] = {
    (0, 1): 1,   # Derecha (Horizontal)
    (0, -1): 1,  # Izquierda (Horizontal)
    (1, 0): 2,   # Abajo (Vertical)
    (-1, 0): 2   # Arriba (Vertical)
}

NOMBRES_MOVIMIENTOS: Dict[Tuple[int, int], str] = {
    (0, 1): "Derecha",
    (0, -1): "Izquierda",
    (1, 0): "Abajo",
    (-1, 0): "Arriba"
}


def heuristica_manhattan(actual: Tuple[int, int], meta: Tuple[int, int]) -> int:
    """
    Calcula la distancia Manhattan entre el nodo actual y el objetivo.
    Fórmula: h(n) = |x_actual - x_meta| + |y_actual - y_meta|
    
    Propiedades:
      - Admisible: h(n) <= h*(n) (nunca sobrestima el costo real).
      - Consistente (Monótona): h(n) <= c(n, a, n') + h(n').
    """
    return abs(actual[0] - meta[0]) + abs(actual[1] - meta[1])


def encontrar_inicio_meta(laberinto: List[List[str]]) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """
    Localiza las coordenadas del nodo de inicio ('S') y de la meta ('G') en la matriz.
    
    Retorna:
        Tuple (inicio, meta) donde cada elemento es (fila, columna) o None si no existe.
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
