# 🛠️ VectorForge Developer Guide & Integration Manual

Welcome to the **VectorForge Developer Guide**. This document provides end-to-end instructions for integrating, automating, and customizing 235+ deterministic developer SVG shapes across your GitHub profiles, technical documentation, Next.js / React applications, and CI/CD pipelines.

---

## ⚡ Quickstart: Choose Your Preferred Stack

### Option A: Node.js / NPX (Zero-Install, Recommended for Web Developers)
Run directly via `npx` without cloning or configuring Python:
```bash
# Search presets by keyword
npx vectorforge search "raft"

# Generate a custom shape with parameters
npx vectorforge generate raft-consensus-cluster \
  --theme dracula \
  --param title="Distributed Consensus Engine" \
  --out ./public/architecture.svg

# Initialize a declarative profile config
npx vectorforge init

# Batch build all configured shapes
npx vectorforge build
```

---

### Option B: Python CLI (PIP / PEP 621)
For Python developers and systems engineers:
```bash
pip install -e .

# List all shapes across 7 categories
vectorforge list

# Generate an SVG with custom theme
vectorforge generate kemet-nocturne-rosette -t cyberpunk_2077 -o ./assets/hero.svg

# Batch build shapes from vectorforge.json
vectorforge build
```

---

### Option C: Zero-Install Instant CDN Embed (Fastest)
Embed directly into your GitHub `README.md` or web page via jsDelivr CDN without downloading files:

```markdown
![VectorForge Hero Banner](https://cdn.jsdelivr.net/gh/MikeeeDeV/MikeeeDeV@main/library/shapes/banners/kemet-nocturne-rosette.svg)
```

---

## ⚛️ React, Next.js & Astro Integration

Every VectorForge shape can be exported directly into a clean, typed React component:

1. Open the [VectorForge Showroom](https://mikeeedev.github.io/MikeeeDeV/).
2. Click **`⚛️ JSX`** on any card or open the Inspector modal.
3. Paste the generated component into your project:

```tsx
import React from 'react';

export function RaftConsensusClusterShape(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 280" {...props}>
      {/* Deterministic SVG paths with camelCase JSX attributes */}
    </svg>
  );
}
```

---

## 📋 Declarative Configuration (`vectorforge.json`)

Automate multiple assets across your repository with a single configuration file.

### 1. Scaffold Configuration
```bash
npx vectorforge init
# or: vectorforge init
```

This creates `vectorforge.json` (with VS Code schema autocompletion enabled via `schema.json`):

```json
{
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
}
```

### 2. Batch Build
```bash
npx vectorforge build
```

---

## 🎨 Curated Color Themes (10 Built-In Palettes)

Override colors for any shape using `--theme <id>`:

| Theme ID | Name | Primary Accent | Secondary Accent |
| :--- | :--- | :---: | :---: |
| `kemet_nocturne` | Kemet Nocturne | `#F5C451` (Gold) | `#38BDF8` (Lapis) |
| `cyberpunk_2077` | Cyberpunk 2077 | `#FCEE0A` (Yellow) | `#FF0055` (Pink) |
| `nord_frost` | Nord Frost | `#88C0D0` (Ice) | `#81A1C1` (Polar) |
| `dracula` | Dracula | `#BD93F9` (Purple) | `#FF79C6` (Coral) |
| `tokyo_night` | Tokyo Night | `#7AA2F7` (Blue) | `#BB9AF7` (Purple) |
| `monokai_pro` | Monokai Pro | `#FFD866` (Yellow) | `#FF6188` (Red) |
| `emerald_matrix` | Emerald Matrix | `#00FF66` (Phosphor) | `#10B981` (Emerald) |
| `amber_crt` | Amber CRT | `#FFB000` (Amber) | `#FF8C00` (Orange) |
| `solarized_dark` | Solarized Dark | `#2AA198` (Cyan) | `#CB4B16` (Orange) |
| `rose_pine` | Rosé Pine | `#EB6F92` (Rose) | `#F6C177` (Gold) |

---

## 🤖 GitHub Actions Profile Auto-Sync

To automatically re-render your profile shapes on schedule or on push, copy [examples/profile-sync-workflow.yml](file:///home/mohamed-ayman/Desktop/Me/examples/profile-sync-workflow.yml) to `.github/workflows/vectorforge-sync.yml`:

```yaml
name: Sync VectorForge Profile Assets

on:
  push:
    branches: [main]
    paths: ['vectorforge.json']
  schedule:
    - cron: '0 0 * * 0'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npx -y vectorforge build
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: update vectorforge profile assets [skip ci]"
```

---

## 🌐 Interactive Showroom

Browse all 235 shapes, preview themes live, and copy snippets directly from the browser:
👉 **[Launch VectorForge Showroom Gallery](https://mikeeedev.github.io/MikeeeDeV/)**
