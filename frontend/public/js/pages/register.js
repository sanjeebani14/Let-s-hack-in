document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register-form");
  const statusEl = document.getElementById("register-status");
  const googleBtn = document.getElementById("google-register-btn");

  googleBtn?.addEventListener("click", async () => {
    const role = document.getElementById("role-google")?.value || "student";

    statusEl.textContent = "Opening Google sign-up…";
    statusEl.className = "text-sm text-[#8ed5ff]";
    googleBtn.disabled = true;

    try {
      await InRoadAuth.init();
      const { profile } = await InRoadAuth.signInWithGoogle(role, true);
      statusEl.textContent = "Account created! Redirecting…";
      InRoadAuth.redirectByRole(profile);
    } catch (err) {
      statusEl.textContent = err.message || "Google sign-up failed";
      statusEl.className = "text-sm text-[#ffb4ab]";
      googleBtn.disabled = false;
    }
  });

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email")?.value?.trim();
    const password = document.getElementById("password")?.value;
    const role = document.getElementById("role")?.value;
    const displayName = document.getElementById("display_name")?.value?.trim() || "";

    statusEl.textContent = "Creating account…";
    statusEl.className = "text-sm text-[#8ed5ff]";

    try {
      await InRoadAuth.init();
      await InRoadAuth.register(email, password, role, displayName);
      const profile = await InRoadAuth.fetchProfile();
      statusEl.textContent = "Account created! Redirecting…";
      InRoadAuth.redirectByRole(profile);
    } catch (err) {
      statusEl.textContent = err.message || "Registration failed";
      statusEl.className = "text-sm text-[#ffb4ab]";
    }
  });
});
