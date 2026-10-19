"""
library/engine/color_palettes.py - 10 Curated, High-Contrast Color Palettes
for VectorForge Developer Shapes.
All palettes provide dark mode (default) and light mode overrides.
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class Palette:
    id: str
    name: str
    dark_bg: str
    dark_card: str
    dark_border: str
    dark_text_primary: str
    dark_text_secondary: str
    dark_accent_primary: str
    dark_accent_secondary: str
    dark_accent_tertiary: str
    dark_glow: str
    
    light_bg: str
    light_card: str
    light_border: str
    light_text_primary: str
    light_text_secondary: str
    light_accent_primary: str
    light_accent_secondary: str
    light_accent_tertiary: str
    light_glow: str

PALETTES: Dict[str, Palette] = {
    "kemet_nocturne": Palette(
        id="kemet_nocturne",
        name="Kemet Nocturne (Egyptian Deep Gold & Lapis)",
        dark_bg="#0A0E17",
        dark_card="#111827",
        dark_border="#1F293D",
        dark_text_primary="#F8FAFC",
        dark_text_secondary="#94A3B8",
        dark_accent_primary="#F5C451",   # Gold
        dark_accent_secondary="#38BDF8", # Nile Lapis
        dark_accent_tertiary="#14B8A6",  # Teal
        dark_glow="#F5C45144",
        light_bg="#F8FAFC",
        light_card="#FFFFFF",
        light_border="#CBD5E1",
        light_text_primary="#0F172A",
        light_text_secondary="#475569",
        light_accent_primary="#D97706",
        light_accent_secondary="#0284C7",
        light_accent_tertiary="#0D9488",
        light_glow="#D9770633",
    ),
    "cyberpunk_2077": Palette(
        id="cyberpunk_2077",
        name="Cyberpunk 2077 (Neon Yellow & Cyan Pulse)",
        dark_bg="#08080E",
        dark_card="#121222",
        dark_border="#2B2B47",
        dark_text_primary="#FFFDF0",
        dark_text_secondary="#8E8EA8",
        dark_accent_primary="#FEE715",   # Neon Yellow
        dark_accent_secondary="#00F0FF", # Cyber Cyan
        dark_accent_tertiary="#FF007F",  # Acid Magenta
        dark_glow="#00F0FF44",
        light_bg="#F4F4F8",
        light_card="#FFFFFF",
        light_border="#D1D1DF",
        light_text_primary="#121224",
        light_text_secondary="#5A5A72",
        light_accent_primary="#CA9A00",
        light_accent_secondary="#0099A8",
        light_accent_tertiary="#D6006B",
        light_glow="#0099A833",
    ),
    "nord_frost": Palette(
        id="nord_frost",
        name="Nord Frost (Arctic Glacier & Aurora)",
        dark_bg="#242933",
        dark_card="#2E3440",
        dark_border="#3B4252",
        dark_text_primary="#ECEFF4",
        dark_text_secondary="#D8DEE9",
        dark_accent_primary="#88C0D0",   # Frost Cyan
        dark_accent_secondary="#81A1C1", # Frost Blue
        dark_accent_tertiary="#A3BE8C",  # Aurora Green
        dark_glow="#88C0D044",
        light_bg="#ECEFF4",
        light_card="#E5E9F0",
        light_border="#D8DEE9",
        light_text_primary="#2E3440",
        light_text_secondary="#4C566A",
        light_accent_primary="#4C8A9E",
        light_accent_secondary="#436F94",
        light_accent_tertiary="#688C4E",
        light_glow="#4C8A9E33",
    ),
    "dracula": Palette(
        id="dracula",
        name="Dracula Vampire (Nocturnal Purple & Toxic Green)",
        dark_bg="#1E1F29",
        dark_card="#282A36",
        dark_border="#44475A",
        dark_text_primary="#F8F8F2",
        dark_text_secondary="#B6B8CA",
        dark_accent_primary="#BD93F9",   # Purple
        dark_accent_secondary="#50FA7B", # Green
        dark_accent_tertiary="#FF79C6",  # Pink
        dark_glow="#BD93F944",
        light_bg="#F5F3F8",
        light_card="#FFFFFF",
        light_border="#D6D0E3",
        light_text_primary="#282A36",
        light_text_secondary="#59556B",
        light_accent_primary="#7D49C9",
        light_accent_secondary="#219E47",
        light_accent_tertiary="#C72E85",
        light_glow="#7D49C933",
    ),
    "tokyo_night": Palette(
        id="tokyo_night",
        name="Tokyo Night (Shibuya Rain & Neon Lanterns)",
        dark_bg="#16161E",
        dark_card="#1F2335",
        dark_border="#292E42",
        dark_text_primary="#C0CAF5",
        dark_text_secondary="#7AA2F7",
        dark_accent_primary="#7AA2F7",   # Blue
        dark_accent_secondary="#BB9AF7", # Magenta
        dark_accent_tertiary="#73DACA",  # Teal
        dark_glow="#7AA2F744",
        light_bg="#F3F4F8",
        light_card="#FFFFFF",
        light_border="#D5D9E7",
        light_text_primary="#1A1B26",
        light_text_secondary="#4C5A85",
        light_accent_primary="#3454B4",
        light_accent_secondary="#7245B8",
        light_accent_tertiary="#1B8070",
        light_glow="#3454B433",
    ),
    "monokai_pro": Palette(
        id="monokai_pro",
        name="Monokai Pro (Spectrum Sunset & Vivid Accents)",
        dark_bg="#221F22",
        dark_card="#2D2A2E",
        dark_border="#403E41",
        dark_text_primary="#FCFCFA",
        dark_text_secondary="#939293",
        dark_accent_primary="#FFD866",   # Yellow
        dark_accent_secondary="#FF6188", # Rose
        dark_accent_tertiary="#78DCE8",  # Cyan
        dark_glow="#FFD86644",
        light_bg="#F9F8F9",
        light_card="#FFFFFF",
        light_border="#DAD7DA",
        light_text_primary="#2D2A2E",
        light_text_secondary="#656366",
        light_accent_primary="#B58600",
        light_accent_secondary="#C7204A",
        light_accent_tertiary="#0B8B9B",
        light_glow="#B5860033",
    ),
    "emerald_matrix": Palette(
        id="emerald_matrix",
        name="Emerald Matrix (Terminal Green & Hex Code)",
        dark_bg="#030A05",
        dark_card="#07170B",
        dark_border="#113B1B",
        dark_text_primary="#A3F7BF",
        dark_text_secondary="#4ADE80",
        dark_accent_primary="#00FF66",   # Pure Matrix Green
        dark_accent_secondary="#34D399", # Emerald
        dark_accent_tertiary="#22C55E",  # Light Green
        dark_glow="#00FF6644",
        light_bg="#F0FAF3",
        light_card="#FFFFFF",
        light_border="#B7E6C5",
        light_text_primary="#063815",
        light_text_secondary="#1A6832",
        light_accent_primary="#048A36",
        light_accent_secondary="#0C6B45",
        light_accent_tertiary="#15803D",
        light_glow="#048A3633",
    ),
    "amber_crt": Palette(
        id="amber_crt",
        name="Amber CRT (Phosphor Glow & Vintage Glass)",
        dark_bg="#120800",
        dark_card="#1F1002",
        dark_border="#3E2004",
        dark_text_primary="#FFE6B3",
        dark_text_secondary="#F59E0B",
        dark_accent_primary="#FFB000",   # Amber Phosphor
        dark_accent_secondary="#F97316", # Warm Orange
        dark_accent_tertiary="#FDE047",  # Bright Yellow
        dark_glow="#FFB00044",
        light_bg="#FFF9F0",
        light_card="#FFFFFF",
        light_border="#F4D3B0",
        light_text_primary="#3A1C00",
        light_text_secondary="#7A3F00",
        light_accent_primary="#B45309",
        light_accent_secondary="#C2410C",
        light_accent_tertiary="#854D0E",
        light_glow="#B4530933",
    ),
    "solarized_dark": Palette(
        id="solarized_dark",
        name="Solarized Dark (Precision Science & Clean Contrast)",
        dark_bg="#00212B",
        dark_card="#002B36",
        dark_border="#073642",
        dark_text_primary="#93A1A1",
        dark_text_secondary="#657B83",
        dark_accent_primary="#2AA198",   # Cyan
        dark_accent_secondary="#268BD2", # Blue
        dark_accent_tertiary="#B58900",  # Yellow
        dark_glow="#2AA19844",
        light_bg="#FDF6E3",
        light_card="#EEE8D5",
        light_border="#D33682",
        light_text_primary="#586E75",
        light_text_secondary="#839496",
        light_accent_primary="#1B7871",
        light_accent_secondary="#1A659E",
        light_accent_tertiary="#8A6800",
        light_glow="#1B787133",
    ),
    "rose_pine": Palette(
        id="rose_pine",
        name="Rosé Pine (All-Natural Pastel & Calming Dusk)",
        dark_bg="#14121E",
        dark_card="#191724",
        dark_border="#26233A",
        dark_text_primary="#E0DEF4",
        dark_text_secondary="#908CAA",
        dark_accent_primary="#EBBCBA",   # Rose
        dark_accent_secondary="#9CCFD8", # Foam
        dark_accent_tertiary="#C4A7E7",  # Iris
        dark_glow="#EBBCBA44",
        light_bg="#FAF4ED",
        light_card="#FFFFFF",
        light_border="#E4DFDE",
        light_text_primary="#575279",
        light_text_secondary="#797593",
        light_accent_primary="#B85D6B",
        light_accent_secondary="#3F7A85",
        light_accent_tertiary="#765C9C",
        light_glow="#B85D6B33",
    ),
}

def get_palette(theme_id: str) -> Palette:
    return PALETTES.get(theme_id, PALETTES["kemet_nocturne"])

def list_palette_ids() -> List[str]:
    return list(PALETTES.keys())
