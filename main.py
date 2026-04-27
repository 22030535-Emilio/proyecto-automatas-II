import sys
import os
from lexer import LexerFA
from parser_stack import ParserPDA
from components import ErrorPile
from errors import MiniWebError

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.mweb>")
        return

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe.")
        return

    errors = ErrorPile()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()

        print(f"--- Iniciando traducción de: {input_file} ---")
        
        # 1. Análisis Léxico (Autómata Finito con Matriz)
        lexer = LexerFA(code, errors)
        tokens = lexer.tokenize()
        print(f"Lexer FA: {len(tokens)} tokens generados.")

        if errors.has_errors():
            print("\n[ERRORES LÉXICOS ENCONTRADOS]")
            errors.print_errors()

        # 2. Análisis Sintáctico (Autómata de Pila con Matriz)
        parser = ParserPDA(tokens, errors)
        html_output = parser.parse()
        
        print("\n--- TABLA DE SÍMBOLOS ---")
        print(parser.symbol_table)

        if errors.has_errors():
            print("\n[PILA DE ERRORES]")
            errors.print_errors()
        else:
            # 3. Guardar Resultado si no hay errores
            output_file = input_file.replace('.mweb', '.html')
            if output_file == input_file:
                output_file += '.html'
                
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_output)
                
            print(f"\nTraducción completada con éxito.")
            print(f"Resultado guardado en: {output_file}")

    except Exception as e:
        print(f"\n[ERROR INESPERADO]")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
