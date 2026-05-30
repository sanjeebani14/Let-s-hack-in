/**

 * InRoad backend client — talks to FastAPI Opportunity Engine.

 */

const InRoadAPI = {

  async _headers(json = true) {

    const headers = {};

    if (json) headers["Content-Type"] = "application/json";

    if (window.InRoadAuth) {

      try {

        const token = await InRoadAuth.getIdToken();

        if (token) headers.Authorization = `Bearer ${token}`;

      } catch {

        /* auth optional for some routes */

      }

    }

    return headers;

  },



  async health() {

    const res = await fetch(`${window.INROAD_API_BASE}/api/health`);

    if (!res.ok) throw new Error("API health check failed");

    return res.json();

  },



  async uploadResume(file) {

    const form = new FormData();

    form.append("file", file);

    const headers = await this._headers(false);

    delete headers["Content-Type"];



    const res = await fetch(`${window.INROAD_API_BASE}/api/resume/upload`, {

      method: "POST",

      headers,

      body: form,

    });

    const data = await res.json();

    if (!res.ok) {

      throw new Error(data.detail || "Resume upload failed");

    }

    return data;

  },



  async getProfile() {

    const res = await fetch(`${window.INROAD_API_BASE}/api/profile`, {

      headers: await this._headers(false),

    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Failed to load profile");

    return data.profile;

  },



  async saveProfile(profile) {

    const res = await fetch(`${window.INROAD_API_BASE}/api/profile`, {

      method: "PUT",

      headers: await this._headers(),

      body: JSON.stringify(profile),

    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Failed to save profile");

    return data.profile;

  },



  async analyze(payload) {

    const res = await fetch(`${window.INROAD_API_BASE}/analyze`, {

      method: "POST",

      headers: await this._headers(),

      body: JSON.stringify(payload),

    });

    const data = await res.json();

    if (!res.ok) {

      throw new Error(data.detail || data.message || "Analysis failed");

    }

    return data;

  },



  async generateOutreach(opportunityId, candidateName = "Candidate") {

    const data = InRoadStore.load();

    const opportunity = InRoadStore.getOpportunity(opportunityId);

    if (!opportunity) {

      throw new Error("Opportunity not found. Run analysis first.");

    }

    const res = await fetch(`${window.INROAD_API_BASE}/outreach`, {

      method: "POST",

      headers: await this._headers(),

      body: JSON.stringify({

        opportunity_id: opportunityId,

        candidate_name: candidateName,

        opportunity,

        candidate_profile: data?.candidate_profile || null,

      }),

    });

    const resData = await res.json();

    if (!res.ok) {

      throw new Error(resData.detail || "Outreach generation failed");

    }

    return resData;

  },

};



window.InRoadAPI = InRoadAPI;

