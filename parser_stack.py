from grammar import COMMAND_MAP
from components import SymbolTable, ErrorPile
from html_generator import HTMLGenerator

class ParserPDA:
    """
    Autómata de Pila (PDA) formal manejado por Matriz de Transiciones.
    El estado cambia según el token y el tope de la pila.
    """
    def __init__(self, tokens, error_pile):
        self.tokens = tokens
        self.error_pile = error_pile
        self.stack = ['#']
        self.state = 0 # Q0: Inicio
        self.symbol_table = SymbolTable()
        self.html = HTMLGenerator()
        self.pos = 0
        
        # Auxiliares
        self.temp_val = None
        self.temp_param1 = None

        # MATRIZ DE TRANSICIÓN
        # [Estado][TipoToken] -> (PróximoEstado, AcciónID)
        self.MATRIX = {
            0: { # Q0: Esperando comando o cierre
                'COMANDO': (0, 'A_CMD'), # El estado destino real lo determinará el tipo de comando en la acción
                'PUNTOCOMA': (0, 'A_POP'),
                'LLAVE_C': (0, 'A_POP'),
                'EOF': (99, 'A_NOP')
            },
            1: { # Q_WAIT_VAL: Esperando cadena de texto
                'CADENA': (2, 'A_TEXT'),
            },
            2: { # Q_WAIT_SEMI: Esperando punto y coma o cierre
                'PUNTOCOMA': (0, 'A_POP'),
                'COMANDO': (0, 'A_IMPLICIT_POP'),
                'LLAVE_C': (0, 'A_IMPLICIT_POP'),
            },
            3: { # Q_WAIT_P1: Enlace/Imagen (URL)
                'CADENA': (4, 'A_SAVE_P1'),
            },
            4: { # Q_WAIT_P2: Enlace/Imagen (Texto/Alt)
                'CADENA': (2, 'A_FINISH_P2'),
            },
            5: { # Q_WAIT_VAL_OPT: Elemento (Texto opcional)
                'CADENA': (2, 'A_TEXT'),
                'COMANDO': (0, 'A_NOP'),
                'PUNTOCOMA': (0, 'A_NOP'),
            }
        }

    def parse(self):
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            t_type = token.type
            
            # Buscar en matriz
            row = self.MATRIX.get(self.state, {})
            transition = row.get(t_type)
            
            if transition:
                next_state, action_id = transition
                
                # Ejecutar acción y obtener estado resultante (si la acción lo define)
                act_result = self._execute_action(action_id, token)
                
                # Avanzar puntero a menos que sea una acción que requiere reprocesar
                if action_id not in ['A_IMPLICIT_POP', 'A_NOP']:
                    self.pos += 1
                
                # Actualizar estado (prioridad al resultado de la acción para comandos)
                self.state = act_result if act_result is not None else next_state
            else:
                # Error Sintáctico
                self.error_pile.push("P001", f"Error Sintáctico: Token {t_type} no esperado en estado {self.state}", token.line, token.column)
                self.pos += 1
                self.state = 0 # Recuperación básica

        # Cierre final de pila
        while len(self.stack) > 1:
            top = self.stack.pop()
            self.html.close_tag(top)

        return self.html.generate_full_html()

    def _execute_action(self, action_id, token):
        if action_id == 'A_CMD':
            return self._action_command(token)
        elif action_id == 'A_POP':
            self._action_pop()
        elif action_id == 'A_IMPLICIT_POP':
            self._action_pop()
        elif action_id == 'A_TEXT':
            self.html.add_text(token.value)
        elif action_id == 'A_SAVE_P1':
            self.temp_param1 = token.value
        elif action_id == 'A_FINISH_P2':
            self._action_multi_param(token)
        elif action_id == 'A_NOP':
            pass
        return None

    def _action_command(self, token):
        cmd = token.value
        self.symbol_table.insert(cmd, "COMMAND", token.line)
        
        if cmd in ['TITULO', 'ENCABEZADO', 'PARRAFO', 'BOTON']:
            tag = COMMAND_MAP[cmd]
            self.html.open_tag(tag)
            self.stack.append(tag)
            return 1 # Q_WAIT_VAL
        elif cmd in ['LISTA', 'SECCION']:
            tag = COMMAND_MAP[cmd]
            self.html.open_tag(tag)
            self.stack.append(tag)
            return 0 # Q0
        elif cmd == 'ELEMENTO':
            if self.stack[-1] == 'li':
                self.stack.pop()
                self.html.close_tag('li')
            if self.stack[-1] != 'ul':
                self.error_pile.push("S001", "ELEMENTO fuera de LISTA", token.line, token.column)
            self.html.open_tag('li')
            self.stack.append('li')
            return 5 # Q_WAIT_VAL_OPT
        elif cmd == 'SUBLISTA':
            if self.stack[-1] != 'li':
                self.error_pile.push("S002", "SUBLISTA fuera de ELEMENTO", token.line, token.column)
            self.html.open_tag('ul')
            self.stack.append('ul')
            return 0
        elif cmd in ['ENLACE', 'IMAGEN']:
            self.temp_val = cmd
            return 3 # Q_WAIT_P1
        return 0

    def _action_pop(self):
        if len(self.stack) > 1:
            top = self.stack.pop()
            self.html.close_tag(top)

    def _action_multi_param(self, token):
        if self.temp_val == 'ENLACE':
            self.html.open_tag('a', {'href': self.temp_param1})
            self.html.add_text(token.value)
            self.stack.append('a')
        else: # IMAGEN
            self.html.open_tag('img', {'src': self.temp_param1, 'alt': token.value}, self_closing=True)
