async function checkApiHealth() {
  const res = await fetch(`${window.INROAD_API_BASE}/`);
  if (!res.ok) throw new Error("API unreachable");
  return res.json();
}

async function analyzeCandidate({ resume_text, project_descriptions }) {
  const res = await fetch(`${window.INROAD_API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_text, project_descriptions }),
  });

  const data = await res.json();
  if (!res.ok) {
    const message = data.detail || data.message || "Analysis failed";
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }
  return data;
}
