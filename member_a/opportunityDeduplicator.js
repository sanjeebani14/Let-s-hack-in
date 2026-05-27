function normalizeValue(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/https?:\/\//g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function toSignature(item) {
  return {
    title: normalizeValue(item.title),
    company: normalizeValue(item.company),
    url: normalizeValue(item.url),
  };
}

function tokenSimilarity(a = "", b = "") {
  const setA = new Set(a.split(" ").filter(Boolean));
  const setB = new Set(b.split(" ").filter(Boolean));
  if (!setA.size || !setB.size) return 0;

  let overlap = 0;
  setA.forEach((token) => {
    if (setB.has(token)) overlap += 1;
  });
  return overlap / Math.max(setA.size, setB.size);
}

function isDuplicate(lhs, rhs) {
  const left = toSignature(lhs);
  const right = toSignature(rhs);

  if (left.url && right.url && left.url === right.url) return true;
  if (left.title === right.title && left.company === right.company) return true;

  const titleSim = tokenSimilarity(left.title, right.title);
  const companySim = tokenSimilarity(left.company, right.company);
  return titleSim >= 0.9 && companySim >= 0.8;
}

function deduplicateOpportunities(opportunities = []) {
  const unique = [];
  opportunities.forEach((item) => {
    const duplicate = unique.some((existing) => isDuplicate(item, existing));
    if (!duplicate) unique.push(item);
  });
  return unique;
}

module.exports = {
  deduplicateOpportunities,
  isDuplicate,
};
