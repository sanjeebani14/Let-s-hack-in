/**
 * Persists analysis results in sessionStorage for multi-page navigation.
 */
const INROAD_STORAGE_KEY = "inroad_analysis_v1";

const InRoadStore = {
  save(analysis) {
    sessionStorage.setItem(INROAD_STORAGE_KEY, JSON.stringify(analysis));
  },

  load() {
    const raw = sessionStorage.getItem(INROAD_STORAGE_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  },

  hasAnalysis() {
    return Boolean(this.load()?.matched_opportunities?.length);
  },

  getOpportunity(id) {
    const data = this.load();
    if (!data) return null;
    const numId = Number(id);
    return (
      data.matched_opportunities?.find((o) => o.opportunity_id === numId) ||
      null
    );
  },

  setSelectedOpportunityId(id) {
    sessionStorage.setItem("inroad_selected_opportunity_id", String(id));
  },

  getSelectedOpportunityId() {
    const id = sessionStorage.getItem("inroad_selected_opportunity_id");
    return id ? Number(id) : null;
  },

  getSelectedOpportunity() {
    const id = this.getSelectedOpportunityId();
    if (id) return this.getOpportunity(id);
    const data = this.load();
    return data?.matched_opportunities?.[0] || null;
  },

  clear() {
    sessionStorage.removeItem(INROAD_STORAGE_KEY);
    sessionStorage.removeItem("inroad_selected_opportunity_id");
    sessionStorage.removeItem("inroad_outreach_v1");
  },
};

window.InRoadStore = InRoadStore;
