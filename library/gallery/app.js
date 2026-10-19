/**
 * VectorForge Interactive Showroom Gallery
 * Fast client-side search, category filter, 1-click clipboard copy,
 * live 10-palette theme customizer, React JSX export, CDN links, and SVG downloader.
 */

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

let catalog = null;
let currentCategory = "all";
let searchQuery = "";
let svgCache = new Map();
let activeModalItem = null;
let activeModalTheme = null;
let activeModalTab = "md";

document.addEventListener("DOMContentLoaded", async () => {
  await loadCatalog();
  setupThemeToggle();
  setupSearch();
  renderCategoryTabs();
  renderGrid();
  setupModal();
});

async function loadCatalog() {
  const inlineEl = document.getElementById("catalog-data");
  if (inlineEl && inlineEl.textContent.trim()) {
    try {
      catalog = JSON.parse(inlineEl.textContent);
      return;
    } catch (e) {
      console.warn("Could not parse inline catalog data, attempting fetch...", e);
    }
  }

  try {
    const isDirectGallery = window.location.protocol === "file:" || window.location.pathname.includes("/library/gallery");
    const fetchPath = isDirectGallery ? "../catalog.json" : "catalog.json";
    const res = await fetch(fetchPath);
    catalog = await res.json();
  } catch (err) {
    console.error("Failed to fetch catalog.json:", err);
    catalog = { total_shapes: 0, categories: {}, items: [] };
  }
}

function setupThemeToggle() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;

  const currentTheme = localStorage.getItem("vf-theme") || "dark";
  document.documentElement.setAttribute("data-theme", currentTheme);
  btn.textContent = currentTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";

  btn.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    const nextTheme = isDark ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    localStorage.setItem("vf-theme", nextTheme);
    btn.textContent = nextTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
  });
}

function setupSearch() {
  const input = document.getElementById("search-input");
  if (!input) return;
  input.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderGrid();
  });
}

function renderCategoryTabs() {
  const container = document.getElementById("category-tabs");
  if (!container || !catalog) return;

  container.innerHTML = "";

  const allBtn = document.createElement("button");
  allBtn.className = `tab-btn ${currentCategory === "all" ? "active" : ""}`;
  allBtn.innerHTML = `All Shapes <span class="tab-count">${catalog.total_shapes}</span>`;
  allBtn.addEventListener("click", () => {
    currentCategory = "all";
    updateActiveTab();
    renderGrid();
  });
  container.appendChild(allBtn);

  for (const [catId, catInfo] of Object.entries(catalog.categories)) {
    const btn = document.createElement("button");
    btn.className = `tab-btn ${currentCategory === catId ? "active" : ""}`;
    btn.dataset.category = catId;
    btn.innerHTML = `${catInfo.name} <span class="tab-count">${catInfo.count}</span>`;
    btn.addEventListener("click", () => {
      currentCategory = catId;
      updateActiveTab();
      renderGrid();
    });
    container.appendChild(btn);
  }
}

function updateActiveTab() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    if (currentCategory === "all" && !btn.dataset.category) {
      btn.classList.add("active");
    } else if (btn.dataset.category === currentCategory) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

function getShapePath(category, id) {
  const isDirectGallery = window.location.protocol === "file:" || window.location.pathname.includes("/library/gallery");
  const base = isDirectGallery ? "../shapes/" : "./shapes/";
  return `${base}${category}/${id}.svg`;
}

async function fetchSVGText(svgPath) {
  if (svgCache.has(svgPath)) {
    return svgCache.get(svgPath);
  }
  try {
    const res = await fetch(svgPath);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    svgCache.set(svgPath, text);
    return text;
  } catch (e) {
    console.error("Failed to fetch SVG text:", e);
    return null;
  }
}

function applyThemeToSVG(svgText, themeId) {
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

function convertSVGToJSX(svgText, presetId) {
  if (!svgText) return "// Error loading SVG source";

  const pascalName = presetId
    .split(/[-_]/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join("") + "Shape";

  let cleanSvg = svgText
    .replace(/<\?xml[^>]*\?>/gi, "")
    .replace(/<!DOCTYPE[^>]*>/gi, "")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/\bclass=/g, "className=")
    .replace(/\bxmlns:xlink=/g, "xmlnsXlink=")
    .replace(/\bxml:space=/g, "xmlSpace=")
    .replace(/\bxml:lang=/g, "xmlLang=")
    .replace(/\bstop-color=/g, "stopColor=")
    .replace(/\bstop-opacity=/g, "stopOpacity=")
    .replace(/\bstroke-width=/g, "strokeWidth=")
    .replace(/\bstroke-linecap=/g, "strokeLinecap=")
    .replace(/\bstroke-linejoin=/g, "strokeLinejoin=")
    .replace(/\bstroke-dasharray=/g, "strokeDasharray=")
    .replace(/\bstroke-dashoffset=/g, "strokeDashoffset=")
    .replace(/\bstroke-opacity=/g, "strokeOpacity=")
    .replace(/\bfill-opacity=/g, "fillOpacity=")
    .replace(/\bfill-rule=/g, "fillRule=")
    .replace(/\bclip-rule=/g, "clipRule=")
    .replace(/\bclip-path=/g, "clipPath=")
    .replace(/\btext-anchor=/g, "textAnchor=")
    .replace(/\bdominant-baseline=/g, "dominantBaseline=")
    .replace(/\bletter-spacing=/g, "letterSpacing=")
    .replace(/\bfont-family=/g, "fontFamily=")
    .replace(/\bfont-size=/g, "fontSize=")
    .replace(/\bfont-weight=/g, "fontWeight=")
    .trim();

  return `import React from 'react';

/**
 * ${pascalName} - Generated via VectorForge Shape Studio
 * Zero-runtime-dependency deterministic developer SVG component.
 */
export function ${pascalName}(props) {
  return (
    ${cleanSvg.split('\n').join('\n    ')}
  );
}

export default ${pascalName};`;
}

function renderGrid() {
  const grid = document.getElementById("shapes-grid");
  const countEl = document.getElementById("visible-count");
  if (!grid || !catalog) return;

  grid.innerHTML = "";

  const filtered = catalog.items.filter((item) => {
    const matchesCat = currentCategory === "all" || item.category === currentCategory;
    const matchesQuery =
      !searchQuery ||
      item.id.toLowerCase().includes(searchQuery) ||
      item.title.toLowerCase().includes(searchQuery) ||
      item.default_theme.toLowerCase().includes(searchQuery);
    return matchesCat && matchesQuery;
  });

  if (countEl) {
    countEl.textContent = `Showing ${filtered.length} of ${catalog.total_shapes} components`;
  }

  if (filtered.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
      No developer shapes found matching "${searchQuery}".
    </div>`;
    return;
  }

  filtered.forEach((item) => {
    const card = document.createElement("article");
    card.className = "shape-card";
    card.id = `card-${item.id}`;
    const svgRelPath = getShapePath(item.category, item.id);

    const themeOptions = Object.entries(PALETTES)
      .map(([id, p]) => `<option value="${id}" ${id === item.default_theme ? "selected" : ""}>${p.name}</option>`)
      .join("");

    card.innerHTML = `
      <div class="card-preview-area">
        <img id="img-${item.id}" src="${svgRelPath}" alt="${item.title}" loading="lazy" />
      </div>
      <div class="card-details">
        <div class="card-header-line">
          <h2 class="card-title">${item.title}</h2>
          <span class="category-tag">${item.category}</span>
        </div>
        <div class="card-meta-line">
          ID: <code>${item.id}</code>
        </div>
        <div class="card-actions-grid">
          <button class="action-btn primary" onclick="copyMarkdown('${item.id}')" title="Copy Markdown Embed">
            📋 MD
          </button>
          <button class="action-btn" onclick="copySVG('${item.id}', '${item.category}')" title="Copy Raw SVG">
            ⚡ SVG
          </button>
          <button class="action-btn accent" onclick="copyJSX('${item.id}', '${item.category}')" title="Copy React JSX">
            ⚛️ JSX
          </button>
          <button class="action-btn" onclick="copyCDN('${item.id}', '${item.category}')" title="Copy jsDelivr CDN URL">
            🔗 CDN
          </button>
        </div>
        <div class="card-theme-row">
          <select class="theme-select" id="select-${item.id}" onchange="changeCardTheme('${item.id}', '${item.category}', this.value)" title="Switch Palette Theme">
            ${themeOptions}
          </select>
          <button class="action-btn icon-only" onclick="downloadShape('${item.id}', '${item.category}')" title="Download SVG">
            📥
          </button>
          <button class="action-btn icon-only" onclick="inspectShape('${item.id}')" title="Inspect Component">
            🔍
          </button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

window.changeCardTheme = async function (presetId, category, newTheme) {
  const imgEl = document.getElementById(`img-${presetId}`);
  if (!imgEl) return;

  const svgRelPath = getShapePath(category, presetId);
  const rawText = await fetchSVGText(svgRelPath);
  if (!rawText) return;

  const themedText = applyThemeToSVG(rawText, newTheme);
  const blob = new Blob([themedText], { type: "image/svg+xml;charset=utf-8" });
  imgEl.src = URL.createObjectURL(blob);
  showToast(`Applied ${PALETTES[newTheme]?.name || newTheme} to ${presetId}!`);
};

window.copyMarkdown = function (presetId) {
  const item = catalog.items.find((i) => i.id === presetId);
  if (!item) return;
  const embed = item.markdown_embed;
  navigator.clipboard.writeText(embed).then(() => {
    showToast(`Copied Markdown embed for ${item.title}!`);
  });
};

window.copySVG = async function (presetId, category) {
  const selectEl = document.getElementById(`select-${presetId}`);
  const currentTheme = selectEl ? selectEl.value : null;

  const svgRelPath = getShapePath(category, presetId);
  let text = await fetchSVGText(svgRelPath);
  if (!text) {
    showToast("Error loading SVG code");
    return;
  }

  if (currentTheme) {
    text = applyThemeToSVG(text, currentTheme);
  }

  await navigator.clipboard.writeText(text);
  showToast("Copied raw SVG code to clipboard!");
};

window.copyJSX = async function (presetId, category) {
  const selectEl = document.getElementById(`select-${presetId}`);
  const currentTheme = selectEl ? selectEl.value : null;

  const svgRelPath = getShapePath(category, presetId);
  let text = await fetchSVGText(svgRelPath);
  if (!text) {
    showToast("Error loading SVG source");
    return;
  }

  if (currentTheme) {
    text = applyThemeToSVG(text, currentTheme);
  }

  const jsxCode = convertSVGToJSX(text, presetId);
  await navigator.clipboard.writeText(jsxCode);
  showToast(`Copied React JSX Component for ${presetId}!`);
};

window.copyCDN = function (presetId, category) {
  const cdnUrl = `https://cdn.jsdelivr.net/gh/MikeeeDeV/MikeeeDeV@v1/library/shapes/${category}/${presetId}.svg`;
  navigator.clipboard.writeText(cdnUrl).then(() => {
    showToast("Copied jsDelivr CDN URL!");
  });
};

window.downloadShape = async function (presetId, category) {
  const selectEl = document.getElementById(`select-${presetId}`);
  const currentTheme = selectEl ? selectEl.value : "kemet_nocturne";

  const svgRelPath = getShapePath(category, presetId);
  let text = await fetchSVGText(svgRelPath);
  if (!text) {
    showToast("Error downloading SVG");
    return;
  }

  text = applyThemeToSVG(text, currentTheme);
  const blob = new Blob([text], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${presetId}-${currentTheme}.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast(`Downloaded ${presetId}-${currentTheme}.svg!`);
};

window.inspectShape = async function (presetId) {
  const item = catalog.items.find((i) => i.id === presetId);
  const modal = document.getElementById("inspect-dialog");
  if (!item || !modal) return;

  activeModalItem = item;
  activeModalTheme = item.default_theme;
  activeModalTab = "md";

  document.getElementById("modal-title").textContent = item.title;
  document.getElementById("modal-meta").textContent = `Category: ${item.category} • ID: ${item.id}`;

  const select = document.getElementById("modal-theme-select");
  select.innerHTML = Object.entries(PALETTES)
    .map(([id, p]) => `<option value="${id}" ${id === activeModalTheme ? "selected" : ""}>${p.name}</option>`)
    .join("");

  await updateModalPreviewAndCode();
  modal.showModal();
};

async function updateModalPreviewAndCode() {
  if (!activeModalItem) return;

  const svgRelPath = getShapePath(activeModalItem.category, activeModalItem.id);
  const rawText = await fetchSVGText(svgRelPath);
  const themedText = applyThemeToSVG(rawText, activeModalTheme);

  const modalImg = document.getElementById("modal-img");
  const blob = new Blob([themedText], { type: "image/svg+xml;charset=utf-8" });
  modalImg.src = URL.createObjectURL(blob);

  const displayEl = document.getElementById("modal-code-display");
  if (!displayEl) return;

  if (activeModalTab === "md") {
    displayEl.textContent = activeModalItem.markdown_embed;
  } else if (activeModalTab === "jsx") {
    displayEl.textContent = convertSVGToJSX(themedText, activeModalItem.id);
  } else if (activeModalTab === "svg") {
    displayEl.textContent = themedText;
  } else if (activeModalTab === "cdn") {
    displayEl.textContent = `https://cdn.jsdelivr.net/gh/MikeeeDeV/MikeeeDeV@v1/library/shapes/${activeModalItem.category}/${activeModalItem.id}.svg`;
  }
}

function setupModal() {
  const modal = document.getElementById("inspect-dialog");
  const closeBtn = document.getElementById("modal-close");
  const themeSelect = document.getElementById("modal-theme-select");
  const downloadBtn = document.getElementById("modal-btn-download");
  const copyBtn = document.getElementById("modal-copy-btn");
  const tabBtns = document.querySelectorAll(".modal-tab-btn");

  if (!modal) return;

  if (closeBtn) closeBtn.addEventListener("click", () => modal.close());
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.close();
  });

  if (themeSelect) {
    themeSelect.addEventListener("change", async (e) => {
      activeModalTheme = e.target.value;
      await updateModalPreviewAndCode();
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {
      if (activeModalItem) {
        downloadShape(activeModalItem.id, activeModalItem.category);
      }
    });
  }

  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const displayEl = document.getElementById("modal-code-display");
      if (displayEl && displayEl.textContent) {
        navigator.clipboard.writeText(displayEl.textContent).then(() => {
          showToast(`Copied ${activeModalTab.toUpperCase()} to clipboard!`);
        });
      }
    });
  }

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", async () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeModalTab = btn.dataset.tab;
      await updateModalPreviewAndCode();
    });
  });
}

function showToast(msg) {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2500);
}
