/** Backend API base URL — set VITE_INROAD_API_BASE at build time for production */
window.INROAD_API_BASE =
  window.INROAD_API_BASE ||
  (typeof import.meta !== "undefined" && import.meta.env?.VITE_INROAD_API_BASE) ||
  "http://localhost:8000";
