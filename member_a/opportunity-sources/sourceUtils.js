const axios = require("axios");
const crypto = require("crypto");

const DEFAULT_TIMEOUT_MS = 7000;

function createHttpClient(timeoutMs = DEFAULT_TIMEOUT_MS) {
  return axios.create({
    timeout: timeoutMs,
    headers: {
      "User-Agent": "opportunity-discovery-agent/1.0",
      Accept: "application/json, text/html",
    },
  });
}

function safeText(value) {
  return typeof value === "string" ? value.trim() : "";
}

function toArray(value) {
  if (Array.isArray(value)) {
    return value;
  }
  return value ? [value] : [];
}

function normalizeList(values) {
  return toArray(values)
    .map((item) => safeText(item))
    .filter(Boolean);
}

function hashId(seed) {
  const base = safeText(seed) || `opportunity-${Date.now()}-${Math.random()}`;
  return crypto.createHash("sha1").update(base).digest("hex");
}

function formatError(error) {
  if (!error) return "Unknown error";
  if (error.response?.status) {
    return `HTTP ${error.response.status}: ${safeText(error.response.statusText) || "Request failed"}`;
  }
  return safeText(error.message) || "Request failed";
}

module.exports = {
  createHttpClient,
  safeText,
  toArray,
  normalizeList,
  hashId,
  formatError,
  DEFAULT_TIMEOUT_MS,
};
