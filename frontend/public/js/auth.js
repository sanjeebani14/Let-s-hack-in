/**
 * Firebase Authentication + role-based session for InRoad.
 */
const InRoadAuth = {
  _app: null,
  _auth: null,
  _ready: null,
  _config: null,
  _user: null,
  _initError: null,

  async init() {
    if (this._ready) return this._ready;

    this._ready = (async () => {
      this._initError = null;
      let res;
      try {
        res = await fetch(`${window.INROAD_API_BASE}/api/config/firebase`);
      } catch {
        this._initError =
          "Cannot reach the API. Start the server from the project folder: python main.py — then open http://localhost:8000/login.html";
        return false;
      }

      if (!res.ok) {
        this._initError = `API error (${res.status}). Run python main.py and use http://localhost:8000`;
        return false;
      }

      const data = await res.json();
      this._config = data;

      if (!data.configured || !data.config?.apiKey) {
        this._initError =
          "Firebase web keys missing. Add FIREBASE_API_KEY and FIREBASE_PROJECT_ID to .env in the project root, then restart python main.py";
        return false;
      }

      if (typeof firebase === "undefined") {
        this._initError = "Firebase SDK failed to load. Check your internet connection and refresh.";
        return false;
      }

      try {
        if (firebase.apps && firebase.apps.length) {
          this._app = firebase.app();
        } else {
          this._app = firebase.initializeApp(data.config);
        }
        this._auth = firebase.auth();
        
        await new Promise((resolve) => {
          let initial = true;
          this._auth.onAuthStateChanged((user) => {
            this._user = user;
            window.dispatchEvent(new CustomEvent("inroad-auth-changed", { detail: user }));
            if (initial) {
              initial = false;
              resolve();
            }
          });
        });
        
        return true;
      } catch (err) {
        this._initError = err.message || "Failed to initialize Firebase";
        return false;
      }
    })();

    return this._ready;
  },

  async _ensureAuth() {
    await this.init();
    if (!this._auth) {
      throw new Error(this._initError || "Firebase auth unavailable");
    }
  },

  async getIdToken() {
    await this._ensureAuth();
    const user = this._auth?.currentUser;
    if (!user) return null;
    return user.getIdToken();
  },

  currentUser() {
    return this._auth?.currentUser || null;
  },

  async register(email, password, role, displayName = "") {
    await this._ensureAuth();

    const cred = await this._auth.createUserWithEmailAndPassword(email, password);
    if (displayName) {
      await cred.user.updateProfile({ displayName });
    }

    await this.syncRole(role, displayName);
    return cred.user;
  },

  async login(email, password) {
    await this._ensureAuth();
    const cred = await this._auth.signInWithEmailAndPassword(email, password);
    return cred.user;
  },

  async signInWithGoogle(roleIfNew = "student", forceRoleSync = false) {
    await this._ensureAuth();

    const provider = new firebase.auth.GoogleAuthProvider();
    provider.addScope("email");
    provider.addScope("profile");
    provider.setCustomParameters({ prompt: "select_account" });

    const cred = await this._auth.signInWithPopup(provider);
    const displayName = cred.user.displayName || cred.user.email?.split("@")[0] || "";

    let profile = null;
    try {
      profile = await this.fetchProfile();
    } catch {
      profile = null;
    }

    const isNewUser = !profile?.created_at;
    if (forceRoleSync || isNewUser) {
      try {
        await this.syncRole(roleIfNew, displayName);
        profile = await this.fetchProfile();
      } catch (syncErr) {
        console.warn("Profile sync skipped or failed — proceeding with local session.", syncErr);
        profile = { role: roleIfNew, email: cred.user.email };
      }
    }

    return { user: cred.user, profile };
  },

  async logout() {
    await this.init();
    if (this._auth) await this._auth.signOut();
    InRoadStore.clear();
    sessionStorage.removeItem("inroad_user_profile");
  },

  async syncRole(role, displayName = "") {
    const token = await this.getIdToken();
    if (!token) return null;

    const res = await fetch(`${window.INROAD_API_BASE}/api/auth/sync`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ role, display_name: displayName }),
    });
    const data = await res.json();
    if (!res.ok) {
      const msg = data.detail || "Failed to sync account role";
      if (res.status === 401) {
        throw new Error(`${msg}. Sign in again.`);
      }
      if (res.status === 503) {
        throw new Error(
          "Server profile storage unavailable. Add firebase-service-account.json to the project root (see .env). Google sign-in may still work locally."
        );
      }
      throw new Error(msg);
    }
    sessionStorage.setItem("inroad_user_profile", JSON.stringify(data.user));
    return data.user;
  },

  async fetchProfile() {
    const token = await this.getIdToken();
    if (!token) return null;

    const res = await fetch(`${window.INROAD_API_BASE}/api/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    if (!res.ok) {
      if (res.status === 401) return null;
      throw new Error(data.detail || "Failed to load profile");
    }
    sessionStorage.setItem("inroad_user_profile", JSON.stringify(data.profile));
    return data.profile;
  },

  getCachedProfile() {
    const raw = sessionStorage.getItem("inroad_user_profile");
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  },

  async requireAuth(redirectTo = "/login.html") {
    await this.init();
    if (!this.currentUser()) {
      window.location.href = redirectTo;
      return null;
    }
    let profile = this.getCachedProfile();
    if (!profile) {
      try {
        profile = await this.fetchProfile();
      } catch {
        profile = { role: "student" };
      }
    }
    return { user: this.currentUser(), profile };
  },

  redirectByRole(profile) {
    const role = profile?.role || "student";
    if (role === "recruiter") {
      window.location.href = "/recruiter.html";
      return;
    }
    window.location.href = "/dashboard.html";
  },
};

window.InRoadAuth = InRoadAuth;
