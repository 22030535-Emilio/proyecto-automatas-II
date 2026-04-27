import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import LexerFA
from parser_stack import ParserPDA
from components import ErrorPile

def test_lexer():
    print("Probando Lexer (FA)...")
    code = 'TITULO "Hola"; LISTA ELEMENTO "A";'
    errors = ErrorPile()
    lexer = LexerFA(code, errors)
    tokens = lexer.tokenize()
    assert len(tokens) >= 6
    assert not errors.has_errors()
    print("Lexer FA: OK")

def test_parser_basic():
    print("Probando Parser (PDA Matriz)...")
    code = 'TITULO "Prueba"; PARRAFO "Texto";'
    errors = ErrorPile()
    lexer = LexerFA(code, errors)
    tokens = lexer.tokenize()
    parser = ParserPDA(tokens, errors)
    html = parser.parse()
    assert "<h1>" in html
    assert "<p>" in html
    print("Parser PDA Matriz: OK")

def test_parser_nesting():
    print("Probando Parser (Anidamiento)...")
    code = 'LISTA ELEMENTO "Uno"; ELEMENTO "Dos"; ;'
    errors = ErrorPile()
    lexer = LexerFA(code, errors)
    tokens = lexer.tokenize()
    parser = ParserPDA(tokens, errors)
    html = parser.parse()
    assert "<ul>" in html
    assert "<li>" in html
    assert html.count("<li>") == 2
    print("Parser Anidamiento: OK")

if __name__ == "__main__":
    try:
        test_lexer()
        test_parser_basic()
        test_parser_nesting()
        print("\n--- Todas las pruebas pasaron satisfactoriamente ---")
    except AssertionError as e:
        print(f"\n[FALLO EN PRUEBA]: {e}")
    except Exception as e:
        print(f"\n[ERROR]: {e}")
