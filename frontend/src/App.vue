<template>
	<div>
		<v-app>
			<Navbar />
			<v-main>
				<router-view></router-view>
			</v-main>
			<Footer />
		</v-app>
	</div>
</template>

<script>
import Header from "./components/Header.vue";
import Navbar from "./components/Navbar.vue";
import Sidebar from "./components/Sidebar.vue";
import Footer from "./components/Footer.vue";

export default {
	components: {
		Header,
		Navbar,
		Sidebar,
		Footer,
	},
};
</script>

<style>
/* Additional global styles if needed */
</style>
