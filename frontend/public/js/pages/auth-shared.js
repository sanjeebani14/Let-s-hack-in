/** Shared auth page styles and nav injection */
function injectAuthNav() {
  const el = document.querySelector("[data-auth-nav]");
  if (!el) return;

  InRoadAuth.init().then(() => {
    const user = InRoadAuth.currentUser();
    if (user) {
      const profile = InRoadAuth.getCachedProfile();
      const role = profile?.role || "student";
      el.innerHTML = `
        <span class="text-xs text-primary uppercase tracking-widest">${role}</span>
        <a href="/profile.html" class="text-sm text-on-surface-variant hover:text-primary">Profile</a>
        <button type="button" id="auth-logout" class="text-sm text-error hover:underline">Sign out</button>
      `;
      document.getElementById("auth-logout")?.addEventListener("click", async () => {
        await InRoadAuth.logout();
        window.location.href = "/index.html";
      });
    } else {
      el.innerHTML = `
        <a href="/login.html" class="text-sm text-on-surface-variant hover:text-primary">Login</a>
        <a href="/register.html" class="text-sm bg-primary-container text-on-primary-container px-md py-xs rounded-full font-bold">Register</a>
      `;
    }
  });
}

document.addEventListener("DOMContentLoaded", injectAuthNav);
