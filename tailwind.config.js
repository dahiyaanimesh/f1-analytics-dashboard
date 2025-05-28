/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'f1-red': '#e60012',
        'f1-dark': '#15151e',
        'f1-gray': '#38383f',
        'f1-silver': '#c0c0c0',
        'f1-gold': '#ffd700',
      },
      fontFamily: {
        'f1': ['Formula1', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

