import { bindCopyButtons, renderOpportunityCard, renderTags } from "./results-render.js";

const PIPELINE_STEPS = [
  "Agent 1: Discovering opportunities…",
  "Agent 2: Matching your profile…",
  "Agent 3: InRoad chemistry…",
  "Agent 4: Building skill proof…",
  "Agent 5: Generating outreach…",
];

let stepTimer;

function setLoadingStep(index) {
  const el = document.getElementById("loading-step");
  if (el) el.textContent = PIPELINE_STEPS[index] || PIPELINE_STEPS[PIPELINE_STEPS.length - 1];
}

function startLoadingAnimation() {
  let i = 0;
  setLoadingStep(0);
  stepTimer = window.setInterval(() => {
    i = Math.min(i + 1, PIPELINE_STEPS.length - 1);
    setLoadingStep(i);
  }, 8000);
}

function stopLoadingAnimation() {
  if (stepTimer) window.clearInterval(stepTimer);
  stepTimer = null;
}

function displayResults(data, options = {}) {
  const root = document.getElementById("analyze-results");
  root.innerHTML = renderResults(data, options);
  bindCopyButtons(root);
  document.getElementById("analyze-results-section").classList.remove("hidden");
}

function renderResults(data, options = {}) {
  const profile = data.candidate_profile;
  const summary = data.summary;
  const discoveryLabel =
    summary.discovery_mode === "live"
      ? "Live discovery — real sources"
      : summary.discovery_mode || "unknown";

  const savedBanner = options.savedRunId
    ? `<p class="mb-md rounded-lg border border-primary-container/30 bg-primary-container/10 px-sm py-xs font-body-sm text-body-sm text-on-surface">
        Saved to <a href="history.html" class="font-bold text-primary-container hover:underline">History</a> on this device.
      </p>`
    : options.restored
      ? `<p class="mb-md font-body-sm text-body-sm text-on-surface-variant">Showing a saved run from History.</p>`
      : "";

  return `
    ${savedBanner}
    <p class="mb-md font-body-sm text-body-sm text-primary-container">${discoveryLabel}</p>
    <div class="mb-lg grid grid-cols-2 gap-sm md:grid-cols-4">
      ${[
        ["Evaluated", summary.total_opportunities_evaluated],
        ["Matched", summary.top_opportunities_matched],
        ["Avg fit", `${summary.average_fit_score}%`],
        ["Best InRoad", `${summary.highest_chemistry_score}%`],
      ]
        .map(
          ([label, val]) => `
        <div class="glass-card rounded-xl p-sm text-center">
          <p class="font-data-sm text-data-sm text-on-surface-variant">${label}</p>
          <p class="font-data-lg text-data-lg text-primary-container">${val}</p>
        </div>`
        )
        .join("")}
    </div>

    <section class="glass-card mb-xl rounded-xl p-lg">
      <h2 class="mb-md font-headline-md text-headline-md text-on-surface">Agent 2 — Your skill profile</h2>
      <p class="mb-md font-body-md text-body-md text-on-surface-variant">${profile.semantic_summary}</p>
      <div class="grid gap-md md:grid-cols-2">
        <div>
          <h3 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Core skills</h3>
          <div class="flex flex-wrap gap-xs">${renderTags(profile.core_skills)}</div>
        </div>
        <div>
          <h3 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Domain</h3>
          <div class="flex flex-wrap gap-xs">${renderTags(profile.domain_expertise)}</div>
        </div>
      </div>
    </section>

    <h2 class="mb-md font-headline-lg text-headline-lg text-on-surface">Top matched opportunities</h2>
    <div id="opportunity-list" class="space-y-md">
      ${data.matched_opportunities.map((o, i) => renderOpportunityCard(o, i + 1, { compact: true })).join("")}
    </div>`;
}

function setLoading(isLoading) {
  document.getElementById("analyze-loading").classList.toggle("hidden", !isLoading);
  document.getElementById("analyze-submit").disabled = isLoading;
  if (isLoading) startLoadingAnimation();
  else stopLoadingAnimation();
}

function showError(message) {
  const el = document.getElementById("analyze-error");
  el.textContent = message;
  el.classList.remove("hidden");
}

function hideError() {
  document.getElementById("analyze-error").classList.add("hidden");
}

async function runAnalysis() {
  hideError();
  const resume = document.getElementById("resume_text").value.trim();
  const projects = document.getElementById("project_descriptions").value.trim();
  const candidateName = document.getElementById("candidate_name").value.trim() || "Candidate";

  if (resume.length < 10 || projects.length < 10) {
    showError("Resume and projects must each be at least 10 characters.");
    return;
  }

  setLoading(true);
  const controller = new AbortController();
  const timeoutMs = 120000;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(`${window.INROAD_API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        resume_text: resume,
        project_descriptions: projects,
        candidate_name: candidateName,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Analysis failed");

    sessionStorage.setItem("inroad_last_analysis", JSON.stringify(data));

    let savedRunId = null;
    if (window.InRoadHistory) {
      savedRunId = window.InRoadHistory.saveAnalysisRun(data, { candidateName });
      window.InRoadHistory.activateRun({ id: savedRunId, data });
    }

    displayResults(data, { savedRunId });
    document.getElementById("analyze-results-section").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    if (err.name === "AbortError") {
      showError("Analysis timed out after 2 minutes. Check the API terminal or try again.");
    } else if (err.message.includes("fetch") || err.message.includes("Failed to fetch")) {
      showError("Cannot reach API. Start backend: python main.py");
    } else {
      showError(typeof err.message === "string" ? err.message : "Analysis failed");
    }
  } finally {
    window.clearTimeout(timeoutId);
    setLoading(false);
  }
}

function tryRestoreResults() {
  const params = new URLSearchParams(window.location.search);
  const runId = params.get("run");

  if (runId && window.InRoadHistory) {
    const entry = window.InRoadHistory.getAnalysisRun(runId);
    if (entry?.data) {
      window.InRoadHistory.activateRun(entry);
      if (entry.candidateName) {
        const nameEl = document.getElementById("candidate_name");
        if (nameEl) nameEl.value = entry.candidateName;
      }
      displayResults(entry.data, { restored: true });
      return true;
    }
  }

  try {
    const raw = sessionStorage.getItem("inroad_last_analysis");
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (!data?.matched_opportunities?.length) return false;
    displayResults(data, { restored: true });
    return true;
  } catch {
    return false;
  }
}

function initAnalyzePage() {
  document.getElementById("analyze-form").addEventListener("submit", (e) => {
    e.preventDefault();
    runAnalysis();
  });

  tryRestoreResults();

  fetch(`${window.INROAD_API_BASE}/`)
    .then((r) => r.json())
    .then(() => {
      document.getElementById("api-status").textContent = "API connected — live pipeline ready";
      document.getElementById("api-status").classList.add("text-primary-container");
    })
    .catch(() => {
      document.getElementById("api-status").textContent = "API offline — run: python main.py";
      document.getElementById("api-status").classList.add("text-error");
    });
}

document.addEventListener("DOMContentLoaded", initAnalyzePage);
