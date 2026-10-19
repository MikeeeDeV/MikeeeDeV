/**
 * VectorForge Interactive Showroom Gallery
 * Fast client-side search, category filter, 1-click clipboard copy, and modal inspector.
 */

let catalog = null;
let currentCategory = "all";
let searchQuery = "";

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
    const res = await fetch("../catalog.json");
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

  // 'All' tab
  const allBtn = document.createElement("button");
  allBtn.className = `tab-btn ${currentCategory === "all" ? "active" : ""}`;
  allBtn.innerHTML = `All Shapes <span class="tab-count">${catalog.total_shapes}</span>`;
  allBtn.addEventListener("click", () => {
    currentCategory = "all";
    updateActiveTab();
    renderGrid();
  });
  container.appendChild(allBtn);

  // Category tabs
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
    const svgRelPath = `../shapes/${item.category}/${item.id}.svg`;

    card.innerHTML = `
      <div class="card-preview-area">
        <img src="${svgRelPath}" alt="${item.title}" loading="lazy" />
      </div>
      <div class="card-details">
        <div class="card-header-line">
          <h2 class="card-title">${item.title}</h2>
          <span class="category-tag">${item.category}</span>
        </div>
        <div class="card-meta-line">
          ID: <code>${item.id}</code> • Theme: ${item.default_theme}
        </div>
        <div class="card-actions">
          <button class="action-btn primary" onclick="copyMarkdown('${item.id}')" title="Copy Markdown Embed">
            📋 Markdown
          </button>
          <button class="action-btn" onclick="copySVG('${svgRelPath}')" title="Copy Raw SVG">
            ⚡ SVG
          </button>
          <button class="action-btn" onclick="inspectShape('${item.id}')" title="Inspect Component">
            🔍 Inspect
          </button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

window.copyMarkdown = function (presetId) {
  const item = catalog.items.find((i) => i.id === presetId);
  if (!item) return;
  const embed = item.markdown_embed;
  navigator.clipboard.writeText(embed).then(() => {
    showToast(`Copied Markdown embed for ${item.title}!`);
  });
};

window.copySVG = async function (svgPath) {
  try {
    const res = await fetch(svgPath);
    const text = await res.text();
    await navigator.clipboard.writeText(text);
    showToast("Copied raw SVG code to clipboard!");
  } catch (e) {
    console.error("Failed to copy SVG:", e);
    showToast("Error loading SVG code");
  }
};

window.inspectShape = function (presetId) {
  const item = catalog.items.find((i) => i.id === presetId);
  const modal = document.getElementById("inspect-dialog");
  if (!item || !modal) return;

  const svgRelPath = `../shapes/${item.category}/${item.id}.svg`;
  document.getElementById("modal-title").textContent = item.title;
  document.getElementById("modal-meta").textContent = `Category: ${item.category} • Theme: ${item.default_theme} • Preset: ${item.id}`;
  document.getElementById("modal-img").src = svgRelPath;
  document.getElementById("modal-md-code").textContent = item.markdown_embed;

  modal.showModal();
};

function setupModal() {
  const modal = document.getElementById("inspect-dialog");
  const closeBtn = document.getElementById("modal-close");
  if (!modal || !closeBtn) return;

  closeBtn.addEventListener("click", () => modal.close());
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.close();
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
