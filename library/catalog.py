"""
library/catalog.py - Catalog compiler and SVG batch renderer for VectorForge.
Manages metadata for 235 distinct SVG components across 7 categories.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from library.generators import CATEGORIES
from library.engine.color_palettes import PALETTES

LIBRARY_ROOT = Path(__file__).resolve().parent
SHAPES_DIR = LIBRARY_ROOT / "shapes"
CATALOG_PATH = LIBRARY_ROOT / "catalog.json"

def build_catalog_metadata() -> Dict[str, Any]:
    catalog: Dict[str, Any] = {
        "version": "1.0.0",
        "name": "VectorForge",
        "description": "Deterministic, zero-runtime-dependency developer SVG shape and component library.",
        "author": "Mohamed Ayman (@MikeeeDeV)",
        "total_shapes": 0,
        "categories": {},
        "palettes": [
            {"id": p.id, "name": p.name, "dark_bg": p.dark_bg, "accent": p.dark_accent_primary}
            for p in PALETTES.values()
        ],
        "items": []
    }
    
    total = 0
    for cat_id, cat_info in CATEGORIES.items():
        presets = cat_info["presets"]
        catalog["categories"][cat_id] = {
            "name": cat_info["name"],
            "count": len(presets)
        }
        for p in presets:
            total += 1
            item = {
                "id": p["id"],
                "category": cat_id,
                "title": p["title"],
                "default_theme": p["theme"],
                "file_path": f"library/shapes/{cat_id}/{p['id']}.svg",
                "markdown_embed": f"![{p['title']}](https://raw.githubusercontent.com/MikeeeDeV/MikeeeDeV/main/library/shapes/{cat_id}/{p['id']}.svg)",
            }
            catalog["items"].append(item)
            
    catalog["total_shapes"] = total
    return catalog

def render_all_svgs(output_dir: Path = None, verbose: bool = False) -> int:
    target_dir = output_dir or SHAPES_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    
    for cat_id, cat_info in CATEGORIES.items():
        cat_dir = target_dir / cat_id
        cat_dir.mkdir(parents=True, exist_ok=True)
        gen_fn = cat_info["fn"]
        for p in cat_info["presets"]:
            p_id = p["id"]
            svg_content = gen_fn(p_id)
            out_file = cat_dir / f"{p_id}.svg"
            out_file.write_text(svg_content, encoding="utf-8")
            count += 1
            if verbose:
                print(f"[{count:03d}/235] Rendered {out_file.relative_to(LIBRARY_ROOT)}")
                
    # Also save catalog.json
    catalog_data = build_catalog_metadata()
    CATALOG_PATH.write_text(json.dumps(catalog_data, indent=2), encoding="utf-8")
    return count

if __name__ == "__main__":
    rendered = render_all_svgs(verbose=True)
    print(f"\n[SUCCESS] Successfully generated {rendered} SVGs into {SHAPES_DIR}")
    print(f"[SUCCESS] Wrote catalog manifest to {CATALOG_PATH}")
