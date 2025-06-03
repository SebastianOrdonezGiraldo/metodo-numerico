"""
Clase base para los solucionadores de ecuaciones diferenciales ordinarias.

Este módulo define la interfaz base que todos los solucionadores de EDOs deben implementar.
Proporciona funcionalidad común y métodos abstractos que deben ser implementados por las clases hijas.

Clases:
    BaseSolver: Clase base abstracta para todos los solucionadores de EDOs.
"""

from abc import ABC, abstractmethod
import numpy as np
import sympy as sp

class BaseSolver(ABC):
    """
    Clase base abstracta para los solucionadores de EDOs.
    
    Esta clase define la interfaz común que todos los solucionadores deben implementar.
    Proporciona métodos para la evaluación de funciones y el cálculo de soluciones.
    
    Attributes:
        funcion (str): La función que define la EDO en formato string.
        t (sympy.Symbol): Símbolo para la variable independiente t.
        y (sympy.Symbol): Símbolo para la variable dependiente y.
        f (sympy.Expr): Expresión simbólica de la función.
    """
    
    def __init__(self, funcion):
        """
        Inicializa el solucionador base.
        
        Args:
            funcion (str): La función que define la EDO en formato string.
                          Debe ser una expresión válida en términos de t e y.
        """
        self.funcion = funcion
        self.t = sp.Symbol('t')
        self.y = sp.Symbol('y')
        self.f = sp.sympify(funcion)
    
    def evaluar_funcion(self, t_val, y_val):
        """
        Evalúa la función en un punto específico.
        
        Args:
            t_val (float): Valor de la variable independiente t.
            y_val (float): Valor de la variable dependiente y.
            
        Returns:
            float: El valor de la función evaluada en (t_val, y_val).
        """
        return float(self.f.subs({self.t: t_val, self.y: y_val}))
    
    @abstractmethod
    def solve(self, t0, y0, h, n):
        """
        Resuelve la EDO usando el método numérico específico.
        
        Args:
            t0 (float): Valor inicial de t.
            y0 (float): Valor inicial de y.
            h (float): Tamaño del paso.
            n (int): Número de pasos a calcular.
            
        Returns:
            tuple: (t_values, y_values) donde:
                - t_values es un array numpy con los valores de t
                - y_values es un array numpy con los valores de y
        """
        pass
    
    def _validar_parametros(self, t0, y0, h, n):
        """
        Valida los parámetros de entrada para el cálculo.
        
        Args:
            t0 (float): Valor inicial de t.
            y0 (float): Valor inicial de y.
            h (float): Tamaño del paso.
            n (int): Número de pasos a calcular.
            
        Raises:
            ValueError: Si alguno de los parámetros no es válido.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("El número de pasos debe ser un entero positivo")
        if h <= 0:
            raise ValueError("El tamaño del paso debe ser positivo")
        if not isinstance(t0, (int, float)) or not isinstance(y0, (int, float)):
            raise ValueError("Los valores iniciales deben ser números")
    
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
            func = sp.lambdify((self.t, self.y), expr, modules=['numpy'])
            
            # Verificar que la función sea evaluable
            try:
                func(0.0, 0.0)
            except Exception as e:
                raise ValueError(f"La función no puede ser evaluada: {str(e)}")
                
            return func
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {str(e)}")
    
    def get_info(self):
        """
        Devuelve información sobre el método.
        
        Returns:
            dict: Información sobre el método
        """
        return {
            "name": self.name,
            "description": self.description,
            "order": self.order
        }
    
    def get_local_error_order(self):
        """
        Devuelve el orden del error local.
        
        Returns:
            int: Orden del error local
        """
        return self.order + 1
    
    def get_global_error_order(self):
        """
        Devuelve el orden del error global.
        
        Returns:
            int: Orden del error global
        """
        return self.order 