import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import csv
import os
from PIL import Image, ImageTk
import webbrowser

from solvers.heun_solver import HeunSolver
from solvers.euler_solver import EulerSolver

class EDOSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de EDOs")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Variables para los campos de entrada
        self.var_funcion = tk.StringVar()
        self.var_t_inicial = tk.StringVar()
        self.var_y_inicial = tk.StringVar()
        self.var_paso = tk.StringVar()
        self.var_num_pasos = tk.StringVar()
        self.var_metodo = tk.StringVar(value="heun")  # Valor por defecto: método de Heun
        
        # Ejemplos predefinidos
        self.ejemplos = {
            "Crecimiento exponencial": {
                "funcion": "y",
                "t0": "0",
                "y0": "1",
                "h": "0.1",
                "n": "20",
                "descripcion": "Modelo de crecimiento exponencial: dy/dt = y"
            },
            "Decaimiento exponencial": {
                "funcion": "-0.5*y",
                "t0": "0",
                "y0": "1",
                "h": "0.2",
                "n": "15",
                "descripcion": "Modelo de decaimiento exponencial: dy/dt = -0.5y"
            },
            "Ecuación logística": {
                "funcion": "y*(1-y/10)",
                "t0": "0",
                "y0": "0.5",
                "h": "0.2",
                "n": "25",
                "descripcion": "Modelo de crecimiento logístico: dy/dt = y(1-y/10)"
            },
            "Oscilador": {
                "funcion": "sin(t) - 0.1*y",
                "t0": "0",
                "y0": "0",
                "h": "0.1",
                "n": "50",
                "descripcion": "Oscilador amortiguado: dy/dt = sin(t) - 0.1y"
            }
        }
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Cargar ejemplo predeterminado
        self.cargar_ejemplo("Crecimiento exponencial")
    
    def configurar_estilo(self):
        """Configura el estilo de la aplicación"""
        # Configurar tema
        style = ttk.Style()
        
        # Intentar usar un tema más moderno si está disponible
        try:
            style.theme_use("clam")  # Alternativas: 'alt', 'default', 'classic'
        except:
            pass
        
        # Configurar colores
        bg_color = "#f0f0f0"
        accent_color = "#3498db"  # Azul
        button_color = "#2980b9"  # Azul más oscuro
        
        # Configurar estilo de widgets
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", background=button_color, foreground="white")
        style.configure("TLabelframe", background=bg_color)
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background=bg_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        # Configurar el fondo de la ventana principal
        self.root.configure(background=bg_color)
    
    def _crear_interfaz(self):
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Banner o título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="Solucionador de EDOs - Método de Heun", 
                               font=("Segoe UI", 16, "bold"), foreground="#2c3e50")
        title_label.pack(side=tk.LEFT)
        
        # Crear un panel de pestañas para organizar la interfaz
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para el solucionador
        solver_frame = ttk.Frame(notebook, padding="10")
        notebook.add(solver_frame, text="Solucionador")
        
        # Pestaña para ayuda/información
        help_frame = ttk.Frame(notebook, padding="10")
        notebook.add(help_frame, text="Ayuda")
        
        # Configurar la pestaña del solucionador
        self._crear_pestaña_solucionador(solver_frame)
        
        # Configurar la pestaña de ayuda
        self._crear_pestaña_ayuda(help_frame)
        
        # Barra de estado en la parte inferior
        status_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, padding=(5, 3))
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(status_frame, text="Listo", anchor=tk.W)
        status_label.pack(side=tk.LEFT)
        
        # Guardar referencia para actualizar después
        self.status_label = status_label
    
    def _crear_pestaña_solucionador(self, parent_frame):
        # Panel izquierdo para entradas
        left_frame = ttk.Frame(parent_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Panel derecho para resultados
        right_frame = ttk.Frame(parent_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frame para parámetros de entrada
        input_frame = ttk.LabelFrame(left_frame, text="Parámetros", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Selector de método
        ttk.Label(input_frame, text="Método:").grid(row=0, column=0, sticky=tk.W, pady=8)
        metodo_combo = ttk.Combobox(input_frame, textvariable=self.var_metodo, 
                                  values=["heun", "euler"], state="readonly", width=10)
        metodo_combo.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(5, 0))
        
        # Campos de entrada con mejor organización
        ttk.Label(input_frame, text="Función f(t, y):").grid(row=1, column=0, sticky=tk.W, pady=8)
        func_entry = ttk.Entry(input_frame, textvariable=self.var_funcion, width=30)
        func_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, pady=8, padx=(5, 0))
        
        # Tooltip para la función
        func_tip = ttk.Label(input_frame, text="Ejemplos: y, -0.5*y, y*(1-y/10), sin(t)-0.1*y", 
                            foreground="#555555", font=("Segoe UI", 8))
        func_tip.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=(5, 0))
        
        # Valores iniciales en una fila
        ttk.Label(input_frame, text="Valor inicial de t:").grid(row=3, column=0, sticky=tk.W, pady=8)
        ttk.Entry(input_frame, textvariable=self.var_t_inicial, width=10).grid(row=3, column=1, sticky=tk.W, pady=8, padx=(5, 0))
        
        ttk.Label(input_frame, text="Valor inicial de y:").grid(row=4, column=0, sticky=tk.W, pady=8)
        ttk.Entry(input_frame, textvariable=self.var_y_inicial, width=10).grid(row=4, column=1, sticky=tk.W, pady=8, padx=(5, 0))
        
        # Parámetros de paso en una fila
        ttk.Label(input_frame, text="Tamaño de paso h:").grid(row=5, column=0, sticky=tk.W, pady=8)
        ttk.Entry(input_frame, textvariable=self.var_paso, width=10).grid(row=5, column=1, sticky=tk.W, pady=8, padx=(5, 0))
        
        ttk.Label(input_frame, text="Número de pasos:").grid(row=6, column=0, sticky=tk.W, pady=8)
        ttk.Entry(input_frame, textvariable=self.var_num_pasos, width=10).grid(row=6, column=1, sticky=tk.W, pady=8, padx=(5, 0))
        
        # Separador
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=7, column=0, columnspan=3, sticky=tk.E+tk.W, pady=10)
        
        # Selector de ejemplos
        ttk.Label(input_frame, text="Ejemplos predefinidos:").grid(row=8, column=0, sticky=tk.W, pady=8)
        ejemplo_combo = ttk.Combobox(input_frame, values=list(self.ejemplos.keys()), state="readonly", width=25)
        ejemplo_combo.grid(row=8, column=1, columnspan=2, sticky=tk.W+tk.E, pady=8, padx=(5, 0))
        ejemplo_combo.bind("<<ComboboxSelected>>", lambda event: self.cargar_ejemplo(ejemplo_combo.get()))
        
        # Descripción del ejemplo
        self.desc_ejemplo = ttk.Label(input_frame, text="", wraplength=250, justify=tk.LEFT,
                                    foreground="#555555", font=("Segoe UI", 9))
        self.desc_ejemplo.grid(row=9, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))
        
        # Botones con mejor estilo
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        calcular_btn = ttk.Button(btn_frame, text="Calcular", command=self.calcular, style="Accent.TButton", width=12)
        calcular_btn.pack(side=tk.LEFT, padx=5)
        
        exportar_btn = ttk.Button(btn_frame, text="Exportar a CSV", command=self.exportar_csv, width=15)
        exportar_btn.pack(side=tk.LEFT, padx=5)
        
        limpiar_btn = ttk.Button(btn_frame, text="Limpiar", command=self.limpiar, width=10)
        limpiar_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame para mensajes de log
        log_frame = ttk.LabelFrame(left_frame, text="Mensajes", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=False)
        
        self.log_text = tk.Text(log_frame, height=5, width=40, state="disabled", 
                               font=("Consolas", 9), bg="#f8f9fa", fg="#333333")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame para resultados
        results_frame = ttk.LabelFrame(right_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel con pestañas para tabla y gráfica
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para tabla de resultados
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Tabla")
        
        # Crear tabla con mejor estilo
        columns = ("t", "y")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        
        # Agregar scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Ubicar elementos
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        
        # Configurar grid
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Pestaña para gráfica
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="Gráfica")
    
    def _crear_pestaña_ayuda(self, parent_frame):
        # Crear un panel con pestañas para la ayuda
        help_notebook = ttk.Notebook(parent_frame)
        help_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña para información del método
        method_frame = ttk.Frame(help_notebook, padding="15")
        help_notebook.add(method_frame, text="Método de Heun")
        
        # Pestaña para instrucciones
        instructions_frame = ttk.Frame(help_notebook, padding="15")
        help_notebook.add(instructions_frame, text="Instrucciones")
        
        # Pestaña para fórmulas
        formulas_frame = ttk.Frame(help_notebook, padding="15")
        help_notebook.add(formulas_frame, text="Explicación")
        
        # Contenido de la pestaña de método
        method_title = ttk.Label(method_frame, text="Método de Heun (Euler Mejorado)",
                               font=("Segoe UI", 12, "bold"))
        method_title.pack(anchor=tk.W, pady=(0, 10))
        
        method_desc = ttk.Label(method_frame, wraplength=800, justify=tk.LEFT,
                              text="El método de Heun es un método numérico que nos permite encontrar soluciones aproximadas "
                                  "para ecuaciones diferenciales ordinarias (EDOs). Es una mejora del método de Euler básico, "
                                  "ya que utiliza un enfoque en dos pasos que aumenta considerablemente la precisión.\n\n"
                                  "La idea principal es primero hacer una predicción aproximada (usando el método de Euler) y "
                                  "luego corregir esta predicción para obtener un resultado más preciso.")
        method_desc.pack(anchor=tk.W, pady=(0, 10))
        
        # Explicación visual del método
        visual_frame = ttk.LabelFrame(method_frame, text="¿Cómo funciona?", padding=10)
        visual_frame.pack(fill=tk.X, pady=10)
        
        visual_desc = ttk.Label(visual_frame, wraplength=800, justify=tk.LEFT,
                              text="Imagina que quieres predecir cómo cambia una cantidad (y) a lo largo del tiempo (t):\n\n"
                                  "1. Primero, observas cómo está cambiando y en este momento (la pendiente actual).\n"
                                  "2. Usando esta pendiente, haces una primera estimación de dónde estará y después de un pequeño paso.\n"
                                  "3. Luego, calculas cómo sería la pendiente en ese punto estimado.\n"
                                  "4. Finalmente, usas el promedio de ambas pendientes (la inicial y la estimada) para hacer un "
                                  "cálculo más preciso de dónde estará y realmente.")
        visual_desc.pack(fill=tk.X, pady=5)
        
        steps_frame = ttk.Frame(method_frame)
        steps_frame.pack(fill=tk.X, pady=10)
        
        steps_title = ttk.Label(steps_frame, text="Los dos pasos principales:", font=("Segoe UI", 10, "bold"))
        steps_title.pack(anchor=tk.W, pady=(0, 5))
        
        steps_text = (
            "1. Paso predictor: Hacemos una primera estimación usando el método de Euler.\n"
            "2. Paso corrector: Mejoramos la estimación usando el promedio de las pendientes."
        )
        
        steps_label = ttk.Label(steps_frame, text=steps_text, font=("Segoe UI", 10),
                              background="#f8f9fa", padding=10)
        steps_label.pack(fill=tk.X)
        
        # Contenido de la pestaña de instrucciones
        instr_title = ttk.Label(instructions_frame, text="Instrucciones de uso",
                              font=("Segoe UI", 12, "bold"))
        instr_title.pack(anchor=tk.W, pady=(0, 10))
        
        instructions = [
            "1. Ingrese la función f(t,y) que define cómo cambia y con respecto a t.",
            "2. Especifique el punto inicial: valor de t y valor de y donde comienza el problema.",
            "3. Defina el tamaño de paso h (qué tan pequeños serán los intervalos) y cuántos pasos calcular.",
            "4. Haga clic en 'Calcular' para resolver y ver la solución aproximada.",
            "5. Examine los resultados en la tabla o visualícelos en la gráfica.",
            "6. Si lo desea, exporte los resultados a un archivo CSV para análisis posterior."
        ]
        
        for instr in instructions:
            instr_label = ttk.Label(instructions_frame, text=instr, wraplength=800, justify=tk.LEFT)
            instr_label.pack(anchor=tk.W, pady=3)
        
        # Ejemplos de funciones
        examples_title = ttk.Label(instructions_frame, text="\nEjemplos de funciones que puede ingresar:",
                                 font=("Segoe UI", 11, "bold"))
        examples_title.pack(anchor=tk.W, pady=(15, 5))
        
        examples = [
            "y                  → Crecimiento exponencial simple",
            "-0.5*y             → Decaimiento exponencial",
            "y*(1-y/10)         → Crecimiento logístico (limitado)",
            "sin(t) - 0.1*y     → Oscilador amortiguado"
        ]
        
        for example in examples:
            example_label = ttk.Label(instructions_frame, text=example, font=("Consolas", 10))
            example_label.pack(anchor=tk.W, pady=2)
        
        # Contenido de la pestaña de explicación de fórmulas
        formulas_title = ttk.Label(formulas_frame, text="Entendiendo las Fórmulas",
                                 font=("Segoe UI", 12, "bold"))
        formulas_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Explicación de la ecuación diferencial
        edo_frame = ttk.LabelFrame(formulas_frame, text="¿Qué es una ecuación diferencial?", padding=10)
        edo_frame.pack(fill=tk.X, pady=10)
        
        edo_text = ("Una ecuación diferencial ordinaria (EDO) describe cómo una cantidad cambia con respecto a otra. "
                   "En nuestro caso, estamos trabajando con ecuaciones de la forma:\n\n"
                   "dy/dt = f(t, y)\n\n"
                   "Esto significa: 'La tasa de cambio de y con respecto a t es igual a alguna función f que "
                   "depende de los valores actuales de t e y'.")
        
        edo_label = ttk.Label(edo_frame, text=edo_text, wraplength=800, justify=tk.LEFT)
        edo_label.pack(fill=tk.X)
        
        # Explicación del método de Euler
        euler_frame = ttk.LabelFrame(formulas_frame, text="El método de Euler (primer paso)", padding=10)
        euler_frame.pack(fill=tk.X, pady=10)
        
        euler_text = ("El método de Euler es la base del primer paso del método de Heun. La idea es simple:\n\n"
                     "y_{siguiente} = y_{actual} + (tamaño_paso) × (pendiente_actual)\n\n"
                     "Donde la pendiente_actual es f(t, y) evaluada en el punto actual.\n\n"
                     "Es como decir: 'Si sigo en línea recta con la pendiente actual durante un pequeño paso, "
                     "llegaré aproximadamente a este nuevo punto'.")
        
        euler_label = ttk.Label(euler_frame, text=euler_text, wraplength=800, justify=tk.LEFT)
        euler_label.pack(fill=tk.X)
        
        # Explicación del método de Heun
        heun_frame = ttk.LabelFrame(formulas_frame, text="El método de Heun completo (segundo paso)", padding=10)
        heun_frame.pack(fill=tk.X, pady=10)
        
        heun_text = ("El método de Heun mejora la precisión usando dos pendientes:\n\n"
                    "1. La pendiente al inicio del intervalo (donde estamos ahora)\n"
                    "2. La pendiente al final del intervalo (donde estaríamos según Euler)\n\n"
                    "Luego calcula el promedio de estas dos pendientes y usa este promedio para dar un paso más preciso:\n\n"
                    "y_{siguiente} = y_{actual} + (tamaño_paso) × (promedio_de_pendientes)\n\n"
                    "Esto es como decir: 'En lugar de asumir que la pendiente es constante durante todo el paso, "
                    "consideraré cómo cambia la pendiente y usaré un valor más representativo'.")
        
        heun_label = ttk.Label(heun_frame, text=heun_text, wraplength=800, justify=tk.LEFT)
        heun_label.pack(fill=tk.X)
        
        # Explicación del error
        error_frame = ttk.LabelFrame(formulas_frame, text="Precisión del método", padding=10)
        error_frame.pack(fill=tk.X, pady=10)
        
        error_text = ("El método de Heun es mucho más preciso que el método de Euler simple. Técnicamente, "
                     "el error en cada paso es proporcional al cubo del tamaño del paso (h³), mientras que "
                     "en Euler el error es proporcional al cuadrado del tamaño del paso (h²).\n\n"
                     "En términos prácticos, esto significa que:\n\n"
                     "• Si reduce el tamaño del paso a la mitad, el error en cada paso se reduce aproximadamente "
                     "a 1/8 de su valor anterior.\n"
                     "• Para obtener resultados más precisos, use un tamaño de paso más pequeño.")
        
        error_label = ttk.Label(error_frame, text=error_text, wraplength=800, justify=tk.LEFT)
        error_label.pack(fill=tk.X)
    
    def cargar_ejemplo(self, nombre_ejemplo):
        """Carga un ejemplo predefinido en los campos de entrada"""
        if nombre_ejemplo in self.ejemplos:
            ejemplo = self.ejemplos[nombre_ejemplo]
            self.var_funcion.set(ejemplo["funcion"])
            self.var_t_inicial.set(ejemplo["t0"])
            self.var_y_inicial.set(ejemplo["y0"])
            self.var_paso.set(ejemplo["h"])
            self.var_num_pasos.set(ejemplo["n"])
            
            # Mostrar descripción del ejemplo
            if "descripcion" in ejemplo:
                self.desc_ejemplo.config(text=ejemplo["descripcion"])
            else:
                self.desc_ejemplo.config(text="")
            
            self.log_mensaje(f"Ejemplo cargado: {nombre_ejemplo}")
            self.status_label.config(text=f"Ejemplo cargado: {nombre_ejemplo}")
        
    def log_mensaje(self, mensaje):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, mensaje + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")
        
    def validar_entradas(self):
        # Verificar que todos los campos estén completos
        if not all([self.var_funcion.get(), self.var_t_inicial.get(), 
                   self.var_y_inicial.get(), self.var_paso.get(), 
                   self.var_num_pasos.get()]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        
        try:
            # Convertir y validar valores numéricos
            t0 = float(self.var_t_inicial.get())
            y0 = float(self.var_y_inicial.get())
            h = float(self.var_paso.get())
            n = int(self.var_num_pasos.get())
            
            # Validar restricciones
            if h <= 0:
                messagebox.showerror("Error", "El tamaño de paso debe ser mayor que cero.")
                return False
            
            if n <= 0:
                messagebox.showerror("Error", "El número de pasos debe ser mayor que cero.")
                return False
                
            return True
        except ValueError:
            messagebox.showerror("Error", "Los valores deben ser numéricos válidos.")
            return False
    
    def calcular(self):
        if not self.validar_entradas():
            return
        
        try:
            # Actualizar estado
            self.status_label.config(text="Calculando...")
            self.root.update_idletasks()
            
            # Obtener valores de los campos
            funcion_str = self.var_funcion.get()
            t0 = float(self.var_t_inicial.get())
            y0 = float(self.var_y_inicial.get())
            h = float(self.var_paso.get())
            n = int(self.var_num_pasos.get())
            metodo = self.var_metodo.get()
            
            # Crear el solucionador apropiado
            if metodo == "heun":
                solver = HeunSolver()
                metodo_nombre = "Heun"
            else:  # metodo == "euler"
                solver = EulerSolver()
                metodo_nombre = "Euler"
            
            # Calcular solución
            t_values, y_values = solver.solve(funcion_str, t0, y0, h, n)
            
            # Mostrar resultados en la tabla
            self.mostrar_resultados(t_values, y_values)
            
            # Mostrar gráfica
            self.mostrar_grafica(t_values, y_values, metodo_nombre)
            
            self.log_mensaje(f"Cálculo completado con éxito usando método de {metodo_nombre}: {n} pasos con h={h}")
            self.status_label.config(text=f"Cálculo completado: {len(t_values)} puntos generados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
            self.log_mensaje(f"ERROR: {str(e)}")
            self.status_label.config(text="Error en el cálculo")
    
    def mostrar_resultados(self, t_values, y_values):
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos valores
        for i in range(len(t_values)):
            self.tree.insert("", tk.END, values=(f"{t_values[i]:.6f}", f"{y_values[i]:.6f}"))
            
        # Alternar colores de fila para mejor legibilidad
        for i, item in enumerate(self.tree.get_children()):
            if i % 2 == 0:
                self.tree.item(item, tags=("evenrow",))
            else:
                self.tree.item(item, tags=("oddrow",))
        
        # Configurar tags
        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="#ffffff")
    
    def mostrar_grafica(self, t_values, y_values, metodo_nombre="Heun"):
        # Limpiar frame de gráfica
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Crear figura y gráfica con mejor estilo
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # Graficar solución numérica
        ax.plot(t_values, y_values, '-o', linewidth=2, markersize=4, 
               label=f'Solución numérica ({metodo_nombre})', color="#3498db")
        
        # Añadir título y etiquetas
        ax.set_xlabel('t', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(f'Solución por método de {metodo_nombre}', fontsize=14, fontweight='bold')
        
        # Mejorar aspecto
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Mostrar gráfica en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Añadir barra de herramientas de navegación
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = ttk.Frame(self.graph_frame)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
    
    def exportar_csv(self):
        if not hasattr(self, 'tree') or not self.tree.get_children():
            messagebox.showinfo("Información", "No hay datos para exportar.")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar resultados como CSV"
            )
            
            if not filename:
                return
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["t", "y"])  # Encabezados
                
                for item_id in self.tree.get_children():
                    values = self.tree.item(item_id, 'values')
                    writer.writerow(values)
            
            self.log_mensaje(f"Datos exportados a {filename}")
            self.status_label.config(text=f"Datos exportados a {os.path.basename(filename)}")
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
            self.log_mensaje(f"ERROR en exportación: {str(e)}")
            self.status_label.config(text="Error al exportar")
    
    def limpiar(self):
        # Limpiar campos de entrada
        self.var_funcion.set("")
        self.var_t_inicial.set("")
        self.var_y_inicial.set("")
        self.var_paso.set("")
        self.var_num_pasos.set("")
        self.desc_ejemplo.config(text="")
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpiar gráfica
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Limpiar log
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        
        # Actualizar estado
        self.status_label.config(text="Datos limpiados")
        self.log_mensaje("Todos los datos han sido limpiados")

def main():
    root = tk.Tk()
    app = EDOSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 