"""
Utilidades para la visualización de gráficas en la aplicación.

Este módulo proporciona funciones para crear y personalizar gráficas
de las soluciones de ecuaciones diferenciales ordinarias.

Funciones:
    crear_grafica: Crea una gráfica de la solución de una EDO.
    personalizar_grafica: Personaliza el estilo de una gráfica.
"""

import matplotlib.pyplot as plt
import numpy as np

def crear_grafica(t_values, y_values, titulo="Solución de la EDO", etiqueta="y(t)"):
    """
    Crea una gráfica de la solución de una EDO.
    
    Args:
        t_values (numpy.ndarray): Valores de la variable independiente t.
        y_values (numpy.ndarray): Valores de la variable dependiente y.
        titulo (str, optional): Título de la gráfica.
        etiqueta (str, optional): Etiqueta para la curva.
        
    Returns:
        tuple: (fig, ax) donde:
            - fig es la figura de matplotlib
            - ax es el eje de la gráfica
    """
    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Graficar la solución
    ax.plot(t_values, y_values, 'b-', label=etiqueta)
    
    # Personalizar la gráfica
    personalizar_grafica(ax, titulo)
    
    return fig, ax

def personalizar_grafica(ax, titulo):
    """
    Personaliza el estilo de una gráfica.
    
    Args:
        ax (matplotlib.axes.Axes): El eje de la gráfica a personalizar.
        titulo (str): Título de la gráfica.
    """
    # Configurar título y etiquetas
    ax.set_title(titulo, fontsize=12, pad=15)
    ax.set_xlabel('t', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    
    # Configurar cuadrícula
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Configurar leyenda
    ax.legend(loc='best')
    
    # Configurar márgenes
    ax.margins(x=0.02, y=0.02)
    
    # Configurar estilo de los ejes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Configurar ticks
    ax.tick_params(direction='out', length=6, width=1, colors='black')
    ax.tick_params(axis='both', which='minor', length=4, width=1)

def save_plot(fig, filename):
    """
    Guarda la gráfica en un archivo.
    
    Args:
        fig (matplotlib.figure.Figure): Figura a guardar
        filename (str): Nombre del archivo
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight') 