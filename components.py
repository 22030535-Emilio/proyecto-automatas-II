class SymbolTable:
    """Tabla de Símbolos para registrar comandos y su uso en el documento."""
    def __init__(self):
        self.symbols = {}

    def insert(self, name, kind, line):
        if name not in self.symbols:
            self.symbols[name] = {"kind": kind, "occurrences": [line]}
        else:
            self.symbols[name]["occurrences"].append(line)

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

class ErrorEntry:
    def __init__(self, code, message, line, column):
        self.code = code
        self.message = message
        self.line = line
        self.column = column

    def __repr__(self):
        return f"[{self.code}] L{self.line}:C{self.column} - {self.message}"

class ErrorPile:
    """Pila de errores para recolectar fallos durante el análisis."""
    def __init__(self):
        self.errors = []

    def push(self, code, message, line, column):
        self.errors.append(ErrorEntry(code, message, line, column))

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for e in self.errors:
            print(e)
