/**
 * Shared navigation wiring for all InRoad pages.
 */
(function initInRoadNav() {
  const routes = {
    index: "/index.html",
    dashboard: "/dashboard.html",
    skills: "/skills.html",
    opportunity: "/opportunity.html",
    outreach: "/outreach.html",
    analyze: "/analyze.html",
    login: "/login.html",
    register: "/register.html",
    profile: "/profile.html",
    recruiter: "/recruiter.html",
  };

  function wireLinks() {
    document.querySelectorAll("[data-inroad-nav]").forEach((el) => {
      const key = el.getAttribute("data-inroad-nav");
      if (routes[key]) el.setAttribute("href", routes[key]);
    });

    document.querySelectorAll("[data-inroad-analyze]").forEach((el) => {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = routes.analyze;
      });
    });
  }

  document.addEventListener("DOMContentLoaded", wireLinks);
})();
