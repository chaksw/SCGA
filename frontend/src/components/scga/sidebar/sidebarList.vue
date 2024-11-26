<template>
	<el-menu :default-active="selectedIndex" class="uncpllapsed-sidebar-list">
		<el-menu-item index="0" class="sidebar-item">
			<el-icon><Document /></el-icon>
			<p>Current</p>
		</el-menu-item>
		<el-menu-item index="1" class="sidebar-item">
			<el-icon><Files /></el-icon>
			<p>Previous</p>
		</el-menu-item>
	</el-menu>
</template>

<script setup>
	import { ref } from "vue";
	const selectedIndex = ref("0");
</script>

<style lang="css" scoped>
	.uncpllapsed-sidebar-list {
		display: flex;
		flex-direction: column;
		justify-content: top;
		align-items: center;
		width: 25%;
		padding: 8px 0;
		min-height: 100vh;
	}
	.sidebar-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		font-size: 14px;
		padding-top: 12px;
		line-height: 30px;
	}
</style>
