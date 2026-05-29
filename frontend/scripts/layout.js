const NAV_LINKS = [
  { id: "home", label: "Home", href: "index.html" },
  { id: "analyze", label: "Analyze", href: "analyze.html" },
  { id: "history", label: "History", href: "history.html" },
  { id: "agents", label: "Agents", href: "agents.html" },
];

function navLinkClass(active, href) {
  const isActive = active;
  return isActive
    ? "border-b-2 border-primary-container pb-1 font-body-md text-body-md font-bold text-primary-container"
    : "font-body-md text-body-md text-on-surface-variant transition-colors hover:text-primary-container";
}

function renderSiteNav(activePage) {
  const links = NAV_LINKS.map(
    (link) =>
      `<a class="${navLinkClass(link.id === activePage, link.href)}" href="${link.href}">${link.label}</a>`
  ).join("");

  return `
    <nav id="site-nav" aria-label="Main navigation"
      class="fixed top-0 z-50 flex h-20 w-full items-center border-b border-outline-variant bg-background/85 shadow-[0_4px_32px_rgba(0,0,0,0.25)] backdrop-blur-xl transition-colors duration-300">
      <div class="mx-auto flex w-full max-w-[1440px] items-center justify-between px-margin-mobile md:px-margin-desktop">
        <div class="flex items-center gap-md">
          <a href="index.html" class="font-display-lg text-display-lg font-bold tracking-tighter text-primary-container">InRoad</a>
          <div class="ml-lg hidden gap-sm md:flex">${links}</div>
        </div>
        <div class="flex items-center gap-sm">
          <button type="button" id="mobile-nav-toggle"
            class="flex h-10 w-10 items-center justify-center rounded-lg text-on-surface-variant hover:bg-primary-container/15 md:hidden"
            aria-expanded="false" aria-controls="mobile-nav-panel" aria-label="Open menu">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <a href="analyze.html"
            class="scale-105 rounded-full bg-primary-container px-lg py-xs font-bold text-on-primary-container transition-transform active:scale-95">
            Analyze Profile
          </a>
        </div>
      </div>
      <div id="mobile-nav-panel"
        class="absolute left-0 right-0 top-20 hidden border-b border-outline-variant bg-surface-container px-margin-mobile py-md backdrop-blur-xl md:hidden">
        <div class="flex flex-col gap-sm">${NAV_LINKS.map(
          (l) =>
            `<a class="font-body-md text-body-md ${l.id === activePage ? "font-bold text-primary-container" : "text-on-surface-variant"}" href="${l.href}">${l.label}</a>`
        ).join("")}</div>
      </div>
    </nav>`;
}

function renderSiteFooter() {
  return `
    <footer class="border-t border-outline-variant bg-surface-container-lowest py-xl">
      <div class="mx-auto flex w-full max-w-[1440px] flex-col items-center justify-between gap-md px-margin-mobile md:flex-row md:px-margin-desktop">
        <div class="flex flex-col items-center md:items-start">
          <span class="mb-2 font-display-lg text-display-lg text-primary-container">InRoad</span>
          <p class="max-w-xs text-center font-data-sm text-data-sm text-on-surface-variant md:text-left">
            Discover the opportunity. Find your way in. Prove you belong.
          </p>
        </div>
        <div class="flex gap-lg">
          <div class="flex flex-col gap-xs">
            <span class="mb-2 font-data-sm text-data-sm text-primary-container">Product</span>
            <a class="font-data-sm text-data-sm text-on-surface-variant hover:text-primary-container" href="analyze.html">Analyze</a>
            <a class="font-data-sm text-data-sm text-on-surface-variant hover:text-primary-container" href="history.html">History</a>
            <a class="font-data-sm text-data-sm text-on-surface-variant hover:text-primary-container" href="agents.html">Agents</a>
          </div>
          <div class="flex flex-col gap-xs">
            <span class="mb-2 font-data-sm text-data-sm text-primary-container">Systems</span>
            <a class="font-data-sm text-data-sm text-on-surface-variant hover:text-primary-container" href="${window.INROAD_API_BASE}/docs" target="_blank" rel="noopener noreferrer">API Docs</a>
          </div>
        </div>
      </div>
    </footer>`;
}

function initSharedLayout(activePage) {
  const headerSlot = document.getElementById("site-header");
  const footerSlot = document.getElementById("site-footer");
  if (headerSlot) headerSlot.innerHTML = renderSiteNav(activePage);
  if (footerSlot) footerSlot.innerHTML = renderSiteFooter();
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;
  if (page) initSharedLayout(page);
});
