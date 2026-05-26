from grammar import COMMAND_MAP
from components import SymbolTable, ErrorPile
from html_generator import HTMLGenerator

class ParserPDA:
    """
    Autómata de Pila (PDA) formal manejado por Matriz de Transiciones estricta sin ifs.
    """
    def __init__(self, tokens, error_pile):
        from lexer import Token
        self.tokens = tokens + [Token('EOF', '', -1, -1)]
        self.error_pile = error_pile
        self.stack = ['#']
        self.state = 0
        self.symbol_table = SymbolTable()
        self.html = HTMLGenerator()
        self.pos = 0
        self.temp_val = None
        self.temp_param1 = None

        # MATRIZ DE TRANSICIÓN
        # [Estado][TipoToken] -> (NuevoEstado, AccionID)
        self.MATRIX = {
            0: {
                'COMANDO': (0, 'A_CMD'), 
                'PUNTOCOMA': (0, 'A_POP'),
                'LLAVE_A': (0, 'A_NOP'),
                'LLAVE_C': (0, 'A_POP'),
                'EOF': (99, 'A_FINISH')
            },
            1: {
                'CADENA': (2, 'A_TEXT'),
                'LLAVE_A': (1, 'A_NOP'),
                'LLAVE_C': (0, 'A_POP'), # Cierre seguro
                'COMANDO': (0, 'A_CMD')  # Soporte para comandos sin cadena
            },
            2: {
                'PUNTOCOMA': (0, 'A_POP'),
                'COMANDO': (0, 'A_CMD'),
                'LLAVE_A': (2, 'A_NOP'),
                'LLAVE_C': (0, 'A_POP'),
                'EOF': (99, 'A_FINISH')
            },
            3: {
                'CADENA': (4, 'A_SAVE_P1'),
            },
            4: {
                'CADENA': (2, 'A_FINISH_P2'),
            },
            5: {
                'CADENA': (2, 'A_TEXT'),
                'COMANDO': (0, 'A_CMD'),
                'LLAVE_A': (5, 'A_NOP'),
                'PUNTOCOMA': (0, 'A_POP'),
                'LLAVE_C': (0, 'A_POP'),
                'EOF': (99, 'A_FINISH')
            }
        }

        # Despachador de funciones para acciones
        self.DISPATCHER = {
            'A_CMD': self._action_command,
            'A_POP': self._action_pop,
            'A_IMPLICIT_POP': self._action_implicit_pop,
            'A_TEXT': self._action_text,
            'A_SAVE_P1': self._action_save_p1,
            'A_FINISH_P2': self._action_finish_p2,
            'A_NOP': lambda t: None,
            'A_FINISH': lambda t: None,
            'E_SYNTAX': self._action_error
        }

        # Tabla estricta de comportamientos por comando
        self.CMD_RULES = {
            'TITULO': {'tag': 'h1', 'push': 'h1', 'next': 1},
            'ENCABEZADO': {'tag': 'h2', 'push': 'h2', 'next': 1},
            'PARRAFO': {'tag': 'p', 'push': 'p', 'next': 1},
            'BOTON': {'tag': 'button', 'push': 'button', 'next': 1},
            'LISTA': {'tag': 'ul', 'push': 'ul', 'next': 0},
            'SECCION': {'tag': 'section', 'push': 'section', 'next': 0},
            'NAVEGACION': {'tag': 'nav', 'push': 'nav', 'next': 0},
            'PIE': {'tag': 'footer', 'push': 'footer', 'next': 0},
            'ARTICULO': {'tag': 'article', 'push': 'article', 'next': 0},
            'ELEMENTO': {'tag': 'li', 'push': 'li', 'next': 5, 'require_top': 'ul', 'implicit_close': 'li'},
            'SUBLISTA': {'tag': 'ul', 'push': 'ul', 'next': 0, 'require_top': 'li'},
            'NEGRILLA': {'tag': 'strong', 'push': 'strong', 'next': 1},
            'CURSIVA': {'tag': 'em', 'push': 'em', 'next': 1},
            'SUBRAYADO': {'tag': 'u', 'push': 'u', 'next': 1},
            'CITA': {'tag': 'blockquote', 'push': 'blockquote', 'next': 1},
            'DIVISOR': {'tag': 'hr', 'push': None, 'next': 0, 'self_closing': True},
            'ENLACE': {'next': 3, 'special': True},
            'IMAGEN': {'next': 3, 'special': True},
            'VIDEO': {'next': 3, 'special': True},
            'CONTENEDOR': {'tag': 'div', 'push': 'div', 'next': 0},
            'GRID': {'tag': 'div', 'push': 'div', 'next': 0, 'class': 'grid-layout'},
            'COLUMNA': {'tag': 'div', 'push': 'div', 'next': 0, 'require_top': 'div'},
            'CODIGO': {'tag': 'code', 'push': 'code', 'next': 1},
            'PEQUENO': {'tag': 'small', 'push': 'small', 'next': 1},
            'SPAN': {'tag': 'span', 'push': 'span', 'next': 1},
            'SALTO': {'tag': 'br', 'push': None, 'next': 0, 'self_closing': True},
            'FORMULARIO': {'tag': 'form', 'push': 'form', 'next': 0},
            'ENTRADA': {'next': 3, 'special': True},
            'AREA_TEXTO': {'next': 3, 'special': True},
            'TEXTO': {'tag': 'p', 'push': 'p', 'next': 1},
            'CONSULTA': {'tag': 'div', 'push': 'div', 'next': 0, 'class': 'query-container'},
            'FILTRO': {'tag': 'aside', 'push': 'aside', 'next': 0},
            'DATO': {'next': 3, 'special': True}, # Especial: Clave y Valor
            'TABLA': {'tag': 'table', 'push': 'table', 'next': 0},
            'FILA': {'tag': 'tr', 'push': 'tr', 'next': 0, 'require_top': 'table'},
            'CELDA': {'tag': 'td', 'push': 'td', 'next': 1, 'require_top': 'tr'},
            'HERO': {'tag': 'section', 'push': 'section', 'next': 0, 'class': 'hero-banner'},
            'MODAL': {'tag': 'div', 'push': 'div', 'next': 0, 'class': 'modal-overlay'},
            'PROGRESO': {'tag': 'div', 'push': None, 'next': 3, 'special': True}, # Valor y Max
            'CHIP': {'tag': 'span', 'push': 'span', 'next': 1, 'class': 'chip'},
            'AVATAR': {'tag': 'img', 'push': None, 'next': 1, 'self_closing': True, 'class': 'avatar'},
            'INTERRUPTOR': {'tag': 'label', 'push': 'label', 'next': 1, 'class': 'toggle-switch'},
            'DESPLEGABLE': {'tag': 'select', 'push': 'select', 'next': 0},
            'ICONO': {'tag': 'i', 'push': None, 'next': 1, 'class': 'icon'}
        }

    def parse(self, design="nebula"):
        # El while comprueba que no estemos en estado final ni fuera de límites
        while self.state != 99 and self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            t_type = token.type
            
            # Obtener transición sin IF
            row = self.MATRIX.get(self.state, {})
            transition = row.get(t_type, (99, 'E_SYNTAX'))
            
            next_state, action_id = transition
            
            # Ejecutar función sin IF
            act_func = self.DISPATCHER.get(action_id, lambda t: None)
            act_result = act_func(token)
            
            # Actualizar estado usando el resultado (si lo hubo) o el siguiente
            self.state = {True: act_result, False: next_state}.get(act_result is not None)
            
            # Decidir si avanza el puntero de pos sin IF
            advance = {'A_IMPLICIT_POP': 0, 'E_SYNTAX': 1}.get(action_id, 1)
            self.pos += advance

        return self.html.generate_full_html(design=design)

    def _action_error(self, token):
        self.error_pile.push("P001", f"Error Sintáctico: Token {token.type} no esperado", token.line, token.column)
        return 0 # Recuperación forzada a 0

    def _action_implicit_pop(self, token):
        self._action_pop(token)
        return 0

    def _action_text(self, token):
        self.html.add_text(token.value)
        return None

    def _action_save_p1(self, token):
        self.temp_param1 = token.value
        return None

    def _action_finish_p2(self, token):
        cmds = {
            'ENLACE': lambda: self.html.open_tag('a', {'href': self.temp_param1}) or self.html.add_text(token.value) or self.stack.append('a'),
            'IMAGEN': lambda: self.html.open_tag('img', {'src': self.temp_param1, 'alt': token.value}, self_closing=True),
            'VIDEO': lambda: self.html.open_tag('video', {'src': self.temp_param1, 'controls': True}) or self.html.add_text(token.value) or self.stack.append('video'),
            'ENTRADA': lambda: self.html.open_tag('input', {'placeholder': self.temp_param1, 'name': token.value, 'class': 'modern-input'}, self_closing=True),
            'AREA_TEXTO': lambda: self.html.open_tag('textarea', {'placeholder': self.temp_param1, 'name': token.value, 'class': 'modern-input'}) or self.stack.append('textarea'),
            'DATO': lambda: self.html.open_tag('div', {'class': 'key-value-pair'}) or self.html.open_tag('span', {'class': 'key'}) or self.html.add_text(self.temp_param1) or self.html.close_tag('span') or self.html.open_tag('span', {'class': 'value'}) or self.html.add_text(token.value) or self.html.close_tag('span') or self.html.close_tag('div'),
            'PROGRESO': lambda: self.html.open_tag('div', {'class': 'progress-container'}) or self.html.open_tag('div', {'class': 'progress-bar', 'style': f'width: {self.temp_param1}%'}) or self.html.close_tag('div') or self.html.close_tag('div')
        }
        res_func = cmds.get(self.temp_val, lambda: None)
        res_func()
        return None

    def _action_command(self, token):
        cmd = token.value
        self.symbol_table.insert(cmd, "COMMAND", token.line)
        
        conf = self.CMD_RULES.get(cmd, {})
        
        # Validar error de comando inexistente sin IF usando diccionarios
        error_val = {True: None, False: "C001"}.get(bool(conf))
        err_func = {
            "C001": lambda: self.error_pile.push("C001", f"Comando {cmd} no válido", token.line, token.column)
        }.get(error_val, lambda: None)
        err_func()
        
        # Manejo de cierre implícito en la pila
        implicit_close = conf.get('implicit_close')
        close_needed = implicit_close == self.stack[-1]
        close_func = {True: lambda: self._action_pop(token), False: lambda: None}.get(close_needed)
        close_func()
        
        # Validación de Pila (Require top)
        req_top = conf.get('require_top')
        is_invalid = req_top is not None and self.stack[-1] != req_top
        invalid_func = {True: lambda: self.error_pile.push("S001", f"{cmd} debe estar dentro de {req_top}", token.line, token.column), False: lambda: None}.get(is_invalid)
        invalid_func()
        
        # Apertura de etiquetas
        is_special = conf.get('special', False)
        is_self_closing = conf.get('self_closing', False)
        
        tag = conf.get('tag')
        css_class = conf.get('class')
        attributes = {'class': css_class} if css_class else None
        
        tag_func = {
            True: lambda: None, 
            False: lambda: self.html.open_tag(tag, attributes=attributes, self_closing=is_self_closing) or (self.stack.append(conf.get('push')) if conf.get('push') else None)
        }.get(is_special or tag is None)
        tag_func()
        
        self.temp_val = cmd
        return conf.get('next', 0)

    def _action_pop(self, token=None):
        can_pop = len(self.stack) > 1
        pop_func = {True: lambda: self.html.close_tag(self.stack.pop()), False: lambda: None}.get(can_pop)
        pop_func()
        return None
