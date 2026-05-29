import { bindCopyButtons, renderOpportunityCard } from "./results-render.js";

function loadAnalysisPayload() {
  const params = new URLSearchParams(window.location.search);
  const runId = params.get("run");

  if (runId && window.InRoadHistory) {
    const entry = window.InRoadHistory.getAnalysisRun(runId);
    if (entry?.data) {
      window.InRoadHistory.activateRun(entry);
      return entry.data;
    }
  }

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
    err.innerHTML =
      'No analysis in session. <a href="analyze.html" class="text-primary-container underline">Run Analyze</a> or open a run from <a href="history.html" class="text-primary-container underline">History</a>.';
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
