# Definición de Tokens para MiniWebLang
TOKENS = {
    'COMANDO': r'[A-Z]+',
    'CADENA': r'"[^"]*"',
    'NUMERO': r'\d+',
    'PUNTOCOMA': r';',
    'LLAVE_A': r'\{',
    'LLAVE_C': r'\}',
    'COMENTARIO': r'//.*',
    'ESPACIO': r'\s+',
}

# Comandos y su mapeo a HTML (Básico)
COMMAND_MAP = {
    'TITULO': 'h1',
    'ENCABEZADO': 'h2',
    'PARRAFO': 'p',
    'BOTON': 'button',
    'LISTA': 'ul',
    'ELEMENTO': 'li',
    'SUBLISTA': 'ul',
    'SECCION': 'section',
    'NAVEGACION': 'nav',
    'PIE': 'footer',
    'ARTICULO': 'article',
    'NEGRILLA': 'strong',
    'CURSIVA': 'em',
    'SUBRAYADO': 'u',
    'CITA': 'blockquote',
    'DIVISOR': 'hr'
}

# Comandos que pueden contener otros comandos (Anidables)
NESTABLE_COMMANDS = ['LISTA', 'ELEMENTO', 'SUBLISTA', 'SECCION']

# Símbolos de la Pila para el Autómata (Gamma)
STACK_SYMBOLS = {
    'LISTA': 'ul',
    'ELEMENTO': 'li',
    'SUBLISTA': 'ul',
    'SECCION': 'section',
    'BOTTOM': '#'
}
