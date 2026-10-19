"""
library/generators - Category generator exports for VectorForge.
"""

from library.generators.banners import BANNER_PRESETS, generate_banner_svg
from library.generators.terminals import TERMINAL_PRESETS, generate_terminal_svg
from library.generators.skylines import SKYLINE_PRESETS, generate_skyline_svg
from library.generators.architectures import ARCHITECTURE_PRESETS, generate_architecture_svg
from library.generators.badges import BADGE_PRESETS, generate_badge_svg
from library.generators.repo_cards import REPO_PRESETS, generate_repo_card_svg
from library.generators.holograms import HOLOGRAM_PRESETS, generate_hologram_svg

CATEGORIES = {
    "banners": {"name": "Geometric Banners", "presets": BANNER_PRESETS, "fn": generate_banner_svg},
    "terminals": {"name": "Neofetch & Terminals", "presets": TERMINAL_PRESETS, "fn": generate_terminal_svg},
    "skylines": {"name": "Skylines & Horizons", "presets": SKYLINE_PRESETS, "fn": generate_skyline_svg},
    "architectures": {"name": "System Architectures", "presets": ARCHITECTURE_PRESETS, "fn": generate_architecture_svg},
    "badges": {"name": "HUD Badges & Pills", "presets": BADGE_PRESETS, "fn": generate_badge_svg},
    "repo_cards": {"name": "Bento & Repo Cards", "presets": REPO_PRESETS, "fn": generate_repo_card_svg},
    "holograms": {"name": "Holograms & Ledgers", "presets": HOLOGRAM_PRESETS, "fn": generate_hologram_svg},
}

__all__ = [
    "BANNER_PRESETS", "generate_banner_svg",
    "TERMINAL_PRESETS", "generate_terminal_svg",
    "SKYLINE_PRESETS", "generate_skyline_svg",
    "ARCHITECTURE_PRESETS", "generate_architecture_svg",
    "BADGE_PRESETS", "generate_badge_svg",
    "REPO_PRESETS", "generate_repo_card_svg",
    "HOLOGRAM_PRESETS", "generate_hologram_svg",
    "CATEGORIES",
]
