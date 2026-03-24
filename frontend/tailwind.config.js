/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../web/templates/**/*.html",
    "../web/static/**/*.js",
    "./css/*.css",
  ],
  theme: {
    extend: {
      fontFamily: {
        syne:   ['Syne', 'system-ui', 'sans-serif'],
        dm:     ['DM Sans', 'system-ui', 'sans-serif'],
      },
      colors: {
        pitch:  '#050d1a',
        navy:   '#0c1f3d',
        cobalt: '#1243a8',
        azure:  '#1f6feb',
        sky:    '#5ea5f8',
        foam:   '#c8e4fd',
        chalk:  '#f4f7fd',
      },
      borderRadius: {
        card: '1.25rem',
        btn:  '0.625rem',
      },
      boxShadow: {
        card: '0 24px 60px -8px rgba(5,13,26,.18)',
        nav:  '0 8px 32px -4px rgba(5,13,26,.28)',
        btn:  '0 4px 14px rgba(31,111,235,.4)',
      },
      keyframes: {
        'fade-in': {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-up': {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-in':  'fade-in 0.45s ease both',
        'slide-up': 'slide-up 0.4s cubic-bezier(0.22,1,0.36,1) both',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
