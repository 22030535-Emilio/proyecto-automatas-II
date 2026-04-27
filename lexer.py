from components import ErrorPile

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}, {self.column})"

class LexerFA:
    """
    Lexer basado en un Autómata Finito (FA) con Matriz de Transiciones.
    Validación carácter por carácter.
    """
    def __init__(self, code, error_pile):
        self.code = code
        self.error_pile = error_pile
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Mapeo de Caracteres a Clases (Columnas de la Matriz)
        # 0: Letra (A-Z), 1: Dígito (0-9), 2: Comilla ("), 3: PuntoComa (;), 
        # 4: LlaveA ({), 5: LlaveC (}), 6: Slash (/), 7: Espacio, 8: Otros
        self.CHAR_MAP = {} # Se llena dinámicamente

        # Matriz de Transiciones
        # Estados: 0: Inicio, 1: Comando, 2: String(Abierto), 3: String(Cerrando), 4: Slash, 5: Comentario
        # -1 representa estado de error léxico
        # [LTR, DIG, QUO, PSC, LA, LC, SLH, SPC, OTR]
        self.MATRIX = [
            [ 1, -1,  2,  7,  8,  9,  4,  0, -1], # 0: Inicio
            [ 1,  1, -1, -1, -1, -1, -1, -1, -1], # 1: Comando (Sigue leyendo letras/nums)
            [ 2,  2,  3,  2,  2,  2,  2,  2,  2], # 2: Leyendo interior String (Acepta casi todo)
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], # 3: String Cerrado (Estado de aceptación)
            [-1, -1, -1, -1, -1, -1,  5, -1, -1], # 4: Primer SLASH visto
            [ 5,  5,  5,  5,  5,  5,  5,  5,  5], # 5: Ignorando comentario hasta \n
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], # 6: (No usado)
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], # 7: PuntoComa (Aceptación)
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], # 8: LlaveA (Aceptación)
            [-1, -1, -1, -1, -1, -1, -1, -1, -1], # 9: LlaveC (Aceptación)
        ]

    def _get_char_class(self, char):
        if char.isalpha(): return 0
        if char.isdigit(): return 1
        if char == '"': return 2
        if char == ';': return 3
        if char == '{': return 4
        if char == '}': return 5
        if char == '/': return 6
        if char.isspace(): return 7
        return 8

    def tokenize(self):
        while self.pos < len(self.code):
            state = 0
            lexeme = ""
            start_col = self.column
            
            # El autómata avanza mientras no llegue a un estado final (o error)
            # y el carácter no sea un espacio que reinicia el ciclo en el estado 0
            while self.pos < len(self.code):
                char = self.code[self.pos]
                char_class = self._get_char_class(char)
                next_state = self.MATRIX[state][char_class]

                if next_state == -1:
                    # Si estamos en inicio y no reconoce, es error
                    if state == 0 and char_class != 7:
                        self.error_pile.push("L001", f"Carácter inválido: {char}", self.line, self.column)
                        self.pos += 1
                        self.column += 1
                        break
                    else:
                        # Si estábamos reconociendo algo, el estado anterior era el lexema completo
                        break 

                # Manejo de línea y columna
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1

                # Acumular lexema si no es espacio en el estado inicial
                if not (state == 0 and char_class == 7):
                    lexeme += char
                
                state = next_state
                self.pos += 1

                # Salir si llegamos a un estado que es atómico (punto y coma, llaves)
                if state in [3, 7, 8, 9]:
                    break
                
                # Para comentarios, consumimos hasta fin de línea
                if state == 5:
                    while self.pos < len(self.code) and self.code[self.pos] != '\n':
                        self.pos += 1
                        self.column += 1
                    state = 0 # Reiniciar tras comentario
                    lexeme = ""
                    break

            # Determinar tipo de token al salir del autómata
            if state == 1:
                self.tokens.append(Token('COMANDO', lexeme, self.line, start_col))
            elif state == 3:
                self.tokens.append(Token('CADENA', lexeme[1:-1], self.line, start_col))
            elif state == 7:
                self.tokens.append(Token('PUNTOCOMA', ';', self.line, start_col))
            elif state == 8:
                self.tokens.append(Token('LLAVE_A', '{', self.line, start_col))
            elif state == 9:
                self.tokens.append(Token('LLAVE_C', '}', self.line, start_col))
            
        return self.tokens
