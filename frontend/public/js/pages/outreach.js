document.addEventListener("DOMContentLoaded", async () => {
  if (!(await InRoadAuth.requireAuth())) return;
  if (!requireAnalysis()) return;

  const params = new URLSearchParams(window.location.search);
  const id =
    params.get("id") ||
    InRoadStore.getSelectedOpportunityId() ||
    InRoadStore.load()?.matched_opportunities?.[0]?.opportunity_id;

  const data = InRoadStore.load() || {};
  const opportunities = data.matched_opportunities || [];
  const listEl = document.querySelector("[data-outreach-opportunities]");
  const textarea = document.getElementById("outreach-textarea");
  const subjectEl = document.querySelector("[data-outreach-subject]");
  const statusEl = document.querySelector("[data-outreach-status]");
  const generateBtn = document.querySelector("[data-outreach-generate]");

  let selectedId = id ? Number(id) : opportunities[0]?.opportunity_id;

  function renderOpportunityList() {
    if (!listEl) return;
    listEl.innerHTML = "";
    opportunities.forEach((opp) => {
      const btn = document.createElement("button");
      const active = opp.opportunity_id === selectedId;
      btn.type = "button";
      btn.className = `w-full p-sm rounded-lg border text-left transition-all ${
        active
          ? "border-primary-container bg-primary-container/5 active-glow"
          : "border-outline-variant/30 bg-surface-container/30 hover:border-outline"
      }`;
      btn.innerHTML = `
        <div class="flex justify-between items-start mb-xs">
          <span class="font-bold text-on-surface">${opp.title}</span>
          <span class="text-[12px] bg-tertiary-container/20 text-tertiary px-xs py-[2px] rounded-full">${formatScore(opp.fit_score)}% Match</span>
        </div>
        <p class="text-body-sm text-on-surface-variant">${opp.company}</p>`;
      btn.addEventListener("click", () => {
        selectedId = opp.opportunity_id;
        InRoadStore.setSelectedOpportunityId(selectedId);
        renderOpportunityList();
        loadOutreach();
      });
      listEl.appendChild(btn);
    });
  }

  async function loadOutreach() {
    if (!textarea) return;
    const cached = sessionStorage.getItem(`inroad_outreach_${selectedId}`);
    if (cached) {
      try {
        const pkg = JSON.parse(cached);
        applyOutreach(pkg);
        return;
      } catch {
        /* regenerate */
      }
    }
    if (statusEl) statusEl.textContent = "Generating outreach…";
    if (generateBtn) generateBtn.disabled = true;
    try {
      const pkg = await InRoadAPI.generateOutreach(selectedId);
      sessionStorage.setItem(`inroad_outreach_${selectedId}`, JSON.stringify(pkg));
      applyOutreach(pkg);
      if (statusEl) statusEl.textContent = "";
    } catch (err) {
      const opp = InRoadStore.getOpportunity(selectedId);
      const fallback = buildFallbackMessage(opp);
      textarea.value = fallback.body;
      if (subjectEl) subjectEl.textContent = fallback.subject;
      if (statusEl)
        statusEl.textContent =
          (err.message || "Using chemistry-based draft.") + "";
    } finally {
      if (generateBtn) generateBtn.disabled = false;
    }
  }

  function applyOutreach(pkg) {
    const email = pkg.email_package || pkg.cold_email || {};
    const primary = email.primary_email || email;
    const linkedin = pkg.linkedin_dm || {};
    const body =
      pkg.message_body ||
      primary.body ||
      email.body ||
      linkedin.message_body ||
      pkg.linkedin_body ||
      "";
    const subject =
      primary.subject_line ||
      email.subject_line ||
      linkedin.subject_line ||
      `Interest in role — ${pkg.company_name || ""}`;
    if (textarea) textarea.value = body;
    if (subjectEl) subjectEl.textContent = `Subject: ${subject}`;
  }

  function buildFallbackMessage(opp) {
    if (!opp) return { subject: "Career interest", body: "" };
    const chem = opp.chemistry || {};
    return {
      subject: `Interest — ${opp.title} at ${opp.company}`,
      body: `Hello,

${chem.way_in_strategy || opp.match_reasoning}

I'd welcome a brief conversation about how my background aligns with the ${opp.title} role at ${opp.company}.

Best regards`,
    };
  }

  renderOpportunityList();
  if (generateBtn) {
    generateBtn.addEventListener("click", () => {
      sessionStorage.removeItem(`inroad_outreach_${selectedId}`);
      loadOutreach();
    });
  }
  await loadOutreach();
});
