document.addEventListener("DOMContentLoaded", async () => {
  if (!(await InRoadAuth.requireAuth())) return;
  // Allow dashboard to render even if analysis hasn't been run yet

  const data = InRoadStore.load() || {};
  const summary = data.summary || {};
  const opportunities = data.matched_opportunities || [];
  const profile = data.candidate_profile || {};

  const avgChemistry =
    summary.average_chemistry_score ??
    (opportunities.length
      ? opportunities.reduce((a, o) => a + (o.chemistry?.inroad_score || 0), 0) /
        opportunities.length
      : 0);

  const avgFit =
    summary.average_fit_score ??
    (opportunities.length
      ? opportunities.reduce((a, o) => a + (o.fit_score || 0), 0) /
        opportunities.length
      : 0);

  const welcome = document.querySelector("[data-inroad-welcome]");
  if (welcome) {
    const domain = profile.domain_expertise?.[0] || "your profile";
    welcome.textContent = `Welcome back. Your engine found ${opportunities.length} high-priority matches in ${domain}.`;
  }

  const inroadScoreEl = document.querySelector("[data-inroad-score-value]");
  const inroadTierEl = document.querySelector("[data-inroad-score-tier]");
  const inroadRing = document.querySelector("[data-inroad-score-ring]");
  if (inroadScoreEl) inroadScoreEl.textContent = formatScore(avgChemistry);
  if (inroadTierEl) inroadTierEl.textContent = scoreTier(avgChemistry);
  setProgressRing(inroadRing, avgChemistry);

  const fitScoreEl = document.querySelector("[data-fit-score-value]");
  const fitTierEl = document.querySelector("[data-fit-score-tier]");
  const fitRing = document.querySelector("[data-fit-score-ring]");
  if (fitScoreEl) fitScoreEl.textContent = formatScore(avgFit);
  if (fitTierEl) fitTierEl.textContent = scoreTier(avgFit);
  setProgressRing(fitRing, avgFit);

  const matchCountEl = document.querySelector("[data-match-count]");
  if (matchCountEl) matchCountEl.textContent = String(opportunities.length);

  const skillPctEl = document.querySelector("[data-skill-completion]");
  if (skillPctEl && profile.core_skills?.length) {
    const pct = Math.min(95, 60 + profile.core_skills.length * 4);
    skillPctEl.textContent = `${pct}%`;
  }

  const skillsContainer = document.querySelector("[data-skill-bars]");
  if (skillsContainer && profile.core_skills?.length) {
    skillsContainer.innerHTML = "";
    profile.core_skills.slice(0, 4).forEach((skill, i) => {
      const width = Math.max(25, 90 - i * 15);
      skillsContainer.insertAdjacentHTML(
        "beforeend",
        `<div class="p-sm glass-card bg-surface-container/20 rounded-lg space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-[20px]">verified</span>
              <span class="text-body-sm font-medium">${skill}</span>
            </div>
            <span class="text-on-surface-variant text-[11px] font-bold">Core skill</span>
          </div>
          <div class="w-full h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
            <div class="h-full bg-primary rounded-full" style="width: ${width}%"></div>
          </div>
        </div>`
      );
    });
  }

  const listEl = document.querySelector("[data-opportunities-list]");
  if (listEl) {
    listEl.innerHTML = "";
    opportunities.forEach((opp) => {
      const matchPct = formatScore(opp.fit_score);
      const row = document.createElement("div");
      row.className =
        "glass-card bg-surface/40 p-md rounded-lg flex items-center gap-md border border-outline-variant/10 hover:border-primary/30 transition-all group cursor-pointer";
      row.innerHTML = `
        <div class="w-14 h-14 bg-surface-container-highest rounded-lg flex items-center justify-center border border-outline-variant/20">
          <span class="material-symbols-outlined text-primary text-3xl">work</span>
        </div>
        <div class="flex-grow min-w-0">
          <h4 class="font-headline-md text-body-lg text-on-surface group-hover:text-primary transition-colors truncate">${opp.title}</h4>
          <p class="text-on-surface-variant text-body-sm truncate">${opp.company} • ${sourceLabel(opp.source_type)}</p>
        </div>
        <div class="text-right flex flex-col items-end gap-1 shrink-0">
          <span class="bg-primary/10 text-primary border border-primary/20 px-3 py-1 rounded-full text-[12px] font-bold">${matchPct}% Match</span>
          <span class="text-on-surface-variant/40 text-[10px] uppercase">InRoad ${formatScore(opp.chemistry?.inroad_score)}</span>
        </div>`;
      row.addEventListener("click", () => {
        InRoadStore.setSelectedOpportunityId(opp.opportunity_id);
        window.location.href = `/opportunity.html?id=${opp.opportunity_id}`;
      });
      listEl.appendChild(row);
    });
  }
});
