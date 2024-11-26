<template>
	<el-container class="treeview">
		<el-input
			v-model="filterText"
			placeholder="Search file"
			:prefix-icon="Search"
			clearable
			style="width: 100%" />
		<el-tree
			ref="treeRef"
			class="filter-tree"
			:data="treeViewData"
			:props="defaultProps"
			:filter-node-method="filterNode"
			@node-click="handleNodeClick"
			highlight-current
			style="max-width: 400px" />
	</el-container>
</template>

<script setup>
	import { Search } from "@element-plus/icons-vue";
	import { ref, inject, watch } from "vue";
	const filterText = ref("");
	const treeRef = ref();
	const defaultProps = {
		label: "label",
		children: "children",
	};
	const levels = inject("levels");
	// treeview data processed from levels
	const treeViewData = ref();

	const selectedModule = ref({});
	// define a emit method name: emitModule
	const emit = defineEmits(["emitModule"]);

	// level data process
	const processLevelData = (levels) => {
		let data = [];
		// for each level data
		for (let idx = 0; idx < levels.value.length; idx++) {
			let level = {};
			let testPlan = {};
			let testException = {};
			level.id = levels.value[idx].id;
			level.label = "Level " + levels.value[idx].level;
			level.baseline = levels.value.baseline;
			level.children = [];

			// test plan
			if (levels.value[idx].test_plan) {
				testPlan = precessTestPlanData(
					level.baseline,
					levels.value[idx].test_plan
				);
				level.children.push(testPlan);
			}
			// test exception
			if (levels.value[idx].test_exception) {
				testException = precessTesExceptionData(
					level.baseline,
					levels.value[idx].test_exception
				);
				level.children.push(testException);
			}
			if (level.children.length !== 0) {
				data.push(level);
			}
		}
		// console.log(data);
		return data;
	};

	const precessTestPlanData = (root, testPlanData) => {
		// console.log(testPlanData);
		let testPlan = {};
		testPlan.id = testPlanData.id;
		testPlan.label = testPlanData.sheet_name;
		testPlan.root = root;
		testPlan.lv_total_coverage = testPlanData.lv_total_coverage;
		// console.log(testPlan.lv_total_coverage);
		testPlan.children = processModulesData(testPlan.root, testPlanData);
		return testPlan;
	};

	const precessTesExceptionData = (root, testExceptionData) => {
		let testException = {};
		testException.id = testExceptionData.id;
		testException.label = testExceptionData.sheet_name;
		testException.root = root;
		testException.children = processModulesData(
			testException.root,
			testExceptionData
		);
		return testException;
	};

	const processModulesData = (superRoot, testData) => {
		let modules = [];
		const modulesData = testData.modules;
		for (let idx = 0; idx < modulesData.length; idx++) {
			let module = {};
			module.id = modulesData[idx].id;
			module.label = modulesData[idx].module_name;
			module.root = {};
			module.root.name = testData.sheet_name;
			module.root.root = superRoot;
			module.functions = modulesData[idx].functions;
			modules.push(module);
		}
		return modules;
	};

	// fetch levels data
	watch(() => {
		if (levels.value) {
			treeViewData.value = processLevelData(levels);
		}
	});

	// expand method
	watch(filterText, (val) => {
		treeRef.value.filter(val);
	});

	// filter method
	const filterNode = (value, data) => {
		if (!value) return true;
		return data.label.toLowerCase().includes(value.toLowerCase());
	};

	// handle node-click
	const handleNodeClick = (data) => {
		// emit module data
		if (data.hasOwnProperty("functions")) {
			selectedModule.value = data;
			// send to sidebar container -- delete container,
			// send to sidebar.vue
			emit("emitModule", selectedModule);
			// console.log(selectedModule.value);
		}
	};
</script>

<style lang="css" scoped>
	.treeview {
		display: flex;
		flex-direction: column;
		justify-content: top;
		padding: 10px;
	}
	.filter-tree {
		padding-top: 8px;
	}
</style>
