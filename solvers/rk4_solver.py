import numpy as np
from solvers.base_solver import BaseSolver

class RK4Solver(BaseSolver):
    """
    Implementación del método de Runge-Kutta de cuarto orden para resolver 
    ecuaciones diferenciales ordinarias de primer orden.
    
    El método RK4 es un método de cuarto orden que proporciona una alta precisión
    utilizando cuatro evaluaciones de la función por paso.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Método de Runge-Kutta 4"
        self.description = "Método numérico de cuarto orden para resolver EDOs"
        self.order = 4  # Método de cuarto orden
    
    def solve(self, func_str, t0, y0, h, n):
        """
        Resuelve una EDO de primer orden usando el método de Runge-Kutta de cuarto orden.
        
        Args:
            func_str (str): Cadena de texto que representa la función f(t,y)
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            h (float): Tamaño de paso
            n (int): Número de pasos
            
        Returns:
            tuple: (t_values, y_values) - Arrays con los valores de t e y en cada paso
        """
        # Validar parámetros
        self._validate_parameters(t0, y0, h, n)
        
        # Parsear la función
        f = self._parse_function(func_str)
        
        # Inicializar arrays para almacenar resultados
        t_values = np.zeros(n + 1)
        y_values = np.zeros(n + 1)
        
        # Establecer valores iniciales
        t_values[0] = t0
        y_values[0] = y0
        
        try:
            # Implementación del método RK4
            for i in range(n):
                t = t_values[i]
                y = y_values[i]
                
                # Calcular los cuatro coeficientes k
                k1 = f(t, y)
                k2 = f(t + h/2, y + h*k1/2)
                k3 = f(t + h/2, y + h*k2/2)
                k4 = f(t + h, y + h*k3)
                
                # Calcular el siguiente valor de y
                y_next = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
                t_next = t + h
                
                # Almacenar resultados
                t_values[i + 1] = t_next
                y_values[i + 1] = y_next
                
            return t_values, y_values
            
        except Exception as e:
            raise ValueError(f"Error durante el cálculo: {str(e)}") 