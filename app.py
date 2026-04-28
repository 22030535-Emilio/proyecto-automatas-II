from flask import Flask, render_template, request, jsonify
from lexer import LexerFA
from parser_stack import ParserPDA
from components import ErrorPile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')
    
    errors = ErrorPile()
    
    try:
        # 1. Lexer FA (Matrix driven)
        lexer = LexerFA(code, errors)
        tokens = lexer.tokenize()
        
        # 2. Parser PDA (Matrix driven)
        parser = ParserPDA(tokens, errors)
        html_output = parser.parse()
        
        # Format Symbol Table for JSON
        symbol_table = []
        for name, info in parser.symbol_table.symbols.items():
            symbol_table.append({
                "name": name,
                "kind": info["kind"],
                "occurrences": ", ".join(map(str, info["occurrences"]))
            })
            
        # Format Errors for JSON
        error_list = []
        for err in errors.errors:
            error_list.append({
                "code": err.code,
                "message": err.message,
                "line": err.line,
                "column": err.column
            })
            
        return jsonify({
            "html": html_output,
            "symbols": symbol_table,
            "errors": error_list,
            "tokens_count": len(tokens)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
