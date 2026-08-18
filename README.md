# 🤖 Sistema Inteligente de Búsqueda y Navegación en Laberintos

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![University](https://img.shields.io/badge/PUCE-Facultad%20de%20Ingenier%C3%ADa-1a365d.svg)](https://www.puce.edu.ec/)

> **Proyecto Final - Fundamentos de Inteligencia Artificial (NRC: 1371)**  
> **Pontificia Universidad Católica del Ecuador (PUCE)**  
> **Autor:** Isaac Oña  
> **Docente:** Ing. Patricio Alvear  

---

## 📌 Descripción del Proyecto

Este repositorio contiene el desarrollo, implementación modular y benchmarking experimental de un **Sistema Inteligente de Búsqueda y Navegación en Laberintos**, diseñado para modelar y resolver el problema de planificación de trayectorias y rescate robótico autónomo (USAR) en edificaciones colapsadas.

El sistema modela el entorno físico como una matriz bidimensional $M \times N$ sujeta a restricciones de transitabilidad (muros/escombros) y a un **modelo de costos de movimiento asimétricos**:
* **Movimiento Horizontal (Izquierda / Derecha):** Costo = **1**
* **Movimiento Vertical (Arriba / Abajo):** Costo = **2** *(simulación del esfuerzo motriz y gravitacional sobre pendientes y escombros)*

---

## 🧠 Algoritmos Implementados

| Tipo de Búsqueda | Algoritmo | Estructura de Datos | Heurística | Garantía de Optimalidad |
| :--- | :--- | :--- | :--- | :--- |
| **No Informada (Ciega)** | **BFS** (Breadth-First Search) | Cola FIFO (`collections.deque`) | Ninguna | Óptimo en número de pasos |
| **No Informada (Ciega)** | **DFS** (Depth-First Search) | Pila LIFO (`list`) | Ninguna | No óptimo (vulnerable a desvíos) |
| **No Informada (Ciega)** | **UCS** (Uniform Cost Search) | Min-Heap (`heapq` por $g(n)$) | Ninguna | **Óptimo en costo acumulado** |
| **Informada (Heurística)** | **Greedy** (Avara Best-First) | Min-Heap (`heapq` por $h(n)$) | Manhattan $h(n)$ | Rápido / No óptimo |
| **Informada (Heurística)** | **A\*** (A-Star Search) | Min-Heap (`heapq` por $f=g+h$) | Manhattan $h(n)$ | **Óptimo en costo acumulado** |

### 📐 Función Heurística (Distancia Manhattan)
$$h(n) = |x_{\text{actual}} - x_{\text{meta}}| + |y_{\text{actual}} - y_{\text{meta}}|$$
* **Admisible:** $h(n) \le h^*(n)$ (nunca sobrestima el costo real a la meta).
* **Consistente (Monótona):** $h(n) \le c(n, a, n') + h(n')$ (cumple la desigualdad triangular).

---

## 📁 Arquitectura y Estructura del Proyecto

El código está estructurado de manera modular y desacoplada siguiendo las mejores prácticas de ingeniería de software en Python:

```text
Sistema-de-Navegacion-Laverintos/
├── assets/                                      # Gráficos estadísticos y recursos visuales
│   ├── grafico_comparativo.png
│   ├── grafico_comparativo_oficial.png
│   ├── grafico_preset_1.png
│   ├── grafico_preset_2.png
│   ├── grafico_preset_3.png
│   ├── grafico_preset_4.png
│   ├── mapa_visual_oficial.png
│   ├── mapa_visual_trampa.png
│   └── mapa_visual_urbano.png
├── docs/                                        # Documentación académica y especificaciones
│   ├── PROYECTO FINAL FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (1).pdf
│   ├── Proyecto Final Fundamentos de Inteligencia Artificial.docx
│   └── Resultados_y_Plan_Implementacion.txt
├── src/                                         # Código fuente modularizado del sistema
│   ├── __init__.py                              # Metadata del paquete principal
│   ├── core/                                    # Lógica pura de Inteligencia Artificial
│   │   ├── __init__.py
│   │   ├── algorithms.py                        # Implementación de BFS, DFS, UCS, Greedy y A*
│   │   ├── heuristics.py                        # Modelo de costos y función heurística Manhattan
│   │   └── maze.py                              # Catálogo de presets y generador estocástico
│   ├── gui/                                     # Interfaz Gráfica de Usuario (Tkinter)
│   │   ├── __init__.py
│   │   └── app.py                               # Ventana interactiva, animaciones y canvas
│   └── utils/                                   # Utilidades auxiliares
│       ├── __init__.py
│       ├── plotting.py                          # Generador de gráficos comparativos (Matplotlib)
│       └── report_generator.py                  # Compilador de informe formal APA 7 en Word
├── main.py                                      # Punto de entrada principal (GUI y CLI)
├── ProyectoFinal.py                             # Lanzador raíz de compatibilidad directa
├── generate_report.py                           # Lanzador raíz para generar el reporte Word
├── requirements.txt                             # Dependencias del proyecto
├── .gitignore                                   # Archivos y temporales excluidos de Git
└── README.md                                    # Documentación técnica del repositorio
```

---

## 🚀 Características Principales

1. **Interfaz Gráfica Interactiva (Tkinter):**
   * Editor de laberintos en vivo (dibujar muros, celdas transitables, inicio `S` y meta `G` con el ratón).
   * Animación en tiempo real de la frontera de búsqueda (amarillo) y ruta solución trazada (azul/dorado).
   * Control de velocidad en milisegundos (1 ms a 150 ms) y modo de resolución instantánea.
   * Carga de presets y generador estocástico de laberintos solvables.
   * Tarjetas de métricas en vivo y modal de benchmarking con tablas `Treeview`.
2. **Motor de Benchmarking y Gráficos Estadísticos:**
   * Comparación de los 5 algoritmos en consola con tablas formateadas.
   * Generación automatizada de gráficos comparativos en cuadrícula 2x2 (Matplotlib).
3. **Informe Técnico Académico:**
   * Generador automatizado de documento Word formal bajo formato APA 7ma Edición (`docs/Proyecto Final Fundamentos de Inteligencia Artificial.docx`).

---

## 📊 Resultados de Rendimiento (Benchmark Laberinto Oficial 5x5)

```text
MÉTRICA                   | BFS        | DFS        | UCS        | Greedy     | A*        
-----------------------------------------------------------------------------------------
Nodos explorados          | 16         | 12         | 16         | 10         | 12        
Tiempo ejecución (ms)     | 0.0631     | 0.0388     | 0.0590     | 0.0382     | 0.0464    
Costo total (H=1, V=2)    | 13         | 15         | 13         | 13         | 13        
Longitud ruta (pasos)     | 9          | 11         | 9          | 9          | 9         
¿Ruta Óptima en Costo?    | No*        | No         | Sí (Mín.)  | Coincidente| Sí (Mín.) 
```
*\*BFS optimiza la cantidad de pasos (9), coincidiendo en este caso con el costo óptimo de 13.*

---

## 🛠️ Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/dalton-isaac/Sistema-de-Navegacion-Laverintos.git
cd Sistema-de-Navegacion-Laverintos
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación Interactiva (GUI)
```bash
python main.py
```
*(O de forma equivalente: `python ProyectoFinal.py`)*

### 4. Ejecutar el Benchmark por Consola
```bash
python main.py --benchmark
```

### 5. Compilar el Informe Técnico APA 7 en Word
```bash
python main.py --report
```
*(O mediante el script directo: `python generate_report.py`)*

---

## 👨‍💻 Autor

* **Isaac Oña** — [Pontificia Universidad Católica del Ecuador (PUCE)](https://www.puce.edu.ec/)
