function initLandingApiStatus() {
  const el = document.getElementById("landing-api-status");
  if (!el) return;

  fetch(`${window.INROAD_API_BASE}/`)
    .then((r) => r.json())
    .then((data) => {
      el.textContent = `API online — ${data.engine || "ready"}`;
      el.classList.add("text-primary-container");
    })
    .catch(() => {
      el.textContent = "API offline — start python main.py for live analyze";
      el.classList.add("text-on-surface-variant");
    });
}

document.addEventListener("DOMContentLoaded", initLandingApiStatus);
