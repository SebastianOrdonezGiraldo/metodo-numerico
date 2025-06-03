"""
Implementación del método de Heun para resolver ecuaciones diferenciales ordinarias.

Este módulo implementa el método de Heun (también conocido como método de Euler mejorado),
que es un método numérico de segundo orden para resolver ecuaciones diferenciales ordinarias
de la forma dy/dt = f(t,y).

Clases:
    HeunSolver: Implementación del método de Heun.
"""

import numpy as np
import sympy as sp
from .base_solver import BaseSolver

class HeunSolver(BaseSolver):
    """
    Implementación del método de Heun para resolver EDOs.
    
    El método de Heun es un método numérico de segundo orden que mejora la precisión
    del método de Euler usando un enfoque predictor-corrector. La fórmula es:
    
    Predictor (Euler):
    y_pred = y_n + h * f(t_n, y_n)
    
    Corrector (Heun):
    y_{n+1} = y_n + (h/2) * [f(t_n, y_n) + f(t_{n+1}, y_pred)]
    
    donde:
    - h es el tamaño del paso
    - f(t,y) es la función que define la EDO
    - y_n es el valor de y en el paso n
    - t_n es el valor de t en el paso n
    
    Attributes:
        name (str): Nombre del método ("Heun")
        order (int): Orden del método (2)
    """
    
    def __init__(self, funcion):
        """
        Inicializa el solucionador de Heun.
        
        Args:
            funcion (str): La función que define la EDO en formato string.
        """
        super().__init__(funcion)
        self.name = "Heun"
        self.order = 2
        # Definir símbolos para la función
        self.t_sym = sp.Symbol('t')
        self.y_sym = sp.Symbol('y')
    
    def _parse_function(self, func_str):
        """
        Convierte una cadena de texto que representa una función f(t,y)
        en una función evaluable usando sympy.
        
        Args:
            func_str (str): Cadena de texto que representa la función f(t,y)
            
        Returns:
            callable: Función evaluable que toma (t,y) como argumentos
            
        Raises:
            ValueError: Si la función no puede ser parseada correctamente
        """
        try:
            # Convertir la cadena a una expresión sympy
            expr = sp.sympify(func_str)
            
            # Convertir la expresión a una función evaluable
            func = sp.lambdify((self.t_sym, self.y_sym), expr, modules=['numpy'])
            
            # Verificar que la función sea evaluable
            try:
                func(0.0, 0.0)
            except Exception as e:
                raise ValueError(f"La función no puede ser evaluada: {str(e)}")
                
            return func
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {str(e)}")
    
    def solve(self, t0, y0, h, n):
        """
        Resuelve la EDO usando el método de Heun.
        
        Args:
            t0 (float): Valor inicial de t.
            y0 (float): Valor inicial de y.
            h (float): Tamaño del paso.
            n (int): Número de pasos a calcular.
            
        Returns:
            tuple: (t_values, y_values) donde:
                - t_values es un array numpy con los valores de t
                - y_values es un array numpy con los valores de y
                
        Raises:
            ValueError: Si los parámetros no son válidos.
        """
        # Validar parámetros
        self._validar_parametros(t0, y0, h, n)
        
        # Inicializar arrays
        t_values = np.zeros(n + 1)
        y_values = np.zeros(n + 1)
        
        # Establecer valores iniciales
        t_values[0] = t0
        y_values[0] = y0
        
        # Aplicar método de Heun
        for i in range(n):
            t = t_values[i]
            y = y_values[i]
            
            # Paso predictor (Euler)
            f1 = self.evaluar_funcion(t, y)
            y_pred = y + h * f1
            
            # Paso corrector (Heun)
            f2 = self.evaluar_funcion(t + h, y_pred)
            y_next = y + (h/2) * (f1 + f2)
            
            # Guardar valores
            t_values[i + 1] = t + h
            y_values[i + 1] = y_next
        
        return t_values, y_values 