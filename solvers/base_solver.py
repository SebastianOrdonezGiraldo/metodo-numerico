import numpy as np
import sympy as sp

class BaseSolver:
    """
    Clase base para implementar métodos numéricos para resolver EDOs.
    Esta clase define la interfaz común y funcionalidad compartida para todos los métodos.
    """
    
    def __init__(self):
        # Definir símbolos para la función
        self.t_sym = sp.Symbol('t')
        self.y_sym = sp.Symbol('y')
        self.name = "Método Base"
        self.description = "Clase base para métodos numéricos"
        self.order = 0  # Orden del método (precisión)
    
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
    
    def _validate_parameters(self, t0, y0, h, n):
        """
        Valida los parámetros de entrada.
        
        Args:
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            h (float): Tamaño de paso
            n (int): Número de pasos
            
        Raises:
            ValueError: Si los parámetros no son válidos
        """
        if h <= 0:
            raise ValueError("El tamaño de paso h debe ser mayor que cero")
        
        if n <= 0:
            raise ValueError("El número de pasos n debe ser mayor que cero")
    
    def solve(self, func_str, t0, y0, h, n):
        """
        Método que debe ser implementado por las clases derivadas.
        
        Args:
            func_str (str): Cadena de texto que representa la función f(t,y)
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            h (float): Tamaño de paso
            n (int): Número de pasos
            
        Returns:
            tuple: (t_values, y_values) - Arrays con los valores de t e y en cada paso
            
        Raises:
            NotImplementedError: Si la clase derivada no implementa este método
        """
        raise NotImplementedError("Las clases derivadas deben implementar este método")
    
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