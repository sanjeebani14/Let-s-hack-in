const cheerio = require("cheerio");
const { createHttpClient, safeText, hashId, formatError } = require("./sourceUtils");

const TITLE_SELECTORS = [
  "[data-qa='job-title']",
  ".job-title",
  ".posting-title",
  "h2",
  "h3",
  "a[href*='job']",
  "a[href*='career']",
];

function extractOpportunitiesFromHtml(html, pageUrl) {
  const $ = cheerio.load(html);
  const opportunities = [];
  const seen = new Set();

  TITLE_SELECTORS.forEach((selector) => {
    $(selector).each((_, el) => {
      const title = safeText($(el).text());
      if (!title || title.length < 6) return;

      const lower = title.toLowerCase();
      if (!/(engineer|developer|intern|designer|manager|scientist|hiring)/i.test(lower)) return;

      const href = $(el).attr("href");
      const absoluteUrl = href ? new URL(href, pageUrl).toString() : pageUrl;
      const dedupKey = `${title}::${absoluteUrl}`;
      if (seen.has(dedupKey)) return;
      seen.add(dedupKey);

      opportunities.push({
        id: hashId(`career-${dedupKey}`),
        title,
        company: "Unknown",
        location: "Unknown",
        description: `Public career listing discovered at ${pageUrl}`,
        skills: [],
        source: "company-career",
        url: absoluteUrl,
        postedDate: new Date().toISOString(),
        opportunityType: /intern/i.test(title) ? "Internship" : "Full-time",
      });
    });
  });

  return opportunities;
}

async function fetchCompanyCareerOpportunities(careerUrls = []) {
  if (!Array.isArray(careerUrls) || careerUrls.length === 0) {
    return {
      opportunities: [],
      status: { active: false, disabled: true, reason: "No career page URLs provided" },
    };
  }

  const client = createHttpClient(8000);
  const opportunities = [];
  const failedUrls = [];

  for (const careerUrl of careerUrls) {
    try {
      const response = await client.get(careerUrl, {
        headers: { Accept: "text/html,application/xhtml+xml" },
      });
      opportunities.push(...extractOpportunitiesFromHtml(response.data, careerUrl));
    } catch (error) {
      failedUrls.push({ url: careerUrl, error: formatError(error) });
    }
  }

  return {
    opportunities,
    status: {
      active: opportunities.length > 0,
      disabled: false,
      reason: opportunities.length > 0 ? "Scraped public career listings" : "No opportunities parsed",
      failedUrls,
    },
  };
}

module.exports = { fetchCompanyCareerOpportunities };
