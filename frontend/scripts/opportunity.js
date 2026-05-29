function loadAnalysisPayload() {
  try {
    const raw = sessionStorage.getItem("inroad_last_analysis");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function initOpportunityPage() {
  const params = new URLSearchParams(window.location.search);
  const index = Number(params.get("i") || "0");
  const data = loadAnalysisPayload();
  const root = document.getElementById("opportunity-detail");
  const err = document.getElementById("opportunity-error");

  if (!data?.matched_opportunities?.length) {
    err.textContent = "No analysis in session. Run Analyze first.";
    err.classList.remove("hidden");
    return;
  }

  const opp = data.matched_opportunities[index];
  if (!opp) {
    err.textContent = "Opportunity not found.";
    err.classList.remove("hidden");
    return;
  }

  root.innerHTML = `
    <p class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Opportunity detail</p>
    ${renderOpportunityCard(opp, index + 1, { compact: false, forceOpen: true })}
  `;
  bindCopyButtons(root);
}

document.addEventListener("DOMContentLoaded", initOpportunityPage);
