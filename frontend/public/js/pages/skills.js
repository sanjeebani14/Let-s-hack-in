document.addEventListener("DOMContentLoaded", async () => {
  if (!(await InRoadAuth.requireAuth())) return;
  if (!requireAnalysis()) return;

  const data = InRoadStore.load();
  const profile = data.candidate_profile || {};

  const skillsEl = document.querySelector("[data-proof-cards]");
  const graphEl = document.querySelector("[data-skill-graph-nodes]");

  if (skillsEl) {
    const items = [
      ...(profile.core_skills || []).map((s) => ({
        title: s,
        type: "Core skill",
        evidence: profile.semantic_summary,
      })),
      ...(profile.ownership_signals || []).slice(0, 3).map((s) => ({
        title: "Ownership",
        type: s,
        evidence: "Extracted from resume analysis",
      })),
      ...(profile.measurable_outcomes || []).slice(0, 3).map((s) => ({
        title: "Outcome",
        type: s,
        evidence: "Measurable impact signal",
      })),
    ];

    skillsEl.innerHTML = items
      .slice(0, 8)
      .map(
        (item) => `
      <div class="glass-card p-md rounded-xl hover:border-primary/30 transition-all">
        <div class="flex items-center gap-xs mb-sm">
          <span class="material-symbols-outlined text-primary text-[20px]">verified_user</span>
          <span class="font-data-sm text-data-sm text-primary uppercase tracking-widest">${item.title}</span>
        </div>
        <h3 class="font-headline-md text-headline-md text-on-surface mb-xs">${item.type}</h3>
        <p class="text-body-sm text-on-surface-variant line-clamp-3">${item.evidence || "Verified via profile extraction pipeline."}</p>
      </div>`
      )
      .join("");
  }

  if (graphEl && profile.core_skills?.length) {
    const center = profile.seniority_level || "You";
    const skills = profile.core_skills.slice(0, 5);
    graphEl.innerHTML = `
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-32 h-32 rounded-full border-2 border-primary flex items-center justify-center glow-cyan bg-surface-container/50">
          <span class="font-data-lg text-data-lg text-primary text-center px-2">${center}</span>
        </div>
      </div>`;
    skills.forEach((skill, i) => {
      const angle = (i / skills.length) * 2 * Math.PI - Math.PI / 2;
      const x = 50 + 35 * Math.cos(angle);
      const y = 50 + 35 * Math.sin(angle);
      graphEl.insertAdjacentHTML(
        "beforeend",
        `<div class="skill-node absolute px-sm py-xs glass-card rounded-full text-body-sm font-medium border border-primary/30"
             style="left: ${x}%; top: ${y}%; transform: translate(-50%, -50%);">${skill}</div>`
      );
    });
  }

  const summaryEl = document.querySelector("[data-profile-summary]");
  if (summaryEl) summaryEl.textContent = profile.semantic_summary || "";

  const expEl = document.querySelector("[data-experiences]");
  if (expEl && profile.experiences?.length) {
    expEl.innerHTML = profile.experiences
      .map(
        (e) =>
          `<li class="glass-card rounded-lg p-3"><strong>${e.title}</strong> — ${e.company} <span class="text-on-surface-variant text-xs">${e.duration || ""}</span></li>`
      )
      .join("");
  }

  const internEl = document.querySelector("[data-internships]");
  if (internEl && profile.internships?.length) {
    internEl.innerHTML = profile.internships
      .map(
        (e) =>
          `<li class="glass-card rounded-lg p-3"><strong>${e.title}</strong> — ${e.company}</li>`
      )
      .join("");
  }
});
