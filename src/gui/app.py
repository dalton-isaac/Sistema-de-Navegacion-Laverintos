"""
===============================================================================
MÓDULO: INTERFAZ GRÁFICA DE USUARIO INTERACTIVA (TKINTER)
Sistema Inteligente de Búsqueda y Navegación en Laberintos - PUCE
===============================================================================
Descripción:
Implementa la interfaz gráfica moderna en Tkinter con:
  • Editor interactivo de rejilla (muros, celdas libres, inicio, meta).
  • Animación paso a paso de la frontera de exploración y ruta solución.
  • Control de velocidad en milisegundos y resolución instantánea.
  • Presets oficiales de prueba y generador estocástico solvable.
  • Tarjetas de métricas en tiempo real.
  • Modal de benchmarking comparativo con tabla Treeview y exportación Matplotlib.
===============================================================================
"""

import copy
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict, Optional, Any

from ..core import (
    PRESETS_LABERINTOS,
    encontrar_inicio_meta,
    bfs,
    dfs,
    ucs,
    greedy,
    a_star,
    ejecutar_todos,
    generar_laberinto_aleatorio
)
from ..utils import generar_graficos_comparativos

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


class InterfazLaberinto:
    """Clase principal que gestiona el estado, canvas y eventos de la GUI."""

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

        # Contenedor Principal (Panel Izquierdo + Panel Central)
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

        # === PANEL CENTRAL: CANVAS + MÉTRICAS ===
        panel_central = tk.Frame(main_container, bg=self.COLOR_PANEL, bd=1, relief=tk.SOLID, padx=10, pady=10)
        panel_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_laberinto = tk.Canvas(panel_central, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#cbd5e0")
        self.canvas_laberinto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_laberinto.bind("<Button-1>", self._on_canvas_click)
        self.canvas_laberinto.bind("<B1-Motion>", self._on_canvas_drag)

        # Tarjetas de Métricas en Tiempo Real
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
        card.lbl_valor = lbl_v
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
                for i in range(filas):
                    for j in range(cols):
                        if self.laberinto[i][j] == 'S':
                            self.laberinto[i][j] = '0'
                self.laberinto[r][c] = 'S'
            elif modo == "meta":
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
                        self._dibujar_laberinto_completo(ruta=ruta, explorados=exploracion)
                        self._actualizar_tarjetas_metricas(nombre_alg, nodos, t_exec * 1000.0, costo, longitud)
                        self.animacion_activa = False
                        self.status_var.set(f"✅ Animación completada: {nombre_alg} | Costo: {costo} | Nodos: {nodos} | Tiempo: {t_exec*1000:.3f} ms")
                        
                paso_ruta()
                
        paso_exploracion()

    def _comparar_todos_algoritmos(self):
        self.resultados_comparacion = ejecutar_todos(self.laberinto)
        
        win = tk.Toplevel(self.root)
        win.title("📊 Comparación Integral de Desempeño - Algoritmos de Búsqueda")
        win.geometry("880x560")
        win.configure(bg=self.COLOR_FONDO)
        win.transient(self.root)
        
        lbl_title = tk.Label(win, text="Tabla Comparativa de Métricas de Desempeño", font=('Segoe UI', 13, 'bold'), bg=self.COLOR_FONDO, fg=self.COLOR_PRIMARIO, pady=10)
        lbl_title.pack()

        columns = ("Métrica", "BFS", "DFS", "UCS", "Greedy", "A*")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=6)
        
        tree.heading("Métrica", text="Métrica Evaluada")
        for col in ["BFS", "DFS", "UCS", "Greedy", "A*"]:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=120)
        tree.column("Métrica", anchor=tk.W, width=220)

        res = self.resultados_comparacion
        tree.insert("", tk.END, values=("Nodos explorados", res["BFS"]["nodos_explorados"], res["DFS"]["nodos_explorados"], res["UCS"]["nodos_explorados"], res["Greedy"]["nodos_explorados"], res["A*"]["nodos_explorados"]))
        tree.insert("", tk.END, values=("Tiempo ejecución (ms)", f"{res['BFS']['tiempo_ms']:.4f}", f"{res['DFS']['tiempo_ms']:.4f}", f"{res['UCS']['tiempo_ms']:.4f}", f"{res['Greedy']['tiempo_ms']:.4f}", f"{res['A*']['tiempo_ms']:.4f}"))
        tree.insert("", tk.END, values=("Costo total (H=1, V=2)", res["BFS"]["costo_total"], res["DFS"]["costo_total"], res["UCS"]["costo_total"], res["Greedy"]["costo_total"], res["A*"]["costo_total"]))
        tree.insert("", tk.END, values=("Longitud ruta (pasos)", res["BFS"]["longitud_ruta"], res["DFS"]["longitud_ruta"], res["UCS"]["longitud_ruta"], res["Greedy"]["longitud_ruta"], res["A*"]["longitud_ruta"]))
        tree.insert("", tk.END, values=("¿Ruta Óptima en Costo?", "No (salvo coincidencia)", "No", "Sí (Garantizado)", "No (Heurística pura)", "Sí (Garantizado)"))
        tree.pack(fill=tk.X, padx=20, pady=10)

        def ver_graficos():
            save_dest = os.path.join(ASSETS_DIR, "grafico_comparativo.png")
            generar_graficos_comparativos(self.resultados_comparacion, guardar_path=save_dest, mostrar=True)
            messagebox.showinfo("Gráfico Generado", f"El gráfico comparativo de alta resolución se ha guardado en:\n{save_dest}")

        frame_btn = tk.Frame(win, bg=self.COLOR_FONDO)
        frame_btn.pack(pady=15)
        
        btn_ver_graf = tk.Button(frame_btn, text="📈 Ver y Exportar Gráficos Comparativos (Matplotlib)", bg="#2b6cb0", fg="#ffffff", font=('Segoe UI', 10, 'bold'), padx=15, pady=6, relief=tk.FLAT, cursor="hand2", command=ver_graficos)
        btn_ver_graf.pack(side=tk.LEFT, padx=10)

        btn_cerrar = tk.Button(frame_btn, text="Cerrar", bg="#718096", fg="#ffffff", font=('Segoe UI', 10), padx=15, pady=6, relief=tk.FLAT, cursor="hand2", command=win.destroy)
        btn_cerrar.pack(side=tk.LEFT, padx=10)


def iniciar_interfaz_grafica():
    """Inicializa la ventana principal de la interfaz gráfica Tkinter."""
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()
