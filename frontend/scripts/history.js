function formatRunDate(iso) {
  try {
    return new Date(iso).toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
}

function formatTitle(title) {
  if (!title) return "Analysis run";
  const t = title.trim();
  return t.length > 72 ? `${t.slice(0, 69)}…` : t;
}

function renderHistoryList() {
  const runs = window.InRoadHistory.listAnalysisRuns();
  const list = document.getElementById("history-list");
  const empty = document.getElementById("history-empty");
  const count = document.getElementById("history-count");
  const clearBtn = document.getElementById("history-clear-all");

  count.textContent =
    runs.length === 0
      ? "0 saved runs"
      : `${runs.length} saved run${runs.length === 1 ? "" : "s"} (max 20)`;

  clearBtn.classList.toggle("hidden", runs.length === 0);
  empty.classList.toggle("hidden", runs.length > 0);
  list.classList.toggle("hidden", runs.length === 0);

  if (!runs.length) {
    list.innerHTML = "";
    return;
  }

  list.innerHTML = runs
    .map(
      (run) => `
    <article class="glass-card rounded-xl p-lg" data-run-id="${run.id}">
      <div class="flex flex-col gap-md sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="font-data-sm text-data-sm text-primary-container">${formatRunDate(run.savedAt)}</p>
          <h2 class="font-headline-md text-headline-md text-on-surface">${run.candidateName}</h2>
          <p class="font-body-sm text-body-sm text-on-surface-variant">${formatTitle(run.topTitle)}</p>
          <p class="mt-xs font-data-sm text-data-sm text-on-surface-variant">
            ${run.matchedCount} matched · ${run.discoveryMode} discovery
            ${run.avgFit != null ? ` · avg fit ${Math.round(run.avgFit)}%` : ""}
          </p>
        </div>
        <div class="flex shrink-0 flex-wrap gap-sm">
          <a
            href="analyze.html?run=${encodeURIComponent(run.id)}"
            class="rounded-full bg-primary-container px-md py-xs font-bold text-on-primary-container"
            data-action="view"
          >
            View results
          </a>
          <button
            type="button"
            class="rounded-full border border-outline-variant px-md py-xs font-data-sm text-data-sm text-on-surface-variant hover:border-error hover:text-error"
            data-action="delete"
            data-id="${run.id}"
          >
            Delete
          </button>
        </div>
      </div>
    </article>`
    )
    .join("");
}

function initHistoryPage() {
  renderHistoryList();

  document.getElementById("history-clear-all")?.addEventListener("click", () => {
    if (!window.confirm("Delete all saved runs on this device?")) return;
    window.InRoadHistory.clearAnalysisHistory();
    sessionStorage.removeItem("inroad_last_analysis");
    sessionStorage.removeItem("inroad_active_run_id");
    renderHistoryList();
  });

  document.getElementById("history-list")?.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action='delete']");
    if (!btn) return;
    const id = btn.getAttribute("data-id");
    if (!id) return;
    window.InRoadHistory.deleteAnalysisRun(id);
    if (sessionStorage.getItem("inroad_active_run_id") === id) {
      sessionStorage.removeItem("inroad_last_analysis");
      sessionStorage.removeItem("inroad_active_run_id");
    }
    renderHistoryList();
  });
}

document.addEventListener("DOMContentLoaded", initHistoryPage);
