# Conceptos Científicos y Matemáticos en grafIA

### 1. Regresión Polinomial (Machine Learning / Análisis Numérico)
Se utiliza para que la "IA" deduzca la ecuación matemática de la curva que el usuario dibuja a mano alzada en el modo **Learn**.
*   **Dónde:** En `games/views.py` dentro de la función `api_fit_curve`.
*   **Cómo funciona:** Extrae los puntos $(x, y)$ proporcionados por el dibujo del usuario y utiliza el método de mínimos cuadrados a través de interpolación de NumPy (`np.polyfit`). Itera probando polinomios de grado 1 al 7 para encontrar la curva que mejor imite el trazo humano (generando coeficientes para formas de tipo $ax^2 + bx + c$, $ax^3...$).

### 2. Regularización y Prevención de Sobreajuste (Estadística)
Al buscar la mejor curva, un polinomio de grado 7 casi siempre tocará todos los puntos, pero creará una gráfica muy caótica (conocido matemáticamente como el *Fenómeno de Runge* o *Overfitting*).
*   **Dónde:** En `games/views.py` dentro del bucle de grados en `api_fit_curve`.
*   **Cómo funciona:** Se implementó un **factor de penalización** algorítmica: `adjusted_mse = mse * (1 + 0.15 * degree)`. Esto obliga al sistema (fiel al principio científico de la *Navaja de Ockham*) a preferir explicaciones o fórmulas más simples y suaves a menos que un grado superior justifique la ganancia en precisión.

### 3. Métricas de Error y Desempeño (Estadística)
Para calcular qué tan cerca está la IA de tu dibujo o qué tan bien adivinaste en el modo Guess, el código depende de medidas estadísticas rigurosas.
*   **Dónde:** En `games/views.py` en `api_fit_curve` y `api_compare_function`.
*   **Cómo funciona:** 
    *   **MSE (Mean Squared Error)** y **RMSE (Root Mean Squared Error):** Calculan la distancia vertical promedio al cuadrado entre la función generada y los puntos reales.
    *   **Coeficiente de Determinación ($R^2$):** Una fórmula estadística que dice qué "porcentaje de la varianza" fue correctamente modelada (1 es perfecto, 0 es pésimo). En base al error $1 - R^2$, el juego asigna la puntuación que ves en pantalla.
