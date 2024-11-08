import { createApp } from "vue";
import { createVuetify } from "vuetify";

export default createVuetify({
	defaults: {
		global: {
			ripple: false,
		},
		VSheet: {
			elevation: 4,
		},
	},
});
