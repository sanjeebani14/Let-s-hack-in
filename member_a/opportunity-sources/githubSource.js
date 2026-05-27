const {
  createHttpClient,
  normalizeList,
  safeText,
  hashId,
  formatError,
} = require("./sourceUtils");

const SEARCH_KEYWORDS = [
  "hiring",
  "internship",
  "founder looking for",
  "open roles",
  "good first issue",
];

function buildHeaders() {
  const headers = {};
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  return headers;
}

function issueToOpportunity(issue) {
  const title = safeText(issue.title);
  const description = safeText(issue.body);
  const company = safeText(issue.repository_url?.split("/").slice(-2, -1)[0]) || "Unknown";

  return {
    id: hashId(`gh-issue-${issue.id}-${issue.html_url}`),
    title,
    company,
    location: "Remote/Unknown",
    description,
    skills: normalizeList(issue.labels?.map((label) => label?.name)),
    source: "github",
    url: issue.html_url,
    postedDate: issue.created_at || new Date().toISOString(),
    opportunityType: title.toLowerCase().includes("intern") ? "Internship" : "Open Source",
  };
}

function repoToOpportunity(repo) {
  const title = safeText(repo.name);
  const description = safeText(repo.description);
  const skills = normalizeList([repo.language, ...(repo.topics || [])]);

  return {
    id: hashId(`gh-repo-${repo.id}-${repo.html_url}`),
    title: `${title} - Open Roles`,
    company: safeText(repo.owner?.login) || "Unknown",
    location: "Remote/Unknown",
    description: description || "Repository discovered via hiring signal search.",
    skills,
    source: "github",
    url: repo.html_url,
    postedDate: repo.updated_at || new Date().toISOString(),
    opportunityType: "Open Source",
  };
}

async function searchIssues(client, query, headers) {
  const url = "https://api.github.com/search/issues";
  const response = await client.get(url, {
    headers,
    params: { q: `${query} in:title,body is:issue`, sort: "updated", per_page: 10 },
  });
  return (response.data?.items || []).map(issueToOpportunity);
}

async function searchRepos(client, query, headers) {
  const url = "https://api.github.com/search/repositories";
  const response = await client.get(url, {
    headers,
    params: { q: `${query} in:name,description,readme`, sort: "updated", per_page: 10 },
  });
  return (response.data?.items || []).map(repoToOpportunity);
}

async function fetchGitHubOpportunities() {
  const client = createHttpClient(8000);
  const headers = buildHeaders();

  try {
    const keywordResults = await Promise.all(
      SEARCH_KEYWORDS.slice(0, 3).map(async (keyword) => {
        try {
          const [issues, repos] = await Promise.all([
            searchIssues(client, keyword, headers),
            searchRepos(client, keyword, headers),
          ]);
          return [...issues, ...repos];
        } catch (error) {
          // Rate limits and individual query failures should not crash discovery.
          return [];
        }
      })
    );

    const opportunities = keywordResults.flat();
    return {
      opportunities,
      status: { active: true, disabled: false, reason: process.env.GITHUB_TOKEN ? "Using token auth" : "Using public GitHub API" },
    };
  } catch (error) {
    return {
      opportunities: [],
      status: { active: false, disabled: false, error: formatError(error) },
    };
  }
}

module.exports = { fetchGitHubOpportunities };
