/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./dist/**/*.html",
    "./public/**/*.html",
    "./src/**/*.py"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
      },
      colors: {
        uai: {
          gold: '#6493B5',
          citCeleste: '#6493B5',
          goldHover: '#4e7b9d',
          citCelesteHover: '#4e7b9d',
          black: '#000000',
          charcoal: '#1f1f23',
          bgSoft: '#f8fafc',
          border: '#e2e8f0',
          navy: '#003865',
          citBlue: '#6493B5'
        }
      },
      boxShadow: {
        clean: '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        hover: '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
        widget: '0 20px 25px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.08)'
      }
    }
  },
  plugins: []
};
