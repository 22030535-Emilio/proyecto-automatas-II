# Guion Maestro para Video de Exposición (40 Minutos)
## Proyecto: Traductor MiniWebLang - Equipo 10

Este guion está diseñado para una exposición detallada y técnica de 40 minutos. Se recomienda dividir la pantalla entre la presentación de diapositivas (o los reportes HTML generados) y el código fuente en VS Code.

---

### BLOQUE 1: Introducción y Contexto (0:00 - 4:00)
*   **0:00 - 1:00: Apertura.** Bienvenida, presentación de los integrantes del Equipo 10 y nombre del proyecto: "Traductor MiniWebLang: De Pseudocódigo a HTML5 mediante Autómatas de Pila".
*   **1:00 - 2:30: El Problema.** Explicar por qué creamos MiniWebLang. La complejidad de HTML5 para principiantes y la necesidad de un lenguaje de marcado simplificado pero formalmente validado.
*   **2:30 - 4:00: Objetivos del Proyecto.** Mencionar la implementación de un compilador completo (Lexer, Parser, Semántico) basado estrictamente en la teoría de autómatas vista en clase.

### BLOQUE 2: Fundamentos Teóricos (4:00 - 12:00)
*   **4:00 - 6:00: Gramática Formal.** Mostrar la gramática EBNF (está en la Documentación V3/V4). Explicar por qué es una Gramática de Contexto Libre y por qué requiere un Autómata de Pila (PDA) en lugar de solo expresiones regulares.
*   **6:00 - 9:00: El Modelo Matemático.** Explicar la 7-tupla del PDA. Mostrar los estados (Q), el alfabeto (Σ) y los símbolos de la pila (Γ). Esto demuestra que el proyecto no es solo código, sino ciencia de la computación aplicada.
*   **9:00 - 12:00: Ventaja de la Matriz de Transiciones.** Explicar por qué decidimos no usar "if-else" anidados. Hablar sobre la eficiencia O(n) y la elegancia matemática de usar una matriz de estados.

### BLOQUE 3: Análisis Léxico - El Autómata Finito (12:00 - 18:00)
*   **12:00 - 14:00: Explicación de lexer.py.** Abrir el archivo `lexer.py`. Mostrar la `CHAR_MAP`. Explicar cómo convertimos cualquier caracter ASCII en un número de columna (0-9).
*   **14:00 - 16:00: La Matriz del Lexer.** Mostrar la tabla `MATRIX` en el código. Explicar el Estado 0 (Inicio), Estado 1 (Comandos), Estado 2 (Cadenas) y cómo los estados negativos (-1, -2) indican error o aceptación.
*   **16:00 - 18:00: Demo en Vivo (Errores Léxicos).** Abrir el Dashboard, escribir caracteres inválidos como `$` o `@` y mostrar cómo el Lexer los detecta inmediatamente y los manda a la pila de errores.

### BLOQUE 4: Análisis Sintáctico y Semántico - El PDA (18:00 - 28:00)
*   **18:00 - 20:00: El Corazón del Parser.** Abrir `parser_stack.py`. Explicar el uso de la Pila (Stack) de Python para simular el comportamiento de un PDA real.
*   **20:00 - 23:00: Reglas de Transición.** Explicar cómo la matriz decide qué hacer. Ejemplo: "Si estoy en Q0 y llega un comando TITULO, apilo 'h1' y cambio al estado Q_WAIT_VAL".
*   **23:00 - 26:00: Validación Semántica.** Mostrar la lógica de `ELEMENTO` y `SUBLISTA`. Explicar que el programa verifica que un `ELEMENTO` esté dentro de una `LISTA` mirando el tope de la pila. Si el tope no es `ul`, es un error semántico.
*   **26:00 - 28:00: Demo en Vivo (Errores de Estructura).** Mostrar qué pasa si olvidas cerrar una sección o si pones un elemento de lista en el lugar equivocado. Mostrar la Pila de Errores en el Dashboard.

### BLOQUE 5: Componentes Internos y Generación (28:00 - 33:00)
*   **28:00 - 30:00: Tabla de Símbolos.** Mostrar el archivo `components.py`. Explicar cómo se guardan los lexemas y sus ocurrencias (líneas). Mostrar la pestaña de "Tabla de Símbolos" en el Dashboard después de compilar.
*   **30:00 - 33:00: Generador de HTML.** Explicar `html_generator.py`. Cómo se van construyendo las etiquetas dinámicamente y el proceso de cierre final de la pila (cuando el PDA termina, vacía la pila cerrando todas las etiquetas pendientes).

### BLOQUE 6: Interfaz Web y Arquitectura (33:00 - 37:00)
*   **33:00 - 35:00: El Dashboard (Frontend).** Mostrar el diseño premium del Dashboard. Explicar el uso de AJAX/Fetch para enviar el código al servidor Flask sin recargar la página.
*   **35:00 - 37:00: Servidor Flask.** Mostrar `app.py`. Explicar la ruta `/compile` y cómo integra todas las piezas (Lexer -> Parser -> JSON Response).

### BLOQUE 7: Conclusiones y Cierre (37:00 - 40:00)
*   **37:00 - 38:30: Retos Superados.** Hablar sobre la dificultad de implementar el PDA sin usar librerías externas de parsing. Lo que aprendieron sobre el manejo de estados.
*   **38:30 - 39:30: Futuro del Proyecto.** Menciones sobre agregar estilos CSS personalizados o un modo "Live Preview" mientras escribes.
*   **39:30 - 40:00: Despedida.** Agradecimientos al profesor y a la audiencia. Cierre del video.

---

### Consejos para la grabación:
1.  **Ritmo:** No corras. Tienes 40 minutos, así que tómate tu tiempo para explicar el código línea por línea en las secciones clave.
2.  **Visuales:** Usa la **Especificación Maestra V4** que te generé. Es un recurso visual excelente para mostrar las tablas y diagramas mientras hablas.
3.  **Preparación:** Ten listos los archivos de `ejemplos_errores/` para cargarlos rápidamente en el dashboard durante las demostraciones.
