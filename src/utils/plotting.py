"""
===============================================================================
MÓDULO: GENERADOR DE GRÁFICOS COMPARATIVOS (MATPLOTLIB)
Sistema Inteligente de Búsqueda y Navegación en Laberintos - PUCE
===============================================================================
Descripción:
Genera figuras multipanel de alta calidad en 2x2 comparando métricas:
  1. Nodos Explorados
  2. Tiempo de Ejecución (ms)
  3. Costo Total de la Ruta
  4. Longitud de la Ruta (Pasos)
===============================================================================
"""

import os
from typing import Dict, Any, Optional

# Directorio por defecto de assets
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def generar_graficos_comparativos(
    resultados: Dict[str, Dict[str, Any]], 
    guardar_path: Optional[str] = None, 
    mostrar: bool = False
):
    """
    Genera una figura de 2x2 con gráficos de barras de alta resolución comparando:
      1. Nodos Explorados
      2. Tiempo de Ejecución (ms)
      3. Costo Total de la Ruta
      4. Longitud de la Ruta (pasos)
      
    Parámetros:
        resultados: Diccionario devuelto por core.algorithms.ejecutar_todos
        guardar_path: Ruta del archivo de imagen a guardar (por defecto en assets/)
        mostrar: Si es True, despliega la ventana interactiva de Matplotlib
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ADVERTENCIA] matplotlib no está instalado. No se pueden generar gráficos.")
        return None

    if guardar_path is None:
        os.makedirs(ASSETS_DIR, exist_ok=True)
        guardar_path = os.path.join(ASSETS_DIR, "grafico_comparativo.png")

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
    max_t = max(tiempos) if tiempos else 1
    for bar in bars2:
        yval = bar.get_height()
        axs[0, 1].text(bar.get_x() + bar.get_width()/2.0, yval + (max_t * 0.02 if max_t > 0 else 0.001), f'{yval:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

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
        os.makedirs(os.path.dirname(os.path.abspath(guardar_path)), exist_ok=True)
        plt.savefig(guardar_path, dpi=300, bbox_inches='tight')
        print(f"[INFO] Gráfico comparativo guardado exitosamente en: {guardar_path}")
        
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
        
    return fig
