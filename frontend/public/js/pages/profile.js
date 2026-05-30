/** Editable profile: skills, experiences, internships */
(function () {
  let state = {
    skills: [],
    experiences: [],
    internships: [],
    resume_text: "",
    project_descriptions: "",
  };

  function entryRow(entry, type, index) {
    return `
      <div class="border border-white/10 rounded-lg p-4 space-y-2" data-entry="${type}" data-index="${index}">
        <input data-field="title" value="${escapeHtml(entry.title || "")}" placeholder="Title" class="w-full bg-[#222a3d]/50 border border-white/20 rounded p-2 text-sm"/>
        <input data-field="company" value="${escapeHtml(entry.company || "")}" placeholder="Company" class="w-full bg-[#222a3d]/50 border border-white/20 rounded p-2 text-sm"/>
        <input data-field="duration" value="${escapeHtml(entry.duration || "")}" placeholder="Duration (e.g. Jan 2024 - Present)" class="w-full bg-[#222a3d]/50 border border-white/20 rounded p-2 text-sm"/>
        <textarea data-field="description" rows="2" placeholder="Description" class="w-full bg-[#222a3d]/50 border border-white/20 rounded p-2 text-sm">${escapeHtml(entry.description || "")}</textarea>
        <button type="button" data-remove-entry class="text-xs text-[#ffb4ab]">Remove</button>
      </div>`;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderSkills() {
    const el = document.getElementById("skills-list");
    if (!el) return;
    el.innerHTML = state.skills
      .map(
        (s, i) => `
      <div class="flex items-center justify-between bg-[#222a3d]/30 rounded px-3 py-2">
        <span class="text-sm">${escapeHtml(s)}</span>
        <button type="button" data-remove-skill="${i}" class="text-xs text-[#ffb4ab]">×</button>
      </div>`
      )
      .join("");
    el.querySelectorAll("[data-remove-skill]").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.skills.splice(Number(btn.dataset.removeSkill), 1);
        renderSkills();
      });
    });
  }

  function renderEntries(type) {
    const el = document.getElementById(`${type}-list`);
    if (!el) return;
    const items = state[type];
    el.innerHTML = items.map((e, i) => entryRow(e, type, i)).join("");
    el.querySelectorAll("[data-remove-entry]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const row = btn.closest("[data-entry]");
        const idx = Number(row?.dataset.index);
        state[type].splice(idx, 1);
        renderEntries(type);
      });
    });
  }

  function collectEntries(type) {
    const rows = document.querySelectorAll(`#${type}-list [data-entry="${type}"]`);
    const items = [];
    rows.forEach((row) => {
      items.push({
        title: row.querySelector('[data-field="title"]')?.value?.trim() || "",
        company: row.querySelector('[data-field="company"]')?.value?.trim() || "",
        duration: row.querySelector('[data-field="duration"]')?.value?.trim() || "",
        description: row.querySelector('[data-field="description"]')?.value?.trim() || "",
      });
    });
    return items;
  }

  document.addEventListener("DOMContentLoaded", async () => {
    await InRoadAuth.requireAuth();
    const statusEl = document.getElementById("profile-status");

    try {
      const profile = await InRoadAPI.getProfile();
      state.skills = profile.skills || [];
      state.experiences = profile.experiences || [];
      state.internships = profile.internships || [];
      state.resume_text = profile.resume_text || "";
      state.project_descriptions = profile.project_descriptions || "";
    } catch {
      const cached = InRoadStore.load();
      const cp = cached?.candidate_profile;
      if (cp) {
        state.skills = cp.skills || cp.core_skills || [];
        state.experiences = cp.experiences || [];
        state.internships = cp.internships || [];
      }
    }

    renderSkills();
    renderEntries("experiences");
    renderEntries("internships");

    document.getElementById("add-skill")?.addEventListener("click", () => {
      const v = document.getElementById("new-skill")?.value?.trim();
      if (v) {
        state.skills.push(v);
        document.getElementById("new-skill").value = "";
        renderSkills();
      }
    });

    document.getElementById("add-experience")?.addEventListener("click", () => {
      state.experiences.push({ title: "", company: "", duration: "", description: "" });
      renderEntries("experiences");
    });

    document.getElementById("add-internship")?.addEventListener("click", () => {
      state.internships.push({ title: "", company: "", duration: "", description: "" });
      renderEntries("internships");
    });

    document.getElementById("profile-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      state.experiences = collectEntries("experiences");
      state.internships = collectEntries("internships");

      statusEl.textContent = "Saving…";
      statusEl.className = "text-sm text-[#8ed5ff]";

      try {
        await InRoadAPI.saveProfile({
          skills: state.skills,
          experiences: state.experiences,
          internships: state.internships,
          resume_text: state.resume_text,
          project_descriptions: state.project_descriptions,
        });
        statusEl.textContent = "Profile saved.";
        statusEl.className = "text-sm text-[#8ed5ff]";
      } catch (err) {
        statusEl.textContent = err.message;
        statusEl.className = "text-sm text-[#ffb4ab]";
      }
    });
  });
})();
