class HTMLGenerator:
    def __init__(self, title="WebLang Output"):
        self.title = title
        self.indent_level = 0
        self.content = []

    def _get_indent(self):
        return "  " * self.indent_level

    def open_tag(self, tag, attributes=None, self_closing=False):
        attr_str = ""
        if attributes:
            attr_str = " " + " ".join([f'{k}="{v}"' for k, v in attributes.items()])
        
        if self_closing:
            self.content.append(f"{self._get_indent()}<{tag}{attr_str}>")
        else:
            self.content.append(f"{self._get_indent()}<{tag}{attr_str}>")
            self.indent_level += 1

    def close_tag(self, tag):
        self.indent_level -= 1
        self.content.append(f"{self._get_indent()}</{tag}>")

    def add_text(self, text):
        self.content.append(f"{self._get_indent()}{text}")

    def generate_full_html(self, design="nebula"):
        css_content = self._get_design_css(design)
        
        # Base body classes depending on design
        body_class = "py-20 px-6"
        if design == "minimalist":
            body_class = "py-20 px-6 bg-slate-50"
        elif design == "sakura":
            body_class = "py-20 px-6 min-h-screen"
        elif design == "matrix":
            body_class = "py-20 px-6 min-h-screen"
            
        header = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"  <title>{self.title}</title>",
            "  <script src='https://cdn.tailwindcss.com'></script>",
            "  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'/>",
            "  <link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap' rel='stylesheet'>",
            "  <style>",
            css_content,
            "  </style>",
            "</head>",
            f"<body class='{body_class}'>",
            "  <div class='max-w-4xl mx-auto animate__animated animate__fadeIn'>",
        ]
        
        # Wrapping content with classes and animations
        wrapped_content = []
        for line in self.content:
            l = line.strip()
            if l.startswith('<h1>'):
                l = l.replace('<h1>', '<h1 class="glow-text">')
            elif l.startswith('<nav>'):
                l = l.replace('<nav>', '<nav class="animate__animated animate__fadeInDown">')
            elif l.startswith('<article>') or l.startswith('<section>'):
                tag = 'article' if l.startswith('<article>') else 'section'
                l = l.replace(f'<{tag}>', f'<{tag} class="nebula-card animate__animated animate__fadeInUp">')
            
            wrapped_content.append("    " + l)

        footer = [
            "  </div>",
            "</body>",
            "</html>"
        ]
        
        return "\n".join(header + wrapped_content + footer)

    def _get_design_css(self, design):
        if design == 'matrix':
            return """
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap');
            body { 
              font-family: 'Fira Code', monospace; 
              background: #000000 !important;
              color: #33ff33 !important;
              line-height: 1.7;
              position: relative;
            }
            body::before {
              content: " ";
              display: block;
              position: fixed;
              top: 0; left: 0; bottom: 0; right: 0;
              background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
              z-index: 99999;
              background-size: 100% 4px, 6px 100%;
              pointer-events: none;
            }
            .nebula-card {
              background: #000000 !important;
              border: 2px solid #33ff33 !important;
              border-radius: 0px !important;
              padding: 2.5rem !important;
              box-shadow: 0 0 15px rgba(51, 255, 51, 0.4) !important;
              margin-bottom: 2rem;
            }
            .grid-layout {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 2rem;
            }
            .modern-input {
              width: 100%;
              background: #000000 !important;
              border: 1px solid #33ff33 !important;
              padding: 1rem 1.5rem;
              border-radius: 0px !important;
              color: #33ff33 !important;
              font-family: 'Fira Code', monospace;
              margin-bottom: 1rem;
              transition: 0.3s;
            }
            .modern-input:focus {
              outline: none;
              border-color: #33ff33 !important;
              box-shadow: 0 0 10px rgba(51, 255, 51, 0.8) !important;
              background: rgba(51, 255, 51, 0.05) !important;
            }
            code {
              background: rgba(51, 255, 51, 0.1) !important;
              padding: 0.2rem 0.5rem;
              font-family: 'Fira Code', monospace;
              color: #33ff33 !important;
              border: 1px solid #33ff33 !important;
            }
            form {
              display: flex;
              flex-direction: column;
              gap: 1rem;
            }
            .query-container {
              background: rgba(51, 255, 51, 0.02) !important;
              border: 2px solid #33ff33 !important;
              padding: 2rem;
              margin: 2rem 0;
              border-radius: 0px !important;
            }
            .key-value-pair {
              display: flex;
              justify-content: space-between;
              padding: 0.75rem 0;
              border-bottom: 1px dashed rgba(51, 255, 51, 0.3);
            }
            .key { color: #33ff33 !important; font-weight: 500; opacity: 0.8; }
            .value { color: #33ff33 !important; font-weight: 900; text-shadow: 0 0 5px #33ff33; }
            .progress-container {
              width: 100%;
              background: #000000 !important;
              border: 2px solid #33ff33 !important;
              height: 16px;
              margin: 1rem 0;
              overflow: hidden;
              border-radius: 0px !important;
            }
            .progress-bar {
              height: 100%;
              background: #33ff33 !important;
              transition: width 0.5s ease;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin: 2rem 0;
              background: #000000 !important;
              border: 2px solid #33ff33 !important;
              border-radius: 0px !important;
            }
            th, td {
              padding: 1rem;
              text-align: left;
              border-bottom: 1px solid #33ff33 !important;
              color: #33ff33 !important;
            }
            th { background: rgba(51, 255, 51, 0.15) !important; font-weight: bold; }
            .hero-banner {
              padding: 5rem 2.5rem !important;
              text-align: center;
              background: rgba(51, 255, 51, 0.05) !important;
              border: 2px dashed #33ff33 !important;
              margin-bottom: 4rem;
              border-radius: 0px !important;
            }
            .chip {
              background: #33ff33 !important;
              color: black !important;
              padding: 0.25rem 0.75rem;
              font-size: 0.75rem;
              font-weight: 700;
              border-radius: 0px !important;
            }
            .avatar {
              width: 48px;
              height: 48px;
              border: 2px solid #33ff33 !important;
              border-radius: 0px !important;
            }
            .icon { font-size: 1.5rem; color: #33ff33 !important; }
            .glow-text {
              text-shadow: 0 0 10px #33ff33;
            }
            h1 { 
              font-size: 3.5rem; font-weight: 800; margin-bottom: 2rem; 
              color: #33ff33 !important;
              -webkit-text-fill-color: initial !important;
              background: none !important;
              letter-spacing: -0.02em;
              text-transform: uppercase;
              text-shadow: 0 0 8px #33ff33;
            }
            h2 { 
              font-size: 1.5rem; font-weight: 700; margin: 3rem 0 1.5rem; color: #33ff33 !important; 
              text-transform: uppercase; letter-spacing: 0.1em; 
            }
            p { margin-bottom: 1.5rem; font-size: 1.15rem; color: #33ff33 !important; opacity: 0.9; }
            nav { 
              background: #000000 !important; 
              padding: 2rem; margin-bottom: 4rem; 
              border: 2px solid #33ff33 !important;
              border-radius: 0px !important;
            }
            article, section { margin-bottom: 3rem; }
            footer { 
              margin-top: 6rem; padding: 3rem; text-align: center; 
              border-top: 2px solid #33ff33 !important; color: #33ff33 !important; opacity: 0.7;
            }
            button { 
              background: #000000 !important; color: #33ff33 !important; padding: 1rem 2.5rem; 
              font-weight: 700; transition: all 0.3s; 
              border: 2px solid #33ff33 !important;
              border-radius: 0px !important;
              font-family: 'Fira Code', monospace;
              cursor: pointer;
            }
            button:hover { background: #33ff33 !important; color: #000000 !important; box-shadow: 0 0 15px #33ff33; }
            blockquote { 
              background: rgba(51, 255, 51, 0.05) !important; padding: 2rem; 
              border-left: 4px solid #33ff33 !important; font-style: italic; font-size: 1.25rem; 
              color: #33ff33 !important; margin: 2.5rem 0; 
              border-radius: 0px !important;
            }
            img, video { border: 2px solid #33ff33 !important; margin: 2rem 0; border-radius: 0px !important; }
            a { color: #33ff33 !important; font-weight: 600; text-decoration: underline; transition: 0.2s; }
            a:hover { opacity: 0.8; }
            """
        elif design == 'minimalist':
            return """
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            body { 
              font-family: 'Inter', sans-serif; 
              background: #f8fafc !important;
              color: #0f172a !important;
              line-height: 1.6;
            }
            .nebula-card {
              background: #ffffff !important;
              border: 1px solid #e2e8f0 !important;
              border-radius: 0.5rem !important;
              padding: 2.5rem !important;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
              margin-bottom: 2rem;
            }
            .grid-layout {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 1.5rem;
            }
            .modern-input {
              width: 100%;
              background: #ffffff !important;
              border: 1px solid #cbd5e1 !important;
              padding: 0.75rem 1.25rem;
              border-radius: 0.375rem !important;
              color: #0f172a !important;
              margin-bottom: 1rem;
              transition: 0.2s;
            }
            .modern-input:focus {
              outline: none;
              border-color: #0f172a !important;
              background: #ffffff !important;
            }
            code {
              background: #f1f5f9 !important;
              padding: 0.2rem 0.4rem;
              border-radius: 0.25rem !important;
              font-family: monospace;
              color: #0f172a !important;
              border: 1px solid #e2e8f0 !important;
            }
            form {
              display: flex;
              flex-direction: column;
              gap: 1rem;
            }
            .query-container {
              background: #f8fafc !important;
              border-left: 2px solid #0f172a !important;
              padding: 1.5rem;
              margin: 2rem 0;
              border-radius: 0 0.5rem 0.5rem 0 !important;
              border-right: none !important;
            }
            .key-value-pair {
              display: flex;
              justify-content: space-between;
              padding: 0.5rem 0;
              border-bottom: 1px solid #e2e8f0;
            }
            .key { color: #64748b !important; font-weight: 500; }
            .value { color: #0f172a !important; font-weight: 700; }
            .progress-container {
              width: 100%;
              background: #e2e8f0 !important;
              height: 6px;
              border-radius: 9999px !important;
              margin: 1rem 0;
              overflow: hidden;
            }
            .progress-bar {
              height: 100%;
              background: #0f172a !important;
              transition: width 0.5s ease;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin: 2rem 0;
              background: #ffffff !important;
              border: 1px solid #e2e8f0 !important;
              border-radius: 0.375rem !important;
              overflow: hidden;
            }
            th, td {
              padding: 0.75rem 1rem;
              text-align: left;
              border-bottom: 1px solid #e2e8f0 !important;
              color: #0f172a !important;
            }
            th { background: #f1f5f9 !important; color: #0f172a !important; font-weight: 600; }
            .hero-banner {
              padding: 4rem 2rem !important;
              text-align: center;
              background: #ffffff !important;
              border: 1px solid #e2e8f0 !important;
              border-radius: 0.5rem !important;
              margin-bottom: 3rem;
            }
            .chip {
              background: #f1f5f9 !important;
              color: #0f172a !important;
              border: 1px solid #e2e8f0 !important;
              padding: 0.2rem 0.5rem;
              border-radius: 0.25rem !important;
              font-size: 0.75rem;
              font-weight: 500;
            }
            .avatar {
              width: 40px;
              height: 40px;
              border-radius: 50% !important;
              border: 1px solid #cbd5e1 !important;
            }
            .icon { font-size: 1.25rem; color: #475569 !important; }
            .glow-text {
              text-shadow: none !important;
            }
            h1 { 
              font-size: 2.75rem; font-weight: 800; margin-bottom: 1.5rem; 
              color: #0f172a !important;
              -webkit-text-fill-color: initial !important;
              background: none !important;
              letter-spacing: -0.03em;
            }
            h2 { 
              font-size: 1.25rem; font-weight: 700; margin: 2rem 0 1rem; color: #0f172a !important; 
              text-transform: uppercase; letter-spacing: 0.05em; 
            }
            p { margin-bottom: 1.25rem; font-size: 1rem; color: #475569 !important; }
            nav { 
              background: #ffffff !important; 
              border-radius: 0.5rem !important; padding: 1.25rem 2rem; margin-bottom: 3rem; 
              border: 1px solid #e2e8f0 !important;
            }
            article, section { margin-bottom: 2.5rem; }
            footer { 
              margin-top: 4rem; padding: 2.5rem; text-align: center; 
              border-top: 1px solid #e2e8f0 !important; color: #94a3b8 !important; font-size: 0.875rem;
            }
            button { 
              background: #0f172a !important; color: white !important; padding: 0.75rem 1.75rem; 
              border-radius: 0.375rem !important; font-weight: 500; transition: all 0.2s; 
              border: none;
              cursor: pointer;
              box-shadow: none !important;
            }
            button:hover { background: #1e293b !important; transform: none !important; }
            blockquote { 
              background: #f8fafc !important; border-radius: 0.375rem !important; padding: 1.5rem; 
              border-left: 2px solid #0f172a !important; font-style: italic; font-size: 1.1rem; 
              color: #475569 !important; margin: 2rem 0; 
            }
            img, video { border-radius: 0.375rem !important; border: 1px solid #e2e8f0 !important; margin: 1.5rem 0; }
            a { color: #0f172a !important; font-weight: 600; text-decoration: underline; transition: 0.2s; }
            a:hover { opacity: 0.8; }
            """
        elif design == 'sakura':
            return """
            @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700;900&display=swap');
            body { 
              font-family: 'Quicksand', sans-serif; 
              background: #fff1f2 !important;
              background-image: 
                radial-gradient(at 0% 0%, #ffe4e6 0px, transparent 50%),
                radial-gradient(at 100% 100%, #fecdd3 0px, transparent 50%) !important;
              background-attachment: fixed;
              color: #4c0519 !important;
              line-height: 1.7;
            }
            .nebula-card {
              background: rgba(255, 255, 255, 0.85) !important;
              backdrop-filter: blur(12px);
              border: 1.5px solid rgba(254, 205, 211, 0.6) !important;
              border-radius: 2.25rem !important;
              padding: 2.5rem !important;
              box-shadow: 0 15px 30px rgba(253, 164, 175, 0.15) !important;
              margin-bottom: 2rem;
            }
            .grid-layout {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 2rem;
            }
            .modern-input {
              width: 100%;
              background: #ffffff !important;
              border: 2.5px solid #fbcfe8 !important;
              padding: 0.85rem 1.35rem;
              border-radius: 1.5rem !important;
              color: #4c0519 !important;
              margin-bottom: 1rem;
              transition: 0.3s;
            }
            .modern-input:focus {
              outline: none;
              border-color: #f43f5e !important;
              background: rgba(244, 63, 94, 0.02) !important;
            }
            code {
              background: #ffe4e6 !important;
              padding: 0.2rem 0.5rem;
              border-radius: 0.75rem !important;
              font-family: monospace;
              color: #be123c !important;
            }
            form {
              display: flex;
              flex-direction: column;
              gap: 1rem;
            }
            .query-container {
              background: rgba(255, 241, 242, 0.6) !important;
              border-left: 5px solid #f43f5e !important;
              padding: 1.75rem;
              margin: 2rem 0;
              border-radius: 0 1.5rem 1.5rem 0 !important;
              border-right: none !important;
            }
            .key-value-pair {
              display: flex;
              justify-content: space-between;
              padding: 0.75rem 0;
              border-bottom: 1px solid #ffe4e6;
            }
            .key { color: #9f1239 !important; font-weight: 500; }
            .value { color: #f43f5e !important; font-weight: 900; }
            .progress-container {
              width: 100%;
              background: #ffe4e6 !important;
              height: 12px;
              border-radius: 6px !important;
              margin: 1rem 0;
              overflow: hidden;
            }
            .progress-bar {
              height: 100%;
              background: linear-gradient(90deg, #f43f5e, #ec4899) !important;
              transition: width 0.5s ease;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin: 2rem 0;
              background: rgba(255, 255, 255, 0.7) !important;
              border-radius: 1.5rem !important;
              overflow: hidden;
              border: 1px solid #fecdd3 !important;
            }
            th, td {
              padding: 1rem;
              text-align: left;
              border-bottom: 1px solid #fecdd3 !important;
              color: #4c0519 !important;
            }
            th { background: #ffe4e6 !important; color: #9f1239 !important; font-weight: bold; }
            .hero-banner {
              padding: 5rem 2.5rem !important;
              text-align: center;
              background: radial-gradient(circle, rgba(255, 228, 230, 0.8) 0%, transparent 70%) !important;
              border-radius: 3rem !important;
              margin-bottom: 4rem;
              border: 2px dashed #fbcfe8 !important;
            }
            .chip {
              background: #f43f5e !important;
              color: white !important;
              padding: 0.25rem 0.75rem;
              border-radius: 9999px !important;
              font-size: 0.75rem;
              font-weight: 700;
            }
            .avatar {
              width: 48px;
              height: 48px;
              border-radius: 50% !important;
              border: 2.5px solid #f43f5e !important;
            }
            .icon { font-size: 1.5rem; color: #f43f5e !important; }
            .glow-text {
              text-shadow: none !important;
            }
            h1 { 
              font-size: 3.5rem; font-weight: 900; margin-bottom: 2rem; 
              background: linear-gradient(135deg, #f43f5e, #db2777) !important;
              -webkit-background-clip: text !important;
              -webkit-text-fill-color: transparent !important;
              letter-spacing: -0.02em;
            }
            h2 { 
              font-size: 1.4rem; font-weight: 800; margin: 3rem 0 1.5rem; color: #be123c !important; 
              letter-spacing: 0.05em; 
            }
            p { margin-bottom: 1.5rem; font-size: 1.1rem; color: #9f1239 !important; }
            nav { 
              background: rgba(255, 255, 255, 0.7) !important; 
              border-radius: 1.75rem !important; padding: 1.5rem 2rem; margin-bottom: 4rem; 
              border: 1.5px solid rgba(254, 205, 211, 0.8) !important;
            }
            article, section { margin-bottom: 3rem; }
            footer { 
              margin-top: 6rem; padding: 3rem; text-align: center; 
              border-top: 1px solid #fecdd3 !important; color: #fda4af !important;
            }
            button { 
              background: #f43f5e !important; color: white !important; padding: 0.9rem 2.25rem; 
              border-radius: 1.75rem !important; font-weight: 700; transition: all 0.3s; 
              border: none;
              box-shadow: 0 8px 20px rgba(244, 63, 94, 0.25) !important;
              cursor: pointer;
            }
            button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 25px rgba(244, 63, 94, 0.4) !important; background: #e11d48 !important; }
            blockquote { 
              background: rgba(255, 255, 255, 0.6) !important; border-radius: 1.5rem !important; padding: 2rem; 
              border-left: 5px solid #f43f5e !important; font-style: italic; font-size: 1.2rem; 
              color: #9f1239 !important; margin: 2.5rem 0; 
            }
            img, video { border-radius: 1.75rem !important; border: 1.5px solid #fecdd3 !important; margin: 2rem 0; }
            a { color: #db2777; font-weight: 700; text-decoration: none; border-bottom: 2px solid transparent; transition: 0.2s; }
            a:hover { border-bottom-color: #db2777; }
            """
        elif design == 'cyberpunk':
            return """
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
            body { 
              font-family: 'Fira Code', monospace; 
              background: #0b0c16 !important;
              background-image: 
                radial-gradient(at 0% 0%, rgba(255, 0, 127, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(0, 255, 255, 0.08) 0px, transparent 50%) !important;
              background-attachment: fixed;
              color: #00ffff !important;
              line-height: 1.7;
            }
            .nebula-card {
              background: #111223 !important;
              border: 2px solid #ff007f !important;
              border-radius: 4px !important;
              padding: 2.5rem !important;
              box-shadow: 4px 4px 0px #00ffff, 0px 0px 20px rgba(255, 0, 127, 0.35) !important;
              margin-bottom: 2.5rem;
            }
            .grid-layout {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 2rem;
            }
            .modern-input {
              width: 100%;
              background: #0b0c16 !important;
              border: 2px solid #00ffff !important;
              padding: 1rem 1.5rem;
              border-radius: 0px !important;
              color: #ff007f !important;
              margin-bottom: 1rem;
              transition: 0.3s;
              font-family: 'Fira Code', monospace;
            }
            .modern-input:focus {
              outline: none;
              border-color: #ff007f !important;
              box-shadow: 0 0 10px #ff007f !important;
            }
            code {
              background: rgba(255, 0, 127, 0.1) !important;
              padding: 0.2rem 0.5rem;
              color: #ff007f !important;
              border: 1px solid #ff007f !important;
              border-radius: 0px !important;
            }
            form {
              display: flex;
              flex-direction: column;
              gap: 1rem;
            }
            .query-container {
              background: rgba(0, 255, 255, 0.03) !important;
              border-left: 4px solid #00ffff !important;
              border-right: 4px solid #ff007f !important;
              padding: 2rem;
              margin: 2rem 0;
              border-radius: 0px !important;
            }
            .key-value-pair {
              display: flex;
              justify-content: space-between;
              padding: 0.75rem 0;
              border-bottom: 1px solid rgba(255, 0, 127, 0.2);
            }
            .key { color: #00ffff !important; font-weight: bold; }
            .value { color: #ff007f !important; font-weight: 700; text-shadow: 0 0 5px #ff007f; }
            .progress-container {
              width: 100%;
              background: #111223 !important;
              height: 12px;
              border: 1px solid #ff007f !important;
              margin: 1rem 0;
              overflow: hidden;
              border-radius: 0px !important;
            }
            .progress-bar {
              height: 100%;
              background: linear-gradient(90deg, #ff007f, #00ffff) !important;
              transition: width 0.5s ease;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin: 2rem 0;
              background: #111223 !important;
              border: 2px solid #00ffff !important;
              border-radius: 0px !important;
            }
            th, td {
              padding: 1rem;
              text-align: left;
              border-bottom: 1px solid #ff007f !important;
            }
            th { background: #ff007f !important; color: #0b0c16 !important; font-weight: bold; }
            td { color: #00ffff !important; }
            .hero-banner {
              padding: 5rem 2.5rem !important;
              text-align: center;
              background: #111223 !important;
              border: 3px double #00ffff !important;
              margin-bottom: 4rem;
              box-shadow: 0 0 20px rgba(0, 255, 255, 0.2) !important;
              border-radius: 0px !important;
            }
            .chip {
              background: #00ffff !important;
              color: #0b0c16 !important;
              padding: 0.25rem 0.75rem;
              font-size: 0.75rem;
              font-weight: 700;
              text-transform: uppercase;
              border-radius: 0px !important;
            }
            .avatar {
              width: 48px;
              height: 48px;
              border: 2px solid #ff007f !important;
              box-shadow: 0 0 10px #ff007f !important;
              border-radius: 0px !important;
            }
            .icon { font-size: 1.5rem; color: #ff007f !important; }
            .glow-text {
              text-shadow: 0 0 8px #00ffff !important;
            }
            h1 { 
              font-size: 3.5rem; font-weight: bold; margin-bottom: 2rem; 
              color: #00ffff !important;
              text-shadow: 0 0 8px #00ffff, 0 0 15px #ff007f !important;
              text-transform: uppercase;
              letter-spacing: -0.02em;
              -webkit-text-fill-color: initial !important;
              background: none !important;
            }
            h2 { 
              font-size: 1.5rem; font-weight: bold; margin: 3rem 0 1.5rem; color: #ff007f !important; 
              text-transform: uppercase; text-shadow: 0 0 5px #ff007f;
            }
            p { margin-bottom: 1.5rem; font-size: 1.1rem; color: #00ffff !important; opacity: 0.9; }
            nav { 
              background: #111223 !important; 
              padding: 2rem; margin-bottom: 4rem; 
              border: 2px solid #00ffff !important;
              box-shadow: 0 0 15px rgba(0, 255, 255, 0.2) !important;
              border-radius: 0px !important;
            }
            article, section { margin-bottom: 3rem; }
            footer { 
              margin-top: 6rem; padding: 3rem; text-align: center; 
              border-top: 2px solid #ff007f !important; color: rgba(0, 255, 255, 0.5) !important;
            }
            button { 
              background: #ff007f !important; color: #0b0c16 !important; padding: 1rem 2.5rem; 
              font-weight: bold; transition: all 0.3s; 
              border: none;
              font-family: 'Fira Code', monospace;
              text-transform: uppercase;
              cursor: pointer;
              box-shadow: 4px 4px 0px #00ffff !important;
              border-radius: 0px !important;
            }
            button:hover { background: #00ffff !important; color: #0b0c16 !important; box-shadow: 4px 4px 0px #ff007f !important; transform: none !important; }
            blockquote { 
              background: rgba(255, 0, 127, 0.05) !important; padding: 2rem; 
              border-left: 4px solid #ff007f !important; font-style: italic; font-size: 1.25rem; 
              color: #00ffff !important; margin: 2.5rem 0; 
              border-radius: 0px !important;
            }
            img, video { border: 2px solid #00ffff !important; margin: 2rem 0; border-radius: 0px !important; }
            a { color: #ff007f !important; font-weight: bold; text-decoration: none; border-bottom: 2px solid #ff007f; transition: 0.2s; }
            a:hover { color: #00ffff !important; border-bottom-color: #00ffff; }
            """
        else: # Default theme: nebula
            return """
            body { 
              font-family: 'Plus Jakarta Sans', sans-serif; 
              background: #020617 !important;
              background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.05) 0px, transparent 50%) !important;
              background-attachment: fixed;
              color: #f1f5f9 !important;
              line-height: 1.7;
            }
            .nebula-card {
              background: rgba(15, 23, 42, 0.4) !important;
              backdrop-filter: blur(16px);
              border: 1px solid rgba(255, 255, 255, 0.05) !important;
              border-radius: 2rem !important;
              padding: 3rem !important;
              box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
            }
            .grid-layout {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
              gap: 2rem;
            }
            .modern-input {
              width: 100%;
              background: rgba(255,255,255,0.05) !important;
              border: 1px solid rgba(255,255,255,0.1) !important;
              padding: 1rem 1.5rem;
              border-radius: 1rem !important;
              color: white !important;
              margin-bottom: 1rem;
              transition: 0.3s;
            }
            .modern-input:focus {
              outline: none;
              border-color: #6366f1 !important;
              background: rgba(99, 102, 241, 0.1) !important;
            }
            code {
              background: rgba(99, 102, 241, 0.1) !important;
              padding: 0.2rem 0.5rem;
              border-radius: 0.5rem !important;
              font-family: 'Fira Code', monospace;
              color: #818cf8 !important;
            }
            form {
              display: flex;
              flex-direction: column;
              gap: 1rem;
            }
            .query-container {
              background: rgba(99, 102, 241, 0.03) !important;
              border-left: 4px solid #6366f1 !important;
              padding: 2rem;
              margin: 2rem 0;
              border-radius: 0 1.5rem 1.5rem 0 !important;
              border-right: none !important;
            }
            .key-value-pair {
              display: flex;
              justify-content: space-between;
              padding: 0.75rem 0;
              border-bottom: 1px solid rgba(255,255,255,0.05);
            }
            .key { color: #94a3b8 !important; font-weight: 500; }
            .value { color: #60a5fa !important; font-weight: 700; }
            .progress-container {
              width: 100%;
              background: rgba(255,255,255,0.05) !important;
              height: 8px;
              border-radius: 4px !important;
              margin: 1rem 0;
              overflow: hidden;
            }
            .progress-bar {
              height: 100%;
              background: linear-gradient(90deg, #6366f1, #c084fc) !important;
              transition: width 0.5s ease;
            }
            table {
              width: 100%;
              border-collapse: collapse;
              margin: 2rem 0;
              background: rgba(255,255,255,0.02) !important;
              border-radius: 1rem !important;
              overflow: hidden;
            }
            th, td {
              padding: 1rem;
              text-align: left;
              border-bottom: 1px solid rgba(255,255,255,0.05) !important;
            }
            th { background: rgba(99, 102, 241, 0.1) !important; color: #818cf8 !important; }
            .hero-banner {
              padding: 6rem 3rem !important;
              text-align: center;
              background: radial-gradient(circle at center, rgba(99, 102, 241, 0.15) 0%, transparent 70%) !important;
              border-radius: 3rem !important;
              margin-bottom: 4rem;
            }
            .chip {
              background: #6366f1 !important;
              color: white !important;
              padding: 0.25rem 0.75rem;
              border-radius: 9999px !important;
              font-size: 0.75rem;
              font-weight: 700;
              text-transform: uppercase;
            }
            .avatar {
              width: 48px;
              height: 48px;
              border-radius: 50% !important;
              border: 2px solid #6366f1 !important;
            }
            .icon { font-size: 1.5rem; color: #6366f1 !important; }
            .glow-text {
              text-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
            }
            h1 { 
              font-size: 4rem; font-weight: 800; margin-bottom: 2rem; 
              background: linear-gradient(135deg, #60a5fa, #c084fc) !important;
              -webkit-background-clip: text !important;
              -webkit-text-fill-color: transparent !important;
              letter-spacing: -0.04em;
            }
            h2 { 
              font-size: 1.5rem; font-weight: 700; margin: 3rem 0 1.5rem; color: #818cf8 !important; 
              text-transform: uppercase; letter-spacing: 0.1em; 
            }
            p { margin-bottom: 1.5rem; font-size: 1.15rem; color: #94a3b8 !important; }
            nav { 
              background: rgba(99, 102, 241, 0.1) !important; 
              border-radius: 1.5rem !important; padding: 2rem; margin-bottom: 4rem; 
              border: 1px solid rgba(99, 102, 241, 0.2) !important;
            }
            article, section { margin-bottom: 3rem; }
            footer { 
              margin-top: 6rem; padding: 3rem; text-align: center; 
              border-top: 1px solid rgba(255,255,255,0.05) !important; color: #475569 !important;
            }
            button { 
              background: #4f46e5 !important; color: white !important; padding: 1rem 2.5rem; 
              border-radius: 1rem !important; font-weight: 700; transition: all 0.3s; 
              box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4) !important;
              cursor: pointer;
            }
            button:hover { transform: translateY(-3px) !important; box-shadow: 0 15px 35px rgba(79, 70, 229, 0.6) !important; }
            blockquote { 
              background: rgba(255, 255, 255, 0.03) !important; border-radius: 1.5rem !important; padding: 2rem; 
              border-left: 4px solid #c084fc !important; font-style: italic; font-size: 1.25rem; 
              color: #cbd5e1 !important; margin: 2.5rem 0; 
            }
            img, video { border-radius: 1.5rem !important; border: 1px solid rgba(255,255,255,0.1) !important; margin: 2rem 0; }
            a { color: #38bdf8; font-weight: 600; text-decoration: none; border-bottom: 1px solid transparent; transition: 0.2s; }
            a:hover { border-bottom-color: #38bdf8; }
            """

    def get_fragment(self):
        return "\n".join(self.content)
