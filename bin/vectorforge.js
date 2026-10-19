#!/usr/bin/env node

/**
 * VectorForge Node.js CLI & NPX Runner
 * Zero-dependency developer SVG generator and configuration build engine.
 * Author: Mohamed Ayman (@MikeeeDeV)
 */

const fs = require('fs');
const path = require('path');

const PALETTES = {
  kemet_nocturne: {
    name: "Kemet Nocturne (Gold & Lapis)",
    bg: "#0A0E17",
    card: "#111827",
    border: "#1F293D",
    text: "#F8FAFC",
    textMuted: "#94A3B8",
    accent1: "#F5C451",
    accent2: "#38BDF8",
    accent3: "#14B8A6",
    glow: "#F5C45144",
  },
  cyberpunk_2077: {
    name: "Cyberpunk 2077 (Neon Yellow & Pink)",
    bg: "#0D0D14",
    card: "#161622",
    border: "#2A2A3E",
    text: "#FFFFFF",
    textMuted: "#A3A3C2",
    accent1: "#FCEE0A",
    accent2: "#FF0055",
    accent3: "#00F0FF",
    glow: "#FCEE0A44",
  },
  nord_frost: {
    name: "Nord Frost (Arctic Ice & Polar)",
    bg: "#242933",
    card: "#2E3440",
    border: "#3B4252",
    text: "#ECEFF4",
    textMuted: "#D8DEE9",
    accent1: "#88C0D0",
    accent2: "#81A1C1",
    accent3: "#A3BE8C",
    glow: "#88C0D044",
  },
  dracula: {
    name: "Dracula (Vampire Purple & Coral)",
    bg: "#21222C",
    card: "#282A36",
    border: "#44475A",
    text: "#F8F8F2",
    textMuted: "#BD93F9",
    accent1: "#BD93F9",
    accent2: "#FF79C6",
    accent3: "#50FA7B",
    glow: "#BD93F944",
  },
  tokyo_night: {
    name: "Tokyo Night (Neon Blue & Purple)",
    bg: "#16161E",
    card: "#1A1B26",
    border: "#292E42",
    text: "#C0CAF5",
    textMuted: "#7AA2F7",
    accent1: "#7AA2F7",
    accent2: "#BB9AF7",
    accent3: "#7DCFFF",
    glow: "#7AA2F744",
  },
  monokai_pro: {
    name: "Monokai Pro (Sublime Yellow & Emerald)",
    bg: "#19181A",
    card: "#221F22",
    border: "#403E41",
    text: "#FCFCFA",
    textMuted: "#939293",
    accent1: "#FFD866",
    accent2: "#FF6188",
    accent3: "#A9DC76",
    glow: "#FFD86644",
  },
  emerald_matrix: {
    name: "Emerald Matrix (Phosphor Green)",
    bg: "#0A110D",
    card: "#0F1A14",
    border: "#1B3324",
    text: "#E6F4EA",
    textMuted: "#5CD68D",
    accent1: "#00FF66",
    accent2: "#10B981",
    accent3: "#6EE7B7",
    glow: "#00FF6644",
  },
  amber_crt: {
    name: "Amber CRT (Retro Monochrome)",
    bg: "#120D04",
    card: "#1A1306",
    border: "#33260C",
    text: "#FFF3DC",
    textMuted: "#D49B24",
    accent1: "#FFB000",
    accent2: "#FF8C00",
    accent3: "#FFD700",
    glow: "#FFB00044",
  },
  solarized_dark: {
    name: "Solarized Dark (Cyan & Orange)",
    bg: "#001E26",
    card: "#002B36",
    border: "#073642",
    text: "#93A1A1",
    textMuted: "#839496",
    accent1: "#2AA198",
    accent2: "#CB4B16",
    accent3: "#B58900",
    glow: "#2AA19844",
  },
  rose_pine: {
    name: "Rosé Pine (Lilac & Rose Gold)",
    bg: "#191724",
    card: "#1F1D2E",
    border: "#26233A",
    text: "#E0DEF4",
    textMuted: "#908CAA",
    accent1: "#EB6F92",
    accent2: "#F6C177",
    accent3: "#9CCFD8",
    glow: "#EB6F9244",
  },
};

function getCatalog() {
  const catalogPath = path.resolve(__dirname, '..', 'library', 'catalog.json');
  if (!fs.existsSync(catalogPath)) {
    console.error(`Error: Catalog metadata not found at ${catalogPath}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
}

function escapeXML(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function applyTheme(svgText, themeId) {
  const p = PALETTES[themeId];
  if (!p || !svgText) return svgText;

  const cssVars = `    --vf-bg: ${p.bg};
    --vf-card: ${p.card};
    --vf-border: ${p.border};
    --vf-text: ${p.text};
    --vf-text-muted: ${p.textMuted};
    --vf-accent-1: ${p.accent1};
    --vf-accent-2: ${p.accent2};
    --vf-accent-3: ${p.accent3};
    --vf-glow: ${p.glow};`;

  return svgText.replace(/:root\s*\{[^}]*\}/s, `:root {\n${cssVars}\n  }`);
}

function applyParameters(svgText, params, presetItem) {
  if (!params) return svgText;

  // 1. Template placeholders
  for (const [k, v] of Object.entries(params)) {
    const esc = escapeXML(v);
    svgText = svgText.split(`{{${k}}}`).join(esc);
    svgText = svgText.split(`\${${k}}`).join(esc);
  }

  // 2. Semantic overrides
  if (params.title && presetItem) {
    const escTitle = escapeXML(params.title);
    svgText = svgText.replace(
      /<title id="title-[^"]*">[^<]*<\/title>/,
      `<title id="title-id">${escTitle}</title>`
    );
    svgText = svgText.split(`>${presetItem.title}<`).join(`>${escTitle}<`);
    svgText = svgText.split(`>${presetItem.title.toUpperCase()}<`).join(`>${escTitle.toUpperCase()}<`);
  }

  if (params.subtitle) {
    const escSub = escapeXML(params.subtitle);
    svgText = svgText.replace(
      /<desc id="desc-[^"]*">[^<]*<\/desc>/,
      `<desc id="desc-id">${escSub}</desc>`
    );
  }

  return svgText;
}

function cmdList(args) {
  const catalog = getCatalog();
  let catFilter = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-c' || args[i] === '--category') {
      catFilter = args[++i];
    } else if (!args[i].startsWith('-')) {
      catFilter = args[i];
    }
  }

  console.log("=".repeat(70));
  console.log("⚡ VECTORFORGE // SHAPE LIBRARY CATALOG (Node.js / npx)");
  console.log("=".repeat(70));

  let total = 0;
  for (const [catId, catInfo] of Object.entries(catalog.categories)) {
    if (catFilter && catFilter !== catId) continue;

    const items = catalog.items.filter((i) => i.category === catId);
    console.log(`\n📂 [${catId.toUpperCase()}] - ${catInfo.name} (${items.length} shapes)`);
    console.log("-".repeat(70));
    for (const item of items) {
      total++;
      console.log(`  • ${item.id.padEnd(32)} | ${item.title.padEnd(30)} | ${item.default_theme}`);
    }
  }

  console.log("\n" + "=".repeat(70));
  console.log(`Total shapes displayed: ${total}`);
  console.log("=".repeat(70));
}

function cmdSearch(args) {
  const query = (args[0] || '').toLowerCase().trim();
  if (!query) {
    console.log("Usage: vectorforge search <keyword>");
    return;
  }

  const catalog = getCatalog();
  console.log(`🔍 Searching VectorForge shapes matching '${query}'...\n`);

  const matches = catalog.items.filter(
    (i) => i.id.toLowerCase().includes(query) ||
           i.title.toLowerCase().includes(query) ||
           i.default_theme.toLowerCase().includes(query)
  );

  if (matches.length === 0) {
    console.log("No shapes found matching query.");
    return;
  }

  for (const item of matches) {
    console.log(`[${item.category}] ${item.id} - ${item.title} (Theme: ${item.default_theme})`);
  }
  console.log(`\nFound ${matches.length} matching shape(s).`);
}

function cmdGenerate(args) {
  const presetId = args[0];
  if (!presetId) {
    console.error("Usage: vectorforge generate <preset_id> [--theme <theme>] [--out <file>] [-p key=value]");
    process.exit(1);
  }

  let theme = null;
  let outPath = null;
  const params = {};

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--theme' || args[i] === '-t') {
      theme = args[++i];
    } else if (args[i] === '--out' || args[i] === '-o') {
      outPath = args[++i];
    } else if (args[i] === '--param' || args[i] === '-p') {
      const pair = args[++i];
      if (pair && pair.includes('=')) {
        const [k, v] = pair.split('=');
        params[k.trim()] = v.trim();
      }
    }
  }

  const catalog = getCatalog();
  const item = catalog.items.find((i) => i.id === presetId);
  if (!item) {
    console.error(`Error: Preset '${presetId}' not found. Run 'vectorforge list' to inspect available presets.`);
    process.exit(1);
  }

  const svgFilePath = path.resolve(__dirname, '..', 'library', 'shapes', item.category, `${item.id}.svg`);
  if (!fs.existsSync(svgFilePath)) {
    console.error(`Error: Shape file not found on disk: ${svgFilePath}`);
    process.exit(1);
  }

  let svgText = fs.readFileSync(svgFilePath, 'utf8');

  if (theme) {
    svgText = applyTheme(svgText, theme);
  }
  if (Object.keys(params).length > 0) {
    svgText = applyParameters(svgText, params, item);
  }

  if (outPath) {
    const resolvedOut = path.resolve(process.cwd(), outPath);
    fs.mkdirSync(path.dirname(resolvedOut), { recursive: true });
    fs.writeFileSync(resolvedOut, svgText, 'utf8');
    const paramDesc = Object.keys(params).length ? ` (params: ${Object.keys(params).length})` : '';
    console.log(`[OK] Generated ${presetId} (theme: ${theme || item.default_theme})${paramDesc} -> ${outPath} (${Buffer.byteLength(svgText, 'utf8')} bytes)`);
  } else {
    process.stdout.write(svgText);
  }
}

function cmdEmbed(args) {
  const presetId = args[0];
  if (!presetId) {
    console.error("Usage: vectorforge embed <preset_id>");
    process.exit(1);
  }

  const catalog = getCatalog();
  const item = catalog.items.find((i) => i.id === presetId);
  if (!item) {
    console.error(`Error: Preset '${presetId}' not found.`);
    process.exit(1);
  }

  const cdnUrl = `https://cdn.jsdelivr.net/gh/MikeeeDeV/MikeeeDeV@v1/library/shapes/${item.category}/${item.id}.svg`;
  console.log("### Markdown Embed Syntax:\n");
  console.log(`![${item.title}](${cdnUrl})`);
  console.log("\n### jsDelivr Raw URL:\n");
  console.log(cdnUrl);
  console.log("\n### HTML Embed Syntax:\n");
  console.log(`<img src="${cdnUrl}" alt="${item.title}" width="100%" />`);
}

function cmdInit(args) {
  const target = args[0] || 'vectorforge.json';
  const resolved = path.resolve(process.cwd(), target);

  if (fs.existsSync(resolved)) {
    console.error(`Error: Configuration file already exists: ${target}`);
    process.exit(1);
  }

  const starterConfig = {
    "$schema": "https://mikeeedev.github.io/MikeeeDeV/schema.json",
    "version": "1.0",
    "output_dir": "./assets/generated",
    "shapes": [
      {
        "preset": "kemet-nocturne-rosette",
        "theme": "kemet_nocturne",
        "out": "profile-hero-banner.svg",
        "params": {
          "title": "Senior Systems Engineer",
          "subtitle": "Zero-Crash • High-Throughput • Deterministic"
        }
      },
      {
        "preset": "raft-consensus-cluster",
        "theme": "nord_frost",
        "out": "architecture-topology.svg",
        "params": {
          "title": "Distributed Consensus Pipeline"
        }
      },
      {
        "preset": "docker-healthy-container",
        "theme": "emerald_matrix",
        "out": "system-status-pill.svg"
      }
    ]
  };

  fs.writeFileSync(resolved, JSON.stringify(starterConfig, null, 2), 'utf8');

  console.log("=".repeat(70));
  console.log("✨ VECTORFORGE // INITIALIZED STARTER CONFIGURATION");
  console.log("=".repeat(70));
  console.log(`\nCreated: ${resolved}`);
  console.log("\nNext Steps:");
  console.log("  1. Inspect and customize your presets in vectorforge.json");
  console.log("  2. Run 'npx vectorforge build' to render all profile assets\n");
}

function cmdBuild(args) {
  let configFile = 'vectorforge.json';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' || args[i] === '-c') {
      configFile = args[++i];
    }
  }

  const resolvedConfig = path.resolve(process.cwd(), configFile);
  if (!fs.existsSync(resolvedConfig)) {
    console.error(`Error: Configuration file not found: ${configFile}. Run 'vectorforge init' first.`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(resolvedConfig, 'utf8'));
  const outDir = path.resolve(process.cwd(), config.output_dir || './assets');
  fs.mkdirSync(outDir, { recursive: true });

  const catalog = getCatalog();
  const shapes = config.shapes || [];

  console.log("=".repeat(75));
  console.log(`⚡ VECTORFORGE // BUILDING ${shapes.length} ASSETS FROM ${path.basename(configFile)}`);
  console.log(`Target Output Directory: ${outDir}`);
  console.log("=".repeat(75));

  let totalBytes = 0;
  let builtCount = 0;

  for (const item of shapes) {
    const presetId = item.preset;
    const theme = item.theme;
    const relOut = item.out || `${presetId}.svg`;
    const params = item.params || {};

    const presetItem = catalog.items.find((i) => i.id === presetId);
    if (!presetItem) {
      console.log(`  [SKIP] Unknown preset ID '${presetId}'`);
      continue;
    }

    const svgFilePath = path.resolve(__dirname, '..', 'library', 'shapes', presetItem.category, `${presetItem.id}.svg`);
    if (!fs.existsSync(svgFilePath)) {
      console.log(`  [SKIP] Shape file not found on disk: ${svgFilePath}`);
      continue;
    }

    let svgText = fs.readFileSync(svgFilePath, 'utf8');
    if (theme) {
      svgText = applyTheme(svgText, theme);
    }
    if (Object.keys(params).length > 0) {
      svgText = applyParameters(svgText, params, presetItem);
    }

    const targetFile = path.resolve(outDir, relOut);
    fs.mkdirSync(path.dirname(targetFile), { recursive: true });
    fs.writeFileSync(targetFile, svgText, 'utf8');

    const byteLen = Buffer.byteLength(svgText, 'utf8');
    totalBytes += byteLen;
    builtCount++;
    console.log(`  ✓ ${presetId.padEnd(28)} -> ${relOut.padEnd(28)} (${byteLen.toLocaleString()} B) [${theme || presetItem.default_theme}]`);
  }

  console.log("-".repeat(75));
  console.log(`[DONE] Successfully built ${builtCount}/${shapes.length} shapes (${totalBytes.toLocaleString()} total bytes)`);
  console.log("=".repeat(75));
}

function printHelp() {
  console.log(`
Usage: vectorforge <command> [options]

Commands:
  list [category]                        List all 235 presets (optional filter)
  search <keyword>                       Search presets by name or palette
  generate <preset_id> [options]         Generate an SVG preset
  embed <preset_id>                      Get markdown / HTML / CDN embed snippet
  init [filename]                        Scaffold starter vectorforge.json
  build [--config <file>]                Batch build shapes from vectorforge.json

Options for 'generate':
  -t, --theme <theme>                    Override color theme
  -o, --out <file>                       Output file path (default: stdout)
  -p, --param <key=value>                Dynamic parameter override
`);
}

const argv = process.argv.slice(2);
const command = argv[0];
const commandArgs = argv.slice(1);

switch (command) {
  case 'list':
    cmdList(commandArgs);
    break;
  case 'search':
    cmdSearch(commandArgs);
    break;
  case 'generate':
    cmdGenerate(commandArgs);
    break;
  case 'embed':
    cmdEmbed(commandArgs);
    break;
  case 'init':
    cmdInit(commandArgs);
    break;
  case 'build':
    cmdBuild(commandArgs);
    break;
  case '--help':
  case '-h':
  case 'help':
  default:
    printHelp();
    break;
}
