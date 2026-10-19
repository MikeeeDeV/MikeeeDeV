"""
library/cli.py - VectorForge Developer CLI.
Command-line tool to inspect, customize, and export 235+ developer SVG shapes.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from library.generators import CATEGORIES
from library.engine.color_palettes import PALETTES, list_palette_ids
from library.catalog import build_catalog_metadata, render_all_svgs

def cmd_list(args):
    cat_filter = args.category
    print("=" * 70)
    print("⚡ VECTORFORGE // SHAPE LIBRARY CATALOG")
    print("=" * 70)
    
    total = 0
    for cat_id, cat_info in CATEGORIES.items():
        if cat_filter and cat_filter != cat_id:
            continue
        presets = cat_info["presets"]
        print(f"\n📂 [{cat_id.upper()}] - {cat_info['name']} ({len(presets)} shapes)")
        print("-" * 70)
        for p in presets:
            total += 1
            print(f"  • {p['id']:<32} | {p['title']:<30} | {p['theme']}")
            
    print("\n" + "=" * 70)
    print(f"Total shapes displayed: {total}")
    print("=" * 70)

def cmd_search(args):
    query = args.query.lower()
    print(f"🔍 Searching VectorForge shapes matching '{query}'...\n")
    matches = []
    for cat_id, cat_info in CATEGORIES.items():
        for p in cat_info["presets"]:
            if query in p["id"].lower() or query in p["title"].lower() or query in p["theme"].lower():
                matches.append((cat_id, p))
                
    if not matches:
        print("No shapes found matching query.")
        return
        
    for cat_id, p in matches:
        print(f"[{cat_id}] {p['id']} - {p['title']} (Theme: {p['theme']})")
    print(f"\nFound {len(matches)} matching shape(s).")

def cmd_generate(args):
    preset_id = args.preset_id
    theme = args.theme
    out_path = args.out
    
    # Locate generator
    target_cat = None
    target_preset = None
    for cat_id, cat_info in CATEGORIES.items():
        for p in cat_info["presets"]:
            if p["id"] == preset_id:
                target_cat = cat_info
                target_preset = p
                break
        if target_preset:
            break
            
    if not target_preset:
        print(f"Error: Preset '{preset_id}' not found. Run 'list' to see available presets.", file=sys.stderr)
        sys.exit(1)
        
    gen_fn = target_cat["fn"]
    svg = gen_fn(preset_id, theme_override=theme)
    
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(svg, encoding="utf-8")
        print(f"[OK] Generated {preset_id} (theme: {theme or target_preset['theme']}) -> {out_path} ({len(svg)} bytes)")
    else:
        print(svg)

def cmd_embed(args):
    preset_id = args.preset_id
    cat_found = None
    preset_found = None
    for cat_id, cat_info in CATEGORIES.items():
        for p in cat_info["presets"]:
            if p["id"] == preset_id:
                cat_found = cat_id
                preset_found = p
                break
        if preset_found:
            break
            
    if not preset_found:
        print(f"Error: Preset '{preset_id}' not found.", file=sys.stderr)
        sys.exit(1)
        
    url = f"https://raw.githubusercontent.com/MikeeeDeV/MikeeeDeV/main/library/shapes/{cat_found}/{preset_id}.svg"
    print("### Markdown Embed Syntax:\n")
    print(f"![{preset_found['title']}]({url})")
    print("\n### HTML Embed Syntax:\n")
    print(f'<img src="{url}" alt="{preset_found["title"]}" width="100%" />')

def cmd_render_all(args):
    print("⚡ Rendering all 235 VectorForge SVGs and updating catalog.json...")
    count = render_all_svgs(verbose=args.verbose)
    print(f"\n[DONE] Rendered {count} SVGs into library/shapes/")

def main():
    parser = argparse.ArgumentParser(description="VectorForge Developer Shape CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # list
    p_list = subparsers.add_parser("list", help="List all shapes in the library")
    p_list.add_argument("--category", "-c", choices=list(CATEGORIES.keys()), help="Filter by category")
    p_list.set_defaults(func=cmd_list)
    
    # search
    p_search = subparsers.add_parser("search", help="Search presets by keyword")
    p_search.add_argument("query", help="Keyword to search")
    p_search.set_defaults(func=cmd_search)
    
    # generate
    p_gen = subparsers.add_parser("generate", help="Generate an SVG preset")
    p_gen.add_argument("preset_id", help="Preset ID")
    p_gen.add_argument("--theme", "-t", choices=list_palette_ids(), help="Override color palette theme")
    p_gen.add_argument("--out", "-o", help="Output file path (default stdout)")
    p_gen.set_defaults(func=cmd_generate)
    
    # embed
    p_embed = subparsers.add_parser("embed", help="Get markdown / HTML embed snippet")
    p_embed.add_argument("preset_id", help="Preset ID")
    p_embed.set_defaults(func=cmd_embed)
    
    # render-all
    p_all = subparsers.add_parser("render-all", help="Batch render all 235 SVGs")
    p_all.add_argument("--verbose", "-v", action="store_true", help="Print each rendered SVG")
    p_all.set_defaults(func=cmd_render_all)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
