/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(217 10% 20%)",
        input: "hsl(217 10% 20%)",
        ring: "hsl(142 76% 36%)",
        background: "hsl(222 47% 5%)",
        foreground: "hsl(210 20% 90%)",
        primary: {
          DEFAULT: "hsl(142 76% 45%)",
          foreground: "hsl(222 47% 5%)",
        },
        secondary: {
          DEFAULT: "hsl(217 10% 15%)",
          foreground: "hsl(210 20% 90%)",
        },
        destructive: {
          DEFAULT: "hsl(0 84% 60%)",
          foreground: "hsl(210 20% 98%)",
        },
        muted: {
          DEFAULT: "hsl(217 10% 15%)",
          foreground: "hsl(215 10% 60%)",
        },
        accent: {
          DEFAULT: "hsl(217 10% 20%)",
          foreground: "hsl(142 76% 45%)",
        },
        popover: {
          DEFAULT: "hsl(222 47% 8%)",
          foreground: "hsl(210 20% 90%)",
        },
        card: {
          DEFAULT: "hsl(222 47% 8%)",
          foreground: "hsl(210 20% 90%)",
        },
      },
      borderRadius: {
        lg: "0.5rem",
        md: "calc(0.5rem - 2px)",
        sm: "calc(0.5rem - 4px)",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "pulse-glow": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-glow": "pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
