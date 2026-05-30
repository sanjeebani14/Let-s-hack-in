document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const statusEl = document.getElementById("login-status");
  const googleBtn = document.getElementById("google-signin-btn");

  googleBtn?.addEventListener("click", async () => {
    statusEl.textContent = "Opening Google sign-in…";
    statusEl.className = "text-sm text-[#8ed5ff]";
    googleBtn.disabled = true;

    try {
      await InRoadAuth.init();
      const { profile } = await InRoadAuth.signInWithGoogle("student");
      statusEl.textContent = "Success! Redirecting…";
      InRoadAuth.redirectByRole(profile);
    } catch (err) {
      statusEl.textContent = err.message || "Google sign-in failed";
      statusEl.className = "text-sm text-[#ffb4ab]";
      googleBtn.disabled = false;
    }
  });

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email")?.value?.trim();
    const password = document.getElementById("password")?.value;

    statusEl.textContent = "Signing in…";
    statusEl.className = "text-sm text-[#8ed5ff]";

    try {
      await InRoadAuth.init();
      await InRoadAuth.login(email, password);
      const profile = await InRoadAuth.fetchProfile();
      statusEl.textContent = "Success! Redirecting…";
      InRoadAuth.redirectByRole(profile);
    } catch (err) {
      statusEl.textContent = err.message || "Login failed";
      statusEl.className = "text-sm text-[#ffb4ab]";
    }
  });
});
