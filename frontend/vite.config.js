import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  root: ".",
  publicDir: "public",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        index: resolve(__dirname, "index.html"),
        analyze: resolve(__dirname, "analyze.html"),
        agents: resolve(__dirname, "agents.html"),
        opportunity: resolve(__dirname, "opportunity.html"),
        history: resolve(__dirname, "history.html"),
      },
    },
  },
  server: {
    port: 5500,
    open: "/index.html",
  },
  preview: {
    port: 5500,
  },
});
