document.addEventListener('DOMContentLoaded', () => {
    const compileBtn = document.getElementById('compile-btn');
    const codeEditor = document.getElementById('code-editor');
    const htmlPreview = document.getElementById('html-preview');
    const symbolTableBody = document.getElementById('symbol-table-body');
    const errorStack = document.getElementById('error-stack');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const highlighter = document.getElementById('highlighter-overlay');
    const bgColorPicker = document.getElementById('editor-bg-color');
    const downloadHtmlBtn = document.getElementById('download-html-btn');
    const downloadSrcBtn = document.getElementById('download-src-btn');
    const previewDesignSelect = document.getElementById('preview-design-select');
    let lastCompiledHtml = '';
    let selectedDesign = 'nebula';

    // --- Editor Color Theme Logic ---
    const editorSection = document.getElementById('code-editor');
    const highlighterOverlay = document.getElementById('highlighter-overlay');

    // Robust hex parsing to handle 3-digit, 6-digit hexes safely
    function getLuminance(hex) {
        let c = hex.startsWith('#') ? hex.substring(1) : hex;
        if (c.length === 3) {
            c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
        }
        if (c.length !== 6) return 0; // Fallback to dark luminance
        const r = parseInt(c.slice(0, 2), 16) / 255;
        const g = parseInt(c.slice(2, 4), 16) / 255;
        const b = parseInt(c.slice(4, 6), 16) / 255;
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    function applyEditorTheme(hex) {
        const lum = getLuminance(hex);
        const isDark = lum < 0.5; // Threshold for dark theme classification
        const caretColor = isDark ? '#a5b4fc' : '#1e1b4b';
        
        // Update variables inside document root
        document.documentElement.style.setProperty('--editor-bg', hex);
        editorSection.style.caretColor = caretColor;

        if (isDark) {
            // High-fidelity dark mode palette (Brilliant neon contrast)
            document.documentElement.style.setProperty('--hl-keyword', '#67e8f9'); // Cyan
            document.documentElement.style.setProperty('--hl-string',  '#34d399'); // Emerald
            document.documentElement.style.setProperty('--hl-comment', '#64748b'); // Slate gray
            document.documentElement.style.setProperty('--hl-symbol',  '#c084fc'); // Purple
            document.documentElement.style.setProperty('--hl-base',    '#cbd5e1'); // Off-white
            document.documentElement.style.setProperty('--editor-grid', 'rgba(255, 255, 255, 0.015)'); // Subtle light grid
        } else {
            // High-fidelity light mode palette (Rich, readable high-contrast print style)
            document.documentElement.style.setProperty('--hl-keyword', '#2563eb'); // Rich blue
            document.documentElement.style.setProperty('--hl-string',  '#166534'); // Dark green
            document.documentElement.style.setProperty('--hl-comment', '#475569'); // Dark slate gray
            document.documentElement.style.setProperty('--hl-symbol',  '#7c3aed'); // Deep violet
            document.documentElement.style.setProperty('--hl-base',    '#0f172a'); // Very dark indigo
            document.documentElement.style.setProperty('--editor-grid', 'rgba(0, 0, 0, 0.045)'); // Subtle dark grid
        }

        updateHighlighting();
        bgColorPicker.value = hex;
    }

    bgColorPicker.addEventListener('input', (e) => applyEditorTheme(e.target.value));

    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => applyEditorTheme(btn.getAttribute('data-color')));
    });

    if (previewDesignSelect) {
        previewDesignSelect.addEventListener('change', (e) => {
            selectedDesign = e.target.value;
            compileBtn.click();
        });
    }

    const keywords = [
        'TITULO', 'ENCABEZADO', 'PARRAFO', 'BOTON', 
        'LISTA', 'ELEMENTO', 'SUBLISTA', 'SECCION', 
        'ENLACE', 'IMAGEN', 'VIDEO', 'NAVEGACION', 
        'PIE', 'ARTICULO', 'NEGRILLA', 'CURSIVA', 
        'SUBRAYADO', 'CITA', 'DIVISOR',
        'CONTENEDOR', 'GRID', 'COLUMNA', 'CODIGO',
        'PEQUENO', 'SPAN', 'SALTO', 'FORMULARIO',
        'ENTRADA', 'AREA_TEXTO', 'TEXTO',
        'CONSULTA', 'FILTRO', 'DATO', 'TABLA', 'FILA', 'CELDA',
        'HERO', 'MODAL', 'PROGRESO', 'CHIP', 'AVATAR',
        'INTERRUPTOR', 'DESPLEGABLE', 'ICONO'
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
            tabContents.forEach(c => {
                c.classList.add('hidden');
                c.classList.remove('active');
            });
            
            btn.classList.add('active');
            const target = document.getElementById(`${tabId}-tab`);
            target.classList.remove('hidden');
            target.classList.add('active');
        });
    });

    // Compilation Logic
    compileBtn.addEventListener('click', async () => {
        const code = codeEditor.value;
        const originalText = compileBtn.innerHTML;
        compileBtn.innerHTML = `
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg> Compilando...`;
        compileBtn.disabled = true;

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, design: selectedDesign })
            });

            const data = await response.json();

            // 1. Update Preview
            lastCompiledHtml = data.html;
            const blob = new Blob([data.html], { type: 'text/html' });
            htmlPreview.src = URL.createObjectURL(blob);

            // 2. Update Symbol Table
            symbolTableBody.innerHTML = '';
            data.symbols.forEach(sym => {
                const row = document.createElement('tr');
                row.className = 'hover:bg-white/5 transition-colors';
                row.innerHTML = `
                    <td class="py-4 font-mono text-indigo-300"><code>${sym.name}</code></td>
                    <td class="py-4"><span class="bg-indigo-500/20 text-indigo-300 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-widest">${sym.kind}</span></td>
                    <td class="py-4 text-slate-400 font-mono text-xs">${sym.occurrences}</td>
                `;
                symbolTableBody.appendChild(row);
            });

            // 3. Update Error Stack
            errorStack.innerHTML = '';
            if (data.errors.length === 0) {
                errorStack.innerHTML = `
                    <div class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-6 rounded-2xl flex items-center gap-4 animate__animated animate__fadeInUp">
                        <div class="w-10 h-10 bg-emerald-500/20 rounded-full flex items-center justify-center shrink-0">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                        </div>
                        <div>
                            <div class="font-bold text-lg text-emerald-300">¡Código WebLang Válido!</div>
                            <div class="text-sm opacity-80 text-emerald-400/80">El autómata finito y el autómata de pila han validado el código correctamente.</div>
                        </div>
                    </div>`;
            } else {
                data.errors.forEach(err => {
                    const div = document.createElement('div');
                    div.className = 'error-item animate__animated animate__shakeX';
                    div.innerHTML = `
                        <div class="error-icon">
                            <svg class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        </div>
                        <div class="error-details">
                            <div class="error-title-row">
                                <span class="error-badge">${err.code}</span>
                                <span class="error-title">Error en compilación</span>
                            </div>
                            <div class="error-msg">${err.message}</div>
                            <div class="error-pos">Localización: Línea ${err.line}, Columna ${err.column}</div>
                        </div>
                    `;
                    errorStack.appendChild(div);
                });
                
                // Auto-switch to errors tab if there are errors
                document.querySelector('[data-tab="errors"]').click();
            }

        } catch (err) {
            console.error(err);
            errorStack.innerHTML = `
                <div class="error-item">
                    <div class="error-icon">❌</div>
                    <div class="error-details">
                        <div class="error-title">Error de Conexión</div>
                        <div class="error-msg">No se pudo contactar al motor de compilación WebLang. Asegúrate de que el servidor local está activo.</div>
                    </div>
                </div>`;
            document.querySelector('[data-tab="errors"]').click();
        } finally {
            compileBtn.innerHTML = originalText;
            compileBtn.disabled = false;
        }
    });

    // Download compiled HTML
    downloadHtmlBtn.addEventListener('click', () => {
        if (!lastCompiledHtml) { alert('Primero ejecuta el compilador.'); return; }
        const b = new Blob([lastCompiledHtml], {type:'text/html'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = 'pagina_compilada.html';
        a.click();
    });

    // Download source .weblang
    downloadSrcBtn.addEventListener('click', () => {
        const code = codeEditor.value;
        if (!code.trim()) { alert('El editor está vacío.'); return; }
        const b = new Blob([code], {type:'text/plain'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = 'codigo.weblang';
        a.click();
    });

    // Initial compilation and highlighting
    updateHighlighting();
    compileBtn.click();
});
