"""
Gestor de temas visuales para la aplicación.

Este módulo proporciona funciones para manejar los temas visuales de la aplicación,
incluyendo colores, fuentes y estilos de los widgets.

Clases:
    ThemeManager: Clase para gestionar los temas visuales de la aplicación.
"""

import tkinter as tk
from tkinter import ttk
import json
import os

class ThemeManager:
    """
    Clase para gestionar los temas visuales de la aplicación.
    
    Esta clase maneja la configuración de estilos visuales, incluyendo
    colores, fuentes y estilos de los widgets de la interfaz gráfica.
    
    Attributes:
        themes (dict): Diccionario con los temas disponibles.
        current_theme (str): Nombre del tema actual.
    """
    
    # Temas predefinidos
    THEMES = {
        "light": {
            "name": "Claro",
            "bg_color": "#f0f0f0",
            "fg_color": "#333333",
            "accent_color": "#3498db",
            "button_color": "#2980b9",
            "success_color": "#27ae60",
            "warning_color": "#f39c12",
            "error_color": "#e74c3c",
            "font_family": "Segoe UI",
            "chart_style": "default"
        },
        "dark": {
            "name": "Oscuro",
            "bg_color": "#2c3e50",
            "fg_color": "#ecf0f1",
            "accent_color": "#3498db",
            "button_color": "#2980b9",
            "success_color": "#2ecc71",
            "warning_color": "#f1c40f",
            "error_color": "#e74c3c",
            "font_family": "Segoe UI",
            "chart_style": "dark_background"
        },
        "high_contrast": {
            "name": "Alto Contraste",
            "bg_color": "#000000",
            "fg_color": "#ffffff",
            "accent_color": "#00ffff",
            "button_color": "#0000ff",
            "success_color": "#00ff00",
            "warning_color": "#ffff00",
            "error_color": "#ff0000",
            "font_family": "Segoe UI",
            "chart_style": "dark_background"
        }
    }
    
    def __init__(self):
        """
        Inicializa el gestor de temas.
        """
        self.current_theme = "light"
        self.custom_themes = {}
        self.load_custom_themes()
    
    def get_theme(self, theme_name=None):
        """
        Obtiene un tema por su nombre.
        
        Args:
            theme_name (str, optional): Nombre del tema. Si es None, se usa el tema actual.
            
        Returns:
            dict: Configuración del tema
        """
        if theme_name is None:
            theme_name = self.current_theme
            
        if theme_name in self.THEMES:
            return self.THEMES[theme_name]
        elif theme_name in self.custom_themes:
            return self.custom_themes[theme_name]
        else:
            return self.THEMES["light"]  # Tema por defecto
    
    def set_theme(self, theme_name):
        """
        Establece el tema actual.
        
        Args:
            theme_name (str): Nombre del tema
            
        Returns:
            bool: True si el tema se estableció correctamente, False en caso contrario
        """
        if theme_name in self.THEMES or theme_name in self.custom_themes:
            self.current_theme = theme_name
            return True
        return False
    
    def apply_theme(self, root):
        """
        Aplica el tema actual a la interfaz.
        
        Args:
            root (tk.Tk): Ventana principal de la aplicación
        """
        theme = self.get_theme()
        
        # Configurar estilo
        style = ttk.Style()
        
        # Intentar usar un tema base adecuado
        try:
            if theme["bg_color"].startswith("#2") or theme["bg_color"].startswith("#3"):
                style.theme_use("clam")  # Mejor para temas oscuros
            else:
                style.theme_use("clam")  # Funciona bien en general
        except:
            pass
        
        # Configurar colores
        bg_color = theme["bg_color"]
        fg_color = theme["fg_color"]
        accent_color = theme["accent_color"]
        button_color = theme["button_color"]
        font_family = theme["font_family"]
        
        # Configurar estilo de widgets
        style.configure(".", background=bg_color, foreground=fg_color, font=(font_family, 10))
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=(font_family, 10))
        style.configure("TButton", font=(font_family, 10, "bold"))
        style.configure("Accent.TButton", background=button_color, foreground="white")
        style.configure("TLabelframe", background=bg_color)
        style.configure("TLabelframe.Label", font=(font_family, 11, "bold"), background=bg_color, foreground=fg_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background=bg_color, foreground=fg_color, padding=[10, 4])
        style.map("TNotebook.Tab", background=[("selected", accent_color)], foreground=[("selected", "white")])
        style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color, font=(font_family, 10))
        style.configure("Treeview.Heading", font=(font_family, 10, "bold"), background=accent_color, foreground="white")
        
        # Configurar el fondo de la ventana principal
        root.configure(background=bg_color)
        
        return theme
    
    def get_available_themes(self):
        """
        Obtiene una lista de los temas disponibles.
        
        Returns:
            dict: Diccionario con los nombres de los temas como claves y los nombres para mostrar como valores
        """
        themes = {}
        for key, theme in self.THEMES.items():
            themes[key] = theme["name"]
        
        for key, theme in self.custom_themes.items():
            themes[key] = theme["name"]
            
        return themes
    
    def save_custom_theme(self, theme_name, theme_config):
        """
        Guarda un tema personalizado.
        
        Args:
            theme_name (str): Nombre del tema
            theme_config (dict): Configuración del tema
            
        Returns:
            bool: True si el tema se guardó correctamente, False en caso contrario
        """
        if not os.path.exists("themes"):
            os.makedirs("themes")
            
        try:
            self.custom_themes[theme_name] = theme_config
            
            with open(f"themes/{theme_name}.json", "w") as f:
                json.dump(theme_config, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Error al guardar el tema: {str(e)}")
            return False
    
    def load_custom_themes(self):
        """
        Carga los temas personalizados desde archivos.
        """
        if not os.path.exists("themes"):
            return
            
        for filename in os.listdir("themes"):
            if filename.endswith(".json"):
                theme_name = filename[:-5]  # Quitar la extensión .json
                try:
                    with open(f"themes/{filename}", "r") as f:
                        theme_config = json.load(f)
                        self.custom_themes[theme_name] = theme_config
                except Exception as e:
                    print(f"Error al cargar el tema {theme_name}: {str(e)}")
    
    def delete_custom_theme(self, theme_name):
        """
        Elimina un tema personalizado.
        
        Args:
            theme_name (str): Nombre del tema
            
        Returns:
            bool: True si el tema se eliminó correctamente, False en caso contrario
        """
        if theme_name in self.custom_themes:
            try:
                del self.custom_themes[theme_name]
                
                if os.path.exists(f"themes/{theme_name}.json"):
                    os.remove(f"themes/{theme_name}.json")
                    
                if self.current_theme == theme_name:
                    self.current_theme = "light"
                    
                return True
            except Exception as e:
                print(f"Error al eliminar el tema: {str(e)}")
        
        return False 