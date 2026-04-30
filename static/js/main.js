document.addEventListener('DOMContentLoaded', () => {
    const compileBtn = document.getElementById('compile-btn');
    const codeEditor = document.getElementById('code-editor');
    const htmlPreview = document.getElementById('html-preview');
    const symbolTableBody = document.querySelector('#symbol-table tbody');
    const errorStack = document.getElementById('error-stack');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const highlighter = document.getElementById('highlighter-overlay');

    const keywords = [
        'TITULO', 'ENCABEZADO', 'PARRAFO', 'BOTON', 
        'LISTA', 'ELEMENTO', 'SUBLISTA', 'SECCION', 
        'ENLACE', 'IMAGEN'
    ];

    function updateHighlighting() {
        let content = codeEditor.value;

        // Escape HTML
        content = content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

        // Highlight strings
        content = content.replace(/"[^"]*"/g, '<span class="hl-string">$&</span>');

        // Highlight comments
        content = content.replace(/\/\/.*$/gm, '<span class="hl-comment">$&</span>');

        // Highlight keywords (only if they are whole words)
        keywords.forEach(kw => {
            const regex = new RegExp(`\\b${kw}\\b`, 'g');
            content = content.replace(regex, `<span class="hl-keyword">${kw}</span>`);
        });

        // Highlight symbols
        content = content.replace(/[;{}]/g, '<span class="hl-symbol">$&</span>');

        highlighter.innerHTML = content + (content.endsWith('\n') ? ' ' : '');
    }

    codeEditor.addEventListener('input', updateHighlighting);
    codeEditor.addEventListener('scroll', () => {
        highlighter.scrollTop = codeEditor.scrollTop;
    });

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // Compilation Logic
    compileBtn.addEventListener('click', async () => {
        const code = codeEditor.value;
        compileBtn.textContent = 'Compilando...';
        compileBtn.disabled = true;

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });

            const data = await response.json();

            // 1. Update Preview
            const blob = new Blob([data.html], { type: 'text/html' });
            htmlPreview.src = URL.createObjectURL(blob);

            // 2. Update Symbol Table
            symbolTableBody.innerHTML = '';
            data.symbols.forEach(sym => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><code>${sym.name}</code></td>
                    <td><span class="badge">${sym.kind}</span></td>
                    <td>${sym.occurrences}</td>
                `;
                symbolTableBody.appendChild(row);
            });

            // 3. Update Error Stack
            errorStack.innerHTML = '';
            if (data.errors.length === 0) {
                errorStack.innerHTML = '<div class="success-msg">✓ No se encontraron errores.</div>';
            } else {
                data.errors.forEach(err => {
                    const div = document.createElement('div');
                    div.className = 'error-item';
                    div.innerHTML = `
                        <div><span class="code">${err.code}</span> ${err.message}</div>
                        <div class="pos">Línea: ${err.line}, Columna: ${err.column}</div>
                    `;
                    errorStack.appendChild(div);
                });
                
                // Auto-switch to errors tab if there are errors
                document.querySelector('[data-tab="errors"]').click();
            }

        } catch (err) {
            console.error(err);
            alert('Error en la conexión con el servidor.');
        } finally {
            compileBtn.textContent = 'Compilar y Ejecutar';
            compileBtn.disabled = false;
        }
    });

    // Initial compilation and highlighting
    updateHighlighting();
    compileBtn.click();
});
