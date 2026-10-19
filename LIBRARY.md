# ⚡ VectorForge Shape Studio

> **Deterministic, Zero-Runtime-Dependency Developer SVG Shape & Component Library**  
> *Crafted by Mohamed Ayman ([@MikeeeDeV](https://github.com/MikeeeDeV)) • Senior Full-Stack & Systems Engineer*

VectorForge is an open-source, mathematically deterministic vector asset library engineered for developers, engineering leaders, and open-source creators. Every component is self-contained SVG with dark/light mode responsiveness (`prefers-color-scheme`), zero external font downloads, zero tracking scripts, and strict `<100KB` file size budgets.

---

## 📊 Catalog Overview

| Category | Shapes | Dimensions | Description |
| :--- | :---: | :---: | :--- |
| **1. Geometric Banners** | `40` | `960x240` | Rosettes, Astrolabes, Mandalas, Penrose grids, Hypercubes, Lissajous curves |
| **2. Neofetch Terminals** | `35` | `680x360` | Authentic terminal cards with ASCII distros, system specs, and memory meters |
| **3. Skylines & Horizons** | `30` | `880x210` | 52-week contribution horizons, cityscapes, audio spectrograms, mountain ridges |
| **4. System Architectures** | `35` | `820x280` | High-density topology diagrams (FastMCP, Raft, Kafka, Nix DAG, Service Mesh) |
| **5. HUD Badges & Pills** | `35` | `420x88` | Reactor core gauges, cyber target locks, uptime SLA badges, status pills |
| **6. Bento & Repo Cards** | `35` | `420x160` | Glassmorphic portfolio cards with stars, language tags, and borders |
| **7. Holographic Ledgers** | `25` | `560x240` | Circular radar sweeps, sonar pings, blockchain ledgers, and astrolabe dials |
| **TOTAL** | **`235`** | — | **100% Valid XML • Self-Contained • Responsive** |

---

## 🎨 10 Curated Color Palettes

Every shape is rendered with native CSS custom properties supporting light/dark system themes:

1. **Kemet Nocturne** (`kemet_nocturne`): Ancient Egyptian gold (#F5C451) & Nile lapis (#38BDF8)
2. **Cyberpunk 2077** (`cyberpunk_2077`): Neon electric yellow (#FEE715) & cyber cyan (#00F0FF)
3. **Nord Frost** (`nord_frost`): Arctic glacier cyan (#88C0D0) & polar night blue (#81A1C1)
4. **Dracula** (`dracula`): Nocturnal purple (#BD93F9) & toxic green (#50FA7B)
5. **Tokyo Night** (`tokyo_night`): Shibuya rain blue (#7AA2F7) & neon magenta (#BB9AF7)
6. **Monokai Pro** (`monokai_pro`): Spectrum sunset yellow (#FFD866) & vivid rose (#FF6188)
7. **Emerald Matrix** (`emerald_matrix`): Pure terminal phosphor green (#00FF66)
8. **Amber CRT** (`amber_crt`): Vintage warm amber phosphor (#FFB000)
9. **Solarized Dark** (`solarized_dark`): Precision science cyan (#2AA198) & deep blue (#268BD2)
10. **Rosé Pine** (`rose_pine`): Soft pastel rose (#EBBCBA) & calming foam (#9CCFD8)

---

## 🚀 Quickstart & Usage

### 1. Interactive Web Showroom
Open the offline showroom gallery in any modern browser:
```bash
python3 -m http.server 8080
# Open http://localhost:8080/library/gallery/index.html
```

### 2. Developer CLI
Inspect, search, and generate any shape via CLI:
```bash
# List all 235 shapes
python3 -m library.cli list

# Search shapes by keyword
python3 -m library.cli search "raft"

# Generate an SVG with a custom theme override
python3 -m library.cli generate raft-consensus-cluster --theme cyberpunk_2077 --out custom-raft.svg

# Get 1-click Markdown embed code
python3 -m library.cli embed kemet-nocturne-rosette
```

### 3. Embed Directly in Your README.md
You can embed any shape directly in your GitHub profile or project documentation:
```markdown
![Kemet Rosette](https://raw.githubusercontent.com/MikeeeDeV/MikeeeDeV/main/library/shapes/banners/kemet-nocturne-rosette.svg)
```

---

## 🧪 Architecture & Validation

- **Deterministic Math**: Rosettes, Lissajous curves, and Phyllotaxis spirals generated via pure vector trigonometry (`library/engine/geometry.py`).
- **Strict Budget**: Every SVG file is validated by CI to be strictly under `100KB`.
- **Accessibility**: Includes `<title>` and `<desc>` accessibility tags compliant with W3C SVG 1.1 specs.
- **Hermetic Testing**: 15 unit and snapshot test suites passing 100% under Python 3.14.
