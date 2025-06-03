"""
Implementación del método de Runge-Kutta de orden 4 (RK4) para resolver ecuaciones diferenciales ordinarias.

Este módulo implementa el método de Runge-Kutta de cuarto orden, que es un método numérico
de alta precisión para resolver ecuaciones diferenciales ordinarias de la forma dy/dt = f(t,y).

Clases:
    RK4Solver: Implementación del método de Runge-Kutta de orden 4.
"""

import numpy as np
from .base_solver import BaseSolver

class RK4Solver(BaseSolver):
    """
    Implementación del método de Runge-Kutta de orden 4 (RK4) para resolver EDOs.
    
    El método RK4 es un método numérico de cuarto orden que proporciona una alta precisión
    en la solución de ecuaciones diferenciales ordinarias. El método utiliza cuatro evaluaciones
    de la función en cada paso:
    
    k1 = f(t_n, y_n)
    k2 = f(t_n + h/2, y_n + h*k1/2)
    k3 = f(t_n + h/2, y_n + h*k2/2)
    k4 = f(t_n + h, y_n + h*k3)
    
    y_{n+1} = y_n + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    donde:
    - h es el tamaño del paso
    - f(t,y) es la función que define la EDO
    - y_n es el valor de y en el paso n
    - t_n es el valor de t en el paso n
    
    Attributes:
        name (str): Nombre del método ("RK4")
        order (int): Orden del método (4)
    """
    
    def __init__(self, funcion):
        """
        Inicializa el solucionador RK4.
        
        Args:
            funcion (str): La función que define la EDO en formato string.
        """
        super().__init__(funcion)
        self.name = "RK4"
        self.order = 4
    
    def solve(self, t0, y0, h, n):
        """
        Resuelve la EDO usando el método de Runge-Kutta de orden 4.
        
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
        
        # Aplicar método RK4
        for i in range(n):
            t = t_values[i]
            y = y_values[i]
            
            # Calcular los coeficientes k1, k2, k3, k4
            k1 = self.evaluar_funcion(t, y)
            k2 = self.evaluar_funcion(t + h/2, y + h*k1/2)
            k3 = self.evaluar_funcion(t + h/2, y + h*k2/2)
            k4 = self.evaluar_funcion(t + h, y + h*k3)
            
            # Calcular siguiente valor
            y_next = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            
            # Guardar valores
            t_values[i + 1] = t + h
            y_values[i + 1] = y_next
        
        return t_values, y_values 