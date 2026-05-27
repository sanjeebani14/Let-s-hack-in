const { createHttpClient, normalizeList, safeText, hashId, formatError } = require("./sourceUtils");

const QUERY = "hiring internship OR frontend developer OR founder hiring";

function mapProviderResult(item, providerName) {
  const title = safeText(item.title || item.position);
  const description = safeText(item.snippet || item.description);
  return {
    id: hashId(`${providerName}-${item.id || item.link || title}`),
    title,
    company: safeText(item.company || item.source || "Unknown"),
    location: safeText(item.location || "Remote/Unknown"),
    description,
    skills: normalizeList(item.skills || []),
    source: "linkedin-provider",
    url: safeText(item.link || item.url),
    postedDate: item.date || new Date().toISOString(),
    opportunityType: /intern/i.test(title) ? "Internship" : "Unknown",
  };
}

async function fetchWithSerpApi(client) {
  const response = await client.get("https://serpapi.com/search.json", {
    params: {
      api_key: process.env.SERPAPI_KEY,
      engine: "google_jobs",
      q: QUERY,
      hl: "en",
      num: 20,
    },
  });
  return (response.data?.jobs_results || []).map((item) => mapProviderResult(item, "serpapi"));
}

async function fetchWithApify(client) {
  // Placeholder style integration: call a dataset endpoint token-backed provider.
  const response = await client.get("https://api.apify.com/v2/datasets/placeholder/items", {
    params: {
      token: process.env.APIFY_TOKEN,
      clean: true,
      limit: 20,
    },
  });
  return (response.data || []).map((item) => mapProviderResult(item, "apify"));
}

async function fetchLinkedInOpportunities() {
  const client = createHttpClient(10000);
  const hasSerpApi = Boolean(process.env.SERPAPI_KEY);
  const hasApify = Boolean(process.env.APIFY_TOKEN);

  if (!hasSerpApi && !hasApify) {
    return {
      opportunities: [],
      status: {
        active: false,
        disabled: true,
        reason: "Missing SERPAPI_KEY/APIFY_TOKEN (LinkedIn provider integration disabled)",
      },
    };
  }

  try {
    if (hasSerpApi) {
      const opportunities = await fetchWithSerpApi(client);
      return { opportunities, status: { active: true, disabled: false, provider: "serpapi" } };
    }

    const opportunities = await fetchWithApify(client);
    return { opportunities, status: { active: true, disabled: false, provider: "apify" } };
  } catch (error) {
    return {
      opportunities: [],
      status: { active: false, disabled: false, error: formatError(error) },
    };
  }
}

module.exports = { fetchLinkedInOpportunities };
