"""
Gestor de configuración para la aplicación.

Este módulo proporciona funciones para manejar la configuración de la aplicación,
incluyendo la carga y guardado de configuraciones, así como la gestión de valores
por defecto.

Clases:
    ConfigManager: Clase para gestionar la configuración de la aplicación.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

class ConfigManager:
    """
    Clase para gestionar la configuración de la aplicación.
    
    Esta clase maneja la carga y guardado de configuraciones, así como
    la gestión de valores por defecto para la aplicación.
    
    Attributes:
        config_file (str): Ruta al archivo de configuración.
        config (dict): Diccionario con la configuración actual.
    """
    
    DEFAULT_CONFIG = {
        "theme": "light",
        "language": "es",
        "decimal_places": 6,
        "window_size": {
            "width": 1100,
            "height": 750
        },
        "chart_settings": {
            "show_grid": True,
            "show_points": True,
            "line_width": 1.5,
            "point_size": 4,
            "dpi": 100
        },
        "recent_files": [],
        "default_method": "heun",
        "accessibility": {
            "large_text": False,
            "high_contrast": False
        },
        "auto_save": True,
        "auto_save_interval": 5  # minutos
    }
    
    CONFIG_FILE = "config.json"
    
    def __init__(self, config_file="config.json"):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_file (str, optional): Nombre del archivo de configuración.
        """
        self.config_file = config_file
        self.config = self._cargar_configuracion()
    
    def _cargar_configuracion(self):
        """
        Carga la configuración desde el archivo.
        
        Returns:
            dict: Configuración cargada o valores por defecto si el archivo no existe.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
        
        return self._get_configuracion_por_defecto()
    
    def _get_configuracion_por_defecto(self):
        """
        Obtiene la configuración por defecto.
        
        Returns:
            dict: Configuración por defecto.
        """
        return {
            'ventana': {
                'ancho': 1100,
                'alto': 750,
                'titulo': 'Solucionador de EDOs'
            },
            'metodo': {
                'predeterminado': 'heun',
                'opciones': ['euler', 'heun', 'rk4']
            },
            'grafica': {
                'estilo': 'seaborn',
                'tamano': [8, 6],
                'color_solucion': 'blue',
                'color_referencia': 'red'
            },
            'ejemplos': {
                'predeterminado': 'Crecimiento exponencial',
                'guardar_ultimo': True
            }
        }
    
    def guardar_configuracion(self):
        """
        Guarda la configuración actual en el archivo.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")
            return False
    
    def get_valor(self, seccion, clave, valor_por_defecto=None):
        """
        Obtiene un valor de la configuración.
        
        Args:
            seccion (str): Sección de la configuración.
            clave (str): Clave del valor a obtener.
            valor_por_defecto: Valor a devolver si no se encuentra la clave.
            
        Returns:
            El valor de la configuración o el valor por defecto.
        """
        try:
            return self.config[seccion][clave]
        except KeyError:
            return valor_por_defecto
    
    def set_valor(self, seccion, clave, valor):
        """
        Establece un valor en la configuración.
        
        Args:
            seccion (str): Sección de la configuración.
            clave (str): Clave del valor a establecer.
            valor: Valor a establecer.
        """
        if seccion not in self.config:
            self.config[seccion] = {}
        self.config[seccion][clave] = valor
    
    def resetear_configuracion(self):
        """
        Resetea la configuración a los valores por defecto.
        """
        self.config = self._get_configuracion_por_defecto()
        self.guardar_configuracion()
    
    def get_config(self, key=None):
        """
        Obtiene la configuración o un valor específico.
        
        Args:
            key (str, optional): Clave de la configuración. Si es None, se devuelve toda la configuración.
            
        Returns:
            dict or any: Configuración completa o valor específico
        """
        if key is None:
            return self.config
        
        keys = key.split(".")
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return None
    
    def set_config(self, key, value):
        """
        Establece un valor de configuración.
        
        Args:
            key (str): Clave de la configuración
            value (any): Valor a establecer
            
        Returns:
            bool: True si se estableció correctamente, False en caso contrario
        """
        keys = key.split(".")
        config = self.config
        
        try:
            # Navegar hasta el último nivel
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Establecer el valor
            config[keys[-1]] = value
            return True
        except Exception as e:
            print(f"Error al establecer la configuración: {str(e)}")
            return False
    
    def save_config(self):
        """
        Guarda la configuración en un archivo.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")
            return False
    
    def load_config(self):
        """
        Carga la configuración desde un archivo.
        
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        if not os.path.exists(self.CONFIG_FILE):
            return False
        
        try:
            with open(self.CONFIG_FILE, "r") as f:
                loaded_config = json.load(f)
                
                # Actualizar la configuración manteniendo los valores por defecto para claves faltantes
                self._update_nested_dict(self.config, loaded_config)
                
            return True
        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
            return False
    
    def reset_config(self):
        """
        Restablece la configuración a los valores por defecto.
        
        Returns:
            bool: True si se restableció correctamente, False en caso contrario
        """
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save_config()
    
    def add_recent_file(self, file_path):
        """
        Añade un archivo a la lista de archivos recientes.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            bool: True si se añadió correctamente, False en caso contrario
        """
        try:
            recent_files = self.config.get("recent_files", [])
            
            # Eliminar el archivo si ya está en la lista
            if file_path in recent_files:
                recent_files.remove(file_path)
            
            # Añadir el archivo al principio de la lista
            recent_files.insert(0, file_path)
            
            # Limitar la lista a 10 archivos
            self.config["recent_files"] = recent_files[:10]
            
            return True
        except Exception as e:
            print(f"Error al añadir archivo reciente: {str(e)}")
            return False
    
    def _update_nested_dict(self, d, u):
        """
        Actualiza un diccionario anidado con otro diccionario.
        
        Args:
            d (dict): Diccionario a actualizar
            u (dict): Diccionario con los nuevos valores
            
        Returns:
            dict: Diccionario actualizado
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d 