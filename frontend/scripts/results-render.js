function pct(value, max = 100) {
  return Math.min(100, Math.max(0, (value / max) * 100));
}

function scoreBar(label, value, scale = 1) {
  const display = scale === 1 ? Math.round(value * 100) : Math.round(value);
  const width = scale === 1 ? pct(value * 100) : pct(value);
  return `
    <div class="mb-sm">
      <div class="mb-1 flex justify-between font-data-sm text-data-sm text-on-surface-variant">
        <span>${label}</span><span>${display}%</span>
      </div>
      <div class="score-meter"><span style="width:${width}%"></span></div>
    </div>`;
}

function renderTags(items) {
  if (!items?.length) return '<span class="text-on-surface-variant">—</span>';
  return items.map((t) => `<span class="tag-chip">${t}</span>`).join(" ");
}

function renderProofSection(proof) {
  if (!proof) return "";
  const skills = (proof.matched_skills || [])
    .map(
      (s) => `
      <li class="font-body-sm text-body-sm text-on-surface-variant">
        <strong class="text-on-surface">${s.name || s.skill_name}</strong>
        — ${Math.round(s.confidence || 0)}% · ${s.evidence || s.best_project_evidence || ""}
      </li>`
    )
    .join("");

  return `
    <div class="mt-md rounded-lg border border-primary-container/25 bg-primary-container/5 p-sm">
      <h4 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Agent 4 — Skill proof</h4>
      <p class="mb-sm font-body-sm text-body-sm text-on-surface-variant">${proof.summary}</p>
      <ul class="list-inside list-disc space-y-1">${skills || "<li>No skills matched</li>"}</ul>
    </div>`;
}

function renderOutreachSection(outreach, index) {
  if (!outreach) return "";
  const actions = (outreach.action_instructions || [])
    .map((line) => `<li class="font-body-sm text-body-sm text-on-surface-variant">${line}</li>`)
    .join("");

  const linkedinId = `linkedin-${index}`;
  const emailId = `email-${index}`;

  return `
    <div class="mt-md rounded-lg border border-outline-variant bg-surface/40 p-sm">
      <h4 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Agent 5 — Outreach</h4>
      <p class="mb-xs font-data-sm text-data-sm text-on-surface-variant">Next actions</p>
      <ul class="mb-md list-inside list-disc space-y-1">${actions || "<li>—</li>"}</ul>
      <div class="mb-md">
        <div class="mb-1 flex items-center justify-between">
          <p class="font-data-sm text-data-sm text-on-surface-variant">LinkedIn</p>
          <button type="button" class="copy-btn font-data-sm text-data-sm text-primary-container" data-copy-target="${linkedinId}">Copy</button>
        </div>
        <p id="${linkedinId}" class="whitespace-pre-wrap font-body-sm text-body-sm text-on-surface">${outreach.linkedin_message}</p>
      </div>
      <div>
        <div class="mb-1 flex items-center justify-between">
          <p class="font-data-sm text-data-sm text-on-surface-variant">Email — ${outreach.email_subject || "Subject"}</p>
          <button type="button" class="copy-btn font-data-sm text-data-sm text-primary-container" data-copy-target="${emailId}">Copy</button>
        </div>
        <p id="${emailId}" class="whitespace-pre-wrap font-body-sm text-body-sm text-on-surface-variant">${outreach.email_body_preview}</p>
      </div>
    </div>`;
}

function renderOpportunityCard(opp, rank, options = {}) {
  const c = opp.chemistry;
  const s = opp.scores;
  const compact = options.compact;
  const forceOpen = options.forceOpen;
  const detailHref = `opportunity.html?i=${rank - 1}`;
  const urlLink = opp.opportunity_url
    ? `<a class="font-data-sm text-data-sm text-primary-container hover:underline" href="${opp.opportunity_url}" target="_blank" rel="noopener noreferrer">Source</a>`
    : "";

  const breakdownBody = `
          <p class="font-body-sm text-body-sm text-on-surface-variant">${opp.match_reasoning}</p>
          <div>
            <h4 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Agent 1 — Opportunity score</h4>
            ${scoreBar("Competition index", s.competition_index)}
            ${scoreBar("Response probability", s.response_probability)}
            ${scoreBar("Growth potential", s.growth_potential)}
            ${scoreBar("Referral likelihood", s.referral_likelihood)}
            <p class="mt-xs font-body-sm text-body-sm text-on-surface-variant">${s.score_reasoning}</p>
          </div>
          <div>
            <h4 class="mb-sm font-data-sm text-data-sm uppercase text-primary-container">Agent 3 — Chemistry</h4>
            <p class="mb-sm font-body-sm text-body-sm">${c.structural_explanation}</p>
            <ul class="space-y-1 font-body-sm text-body-sm text-on-surface-variant">
              <li>Shared contexts: ${c.shared_contexts_count} — ${c.shared_contexts_summary}</li>
              <li>Connector: <strong class="text-on-surface">${c.best_connector_name}</strong> (${c.best_connector_intro})</li>
              <li>Entry probability: ${Math.round(c.entry_probability * 100)}%</li>
              <li>Team fit: ${c.team_fit_category}</li>
            </ul>
          </div>
          ${renderProofSection(opp.proof)}
          ${renderOutreachSection(opp.outreach, rank - 1)}`;

  const expanded = compact
    ? ""
    : forceOpen
      ? `<div class="mt-md space-y-md border-t border-outline-variant pt-md">${breakdownBody}</div>`
      : `
      <details class="opportunity-details mt-md">
        <summary class="font-body-md text-body-md font-medium text-primary-container">Scores, proof & outreach</summary>
        <div class="mt-md space-y-md border-t border-outline-variant pt-md">
          ${breakdownBody}
        </div>
      </details>`;

  return `
    <article class="glass-card rounded-xl p-lg" data-opp-index="${rank - 1}">
      <div class="mb-md flex flex-col gap-sm sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="font-data-sm text-data-sm uppercase tracking-widest text-primary-container">#${rank} · ${opp.source_type.replace(/_/g, " ")}</p>
          <h3 class="font-headline-md text-headline-md text-on-surface">${opp.title}</h3>
          <p class="font-body-md text-body-md text-on-surface-variant">${opp.company}</p>
          <div class="mt-1 flex gap-sm">${urlLink}<a href="${detailHref}" class="font-data-sm text-data-sm text-primary-container hover:underline">Full detail</a></div>
        </div>
        <div class="flex shrink-0 gap-sm">
          <div class="rounded-lg border border-primary-container/30 bg-primary-container/10 px-sm py-xs text-center">
            <p class="font-data-sm text-data-sm text-on-surface-variant">Fit</p>
            <p class="font-data-lg text-data-lg text-primary-container">${opp.fit_score.toFixed(0)}%</p>
          </div>
          <div class="rounded-lg border border-primary-container/30 bg-secondary-container px-sm py-xs text-center">
            <p class="font-data-sm text-data-sm text-on-secondary-container">InRoad</p>
            <p class="font-data-lg text-data-lg text-secondary">${c.inroad_score.toFixed(0)}%</p>
          </div>
        </div>
      </div>
      <p class="mb-md rounded-lg border border-outline-variant bg-surface/60 p-sm font-body-sm text-body-sm text-on-surface">
        <span class="font-bold text-primary-container">Way in:</span> ${c.way_in_strategy}
      </p>
      ${expanded}
    </article>`;
}

function bindCopyButtons(root = document) {
  root.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-copy-target");
      const el = document.getElementById(id);
      if (!el) return;
      try {
        await navigator.clipboard.writeText(el.textContent);
        const prev = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(() => { btn.textContent = prev; }, 1500);
      } catch {
        btn.textContent = "Failed";
      }
    });
  });
}
