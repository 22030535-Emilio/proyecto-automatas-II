import sys

class MiniWebError(Exception):
    """Clase base para errores en el traductor MiniWebLang."""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.message)

    def __str__(self):
        if self.line and self.column:
            return f"Error en Línea {self.line}, Columna {self.column}: {self.message}"
        if self.line:
            return f"Error en Línea {self.line}: {self.message}"
        return f"Error: {self.message}"

class LexicalError(MiniWebError):
    """Error detectado durante el análisis léxico."""
    pass

class SyntacticError(MiniWebError):
    """Error detectado durante el análisis sintáctico (Autómata de Pila)."""
    pass

class SemanticError(MiniWebError):
    """Error de lógica (ej. comando no permitido en cierto contexto)."""
    pass
