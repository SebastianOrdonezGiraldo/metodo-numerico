import numpy as np
import sympy as sp

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