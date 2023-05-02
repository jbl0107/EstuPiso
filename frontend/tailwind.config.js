/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      inset: ['responsive', 'hover', 'focus'],
      backgroundImage: {
        'img': "url('/Fondo 3600x2750.png')",
      },
      borderColor: {
        'white-50': 'rgba(255, 255, 255, 0.6)',
      },
      borderRadius: {
        '20': '20px',
      },
      

    },
  },
  plugins: [],
}