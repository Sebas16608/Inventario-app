import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#FF4500',
          600: '#ea580c',
          700: '#c2410c',
        },
        secondary: {
          DEFAULT: '#1A1A1A',
          50: '#f3f3f3',
          100: '#e5e5e5',
          200: '#cccccc',
          300: '#b3b3b3',
          400: '#666666',
          600: '#333333',
          700: '#1A1A1A',
        },
        accent: {
          DEFAULT: '#FFD700',
          50: '#fffbe6',
          100: '#fff3cd',
          200: '#ffe69c',
          300: '#ffd700',
          400: '#ffc107',
        },
      },
    },
  },
  plugins: [],
}
export default config
