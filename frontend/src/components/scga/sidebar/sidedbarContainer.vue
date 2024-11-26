<template>
	<el-container>
		<!-- <sidebar-list /> -->
		<sidebar-tree @emit-module="onEmitModule" />
	</el-container>
</template>

<script setup>
	// import sidebarList from "./sidebarList.vue";
	import sidebarTree from "./sidebarTree.vue";

	const emit = defineEmits(['sendModule'])
	// send to sidebar.vue
	const onEmitModule = (module) => {
		// console.log("on container", module);
		emit("sendModule", module)
	};
</script>

<style lang="css" scoped></style>
