"""
vectorforge - Deterministic Developer SVG Shape Studio.
235+ developer-oriented vector shapes, banners, terminals, and architectures.
Author: Mohamed Ayman (@MikeeeDeV)
"""

__version__ = "1.0.0"
__author__ = "Mohamed Ayman (@MikeeeDeV)"

from library.catalog import build_catalog_metadata, render_all_svgs
from library.config import load_config, init_config, apply_parameters
from library.engine.color_palettes import PALETTES, list_palette_ids

__all__ = [
    "__version__",
    "build_catalog_metadata",
    "render_all_svgs",
    "load_config",
    "init_config",
    "apply_parameters",
    "PALETTES",
    "list_palette_ids"
]
