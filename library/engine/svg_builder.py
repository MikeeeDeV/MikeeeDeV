"""
library/engine/svg_builder.py - Accessible, Responsive SVG Document Builder.
Injects CSS custom properties, dark/light theme overrides, accessibility tags,
and crisp SVG filters.
"""

import html
from typing import List, Optional
from library.engine.color_palettes import Palette, get_palette

class SVGBuilder:
    def __init__(self, width: int, height: int, palette_or_id="kemet_nocturne", title: str = "", desc: str = ""):
        self.width = width
        self.height = height
        if isinstance(palette_or_id, str):
            self.palette: Palette = get_palette(palette_or_id)
        else:
            self.palette = palette_or_id
        raw_title = title or f"VectorForge Shape - {self.palette.name}"
        raw_desc = desc or "Autonomous deterministic developer SVG shape component"
        self.title = html.escape(raw_title)
        self.desc = html.escape(raw_desc)
        self.defs: List[str] = []
        self.body: List[str] = []
        self.custom_css: List[str] = []

    def add_def(self, def_content: str):
        self.defs.append(def_content)

    def add_custom_css(self, css: str):
        self.custom_css.append(css)

    def add_body(self, snippet: str):
        self.body.append(snippet)

    def build(self) -> str:
        p = self.palette
        defs_block = "\n".join(self.defs)
        if defs_block:
            defs_block = f"<defs>\n{defs_block}\n</defs>"
            
        custom_css_block = "\n".join(self.custom_css)
        
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" role="img" aria-labelledby="title-id desc-id">
  <title id="title-id">{self.title}</title>
  <desc id="desc-id">{self.desc}</desc>
  <style>
    :root {{
      --vf-bg: {p.dark_bg};
      --vf-card: {p.dark_card};
      --vf-border: {p.dark_border};
      --vf-text: {p.dark_text_primary};
      --vf-text-muted: {p.dark_text_secondary};
      --vf-accent-1: {p.dark_accent_primary};
      --vf-accent-2: {p.dark_accent_secondary};
      --vf-accent-3: {p.dark_accent_tertiary};
      --vf-glow: {p.dark_glow};
      --vf-font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --vf-font-mono: "JetBrains Mono", "Fira Code", ui-monospace, Menlo, Monaco, Consolas, monospace;
      --vf-font-arabic: "Cairo", "Amiri", "Tahoma", -apple-system, sans-serif;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --vf-bg: {p.light_bg};
        --vf-card: {p.light_card};
        --vf-border: {p.light_border};
        --vf-text: {p.light_text_primary};
        --vf-text-muted: {p.light_text_secondary};
        --vf-accent-1: {p.light_accent_primary};
        --vf-accent-2: {p.light_accent_secondary};
        --vf-accent-3: {p.light_accent_tertiary};
        --vf-glow: {p.light_glow};
      }}
    }}
    text {{
      user-select: none;
    }}
    {custom_css_block}
  </style>
  {defs_block}
  {chr(10).join(self.body)}
</svg>"""
        return svg.strip()
