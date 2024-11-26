import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: "/",
		alias: "/scga",
		// redirect: '/',
		name: 'scga',
		component: () => import ("@/views/scga.vue"),
	},
	
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
