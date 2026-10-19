"""
library/engine - Core rendering infrastructure for VectorForge.
"""

from library.engine.color_palettes import PALETTES, Palette, get_palette, list_palette_ids
from library.engine.geometry import (
    rosette_path,
    hypocycloid_path,
    lissajous_path,
    circuit_trace_path,
    phyllotaxis_points,
    tesseract_projected_edges,
    wave_spectrogram_points
)
from library.engine.svg_builder import SVGBuilder

__all__ = [
    "PALETTES",
    "Palette",
    "get_palette",
    "list_palette_ids",
    "rosette_path",
    "hypocycloid_path",
    "lissajous_path",
    "circuit_trace_path",
    "phyllotaxis_points",
    "tesseract_projected_edges",
    "wave_spectrogram_points",
    "SVGBuilder",
]
