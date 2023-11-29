/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./templates/**/*.html", "./templates/**/**/*.html"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
    },
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
}
