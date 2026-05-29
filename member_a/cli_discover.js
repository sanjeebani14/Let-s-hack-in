const { discoverOpportunities } = require("./opportunityDiscoveryService");

const careerUrls = (process.env.CAREER_URLS || "")
  .split(",")
  .map((u) => u.trim())
  .filter(Boolean);

discoverOpportunities({ careerUrls })
  .then((result) => {
    process.stdout.write(JSON.stringify(result));
  })
  .catch((error) => {
    process.stderr.write(error.message || String(error));
    process.exit(1);
  });
