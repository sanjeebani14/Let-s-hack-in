const { createHttpClient, normalizeList, safeText, hashId, formatError } = require("./sourceUtils");

const SEARCH_QUERIES = [
  "hiring interns",
  "looking for frontend developer",
  "founder hiring",
  "remote internship",
];

function postToOpportunity(post) {
  const text = safeText(post.text || post.content);
  const author = safeText(post.author?.name || post.author || "Unknown");
  return {
    id: hashId(`x-${post.id}-${post.url || text}`),
    title: text.slice(0, 120) || "Hiring post",
    company: author,
    location: safeText(post.location) || "Remote/Unknown",
    description: text,
    skills: normalizeList(post.entities?.hashtags || []),
    source: "twitter-x",
    url: safeText(post.url),
    postedDate: post.created_at || new Date().toISOString(),
    opportunityType: /intern/i.test(text) ? "Internship" : "Unknown",
  };
}

async function fetchTwitterOpportunities() {
  if (!process.env.X_API_KEY) {
    return {
      opportunities: [],
      status: { active: false, disabled: true, reason: "Missing X_API_KEY" },
    };
  }

  const client = createHttpClient(9000);
  const opportunities = [];

  try {
    for (const query of SEARCH_QUERIES) {
      try {
        // Provider endpoint placeholder; keep structure production-safe.
        const response = await client.get("https://api.x.com/2/tweets/search/recent", {
          headers: { Authorization: `Bearer ${process.env.X_API_KEY}` },
          params: { query, max_results: 15 },
        });
        const data = response.data?.data || [];
        opportunities.push(...data.map(postToOpportunity));
      } catch (error) {
        // Continue other queries even if one fails.
      }
    }

    return {
      opportunities,
      status: { active: opportunities.length > 0, disabled: false, reason: "Queried X API provider" },
    };
  } catch (error) {
    return {
      opportunities: [],
      status: { active: false, disabled: false, error: formatError(error) },
    };
  }
}

module.exports = { fetchTwitterOpportunities };
