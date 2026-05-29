const STORAGE_KEY = "inroad_analysis_history";
const MAX_RUNS = 20;

function listAnalysisRuns() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function persistRuns(runs) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(runs));
}

function saveAnalysisRun(data, meta = {}) {
  const runs = listAnalysisRuns();
  const top = data.matched_opportunities?.[0];
  const entry = {
    id: crypto.randomUUID(),
    savedAt: new Date().toISOString(),
    candidateName: meta.candidateName || "Candidate",
    discoveryMode: data.summary?.discovery_mode || "unknown",
    matchedCount: data.summary?.top_opportunities_matched ?? data.matched_opportunities?.length ?? 0,
    avgFit: data.summary?.average_fit_score ?? null,
    topTitle: top?.title || "Analysis run",
    data,
  };
  runs.unshift(entry);
  if (runs.length > MAX_RUNS) runs.length = MAX_RUNS;
  persistRuns(runs);
  return entry.id;
}

function getAnalysisRun(id) {
  return listAnalysisRuns().find((r) => r.id === id) || null;
}

function deleteAnalysisRun(id) {
  persistRuns(listAnalysisRuns().filter((r) => r.id !== id));
}

function clearAnalysisHistory() {
  localStorage.removeItem(STORAGE_KEY);
}

function activateRun(entry) {
  if (!entry?.data) return;
  sessionStorage.setItem("inroad_last_analysis", JSON.stringify(entry.data));
  sessionStorage.setItem("inroad_active_run_id", entry.id);
}

window.InRoadHistory = {
  listAnalysisRuns,
  saveAnalysisRun,
  getAnalysisRun,
  deleteAnalysisRun,
  clearAnalysisHistory,
  activateRun,
};
