const { createHttpClient, normalizeList, safeText, hashId, formatError } = require("./sourceUtils");

function fromRemotive(job) {
  return {
    id: hashId(`remotive-${job.id}-${job.url}`),
    title: safeText(job.title),
    company: safeText(job.company_name),
    location: safeText(job.candidate_required_location) || "Remote/Unknown",
    description: safeText(job.description),
    skills: normalizeList(job.tags),
    source: "remotive",
    url: job.url,
    postedDate: job.publication_date || new Date().toISOString(),
    opportunityType: /intern/i.test(job.title) ? "Internship" : "Remote",
  };
}

function fromArbeitnow(job) {
  return {
    id: hashId(`arbeitnow-${job.slug}-${job.url}`),
    title: safeText(job.title),
    company: safeText(job.company_name),
    location: safeText(job.location) || "Remote/Unknown",
    description: safeText(job.description),
    skills: normalizeList(job.tags),
    source: "arbeitnow",
    url: job.url || `https://www.arbeitnow.com/jobs/${job.slug}`,
    postedDate: job.created_at || new Date().toISOString(),
    opportunityType: /intern/i.test(job.title) ? "Internship" : "Full-time",
  };
}

function fromRemoteOk(job) {
  return {
    id: hashId(`remoteok-${job.id}-${job.url}`),
    title: safeText(job.position || job.title),
    company: safeText(job.company),
    location: safeText(job.location) || "Remote",
    description: safeText(job.description),
    skills: normalizeList(job.tags),
    source: "remoteok",
    url: job.url ? `https://remoteok.com${job.url}` : safeText(job.apply_url),
    postedDate: job.date || new Date().toISOString(),
    opportunityType: /intern/i.test(job.position || job.title) ? "Internship" : "Remote",
  };
}

function fromAdzuna(job) {
  return {
    id: hashId(`adzuna-${job.id}-${job.redirect_url}`),
    title: safeText(job.title),
    company: safeText(job.company?.display_name),
    location: safeText(job.location?.display_name),
    description: safeText(job.description),
    skills: [],
    source: "adzuna",
    url: job.redirect_url,
    postedDate: job.created || new Date().toISOString(),
    opportunityType: /intern/i.test(job.title) ? "Internship" : "Full-time",
  };
}

async function fetchJobBoardOpportunities() {
  const client = createHttpClient(9000);
  const opportunities = [];
  const status = { active: true, disabled: false, providers: {} };

  try {
    const remotiveResp = await client.get("https://remotive.com/api/remote-jobs", { params: { limit: 25 } });
    opportunities.push(...(remotiveResp.data?.jobs || []).map(fromRemotive));
    status.providers.remotive = "active";
  } catch (error) {
    status.providers.remotive = `error: ${formatError(error)}`;
  }

  try {
    const arbeitResp = await client.get("https://www.arbeitnow.com/api/job-board-api");
    opportunities.push(...(arbeitResp.data?.data || []).slice(0, 25).map(fromArbeitnow));
    status.providers.arbeitnow = "active";
  } catch (error) {
    status.providers.arbeitnow = `error: ${formatError(error)}`;
  }

  try {
    const remoteOkResp = await client.get("https://remoteok.com/api");
    const remoteOkJobs = (remoteOkResp.data || []).filter((row) => row && row.id);
    opportunities.push(...remoteOkJobs.slice(0, 25).map(fromRemoteOk));
    status.providers.remoteok = "active";
  } catch (error) {
    status.providers.remoteok = `error: ${formatError(error)}`;
  }

  const hasAdzunaKeys = process.env.ADZUNA_APP_ID && process.env.ADZUNA_APP_KEY;
  if (hasAdzunaKeys) {
    try {
      const adzunaResp = await client.get(
        `https://api.adzuna.com/v1/api/jobs/in/search/1`,
        {
          params: {
            app_id: process.env.ADZUNA_APP_ID,
            app_key: process.env.ADZUNA_APP_KEY,
            results_per_page: 20,
            what: "software developer internship remote",
            content_type: "application/json",
          },
        }
      );
      opportunities.push(...(adzunaResp.data?.results || []).map(fromAdzuna));
      status.providers.adzuna = "active";
    } catch (error) {
      status.providers.adzuna = `error: ${formatError(error)}`;
    }
  } else {
    status.providers.adzuna = "disabled: missing ADZUNA_APP_ID/ADZUNA_APP_KEY";
  }

  status.active = opportunities.length > 0;
  return { opportunities, status };
}

module.exports = { fetchJobBoardOpportunities };
