const { hashId, normalizeList, safeText } = require("./opportunity-sources/sourceUtils");

const SKILL_HINTS = [
  "javascript",
  "typescript",
  "react",
  "node",
  "python",
  "django",
  "flask",
  "fastapi",
  "java",
  "golang",
  "aws",
  "docker",
  "kubernetes",
  "sql",
  "machine learning",
  "ai",
  "frontend",
  "backend",
];

function cleanText(text) {
  return safeText(String(text || "").replace(/\s+/g, " "));
}

function inferSkills(title, description, explicitSkills = []) {
  const base = `${cleanText(title)} ${cleanText(description)}`.toLowerCase();
  const inferred = SKILL_HINTS.filter((skill) => base.includes(skill));
  return Array.from(new Set([...normalizeList(explicitSkills), ...inferred]));
}

function inferOpportunityType(item) {
  const base = `${cleanText(item.title)} ${cleanText(item.description)} ${cleanText(item.location)}`.toLowerCase();
  if (base.includes("intern")) return "Internship";
  if (base.includes("freelance") || base.includes("contract")) return "Freelance";
  if (base.includes("open source") || base.includes("good first issue")) return "Open Source";
  if (base.includes("remote")) return "Remote";
  if (base.includes("full-time") || base.includes("full time")) return "Full-time";
  return "Unknown";
}

function normalizeOpportunity(rawOpportunity = {}, fallbackSource = "unknown") {
  const title = cleanText(rawOpportunity.title) || "Untitled Opportunity";
  const company = cleanText(rawOpportunity.company) || "Unknown";
  const description = cleanText(rawOpportunity.description);
  const url = cleanText(rawOpportunity.url);
  const source = cleanText(rawOpportunity.source) || fallbackSource;

  const normalized = {
    id: cleanText(rawOpportunity.id) || hashId(`${title}-${company}-${url || Date.now()}`),
    title,
    company,
    location: cleanText(rawOpportunity.location) || "Unknown",
    description,
    skills: inferSkills(title, description, rawOpportunity.skills),
    source,
    url,
    postedDate: rawOpportunity.postedDate || new Date().toISOString(),
    opportunityType: cleanText(rawOpportunity.opportunityType) || inferOpportunityType(rawOpportunity),
  };

  if (!normalized.url) {
    normalized.url = `urn:opportunity:${normalized.id}`;
  }

  return normalized;
}

function normalizeSourceResponse(opportunities = [], sourceName = "unknown") {
  return opportunities.map((item) => normalizeOpportunity(item, sourceName));
}

module.exports = {
  cleanText,
  inferSkills,
  inferOpportunityType,
  normalizeOpportunity,
  normalizeSourceResponse,
};
