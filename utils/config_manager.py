import json
import os
import tkinter as tk
from tkinter import messagebox

class ConfigManager:
    """
    Clase para gestionar la configuración de la aplicación.
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
    
    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
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