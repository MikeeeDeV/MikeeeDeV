# Accessibility Statement (ACCESSIBILITY.md)

**VectorForge & MikeeeDeV Profile Engine** is committed to ensuring digital accessibility for people of all abilities. We continually improve the user experience and apply relevant accessibility standards across all 235+ SVG components, documentation, and the interactive showroom gallery.

---

## ♿ Standards Compliance

Our vector assets and web interfaces strive to conform to:
- **W3C SVG 1.1 Specification (Accessibility Features)**
- **Web Content Accessibility Guidelines (WCAG) 2.1 Level AA**
- **Section 508 Standards**

---

## 🛠️ Accessibility Implementations

### 1. Embedded Semantics & Screen Reader Support
Every generated SVG document includes semantic markup:
- `role="img"` attribute on the root `<svg>` element.
- Accessible `<title>` tag with a human-readable title.
- Accessible `<desc>` tag describing the visual content, meaning, and context.
- `aria-labelledby="title-id desc-id"` linking titles and descriptions directly to assistive technologies.

### 2. High-Contrast Curated Palettes
All 10 color palettes (including Kemet Nocturne, Nord Frost, Amber CRT, Dracula, and Monokai Pro) are tested for luminance and contrast ratios:
- Text-to-background contrast ratio exceeds **4.5:1** for regular text and **3:1** for large text, adhering to WCAG 2.1 AA.
- Light mode tokens (`@media (prefers-color-scheme: light)`) ensure readable contrast in bright environments.

### 3. Font Scalability & Native Stacks
- We avoid hardcoded rasterized text.
- Text uses system font stacks (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `JetBrains Mono`, `Cairo`) that inherit operating system text scaling preferences.
- Arabic typography uses explicit `direction="rtl"` and `xml:lang="ar"` with safe padding bounds to prevent font glyph clipping in Blink and WebKit renderers.

### 4. Reduced Motion & Blinking Standards
- Subtle animations (such as the terminal cursor and status radar dots) use gentle frequency cycles (< 2 Hz) avoiding rapid flashing that could trigger seizures (WCAG 2.3.1).
- Keyframe animations respect user OS settings via CSS media queries.

---

## 🌐 Supported Environments

- Modern screen readers: VoiceOver (macOS / iOS), NVDA (Windows), JAWS (Windows), Orca (Linux).
- Modern web browsers: Google Chrome, Mozilla Firefox, Apple Safari, Microsoft Edge.
- Responsive scaling: Viewport scaling from 320px mobile up to 4K ultra-wide monitors.

---

## 📣 Feedback & Reporting Barriers

We welcome your feedback on the accessibility of VectorForge. If you encounter accessibility barriers, unreadable contrast, or clipped screen reader descriptors:

- **Email**: [mohamed.ayman.developer@gmail.com](mailto:mohamed.ayman.developer@gmail.com)
- **GitHub Issues**: Open an issue labeled `accessibility` via [GitHub Issues](https://github.com/MikeeeDeV/MikeeeDeV/issues)

We aim to respond to accessibility feedback within 3 business days.
