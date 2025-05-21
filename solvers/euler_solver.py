"""
Implementación del método de Euler para resolver ecuaciones diferenciales ordinarias.
"""
import numpy as np
import sympy as sp

class EulerSolver:
    """
    Implementación del método de Euler para resolver 
    ecuaciones diferenciales ordinarias de primer orden.
    
    El método de Euler es un método de primer orden que aproxima
    la solución usando la pendiente en el punto actual.
    """
    
    def __init__(self):
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
    
    def solve(self, func_str, t0, y0, h, n):
        """
        Resuelve una EDO de primer orden usando el método de Euler.
        
        Args:
            func_str (str): Cadena de texto que representa la función f(t,y)
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            h (float): Tamaño de paso
            n (int): Número de pasos
            
        Returns:
            tuple: (t_values, y_values) - Arrays con los valores de t e y en cada paso
            
        Raises:
            ValueError: Si los parámetros no son válidos o si hay un error durante el cálculo
        """
        # Validar parámetros
        if h <= 0:
            raise ValueError("El tamaño de paso h debe ser mayor que cero")
        
        if n <= 0:
            raise ValueError("El número de pasos n debe ser mayor que cero")
        
        # Parsear la función
        f = self._parse_function(func_str)
        
        # Inicializar arrays para almacenar resultados
        t_values = np.zeros(n + 1)
        y_values = np.zeros(n + 1)
        
        # Establecer valores iniciales
        t_values[0] = t0
        y_values[0] = y0
        
        try:
            # Implementación del método de Euler
            for i in range(n):
                t = t_values[i]
                y = y_values[i]
                
                # Calcular pendiente en el punto actual
                k = f(t, y)
                
                # Calcular siguiente punto
                y_next = y + h * k
                t_next = t + h
                
                # Almacenar resultados
                t_values[i + 1] = t_next
                y_values[i + 1] = y_next
                
            return t_values, y_values
            
        except Exception as e:
            raise ValueError(f"Error durante el cálculo: {str(e)}") 