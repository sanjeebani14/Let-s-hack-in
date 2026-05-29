function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function setupGlassCardTracking() {
  if (prefersReducedMotion()) return;

  document.querySelectorAll(".glass-card").forEach((card) => {
    card.addEventListener("mousemove", (event) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty("--mouse-x", `${event.clientX - rect.left}px`);
      card.style.setProperty("--mouse-y", `${event.clientY - rect.top}px`);
    });
  });
}

function createParticleNode() {
  const dot = document.createElement("div");
  dot.className = "fx-particle";
  dot.setAttribute("aria-hidden", "true");
  const size = Math.random() * 300 + 100;
  dot.style.width = `${size}px`;
  dot.style.height = `${size}px`;
  dot.style.left = `${Math.random() * 100}%`;
  dot.style.top = `${Math.random() * 100}%`;
  return dot;
}

function renderBackgroundParticles(count = 12) {
  const particleRoot = document.getElementById("particle-root");
  if (!particleRoot || prefersReducedMotion()) return;

  const reducedCount = window.innerWidth < 768 ? Math.floor(count / 2) : count;
  for (let i = 0; i < reducedCount; i += 1) {
    particleRoot.appendChild(createParticleNode());
  }
}

function setupNavScrollState() {
  const nav = document.getElementById("site-nav");
  if (!nav) return;

  const onScroll = () => {
    nav.classList.toggle("nav-scrolled", window.scrollY > 8);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

function setupMobileNav() {
  const toggle = document.getElementById("mobile-nav-toggle");
  const panel = document.getElementById("mobile-nav-panel");
  if (!toggle || !panel) return;

  const close = () => {
    panel.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    toggle.querySelector(".material-symbols-outlined").textContent = "menu";
    document.body.classList.remove("mobile-nav-open");
  };

  const open = () => {
    panel.classList.remove("hidden");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Close menu");
    toggle.querySelector(".material-symbols-outlined").textContent = "close";
    document.body.classList.add("mobile-nav-open");
  };

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    if (isOpen) close();
    else open();
  });

  panel.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", close);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") close();
  });
}

function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const id = anchor.getAttribute("href");
      if (!id || id === "#") return;

      const target = document.querySelector(id);
      if (!target) return;

      event.preventDefault();
      target.scrollIntoView({
        behavior: prefersReducedMotion() ? "auto" : "smooth",
        block: "start",
      });
    });
  });
}

function initLandingPage() {
  setupGlassCardTracking();
  renderBackgroundParticles();
  setupNavScrollState();
  setupMobileNav();
  setupSmoothScroll();
}

document.addEventListener("DOMContentLoaded", initLandingPage);
