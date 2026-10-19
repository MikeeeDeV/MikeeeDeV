# Contributing to VectorForge & MikeeeDeV Profile Engine

Thank you for your interest in contributing to **VectorForge**! We are building an open-source, mathematically deterministic SVG component and shape library that developers, systems engineers, and creators can use anywhere without external dependencies.

---

## 🧭 Code of Conduct

All contributors are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to [mohamed.ayman.developer@gmail.com](mailto:mohamed.ayman.developer@gmail.com).

---

## 🛠️ Development Setup

The project requires Python 3.9+ and uses standard libraries with zero heavy external frameworks.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MikeeeDeV/MikeeeDeV.git
   cd MikeeeDeV
   ```

2. **Verify tests and environment:**
   ```bash
   make test
   ```

3. **Explore the Showroom Gallery:**
   ```bash
   make gallery
   # Open http://localhost:8080/library/gallery/index.html
   ```

---

## 🎨 Adding a New Shape / Preset

We welcome community-contributed shapes! Every new shape must adhere to the following **Hard Rules**:

1. **Zero External Runtime Dependencies**:
   - No remote Google Webfonts (`@import url(...)`), no external JavaScript, no third-party tracking pixels.
2. **Strict File Size Budget**:
   - Every SVG must stay strictly **under 100 KB** (most shapes should be under 15 KB).
3. **Valid XML**:
   - The SVG must parse without error using `xml.etree.ElementTree`.
   - Characters like `&`, `<`, and `>` in attributes or text nodes must be escaped (`&amp;`, `&lt;`, `&gt;`).
4. **Accessibility Built-in**:
   - Must include `<title>` and `<desc>` tags with descriptive, screen-reader friendly summaries.
5. **Theme Support**:
   - Must support light and dark modes via `:root` CSS custom variables and `@media (prefers-color-scheme: light)`.

### Step-by-Step Shape Creation:
1. Locate the appropriate generator under `library/generators/<category>.py` (e.g. `banners.py`, `terminals.py`, `architectures.py`).
2. Add your preset dictionary to `<CATEGORY>_PRESETS` with a unique, kebab-case `id`.
3. Re-render the batch:
   ```bash
   python3 -m library.catalog
   ```
4. Run the test suite:
   ```bash
   make test
   ```

---

## 🔀 Pull Request Process

1. Fork the repo and create your feature branch:
   ```bash
   git checkout -b feat/new-shape-name
   ```
2. Commit your changes with descriptive commit messages following the Conventional Commits specification:
   ```bash
   git commit -m "feat(banners): add quantum lorenz attractor shape [skip ci]"
   ```
3. Push to your fork and submit a Pull Request.
4. Ensure all unit tests pass in GitHub Actions.

---

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
