/** Resume upload, extraction preview, and analysis pipeline */
(function () {
  let extracted = {
    skills: [],
    experiences: [],
    internships: [],
    projects: [],
  };

  function renderPreview() {
    const block = document.getElementById("extracted-preview");
    if (!block) return;
    const hasData =
      extracted.skills.length ||
      extracted.experiences.length ||
      extracted.internships.length ||
      extracted.projects.length;
    block.classList.toggle("hidden", !hasData);

    const skillsInput = document.getElementById("skills_input");
    if (skillsInput) skillsInput.value = extracted.skills.join(", ");

    const expEl = document.getElementById("experiences-preview");
    if (expEl) {
      expEl.innerHTML = extracted.experiences.length
        ? extracted.experiences
            .map(
              (e) =>
                `<div class="glass-card rounded p-2"><strong>${e.title}</strong> @ ${e.company} <span class="opacity-60">${e.duration || ""}</span></div>`
            )
            .join("")
        : '<p class="opacity-60">None detected — add in Profile.</p>';
    }

    const intEl = document.getElementById("internships-preview");
    if (intEl) {
      intEl.innerHTML = extracted.internships.length
        ? extracted.internships
            .map(
              (e) =>
                `<div class="glass-card rounded p-2"><strong>${e.title}</strong> @ ${e.company}</div>`
            )
            .join("")
        : '<p class="opacity-60">None detected.</p>';
    }

    const projEl = document.getElementById("projects-preview");
    if (projEl) {
      projEl.innerHTML = extracted.projects.length
        ? extracted.projects
            .map(
              (e) =>
                `<div class="glass-card rounded p-2"><strong>${e.title}</strong></div>`
            )
            .join("")
        : '<p class="opacity-60">None detected.</p>';
    }
  }

  function parseSkillsInput() {
    const raw = document.getElementById("skills_input")?.value || "";
    return raw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
  }

  document.addEventListener("DOMContentLoaded", async () => {
    if (!(await InRoadAuth.requireAuth())) return;
    const form = document.getElementById("analyze-form");
    const statusEl = document.getElementById("analyze-status");
    const submitBtn = document.getElementById("analyze-submit");
    const fileInput = document.getElementById("resume_file");
    const resumeTa = document.getElementById("resume_text");

    InRoadAuth.init().then(async () => {
      try {
        const profile = await InRoadAuth.fetchProfile();
        if (profile?.resume_text) resumeTa.value = profile.resume_text;
        extracted.skills = profile.skills || [];
        extracted.experiences = profile.experiences || [];
        extracted.internships = profile.internships || [];
        extracted.projects = profile.projects || [];
        renderPreview();
      } catch {
        /* not signed in */
      }
    });

    fileInput?.addEventListener("change", async () => {
      const file = fileInput.files?.[0];
      if (!file) return;

      statusEl.textContent = "Uploading and parsing resume…";
      statusEl.className = "text-primary text-body-sm";

      try {
        const result = await InRoadAPI.uploadResume(file);
        resumeTa.value = result.resume_text || "";
        extracted.skills = result.skills || result.candidate_profile?.skills || [];
        extracted.experiences = result.experiences || [];
        extracted.internships = result.internships || [];
        extracted.projects = result.projects || [];
        renderPreview();
        statusEl.textContent = "Resume parsed. Review extracted sections below.";
        statusEl.className = "text-primary text-body-sm";
      } catch (err) {
        statusEl.textContent = err.message || "Upload failed";
        statusEl.className = "text-error text-body-sm";
      }
    });

    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const resume = resumeTa?.value?.trim() || "";
      const projects =
        document.getElementById("project_descriptions")?.value?.trim() || "";
      const skills = parseSkillsInput().length
        ? parseSkillsInput()
        : extracted.skills;

      if (resume.length < 10) {
        statusEl.textContent = "Resume text needs at least 10 characters. Upload a file or paste text.";
        statusEl.className = "text-error text-body-sm";
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = "Analyzing…";
      statusEl.textContent =
        "Running profile extraction, matching, and chemistry analysis…";
      statusEl.className = "text-primary text-body-sm";

      try {
        const result = await InRoadAPI.analyze({
          resume_text: resume,
          project_descriptions: projects, // User's manual text
          skills,
          experiences: extracted.experiences,
          internships: extracted.internships,
          projects: extracted.projects, // Extracted structure
        });
        InRoadStore.save(result);
        if (result.matched_opportunities?.[0]) {
          InRoadStore.setSelectedOpportunityId(
            result.matched_opportunities[0].opportunity_id
          );
        }

        if (InRoadAuth.currentUser()) {
          try {
            await InRoadAPI.saveProfile({
              skills,
              experiences: extracted.experiences,
              internships: extracted.internships,
              projects: extracted.projects,
              resume_text: resume,
              project_descriptions: projects,
            });
          } catch {
            /* profile save optional */
          }
        }

        statusEl.textContent = "Analysis complete. Opening dashboard…";
        window.location.href = "/dashboard.html";
      } catch (err) {
        statusEl.textContent = err.message || "Analysis failed. Try again.";
        statusEl.className = "text-error text-body-sm";
        submitBtn.disabled = false;
        submitBtn.textContent = "Run Analysis";
      }
    });
  });
})();
