# grafIA 🎮📊

> Donde las matemáticas se encuentran con la inteligencia artificial

Proyecto generado para la Feria de Matemáticas con sede en CU2 BUAP

## Descripción

**grafIA** es una aplicación web interactiva con dos juegos matemáticos que utilizan conceptos de inteligencia artificial:

### 🎨 grafIA Learn
Dibuja una curva en el canvas y observa cómo un algoritmo de regresión polinomial aprende a replicarla. El sistema calcula el error y genera una puntuación basada en qué tan bien la IA pudo aprender tu dibujo.

### 🧠 grafIA Guess  
El sistema genera una función matemática aleatoria y muestra su gráfica. Tu objetivo es adivinar la función observando la curva. Se evalúa por precisión y tiempo.

## Tecnologías

- **Backend:** Python + Django
- **Frontend:** Django Templates + HTML5 + CSS3 + JavaScript Vanilla
- **Base de datos:** SQLite
- **IA:** Regresión polinomial con NumPy

## Requisitos

- Python 3.10+
- pip

## Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
cd /ruta/al/proyecto/grafIA
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar entorno virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install django numpy
```

### 5. Aplicar migraciones (si es la primera vez)

```bash
python manage.py migrate
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

### 7. Abrir en el navegador

Visita: **http://127.0.0.1:8000**

## Estructura del Proyecto

```
grafIA/
├── grafia_project/      # Configuración de Django
├── games/               # Aplicación principal
│   ├── models.py        # Modelos de puntuaciones
│   ├── views.py         # Vistas y endpoints API
│   └── urls.py          # Rutas
├── templates/           # Templates HTML
│   ├── base.html
│   └── games/
│       ├── landing.html
│       ├── learn.html
│       ├── guess.html
│       ├── leaderboard_learn.html
│       └── leaderboard_guess.html
├── static/
│   └── css/
│       └── styles.css   # Estilos CSS
├── manage.py
└── README.md
```

## Funciones Soportadas en grafIA Guess

El sistema genera y reconoce las siguientes funciones:

- Lineales: `ax + b`
- Cuadráticas: `ax^2 + bx + c`
- Trigonométricas: `sin(x)`, `cos(x)`, `sin(ax)`, `cos(ax)`
- Valor absoluto: `|x|`, `a|x| + b`
- Cúbicas: `ax^3`

## Sintaxis para Escribir Funciones

Al adivinar funciones, puedes usar:

- Multiplicación: `*` → Ejemplo: `2*x`
- Potencias: `^` o `**` → Ejemplo: `x^2` o `x**2`
- Funciones: `sin(x)`, `cos(x)`, `abs(x)`, `log(x)`, `sqrt(x)`
- Constantes: `pi`, `e`
