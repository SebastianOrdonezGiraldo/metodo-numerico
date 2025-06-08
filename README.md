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
- Soporte para múltiples temas visuales
- Comparación con soluciones analíticas cuando están disponibles

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
- Dependencias listadas en `requirements.txt`:
  - numpy
  - matplotlib
  - PyQt6
  - pandas
  - scipy

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
- Crecimiento exponencial: dy/dt = ky
- Decaimiento exponencial: dy/dt = -ky
- Ecuación logística: dy/dt = ry(1-y/K)
- Oscilador amortiguado: d²y/dt² + 2ζω₀dy/dt + ω₀²y = 0

## Características Técnicas

### Métodos Numéricos Implementados

1. **Método de Euler**
   - Método explícito de primer orden
   - Simple pero menos preciso
   - Ideal para introducción a métodos numéricos

2. **Método de Heun**
   - Método predictor-corrector de segundo orden
   - Mayor precisión que Euler
   - Balance entre precisión y complejidad

3. **Método RK4**
   - Método de cuarto orden
   - Alta precisión
   - Requiere más cálculos por paso

### Análisis de Convergencia

- Comparación de errores entre métodos
- Análisis de estabilidad
- Visualización de tasas de convergencia

## Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrese de:
1. Hacer fork del repositorio
2. Crear una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Hacer commit de sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Hacer push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Reportar Problemas

Si encuentra algún problema o tiene una sugerencia, por favor:
1. Revise los issues existentes
2. Cree un nuevo issue con una descripción detallada del problema
3. Incluya pasos para reproducir el problema
4. Adjunte capturas de pantalla si es relevante

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o sugerencias, por favor:
- Abra un issue en el repositorio
- Contacte al mantenedor del proyecto

## Agradecimientos

- A todos los contribuidores que han ayudado a mejorar el proyecto
- A la comunidad de Python por las excelentes bibliotecas utilizadas 