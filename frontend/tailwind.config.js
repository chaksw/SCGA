/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./src/**/*.{vue,html,js}"],
	theme: {
		extend: {
			colors: {
				primary: {
					100: "#31343d",
					200: "#9e9e9e",
					300: "#212329",
					700: "#101114",
				},
				secondary: {
					100: "#E2E2D5",
					200: "#888883",
				},
			},
		},
	},
	plugins: [],
};
