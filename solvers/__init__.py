from solvers.base_solver import BaseSolver
from solvers.euler_solver import EulerSolver
from solvers.heun_solver import HeunSolver
from solvers.rk4_solver import RK4Solver

# Diccionario de solucionadores disponibles
AVAILABLE_SOLVERS = {
    'euler': EulerSolver,
    'heun': HeunSolver,
    'rk4': RK4Solver
}

def get_solver(method_name):
    """
    Obtiene una instancia del solucionador especificado.
    
    Args:
        method_name (str): Nombre del método ('euler', 'heun', 'rk4')
        
    Returns:
        BaseSolver: Instancia del solucionador
        
    Raises:
        ValueError: Si el método no está disponible
    """
    method_name = method_name.lower()
    if method_name not in AVAILABLE_SOLVERS:
        raise ValueError(f"Método no disponible: {method_name}. Métodos disponibles: {', '.join(AVAILABLE_SOLVERS.keys())}")
    
    return AVAILABLE_SOLVERS[method_name]()

def get_available_methods():
    """
    Devuelve una lista de los métodos disponibles.
    
    Returns:
        list: Lista de nombres de métodos disponibles
    """
    return list(AVAILABLE_SOLVERS.keys())

__all__ = ['HeunSolver'] 