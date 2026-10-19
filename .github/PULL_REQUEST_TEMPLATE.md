### Description
<!-- Describe your changes and reference any related issues with "Closes #..." -->

### Type of Change
- [ ] New VectorForge SVG Shape / Preset
- [ ] New Color Palette / Design Token
- [ ] Bug Fix (Rendering, XML escaping, RTL clipping)
- [ ] Documentation Update
- [ ] CI/CD or Tooling Improvement

### Quality Checklist
- [ ] **XML Validity**: SVG parsed cleanly using `xml.etree.ElementTree` without syntax errors.
- [ ] **File Size Budget**: File size is strictly under `100 KB`.
- [ ] **Accessibility**: `<title>` and `<desc>` accessibility tags are present and descriptive.
- [ ] **Theme Support**: Colors are mapped through CSS custom variables with `prefers-color-scheme` support.
- [ ] **Zero Runtime Dependencies**: No remote scripts, external font downloads, or dynamic tracking.
- [ ] **Automated Tests**: All unit tests pass (`make test`).
