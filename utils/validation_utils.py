"""
Utilidades para la validación de entradas en la aplicación.

Este módulo proporciona funciones para validar diferentes tipos de entradas
en la aplicación, como expresiones matemáticas, valores numéricos y parámetros
de los métodos numéricos.

Funciones:
    validar_expresion_matematica: Valida una expresión matemática.
    validar_numero: Valida un valor numérico.
    validar_parametros_metodo: Valida los parámetros de un método numérico.
"""

import sympy as sp
import re

def validar_expresion_matematica(expresion):
    """
    Valida una expresión matemática en formato string.
    
    Args:
        expresion (str): La expresión matemática a validar.
        
    Returns:
        bool: True si la expresión es válida, False en caso contrario.
        
    Raises:
        ValueError: Si la expresión contiene caracteres no permitidos.
    """
    # Verificar caracteres permitidos
    caracteres_permitidos = set('0123456789+-*/()^t y.sin()cos()exp()sqrt()')
    if not all(c in caracteres_permitidos for c in expresion):
        raise ValueError("La expresión contiene caracteres no permitidos")
    
    # Verificar paréntesis balanceados
    if expresion.count('(') != expresion.count(')'):
        raise ValueError("Los paréntesis no están balanceados")
    
    # Intentar parsear la expresión
    try:
        t = sp.Symbol('t')
        y = sp.Symbol('y')
        expr = sp.sympify(expresion)
        return True
    except:
        raise ValueError("La expresión no es una expresión matemática válida")

def validar_numero(valor, min_val=None, max_val=None):
    """
    Valida un valor numérico.
    
    Args:
        valor (str): El valor a validar.
        min_val (float, optional): Valor mínimo permitido.
        max_val (float, optional): Valor máximo permitido.
        
    Returns:
        float: El valor numérico validado.
        
    Raises:
        ValueError: Si el valor no es un número válido o está fuera de los límites.
    """
    try:
        num = float(valor)
    except ValueError:
        raise ValueError("El valor debe ser un número")
    
    if min_val is not None and num < min_val:
        raise ValueError(f"El valor debe ser mayor o igual a {min_val}")
    
    if max_val is not None and num > max_val:
        raise ValueError(f"El valor debe ser menor o igual a {max_val}")
    
    return num

def validar_parametros_metodo(t0, y0, h, n):
    """
    Valida los parámetros de un método numérico.
    
    Args:
        t0 (float): Valor inicial de t.
        y0 (float): Valor inicial de y.
        h (float): Tamaño del paso.
        n (int): Número de pasos.
        
    Returns:
        tuple: (t0, y0, h, n) con los valores validados.
        
    Raises:
        ValueError: Si alguno de los parámetros no es válido.
    """
    # Validar valores iniciales
    t0 = validar_numero(t0)
    y0 = validar_numero(y0)
    
    # Validar tamaño de paso
    h = validar_numero(h, min_val=0.0001)
    
    # Validar número de pasos
    try:
        n = int(n)
        if n <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("El número de pasos debe ser un entero positivo")
    
    return t0, y0, h, n 