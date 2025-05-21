import numpy as np
import matplotlib.pyplot as plt
from solvers import get_solver
from utils.analytic_solution import AnalyticSolution

class ConvergenceAnalysis:
    """
    Clase para realizar análisis de convergencia de métodos numéricos.
    """
    
    def __init__(self):
        self.analytic = AnalyticSolution()
    
    def analyze_step_size(self, method_name, func_str, t0, y0, t_end, solution_str=None, 
                         step_sizes=None, log_scale=True):
        """
        Analiza cómo el error cambia al modificar el tamaño de paso.
        
        Args:
            method_name (str): Nombre del método numérico
            func_str (str): Cadena de texto que representa la función f(t,y)
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            t_end (float): Valor final de t
            solution_str (str, optional): Cadena de texto que representa la solución analítica
            step_sizes (list, optional): Lista de tamaños de paso a analizar
            log_scale (bool, optional): Si es True, se usa escala logarítmica
            
        Returns:
            tuple: (step_sizes, errors, order) - Tamaños de paso, errores y orden de convergencia estimado
        """
        # Si no se proporcionan tamaños de paso, generar una secuencia
        if step_sizes is None:
            if log_scale:
                step_sizes = np.logspace(-4, -1, 10)  # 10 tamaños de paso entre 10^-4 y 10^-1
            else:
                step_sizes = np.linspace(0.001, 0.1, 10)  # 10 tamaños de paso entre 0.001 y 0.1
        
        # Obtener el solucionador
        solver = get_solver(method_name)
        
        # Inicializar arrays para almacenar errores
        errors = np.zeros_like(step_sizes)
        
        # Si se proporciona una solución analítica, parsearla
        analytic_func = None
        if solution_str:
            analytic_func = self.analytic.parse_solution(solution_str)
        
        # Para cada tamaño de paso, calcular el error
        for i, h in enumerate(step_sizes):
            # Calcular el número de pasos
            n = int((t_end - t0) / h)
            
            # Resolver la EDO
            t_values, y_numeric = solver.solve(func_str, t0, y0, h, n)
            
            # Si hay solución analítica, calcular el error
            if analytic_func:
                y_analytic = self.analytic.evaluate(analytic_func, t_values)
                errors[i] = np.max(np.abs(y_numeric - y_analytic))
            else:
                # Si no hay solución analítica, usar una solución de referencia con paso muy pequeño
                if i == 0:
                    h_ref = min(step_sizes) / 10
                    n_ref = int((t_end - t0) / h_ref)
                    _, y_ref = get_solver('rk4').solve(func_str, t0, y0, h_ref, n_ref)
                
                # Interpolar la solución de referencia para compararla con la solución actual
                t_ref = np.linspace(t0, t_end, len(y_ref))
                y_interp = np.interp(t_values, t_ref, y_ref)
                errors[i] = np.max(np.abs(y_numeric - y_interp))
        
        # Estimar el orden de convergencia
        if log_scale and len(step_sizes) > 1:
            # Ajustar una línea recta a log(error) vs log(h)
            log_h = np.log10(step_sizes)
            log_error = np.log10(errors)
            
            # Usar regresión lineal para estimar la pendiente (orden de convergencia)
            A = np.vstack([log_h, np.ones(len(log_h))]).T
            m, c = np.linalg.lstsq(A, log_error, rcond=None)[0]
            
            order = m  # La pendiente es el orden de convergencia
        else:
            order = None
        
        return step_sizes, errors, order
    
    def plot_convergence(self, step_sizes, errors, order=None, method_name="", ax=None):
        """
        Genera un gráfico de convergencia.
        
        Args:
            step_sizes (array): Tamaños de paso
            errors (array): Errores correspondientes
            order (float, optional): Orden de convergencia estimado
            method_name (str, optional): Nombre del método para el título
            ax (matplotlib.axes, optional): Ejes donde dibujar el gráfico
            
        Returns:
            matplotlib.axes: Ejes con el gráfico
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        # Dibujar puntos de datos
        ax.loglog(step_sizes, errors, 'o-', label=f'Error vs. Tamaño de paso')
        
        # Si se proporciona el orden, añadir una línea de referencia
        if order is not None:
            # Generar una línea de referencia con la pendiente del orden estimado
            h_ref = np.logspace(np.log10(min(step_sizes)), np.log10(max(step_sizes)), 100)
            e_ref = errors[0] * (h_ref / step_sizes[0]) ** order
            ax.loglog(h_ref, e_ref, '--', label=f'Orden {order:.2f}')
        
        # Configurar el gráfico
        ax.set_xlabel('Tamaño de paso (h)')
        ax.set_ylabel('Error máximo')
        ax.set_title(f'Análisis de convergencia - {method_name}')
        ax.grid(True, which="both", ls="--", alpha=0.7)
        ax.legend()
        
        return ax
    
    def compare_methods(self, func_str, t0, y0, t_end, solution_str=None, methods=None, h=0.01):
        """
        Compara diferentes métodos numéricos.
        
        Args:
            func_str (str): Cadena de texto que representa la función f(t,y)
            t0 (float): Valor inicial de t
            y0 (float): Valor inicial de y
            t_end (float): Valor final de t
            solution_str (str, optional): Cadena de texto que representa la solución analítica
            methods (list, optional): Lista de nombres de métodos a comparar
            h (float, optional): Tamaño de paso
            
        Returns:
            tuple: (t_values, results, analytic_values) - Valores de t, resultados por método y valores analíticos
        """
        # Si no se proporcionan métodos, usar todos los disponibles
        if methods is None:
            from solvers import get_available_methods
            methods = get_available_methods()
        
        # Calcular el número de pasos
        n = int((t_end - t0) / h)
        
        # Inicializar diccionario para almacenar resultados
        results = {}
        
        # Para cada método, resolver la EDO
        for method_name in methods:
            solver = get_solver(method_name)
            t_values, y_values = solver.solve(func_str, t0, y0, h, n)
            results[method_name] = y_values
        
        # Si se proporciona una solución analítica, calcularla
        analytic_values = None
        if solution_str:
            analytic_func = self.analytic.parse_solution(solution_str)
            analytic_values = self.analytic.evaluate(analytic_func, t_values)
        
        return t_values, results, analytic_values
    
    def plot_comparison(self, t_values, results, analytic_values=None, ax=None):
        """
        Genera un gráfico comparativo de diferentes métodos.
        
        Args:
            t_values (array): Valores de t
            results (dict): Diccionario con los resultados por método
            analytic_values (array, optional): Valores de la solución analítica
            ax (matplotlib.axes, optional): Ejes donde dibujar el gráfico
            
        Returns:
            matplotlib.axes: Ejes con el gráfico
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        # Dibujar resultados de cada método
        for method_name, y_values in results.items():
            ax.plot(t_values, y_values, '-', label=method_name)
        
        # Si se proporciona la solución analítica, dibujarla
        if analytic_values is not None:
            ax.plot(t_values, analytic_values, 'k--', label='Solución analítica')
        
        # Configurar el gráfico
        ax.set_xlabel('t')
        ax.set_ylabel('y')
        ax.set_title('Comparación de métodos numéricos')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return ax 