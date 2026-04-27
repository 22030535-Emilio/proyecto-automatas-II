class HTMLGenerator:
    def __init__(self, title="MiniWeb Output"):
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

    def generate_full_html(self):
        header = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            f"  <title>{self.title}</title>",
            "  <style>",
            "    body { font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; }",
            "    section { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }",
            "  </style>",
            "</head>",
            "<body>"
        ]
        footer = ["</body>", "</html>"]
        
        return "\n".join(header + self.content + footer)

    def get_fragment(self):
        return "\n".join(self.content)
