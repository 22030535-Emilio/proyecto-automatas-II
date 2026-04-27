# Especificación Formal del Autómata de Pila (PDA)

Este documento detalla la definición formal del autómata utilizado para el reconocimiento y traducción de `MiniWebLang` a `HTML5`.

## 1. Definición Formal (7-tupla)
El autómata $M$ se define como:
$M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$

Donde:
- **$Q$**: Conjunto de estados = $\{Q_0, Q_{WAIT\_VAL}, Q_{WAIT\_VAL\_OPT}, Q_{WAIT\_SEMI}, Q_{WAIT\_PARAM1}, Q_{WAIT\_PARAM2}, Q_{error}\}$
- **$\Sigma$**: Alfabeto de entrada = $\{COMANDO, CADENA, PUNTOCOMA, LLAVE\_A, LLAVE\_C, EOF\}$
- **$\Gamma$**: Alfabeto de la pila = $\{h1, h2, p, ul, li, section, a, \#\}$
- **$\delta$**: Función de transición (basada en el estado actual y el token):

| Estado | Token (Entrada) | Tope Pila | Acción (Genera HTML) | Nuevo Estado | Nueva Pila |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $Q_0$ | TITULO | any | emitir `<h1>`, apilar `h1` | $Q_{WAIT\_VAL}$ | `h1, ...` |
| $Q_0$ | LISTA | any | emitir `<ul>`, apilar `ul` | $Q_0$ | `ul, ...` |
| $Q_{WAIT\_VAL}$ | CADENA | `X` | emitir contenido `CADENA` | $Q_{WAIT\_SEMI}$ | `X, ...` |
| $Q_{WAIT\_SEMI}$ | `;` | `X` | desapilar `X`, emitir `</X>` | $Q_0$ | `...` |
| $Q_0$ | ELEMENTO | `ul` | emitir `<li>`, apilar `li` | $Q_{WAIT\_VAL\_OPT}$ | `li, ul, ...` |
| $Q_0$ | ELEMENTO | `li` | desapilar `li`, emitir `<li>`, apilar `li` | $Q_{WAIT\_VAL\_OPT}$ | `li, ul, ...` |
| $Q_0$ | `;` | `X` | desapilar `X`, emitir `</X>` | $Q_0$ | `...` |
| $Q_0$ | EOF | $X \in \Gamma$ | desapilar $X$, emitir `</X>` hasta $\#$ | $F$ | $\#$ |

## 3. Comportamiento de Comandos Atómicos
Los comandos como `TITULO`, `PARRAFO`, `BOTON`, `ENLACE` e `IMAGEN` son tratados como transiciones que no alteran la pila permanentemente (apilan y desapilan inmediatamente al terminar su instrucción).

## 4. Detección de Errores
- Si se encuentra `ELEMENTO` y el tope de la pila NO es `ul` ni `li`, el autómata transita a un estado de error (Error Semántico).
- Si se encuentra `SUBLISTA` y el tope de la pila NO es `li`, se reporta error.
- Cualquier token no reconocido por la gramática genera un Error Léxico.
