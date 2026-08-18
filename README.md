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

Este repositorio contiene el desarrollo, implementación y benchmarking experimental de un **Sistema Inteligente de Búsqueda y Navegación en Laberintos**, diseñado para modelar y resolver el problema de navegación autónoma de robots de búsqueda y rescate (USAR) en estructuras y edificaciones colapsadas.

El sistema modela el entorno físico como una matriz bidimensional $M \times N$ sujeta a restricciones de transitabilidad y a un **modelo de costos asimétricos**:
* **Movimiento Horizontal (Izquierda / Derecha):** Costo = **1**
* **Movimiento Vertical (Arriba / Abajo):** Costo = **2** *(simulación de resistencia gravitacional y esfuerzo mecánico sobre pendientes y escombros)*

---

## 🧠 Algoritmos Implementados

| Tipo de Búsqueda | Algoritmo | Estructura de Datos | Heurística | Garantía de Optimalidad |
| :--- | :--- | :--- | :--- | :--- |
| **No Informada (Ciega)** | **BFS** (Breadth-First Search) | Cola FIFO (`deque`) | Ninguna | Óptimo en cantidad de pasos |
| **No Informada (Ciega)** | **DFS** (Depth-First Search) | Pila LIFO (`list`) | Ninguna | No óptimo (explora ramas) |
| **No Informada (Ciega)** | **UCS** (Uniform Cost Search) | Min-Heap (`heapq` por $g(n)$) | Ninguna | **Óptimo en costo acumulado** |
| **Informada (Heurística)** | **Greedy** (Avara Best-First) | Min-Heap (`heapq` por $h(n)$) | Manhattan $h(n)$ | Rápido / No garantizado |
| **Informada (Heurística)** | **A\*** (A-Star Search) | Min-Heap (`heapq` por $f=g+h$) | Manhattan $h(n)$ | **Óptimo en costo acumulado** |

### 📐 Función Heurística (Distancia Manhattan)
$$h(n) = |x_{\text{actual}} - x_{\text{meta}}| + |y_{\text{actual}} - y_{\text{meta}}|$$
* **Admisible:** $h(n) \le h^*(n)$ (nunca sobrestima el costo real).
* **Consistente:** $h(n) \le c(n, a, n') + h(n')$ (cumple con la desigualdad triangular).

---

## 🚀 Características Principales

1. **Interfaz Gráfica Interactiva (Tkinter):**
   * Editor de laberintos en vivo (dibujar muros, celdas transitables, punto de inicio `S` y meta `G` con el ratón).
   * Animación paso a paso de la frontera de búsqueda (amarillo) y ruta solución (azul).
   * Control de velocidad en milisegundos (1 ms a 150 ms) y modo de resolución instantánea.
   * Carga de presets y generador estocástico de laberintos solvables.
   * Tarjetas de métricas en tiempo real y modal de benchmarking con tablas `Treeview`.
2. **Motor de Benchmarking y Gráficos Estadísticos:**
   * Comparación de los 5 algoritmos en consola.
   * Generación automatizada de gráficos comparativos de alta resolución en 2x2 (Matplotlib).
3. **Informe Técnico Académico:**
   * Documento Word formal bajo formato APA 7ma Edición (`Proyecto Final Fundamentos de Inteligencia Artificial.docx`).

---

## 📊 Resultados de Rendimiento (Benchmark Laberinto Oficial 5x5)

```
MÉTRICA                   | BFS        | DFS        | UCS        | Greedy     | A*        
--------------------------------------------------------------------------------
Nodos explorados          | 16         | 12         | 16         | 10         | 12        
Tiempo ejecución (ms)     | 0.0631     | 0.0388     | 0.0590     | 0.0382     | 0.0464    
Costo total (H=1, V=2)    | 13         | 15         | 13         | 13         | 13        
Longitud ruta (pasos)     | 9          | 11         | 9          | 9          | 9         
¿Ruta Óptima en Costo?    | Sí         | No         | Sí         | Sí         | Sí        
```

---

## 🛠️ Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/PROYECTO_NOMBRE.git
cd PROYECTO_NOMBRE
```

### 2. Instalar dependencias opcionales
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación Interactiva (GUI)
```bash
python ProyectoFinal.py
```

### 4. Ejecutar el Benchmark por Consola
```bash
python ProyectoFinal.py --benchmark
```

### 5. Recompilar el Informe en Word
```bash
python generate_report.py
```

---

## 📁 Estructura del Repositorio

```
.
├── ProyectoFinal.py                                    # Aplicación principal (Algoritmos + GUI + CLI)
├── generate_report.py                                  # Script de generación del informe APA 7
├── Proyecto Final Fundamentos de Inteligencia Artificial.docx # Informe técnico formal en Word
├── Resultados_y_Plan_Implementacion.txt                # Plan de implementación y datos de benchmark
├── PROYECTO FINAL FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (1).pdf # Guía oficial de requerimientos
├── requirements.txt                                    # Dependencias de Python
├── .gitignore                                          # Archivos y carpetas ignorados por Git
├── README.md                                           # Documentación del repositorio
└── *.png                                               # Gráficos estadísticos y mapas visuales
```

---

## 👨‍💻 Autor

* **Isaac Oña** — Pontificia Universidad Católica del Ecuador (PUCE).
