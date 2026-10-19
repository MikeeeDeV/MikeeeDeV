"""
library/cli.py - VectorForge Developer CLI.
Command-line tool to inspect, customize, configure, and batch-render 235+ developer SVG shapes.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List
from library.generators import CATEGORIES
from library.engine.color_palettes import PALETTES, list_palette_ids
from library.catalog import build_catalog_metadata, render_all_svgs
from library.config import (
    find_config_file,
    load_config,
    init_config,
    apply_parameters
)

def parse_param_args(param_list: Optional[List[str]]) -> Dict[str, str]:
    """Parses list of 'key=value' CLI strings into a dictionary."""
    params = {}
    if not param_list:
        return params
    for item in param_list:
        if "=" in item:
            k, v = item.split("=", 1)
            params[k.strip()] = v.strip()
    return params

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
    cli_params = parse_param_args(args.param)
    
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
    
    # Apply dynamic parameters
    if cli_params:
        svg = apply_parameters(svg, cli_params, target_preset)
    
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(svg, encoding="utf-8")
        param_desc = f" (params: {len(cli_params)})" if cli_params else ""
        print(f"[OK] Generated {preset_id} (theme: {theme or target_preset['theme']}){param_desc} -> {out_path} ({len(svg)} bytes)")
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
        
    url = f"https://cdn.jsdelivr.net/gh/MikeeeDeV/MikeeeDeV@main/library/shapes/{cat_found}/{preset_id}.svg"
    print("### Markdown Embed Syntax:\n")
    print(f"![{preset_found['title']}]({url})")
    print("\n### jsDelivr Raw URL:\n")
    print(url)
    print("\n### HTML Embed Syntax:\n")
    print(f'<img src="{url}" alt="{preset_found["title"]}" width="100%" />')

def cmd_init(args):
    target = args.out or "vectorforge.json"
    try:
        created = init_config(target)
        print("=" * 70)
        print("✨ VECTORFORGE // INITIALIZED STARTER CONFIGURATION")
        print("=" * 70)
        print(f"\nCreated: {created.resolve()}")
        print("\nNext Steps:")
        print("  1. Inspect and customize your presets in vectorforge.json")
        print("  2. Run 'vectorforge build' to render all profile assets\n")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_build(args):
    try:
        cfg_path = find_config_file(args.config)
        if not cfg_path:
            print("Error: No vectorforge.json or vectorforge.yaml found. Run 'vectorforge init' first.", file=sys.stderr)
            sys.exit(1)
            
        config = load_config(cfg_path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    out_dir_str = config.get("output_dir", "./assets")
    out_dir = Path(out_dir_str)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    shapes_list = config.get("shapes", [])
    if not shapes_list:
        print("Warning: No shapes defined in configuration 'shapes' array.", file=sys.stderr)
        return
        
    print("=" * 75)
    print(f"⚡ VECTORFORGE // BUILDING {len(shapes_list)} ASSETS FROM {cfg_path.name}")
    print(f"Target Output Directory: {out_dir.resolve()}")
    print("=" * 75)
    
    total_bytes = 0
    built_count = 0
    
    for item in shapes_list:
        preset_id = item.get("preset")
        theme = item.get("theme")
        rel_out = item.get("out") or f"{preset_id}.svg"
        params = item.get("params", {})
        
        target_preset = None
        target_cat = None
        for cat_id, cat_info in CATEGORIES.items():
            for p in cat_info["presets"]:
                if p["id"] == preset_id:
                    target_preset = p
                    target_cat = cat_info
                    break
            if target_preset:
                break
                
        if not target_preset:
            print(f"  [SKIP] Unknown preset ID '{preset_id}'")
            continue
            
        gen_fn = target_cat["fn"]
        svg = gen_fn(preset_id, theme_override=theme)
        if params:
            svg = apply_parameters(svg, params, target_preset)
            
        target_file = out_dir / rel_out
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(svg, encoding="utf-8")
        
        size = len(svg.encode("utf-8"))
        total_bytes += size
        built_count += 1
        print(f"  ✓ {preset_id:<28} -> {rel_out:<28} ({size:,} B) [{theme or target_preset['theme']}]")
        
    print("-" * 75)
    print(f"[DONE] Successfully built {built_count}/{len(shapes_list)} shapes ({total_bytes:,} total bytes)")
    print("=" * 75)

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
    p_gen.add_argument("--param", "-p", action="append", help="Dynamic parameter override (e.g. -p title='My Name')")
    p_gen.set_defaults(func=cmd_generate)
    
    # embed
    p_embed = subparsers.add_parser("embed", help="Get markdown / HTML embed snippet")
    p_embed.add_argument("preset_id", help="Preset ID")
    p_embed.set_defaults(func=cmd_embed)
    
    # init
    p_init = subparsers.add_parser("init", help="Scaffold a starter vectorforge.json configuration")
    p_init.add_argument("--out", "-o", help="Config file path (default vectorforge.json)")
    p_init.set_defaults(func=cmd_init)
    
    # build
    p_build = subparsers.add_parser("build", help="Build all shapes defined in vectorforge.json")
    p_build.add_argument("--config", "-c", help="Path to vectorforge.json or vectorforge.yaml")
    p_build.set_defaults(func=cmd_build)
    
    # render-all
    p_all = subparsers.add_parser("render-all", help="Batch render all 235 SVGs")
    p_all.add_argument("--verbose", "-v", action="store_true", help="Print each rendered SVG")
    p_all.set_defaults(func=cmd_render_all)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
