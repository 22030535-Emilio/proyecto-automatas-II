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
    Lexer basado en un Autómata Finito Estricto.
    Sin sentencias IF para la lógica de estados; utiliza mapeo directo en matriz.
    """
    def __init__(self, code, error_pile):
        # Añadimos un caracter final para forzar la aceptación del último token
        self.code = code + " " 
        self.error_pile = error_pile
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Mapeo ASCII a columnas de la matriz (128 caracteres estándar)
        # 0: Letra, 1: Dígito, 2: Comilla, 3: PuntoComa, 4: LlaveA, 5: LlaveC, 6: Slash, 7: Espacio, 8: Otros, 9: Salto de Línea
        self.CHAR_MAP = [8] * 256
        for c in range(65, 91): self.CHAR_MAP[c] = 0   # A-Z
        for c in range(97, 123): self.CHAR_MAP[c] = 0  # a-z
        for c in range(48, 58): self.CHAR_MAP[c] = 1   # 0-9
        self.CHAR_MAP[ord('"')] = 2
        self.CHAR_MAP[ord(';')] = 3
        self.CHAR_MAP[ord('{')] = 4
        self.CHAR_MAP[ord('}')] = 5
        self.CHAR_MAP[ord('/')] = 6
        self.CHAR_MAP[ord(' ')] = 7
        self.CHAR_MAP[ord('\t')] = 7
        self.CHAR_MAP[ord('\r')] = 7
        self.CHAR_MAP[ord('\n')] = 9 
        self.CHAR_MAP[ord('_')] = 0 # Tratar guion bajo como letra
        self.CHAR_MAP[ord(':')] = 8 # Otros caracteres permitidos
        self.CHAR_MAP[ord('.')] = 8
        self.CHAR_MAP[ord('-')] = 8
        self.CHAR_MAP[ord(',')] = 8
        self.CHAR_MAP[ord('!')] = 8
        self.CHAR_MAP[ord('?')] = 8
        self.CHAR_MAP[ord('(')] = 8
        self.CHAR_MAP[ord(')')] = 8

        # Matriz de Transiciones
        # Estados >= 0 son normales.
        # Estado -1 = Error Léxico
        # Estado -2 = Aceptación de Token
        # LTR(0) DIG(1) QUO(2) PSC(3) LA(4) LC(5) SLH(6) SPC(7) OTR(8) NL(9)
        self.MATRIX = [
            [  1,  -1,   2,   7,   8,   9,   4,   0,  -1,   0], # 0: Inicio
            [  1,   1,  -2,  -2,  -2,  -2,  -2,  -2,  -1,  -2], # 1: Comando (reconoce hasta encontrar algo que no sea letra/num)
            [  2,   2,   3,   2,   2,   2,   2,   2,   2,  -1], # 2: Interior de Cadena
            [ -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -1,  -2], # 3: Cadena cerrada
            [ -1,  -1,  -1,  -1,  -1,  -1,   5,  -1,  -1,  -1], # 4: Primer '/' (Comentario)
            [  5,   5,   5,   5,   5,   5,   5,   5,   5,   0], # 5: Ignorando comentario (NL regresa a 0)
            [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 6: (No usado)
            [ -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -1,  -2], # 7: PuntoComa (Aceptado)
            [ -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -1,  -2], # 8: LlaveA (Aceptado)
            [ -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -1,  -2], # 9: LlaveC (Aceptado)
        ]

        # Diccionario que mapea estados de aceptación de vuelta a un tipo de token
        self.TOKEN_TYPES = {
            1: 'COMANDO',
            3: 'CADENA',
            7: 'PUNTOCOMA',
            8: 'LLAVE_A',
            9: 'LLAVE_C'
        }

    def tokenize(self):
        while self.pos < len(self.code) - 1:
            state = 0
            lexeme = ""
            start_col = self.column
            
            # Ciclo del autómata finito para 1 solo lexema
            while state >= 0 and self.pos < len(self.code):
                char = self.code[self.pos]
                ord_c = ord(char) if ord(char) < 256 else 8
                char_class = self.CHAR_MAP[ord_c]
                next_state = self.MATRIX[state][char_class]

                # Acciones asociadas al salto de línea y espacios manejadas sin ifs anidados
                # usando diccionarios para sumar posiciones
                self.line += {9: 1}.get(char_class, 0)
                self.column = {9: 1}.get(char_class, self.column + 1)
                
                # Para acumular el lexema, usamos un diccionario que determina si sumamos o no basándonos en si es espacio en el estado 0
                add_char = {True: "", False: char}.get(state == 0 and char_class in [7, 9])
                lexeme += add_char

                if next_state == -2:
                    # Aceptación: Creamos token y no avanzamos pos porque el caracter actual causó el quiebre
                    t_type = self.TOKEN_TYPES.get(state, 'UNKNOWN')
                    # Diccionario para limpiar comillas en cadenas sin usar if
                    clean_lex = {'CADENA': lexeme[1:-2]}.get(t_type, lexeme[:-1])
                    self.tokens.append(Token(t_type, clean_lex.strip(), self.line, start_col))
                    break
                
                if next_state == -1:
                    # Error léxico
                    self.error_pile.push("L001", f"Lexema inválido cerca de: {char}", self.line, start_col)
                    self.pos += 1
                    break

                # Comentario multilínea resetea directo con 0 según la matriz, limpiamos lexema
                lexeme = {0: "", 5: ""}.get(next_state, lexeme)
                
                state = next_state
                self.pos += 1

        return self.tokens
