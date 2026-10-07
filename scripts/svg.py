from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG = "#080a0d"
WHITE = "#f0f2f5"
GRAY = "#9ba4b0"
BLUE = "#7195c8"
FONT = 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace'

def text(x, y, value, size=14, color=WHITE, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'

def reveal(content, delay=0):
    return f'<g class="reveal" style="animation-delay:{delay}s">{content}</g>'

def save(name, width, height, title, content):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>text{{font-family:{FONT}}}.reveal{{animation:appear .45s both}}@keyframes appear{{from{{opacity:0}}to{{opacity:1}}}}@media(prefers-reduced-motion:reduce){{.reveal{{animation:none}}}}</style>
<rect width="{width}" height="{height}" fill="{BG}"/>{content}</svg>'''
    (ROOT / "assets" / name).write_text(svg)

def command(value):
    return text(28, 39, "chiyo@github", 13, GRAY) + text(132, 39, "~ $ " + value, 13)
