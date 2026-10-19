"""
library/engine/geometry.py - Algorithmic and Vector Math Helpers.
Generates geometric coordinates for rosettes, astrolabes, wave functions,
hyperbolic nets, circuit paths, polyhedra projections, and fractals.
"""

import math
from typing import List, Tuple

def rosette_path(cx: float, cy: float, r: float, petals: int = 8, pointiness: float = 0.5) -> str:
    """Generates an N-petal Islamic/Pharaonic geometric star rosette SVG path."""
    commands = []
    total_points = petals * 2
    angle_step = (2 * math.pi) / total_points
    
    for i in range(total_points):
        ang = i * angle_step - math.pi / 2
        # Alternate outer tip and inner dip
        current_r = r if (i % 2 == 0) else (r * pointiness)
        x = cx + current_r * math.cos(ang)
        y = cy + current_r * math.sin(ang)
        cmd = "M" if i == 0 else "L"
        commands.append(f"{cmd} {x:.2f} {y:.2f}")
    commands.append("Z")
    return " ".join(commands)

def hypocycloid_path(cx: float, cy: float, R: float, r: float, d: float, steps: int = 160) -> str:
    """Generates a mathematical spirograph / hypocycloid path."""
    points = []
    for i in range(steps + 1):
        theta = (2 * math.pi * i) / steps
        x = cx + (R - r) * math.cos(theta) + d * math.cos((R - r) * theta / r)
        y = cy + (R - r) * math.sin(theta) - d * math.sin((R - r) * theta / r)
        cmd = "M" if i == 0 else "L"
        points.append(f"{cmd} {x:.2f} {y:.2f}")
    return " ".join(points)

def lissajous_path(cx: float, cy: float, A: float, B: float, a: int, b: int, delta: float, steps: int = 180) -> str:
    """Generates Lissajous harmonic curves."""
    points = []
    for i in range(steps + 1):
        t = (2 * math.pi * i) / steps
        x = cx + A * math.sin(a * t + delta)
        y = cy + B * math.sin(b * t)
        cmd = "M" if i == 0 else "L"
        points.append(f"{cmd} {x:.2f} {y:.2f}")
    return " ".join(points)

def circuit_trace_path(x0: float, y0: float, x1: float, y1: float, mid_offset: float = 24.0) -> str:
    """Generates an aesthetic 45-degree or 90-degree PCB circuit trace."""
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        xm = x0 + mid_offset if dx > 0 else x0 - mid_offset
        return f"M {x0:.1f} {y0:.1f} L {xm:.1f} {y0:.1f} L {xm + dy:.1f} {y1:.1f} L {x1:.1f} {y1:.1f}"
    else:
        ym = y0 + mid_offset if dy > 0 else y0 - mid_offset
        return f"M {x0:.1f} {y0:.1f} L {x0:.1f} {ym:.1f} L {x1:.1f} {ym + dx:.1f} L {x1:.1f} {y1:.1f}"

def phyllotaxis_points(cx: float, cy: float, n_points: int = 70, c: float = 7.5) -> List[Tuple[float, float, float]]:
    """Generates golden angle Fibonacci sunflower spiral coordinates (x, y, radius)."""
    golden_angle = 137.50776405 * (math.pi / 180.0)
    pts = []
    for i in range(1, n_points + 1):
        r = c * math.sqrt(i)
        theta = i * golden_angle
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        size = 1.2 + (i / n_points) * 2.2
        pts.append((round(x, 2), round(y, 2), round(size, 2)))
    return pts

def tesseract_projected_edges(cx: float, cy: float, size: float = 70.0) -> List[Tuple[float, float, float, float]]:
    """Computes orthographic 2D projection lines of a 4D hypercube / tesseract."""
    # 8 vertices of outer cube, 8 vertices of inner cube
    outer = []
    inner = []
    s_out = size
    s_in = size * 0.52
    
    # 2D projection angles
    corners = [
        (-1, -1), (1, -1), (1, 1), (-1, 1),
        (-0.7, -1.4), (1.3, -1.4), (1.3, 0.6), (-0.7, 0.6)
    ]
    for dx, dy in corners:
        outer.append((cx + dx * s_out * 0.65, cy + dy * s_out * 0.5))
        inner.append((cx + dx * s_in * 0.65, cy + dy * s_in * 0.5))
        
    edges = []
    # Outer box edges
    for i in range(4):
        edges.append((outer[i][0], outer[i][1], outer[(i+1)%4][0], outer[(i+1)%4][1]))
        edges.append((outer[i+4][0], outer[i+4][1], outer[(i+1)%4 + 4][0], outer[(i+1)%4 + 4][1]))
        edges.append((outer[i][0], outer[i][1], outer[i+4][0], outer[i+4][1]))
        
        # Inner box edges
        edges.append((inner[i][0], inner[i][1], inner[(i+1)%4][0], inner[(i+1)%4][1]))
        edges.append((inner[i+4][0], inner[i+4][1], inner[(i+1)%4 + 4][0], inner[(i+1)%4 + 4][1]))
        edges.append((inner[i][0], inner[i][1], inner[i+4][0], inner[i+4][1]))
        
        # Cross connect outer to inner
        edges.append((outer[i][0], outer[i][1], inner[i][0], inner[i][1]))
        edges.append((outer[i+4][0], outer[i+4][1], inner[i+4][0], inner[i+4][1]))
    return edges

def wave_spectrogram_points(w: float, h: float, bars: int = 48, seed_seed: int = 42) -> List[Tuple[float, float, float, float]]:
    """Computes audio equalizer / spectrogram bar coordinates."""
    res = []
    step = w / bars
    bar_w = step * 0.68
    for i in range(bars):
        # Deterministic multi-harmonic formula
        norm = i / bars
        env = math.sin(norm * math.pi) ** 1.3
        harmonic = (
            math.sin(i * 0.7 + seed_seed) * 0.35 +
            math.sin(i * 1.5 + 2 * seed_seed) * 0.25 +
            math.cos(i * 0.3) * 0.4
        )
        bar_h = max(6.0, env * h * (0.3 + abs(harmonic) * 0.7))
        x = i * step + (step - bar_w) / 2
        y = h - bar_h
        res.append((round(x, 1), round(y, 1), round(bar_w, 1), round(bar_h, 1)))
    return res
