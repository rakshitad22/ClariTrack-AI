/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: {
          dark: '#111116',
          base: '#14141b',
        },
        card: {
          slate: '#1b1b24',
          hover: '#22222e',
        },
        accent: {
          magenta: '#d946ef',
          purple: '#8b5cf6',
          pink: '#ec4899',
          rose: '#f43f5e',
          emerald: '#10b981',
          teal: '#14b8a6',
          cyan: '#06b6d4',
        }
      },
      backgroundImage: {
        'accent-gradient': 'linear-gradient(to right, #d946ef, #8b5cf6)',
        'emerald-gradient': 'linear-gradient(to right, #10b981, #14b8a6)',
        'mesh-glow': 'radial-gradient(at 0% 0%, rgba(217, 70, 239, 0.08) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.08) 0px, transparent 50%), radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.05) 0px, transparent 50%)',
      }
    },
  },
  plugins: [],
}
