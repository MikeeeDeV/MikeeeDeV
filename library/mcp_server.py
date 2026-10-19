"""
library/mcp_server.py - VectorForge Model Context Protocol (MCP) Server.
Enables AI Agents (Claude Desktop, Cursor, Antigravity) to discover, inspect,
and generate deterministic developer SVG shapes over stdio JSON-RPC.
"""

import sys
import json
import logging
from typing import Dict, Any, List, Optional
from library.generators import CATEGORIES
from library.engine.color_palettes import PALETTES, list_palette_ids
from library.config import apply_parameters

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS = [
    {
        "name": "vectorforge_list_shapes",
        "description": "Lists all 235 developer SVG shapes across 7 categories in VectorForge.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional category filter (banners, terminals, skylines, architectures, badges, repo_cards, holograms)",
                    "enum": list(CATEGORIES.keys())
                }
            }
        }
    },
    {
        "name": "vectorforge_search_shapes",
        "description": "Searches VectorForge shapes by keyword (e.g. 'raft', 'docker', 'astrolabe').",
        "inputSchema": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword"
                }
            }
        }
    },
    {
        "name": "vectorforge_generate_shape",
        "description": "Generates a deterministic SVG shape preset with optional theme and dynamic parameter overrides.",
        "inputSchema": {
            "type": "object",
            "required": ["preset_id"],
            "properties": {
                "preset_id": {
                    "type": "string",
                    "description": "Preset ID (e.g. 'kemet-nocturne-rosette', 'raft-consensus-cluster')"
                },
                "theme": {
                    "type": "string",
                    "description": "Color theme palette override",
                    "enum": list_palette_ids()
                },
                "params": {
                    "type": "object",
                    "description": "Key-value parameter overrides (e.g. title, subtitle, role, stack)"
                }
            }
        }
    }
]

def tool_list_shapes(arguments: Dict[str, Any]) -> Dict[str, Any]:
    cat_filter = arguments.get("category")
    results = []
    for cat_id, cat_info in CATEGORIES.items():
        if cat_filter and cat_filter != cat_id:
            continue
        for p in cat_info["presets"]:
            results.append({
                "category": cat_id,
                "id": p["id"],
                "title": p["title"],
                "default_theme": p["theme"]
            })
    return {"total": len(results), "shapes": results}

def tool_search_shapes(arguments: Dict[str, Any]) -> Dict[str, Any]:
    query = arguments.get("query", "").lower().strip()
    matches = []
    for cat_id, cat_info in CATEGORIES.items():
        for p in cat_info["presets"]:
            if query in p["id"].lower() or query in p["title"].lower() or query in p["theme"].lower():
                matches.append({
                    "category": cat_id,
                    "id": p["id"],
                    "title": p["title"],
                    "default_theme": p["theme"]
                })
    return {"query": query, "total_matches": len(matches), "matches": matches}

def tool_generate_shape(arguments: Dict[str, Any]) -> Dict[str, Any]:
    preset_id = arguments.get("preset_id")
    theme = arguments.get("theme")
    params = arguments.get("params", {})

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
        return {"error": f"Preset '{preset_id}' not found."}

    gen_fn = target_cat["fn"]
    svg = gen_fn(preset_id, theme_override=theme)
    if params:
        svg = apply_parameters(svg, params, target_preset)

    return {
        "preset_id": preset_id,
        "theme": theme or target_preset["theme"],
        "bytes": len(svg.encode("utf-8")),
        "svg": svg
    }

def handle_rpc(request: Dict[str, Any]) -> Dict[str, Any]:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "vectorforge",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "vectorforge_list_shapes":
            res = tool_list_shapes(arguments)
        elif tool_name == "vectorforge_search_shapes":
            res = tool_search_shapes(arguments)
        elif tool_name == "vectorforge_generate_shape":
            res = tool_generate_shape(arguments)
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }
                ]
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not supported"}
        }

def main():
    """Stdio loop processing JSON-RPC MCP messages."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
