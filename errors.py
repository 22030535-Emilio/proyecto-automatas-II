import sys

class WebLangError(Exception):
    """Clase base para errores en el traductor WebLang."""
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

class LexicalError(WebLangError):
    """Error detectado durante el análisis léxico."""
    pass

class SyntacticError(WebLangError):
    """Error detectado durante el análisis sintáctico (Autómata de Pila)."""
    pass

class SemanticError(WebLangError):
    """Error de lógica (ej. comando no permitido en cierto contexto)."""
    pass
