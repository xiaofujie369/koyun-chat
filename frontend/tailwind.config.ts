import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172033",
        mist: "#f5f7fb",
        line: "#dce3ef",
        brand: "#2563eb",
        leaf: "#14b8a6",
        sun: "#f59e0b"
      },
      boxShadow: {
        panel: "0 18px 50px rgba(23, 32, 51, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;
