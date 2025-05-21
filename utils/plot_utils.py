"""
Utilidades para la creación y manejo de gráficos.
"""
import matplotlib.pyplot as plt
import numpy as np

def create_solution_plot(t_values, y_values, title="Solución de la EDO"):
    """
    Crea una gráfica de la solución de la EDO.
    
    Args:
        t_values (np.array): Valores del tiempo
        y_values (np.array): Valores de la solución
        title (str): Título de la gráfica
        
    Returns:
        tuple: (fig, ax) - Figura y ejes de matplotlib
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t_values, y_values, 'b-', linewidth=2, label='Solución numérica')
    ax.set_title(title)
    ax.set_xlabel('t')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.legend()
    return fig, ax

def save_plot(fig, filename):
    """
    Guarda la gráfica en un archivo.
    
    Args:
        fig (matplotlib.figure.Figure): Figura a guardar
        filename (str): Nombre del archivo
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight') 