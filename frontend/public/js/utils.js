/** UI helpers shared across pages */
function formatScore(value, decimals = 0) {
  const n = Number(value);
  if (Number.isNaN(n)) return "—";
  return decimals > 0 ? n.toFixed(decimals) : Math.round(n).toString();
}

function scoreTier(score) {
  const s = Number(score);
  if (s >= 85) return "Elite Tier";
  if (s >= 70) return "Highly Active";
  if (s >= 55) return "Building Momentum";
  return "Emerging";
}

function setProgressRing(ringEl, score, max = 100) {
  if (!ringEl) return;
  const circumference = 502.6;
  const pct = Math.min(Math.max(Number(score) / max, 0), 1);
  const offset = circumference * (1 - pct);
  ringEl.setAttribute("stroke-dasharray", String(circumference));
  ringEl.style.strokeDashoffset = String(circumference);
  setTimeout(() => {
    ringEl.style.strokeDashoffset = String(offset);
  }, 200);
}

function sourceLabel(sourceType) {
  const map = {
    founder_post: "Founder post",
    github_repo: "GitHub",
    employee_post: "Employee referral",
    newsletter: "Newsletter",
    hackathon: "Hackathon",
  };
  return map[sourceType] || sourceType || "Hidden channel";
}

function requireAnalysis(redirectTo = "/analyze.html") {
  if (!InRoadStore.hasAnalysis()) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

window.InRoadUtils = {
  formatScore,
  scoreTier,
  setProgressRing,
  sourceLabel,
  requireAnalysis,
};
