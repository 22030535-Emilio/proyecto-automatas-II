# Reporte Técnico Extenso: Compilador MiniWebLang (Matrix Edition)

Este documento contiene la especificación técnica completa y el diseño del compilador desarrollado para la materia de Lenguajes y Autómatas II.

---

## 1. DEFINICIÓN FORMAL DEL AUTÓMATA (7-TUPLA)
El sistema se rige por un Autómata de Pila (PDA) definido matemáticamente como:

**M = (Q, Σ, Γ, δ, q₀, Z₀, F)**

Donde:
- **Q** = {Q₀, Q_WAIT_VAL, Q_WAIT_SEMI, Q_WAIT_P1, Q_WAIT_P2, Q_WAIT_VAL_OPT, Q_FIN}
- **Σ** = {COMANDO, CADENA, PUNTOCOMA, LLAVE_C, EOF}
- **Γ** = {h1, h2, p, ul, li, section, a, #}
- **δ** = Función de transición (definida en la matriz de la Sección 3)
- **q₀** = Q₀ (Estado inicial)
- **Z₀** = # (Fondo de pila)
- **F** = {Q_FIN} (Aceptación por estado final y pila vacía a excepción de Z₀)

---

## 2. ANALIZADOR LÉXICO (FA): MATRIZ DE TRANSICIONES
El Lexer valida carácter por carácter utilizando una matriz de transición de 10 estados.

| E/C | LTR(0) | DIG(1) | QUO(2) | PSC(3) | LA(4) | LC(5) | SLH(6) | SPC(7) | OTR(8) | NL(9) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0 (Ini)** | 1 | -1 | 2 | 7 | 8 | 9 | 4 | 0 | -1 | 0 |
| **1 (Cmd)** | 1 | 1 | -2 | -2 | -2 | -2 | -2 | -2 | -1 | -2 |
| **2 (Str)** | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | -1 |
| **3 (StrC)** | -2 | -2 | -2 | -2 | -2 | -2 | -2 | -2 | -1 | -2 |
| **4 (/)** | -1 | -1 | -1 | -1 | -1 | -1 | 5 | -1 | -1 | -1 |
| **5 (Com)** | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 0 |

*Nota: El estado -1 indica Error Léxico y el -2 indica Aceptación de Lexema.*

---

## 3. ANALIZADOR SINTÁCTICO (PDA): MATRIZ DE ESTADOS
La lógica sintáctica se controla mediante una matriz que asocia el estado actual con el tipo de token entrante.

| Estado | COMANDO | CADENA | PUNTOCOMA | LLAVE_C | EOF |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Q0 (Base)** | (Q0, A_CMD) | Error | (Q0, A_POP) | (Q0, A_POP) | (99, A_FIN) |
| **Q1 (WaitVal)**| Error | (Q2, A_TEXT) | Error | Error | Error |
| **Q2 (WaitSemi)**| (Q0, A_IMPL_P)| Error | (Q0, A_POP) | (Q0, A_IMPL_P)| (99, A_FIN) |
| **Q3 (WaitP1)** | Error | (Q4, A_SAVE_P1)| Error | Error | Error |
| **Q5 (WaitOpt)** | (Q0, A_IMPL_P)| (Q2, A_TEXT) | (Q0, A_NOP) | Error | (99, A_FIN) |

---

## 4. DISEÑO DE LA TABLA DE SÍMBOLOS Y ERRORES
### Tabla de Símbolos
Se implementó un gestor de símbolos que almacena lexemas únicos, su categoría gramatical y un histórico de coordenadas.

### Pila de Errores (Categorización)
Los errores se clasifican mediante un sistema de códigos alfanuméricos:
- **L001**: Léxico. Símbolo no perteneciente al alfabeto.
- **P001**: Sintáctico. Violación de la gramática.
- **C001**: Semántico (Comando). Comando no reconocido.
- **S001**: Semántico (Estructura). Uso incorrecto de anidamiento.

---

## 5. ARQUITECTURA DEL CÓDIGO (ZERO-IF LOGIC)
La implementación cumple estrictamente con el requisito de no utilizar sentencias `if/else` para la toma de decisiones del autómata, sustituyéndolas por despacho de funciones en diccionarios.

```python
# Ejemplo del ciclo principal del Parser
while self.state != 99:
    transition = self.MATRIX[self.state].get(token.type)
    action_id = transition[1]
    self.DISPATCHER[action_id](token) # Llamada directa sin condicionales
```

---

## 6. PROGRAMAS DE PRUEBA Y RESULTADOS
### Ejemplo de Ejecución Exitosa
```miniweblang
TITULO "Proyecto Final";
SECCION {
    PARRAFO "Bienvenido al equipo 10";
    LISTA { ELEMENTO "Matrices"; ELEMENTO "Autómatas"; };
};
```

### Ejemplo de Detección de Error Semántico
```miniweblang
TITULO "Prueba";
ELEMENTO "Error"; // Lanza S001: ELEMENTO debe estar dentro de ul
```
