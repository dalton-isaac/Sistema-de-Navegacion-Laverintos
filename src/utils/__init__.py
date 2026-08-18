"""
Módulo de Utilidades del Sistema
================================
Exporta generadores de gráficos y compilador de reportes.
"""

from .plotting import generar_graficos_comparativos
from .report_generator import construir_informe

__all__ = [
    "generar_graficos_comparativos",
    "construir_informe"
]
