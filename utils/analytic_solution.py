"""
Utilidades para el cálculo y comparación de soluciones analíticas.

Este módulo proporciona funciones para calcular soluciones analíticas
de ecuaciones diferenciales ordinarias y compararlas con soluciones numéricas.

Funciones:
    calcular_solucion_analitica: Calcula la solución analítica de una EDO.
    comparar_soluciones: Compara una solución numérica con su solución analítica.
"""

import numpy as np
import sympy as sp
from scipy.integrate import odeint

class AnalyticSolution:
    """
    Clase para manejar soluciones analíticas de EDOs y calcular errores.
    """
    
    def __init__(self):
        # Definir símbolos para la función
        self.t_sym = sp.Symbol('t')
        self.y_sym = sp.Symbol('y')
        self.C_sym = sp.Symbol('C')  # Constante de integración
    
    def parse_solution(self, solution_str):
        """
        Convierte una cadena de texto que representa una solución analítica
        en una función evaluable.
        
        Args:
            solution_str (str): Cadena de texto que representa la solución y(t)
            
        Returns:
            callable: Función evaluable que toma t como argumento
            
        Raises:
            ValueError: Si la solución no puede ser parseada correctamente
        """
        try:
            # Convertir la cadena a una expresión sympy
            expr = sp.sympify(solution_str)
            
            # Convertir la expresión a una función evaluable
            func = sp.lambdify(self.t_sym, expr, modules=['numpy'])
            
            # Verificar que la función sea evaluable
            try:
                func(0.0)
            except Exception as e:
                raise ValueError(f"La solución no puede ser evaluada: {str(e)}")
                
            return func
        except Exception as e:
            raise ValueError(f"Error al parsear la solución: {str(e)}")
    
    def evaluate(self, solution_func, t_values):
        """
        Evalúa la solución analítica en los puntos dados.
        
        Args:
            solution_func (callable): Función de la solución analítica
            t_values (array): Valores de t donde evaluar la solución
            
        Returns:
            array: Valores de y correspondientes a los valores de t
        """
        try:
            return solution_func(t_values)
        except Exception as e:
            raise ValueError(f"Error al evaluar la solución analítica: {str(e)}")
    
    def calculate_errors(self, y_numeric, y_analytic):
        """
        Calcula los errores absoluto y relativo entre la solución numérica y analítica.
        
        Args:
            y_numeric (array): Valores de y de la solución numérica
            y_analytic (array): Valores de y de la solución analítica
            
        Returns:
            tuple: (error_abs, error_rel) - Arrays con los errores absoluto y relativo
        """
        # Error absoluto
        error_abs = np.abs(y_numeric - y_analytic)
        
        # Error relativo (evitar división por cero)
        with np.errstate(divide='ignore', invalid='ignore'):
            error_rel = np.abs(error_abs / y_analytic)
            # Reemplazar infinitos y NaN con 0
            error_rel = np.nan_to_num(error_rel)
        
        return error_abs, error_rel
    
    def calculate_global_errors(self, y_numeric, y_analytic):
        """
        Calcula los errores globales (normas) entre la solución numérica y analítica.
        
        Args:
            y_numeric (array): Valores de y de la solución numérica
            y_analytic (array): Valores de y de la solución analítica
            
        Returns:
            dict: Diccionario con diferentes medidas de error global
        """
        # Error absoluto
        error_abs = np.abs(y_numeric - y_analytic)
        
        # Norma infinito (error máximo)
        max_error = np.max(error_abs)
        
        # Norma L1 (error promedio)
        mean_error = np.mean(error_abs)
        
        # Norma L2 (error RMS)
        rms_error = np.sqrt(np.mean(np.square(error_abs)))
        
        return {
            'max_error': max_error,
            'mean_error': mean_error,
            'rms_error': rms_error
        }

def calcular_solucion_analitica(funcion, t0, y0, t_values):
    """
    Calcula la solución analítica de una EDO.
    
    Args:
        funcion (str): La función que define la EDO en formato string.
        t0 (float): Valor inicial de t.
        y0 (float): Valor inicial de y.
        t_values (numpy.ndarray): Valores de t donde calcular la solución.
        
    Returns:
        numpy.ndarray: Valores de la solución analítica en los puntos t_values.
        
    Raises:
        ValueError: Si no se puede calcular la solución analítica.
    """
    try:
        # Convertir la función a una función evaluable
        t = sp.Symbol('t')
        y = sp.Symbol('y')
        f = sp.sympify(funcion)
        f_lambda = sp.lambdify((t, y), f, 'numpy')
        
        # Definir la función para odeint
        def dydt(y, t):
            return f_lambda(t, y)
        
        # Calcular la solución
        y_values = odeint(dydt, y0, t_values)
        return y_values.flatten()
        
    except Exception as e:
        raise ValueError(f"No se pudo calcular la solución analítica: {str(e)}")

def comparar_soluciones(t_values, y_numerica, y_analitica, titulo="Comparación de Soluciones"):
    """
    Compara una solución numérica con su solución analítica.
    
    Args:
        t_values (numpy.ndarray): Valores de la variable independiente t.
        y_numerica (numpy.ndarray): Valores de la solución numérica.
        y_analitica (numpy.ndarray): Valores de la solución analítica.
        titulo (str, optional): Título de la gráfica.
        
    Returns:
        tuple: (fig, ax) donde:
            - fig es la figura de matplotlib
            - ax es el eje de la gráfica
    """
    import matplotlib.pyplot as plt
    
    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Graficar ambas soluciones
    ax.plot(t_values, y_numerica, 'b-', label='Solución numérica')
    ax.plot(t_values, y_analitica, 'r--', label='Solución analítica')
    
    # Personalizar la gráfica
    ax.set_title(titulo, fontsize=12, pad=15)
    ax.set_xlabel('t', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Calcular y mostrar el error
    error = np.abs(y_numerica - y_analitica)
    error_max = np.max(error)
    error_medio = np.mean(error)
    
    # Agregar información del error
    ax.text(0.02, 0.98, f'Error máximo: {error_max:.2e}\nError medio: {error_medio:.2e}',
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    return fig, ax 