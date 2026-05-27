const { fetchGitHubOpportunities } = require("./opportunity-sources/githubSource");
const { fetchJobBoardOpportunities } = require("./opportunity-sources/jobBoardSource");
const { fetchLinkedInOpportunities } = require("./opportunity-sources/linkedinSource");
const { fetchTwitterOpportunities } = require("./opportunity-sources/twitterSource");
const { fetchCompanyCareerOpportunities } = require("./opportunity-sources/companyCareerSource");
const { normalizeSourceResponse } = require("./opportunityNormalizer");
const { deduplicateOpportunities } = require("./opportunityDeduplicator");

function toTimestamp(value) {
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 0 : parsed;
}

async function discoverOpportunities(options = {}) {
  const { careerUrls = [] } = options;
  const sourceStatus = {};
  const allOpportunities = [];

  const sourceFetchers = [
    { key: "github", run: () => fetchGitHubOpportunities() },
    { key: "jobBoards", run: () => fetchJobBoardOpportunities() },
    { key: "linkedin", run: () => fetchLinkedInOpportunities() },
    { key: "twitter", run: () => fetchTwitterOpportunities() },
    { key: "companyCareer", run: () => fetchCompanyCareerOpportunities(careerUrls) },
  ];

  await Promise.all(
    sourceFetchers.map(async ({ key, run }) => {
      try {
        const result = await run();
        sourceStatus[key] = result.status || { active: false, disabled: false, error: "No status provided" };
        allOpportunities.push(...normalizeSourceResponse(result.opportunities || [], key));
      } catch (error) {
        sourceStatus[key] = {
          active: false,
          disabled: false,
          error: error.message || "Unexpected source error",
        };
      }
    })
  );

  const deduped = deduplicateOpportunities(allOpportunities)
    .sort((a, b) => toTimestamp(b.postedDate) - toTimestamp(a.postedDate))
    .slice(0, 20);

  return {
    opportunities: deduped,
    sourceStatus,
  };
}

module.exports = { discoverOpportunities };
