const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
  ],
  theme: {
    colors: {
      white: colors.white,
      'sws': {
        main1: '#36b495',
        main2: '#e98787',
        accent1: '#e1e16c',
        accent2: '#80b5da',
        accent3: '#a295c6',
        gray1: '#f4f8fc',
        gray2: '#b5bdcb',
        gray3: '#5f5f5f',
        gray4: '#414141',
        success: '#36b495',
        error: '#ea493d',
        alert: '#eac736',
        normal: '#f4f8fc',
      },
    },
    extend: {
      colors: {
        rose: colors.rose,
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
