<template>
	<el-container>
		<!-- header -->
		<el-header>
			<navigation />
		</el-header>
		<router-view />
	</el-container>
	<!-- <el-footer>Footer</el-footer> -->
</template>

<script setup>
	import navigation from "@/components/navBar.vue";
</script>

<style lang="css" scoped></style>
