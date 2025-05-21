# Solucionador de EDOs - Método de Heun

Esta aplicación de escritorio permite resolver Ecuaciones Diferenciales Ordinarias (EDOs) de primer orden utilizando el método de Heun (también conocido como método de Euler mejorado).

## Características

- Interfaz gráfica amigable desarrollada con Tkinter
- Resolución de EDOs de primer orden mediante el método de Heun
- Visualización de resultados en formato tabular
- Gráficas de la solución numérica usando matplotlib
- Exportación de resultados a formato CSV
- Validación de entradas y manejo de errores robusto
- Registro de mensajes y errores

## Requisitos

- Python 3.10 o superior
- Bibliotecas:
  - numpy
  - matplotlib
  - sympy
  - tkinter (incluido en la mayoría de instalaciones de Python)

## Instalación

1. Clonar o descargar este repositorio
2. Instalar las dependencias:

```bash
pip install numpy matplotlib sympy
```

## Uso

1. Ejecutar la aplicación:

```bash
python main.py
```

2. En la interfaz, completar los siguientes campos:
   - Función f(t, y): La función que define la EDO (ej: `y - t**2 + 1`)
   - Valor inicial de t: El valor inicial para t
   - Valor inicial de y: El valor inicial para y
   - Tamaño de paso h: El incremento entre cada paso
   - Número de pasos: Cantidad de pasos a calcular

3. Hacer clic en "Calcular" para obtener la solución
4. Ver los resultados en la pestaña "Tabla" o "Gráfica"
5. Opcionalmente, exportar los resultados a CSV con el botón "Exportar a CSV"

## Método de Heun

El método de Heun es un método numérico de segundo orden para resolver EDOs de la forma:

```
dy/dt = f(t, y)
```

El algoritmo utiliza un enfoque predictor-corrector:

1. **Predictor** (método de Euler):
   ```
   y_pred = y_n + h * f(t_n, y_n)
   ```

2. **Corrector** (método de Heun):
   ```
   y_{n+1} = y_n + (h/2) * [f(t_n, y_n) + f(t_{n+1}, y_pred)]
   ```

Donde:
- t_n es el tiempo en el paso n
- y_n es el valor de y en el paso n
- h es el tamaño de paso
- f(t, y) es la función que define la EDO

## Ejemplos de funciones

Algunos ejemplos de funciones que puede ingresar:

- `y - t**2 + 1` (EDO lineal simple)
- `y**2 - t` (EDO no lineal)
- `sin(t) + cos(y)` (EDO con funciones trigonométricas)
- `exp(-t) * y` (EDO con función exponencial)

## Limitaciones

- Solo resuelve EDOs de primer orden
- La precisión depende del tamaño de paso elegido
- Para EDOs con soluciones que cambian rápidamente, puede requerir un tamaño de paso muy pequeño 