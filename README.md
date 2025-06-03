# Solucionador de Ecuaciones Diferenciales Ordinarias (EDOs)

Este proyecto es una aplicación de escritorio que permite resolver ecuaciones diferenciales ordinarias utilizando diferentes métodos numéricos. La aplicación cuenta con una interfaz gráfica intuitiva y ofrece visualización de resultados tanto en forma de tabla como de gráficas.

## Características Principales

- Resolución de EDOs usando múltiples métodos numéricos:
  - Método de Euler
  - Método de Heun
  - Método de Runge-Kutta de orden 4 (RK4)
- Interfaz gráfica moderna y fácil de usar
- Visualización de resultados en tablas y gráficas
- Exportación de resultados a CSV
- Ejemplos predefinidos para facilitar el uso
- Validación de entradas
- Análisis de convergencia

## Estructura del Proyecto

```
├── main.py              # Archivo principal de la aplicación
├── app.py              # Punto de entrada de la aplicación
├── solvers/            # Implementaciones de los métodos numéricos
│   ├── base_solver.py  # Clase base para los solucionadores
│   ├── euler_solver.py # Implementación del método de Euler
│   ├── heun_solver.py  # Implementación del método de Heun
│   └── rk4_solver.py   # Implementación del método RK4
├── utils/              # Utilidades y herramientas auxiliares
│   ├── analytic_solution.py    # Soluciones analíticas para comparación
│   ├── config_manager.py       # Gestión de configuración
│   ├── convergence_analysis.py # Análisis de convergencia
│   ├── plot_utils.py          # Utilidades para gráficas
│   ├── theme_manager.py       # Gestión de temas visuales
│   └── validation_utils.py    # Utilidades de validación
└── requirements.txt    # Dependencias del proyecto
```

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
python app.py
```

2. En la interfaz gráfica:
   - Seleccionar el método numérico deseado
   - Ingresar la ecuación diferencial en formato f(t,y)
   - Configurar los valores iniciales y parámetros
   - Hacer clic en "Calcular" para obtener resultados
   - Visualizar resultados en la tabla o gráfica
   - Opcionalmente exportar resultados a CSV

## Ejemplos Predefinidos

La aplicación incluye varios ejemplos predefinidos:
- Crecimiento exponencial
- Decaimiento exponencial
- Ecuación logística
- Oscilador amortiguado

## Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrese de:
1. Hacer fork del repositorio
2. Crear una rama para su feature
3. Hacer commit de sus cambios
4. Hacer push a la rama
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 