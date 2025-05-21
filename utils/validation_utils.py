"""
Utilidades para la validación de datos de entrada.
"""
import sympy as sp

def validate_function(func_str):
    """
    Valida que una cadena de texto represente una función válida.
    
    Args:
        func_str (str): Cadena de texto que representa la función
        
    Returns:
        bool: True si la función es válida
        
    Raises:
        ValueError: Si la función no es válida
    """
    try:
        # Definir símbolos
        t = sp.Symbol('t')
        y = sp.Symbol('y')
        
        # Intentar parsear la función
        expr = sp.sympify(func_str)
        
        # Verificar que la función dependa de t o y
        if not (t in expr.free_symbols or y in expr.free_symbols):
            raise ValueError("La función debe depender de t o y")
            
        return True
    except Exception as e:
        raise ValueError(f"Función inválida: {str(e)}")

def validate_numeric_input(value, min_value=None, max_value=None):
    """
    Valida que un valor sea numérico y esté dentro de un rango.
    
    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido (opcional)
        max_value: Valor máximo permitido (opcional)
        
    Returns:
        float: El valor validado
        
    Raises:
        ValueError: Si el valor no es válido
    """
    try:
        num_value = float(value)
        
        if min_value is not None and num_value < min_value:
            raise ValueError(f"El valor debe ser mayor que {min_value}")
            
        if max_value is not None and num_value > max_value:
            raise ValueError(f"El valor debe ser menor que {max_value}")
            
        return num_value
    except ValueError as e:
        raise ValueError(f"Valor numérico inválido: {str(e)}") 