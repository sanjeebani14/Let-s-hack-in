document.addEventListener("DOMContentLoaded", async () => {
  if (!(await InRoadAuth.requireAuth())) return;
  if (!requireAnalysis()) return;

  const params = new URLSearchParams(window.location.search);
  const id = params.get("id") || InRoadStore.getSelectedOpportunityId();
  const opp = InRoadStore.getOpportunity(id) || InRoadStore.getSelectedOpportunity();
  if (!opp) {
    window.location.href = "/dashboard.html";
    return;
  }
  InRoadStore.setSelectedOpportunityId(opp.opportunity_id);

  const chem = opp.chemistry || {};
  const scores = opp.scores || {};

  const setText = (sel, text) => {
    const el = document.querySelector(sel);
    if (el) el.textContent = text;
  };

  setText("[data-opp-company]", opp.company?.toUpperCase() || "");
  setText("[data-opp-title]", opp.title || "");
  setText("[data-opp-match]", `${formatScore(opp.fit_score)}%`);
  setText("[data-opp-inroad]", formatScore(chem.inroad_score));
  setText("[data-opp-reasoning]", opp.match_reasoning || "");
  setText("[data-opp-way-in]", chem.way_in_strategy || "");
  setText("[data-opp-connector]", chem.best_connector_name || "—");
  setText("[data-opp-connector-intro]", chem.best_connector_intro || "");
  setText("[data-opp-contexts]", chem.shared_contexts_summary || "");
  setText("[data-opp-team-fit]", chem.team_fit_category || "");
  setText(
    "[data-opp-score-reasoning]",
    scores.score_reasoning || chem.structural_explanation || ""
  );

  const mission = document.querySelector("[data-opp-mission]");
  if (mission) {
    mission.innerHTML = `<p class="font-body-lg text-body-lg text-on-surface">${opp.match_reasoning}</p>
      <p class="font-body-md text-body-md mt-sm text-on-surface-variant">${chem.structural_explanation || ""}</p>`;
  }

  const impactBar = document.querySelector("[data-opp-impact-bar]");
  if (impactBar) impactBar.style.width = `${Math.min(100, opp.fit_score)}%`;
  setText("[data-opp-impact-label]", `${formatScore(opp.fit_score)}% FIT`);

  const outreachBtn = document.querySelector("[data-inroad-outreach-btn]");
  if (outreachBtn) {
    outreachBtn.addEventListener("click", () => {
      window.location.href = `/outreach.html?id=${opp.opportunity_id}`;
    });
  }

  const matchRing = document.querySelector(".career-match-ring");
  if (matchRing && opp.fit_score) {
    const circumference = 282.7;
    const offset = circumference * (1 - Math.min(opp.fit_score, 100) / 100);
    matchRing.style.strokeDashoffset = String(offset);
  }
});
