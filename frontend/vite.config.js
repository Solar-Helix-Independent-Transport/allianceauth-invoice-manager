import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  plugins: [react()],
  server: {
    port: 3002,
    proxy: {
      "/invoice/api/": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    sourcemap: true,
    manifest: true,
    outDir: "build/static/",
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          let extType = assetInfo.name.split(".").at(1);
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = "img";
          }
          // fake the path, we copy them over properly later
          return `static/invoices/static/${extType}/[name]-[hash][extname]`;
        },
        manualChunks(id) {
          // creating a chunk to react routes deps. Reducing the vendor chunk size
          if (id.includes("react-router-dom") || id.includes("react-router")) {
            return "@react-router";
          }
          if (
            id.includes("react-query") ||
            id.includes("react-select") ||
            id.includes("javascript-time-ago")
          ) {
            return "@libs";
          }
        },
      },
    },
  },
});
