<template>
	<!-- sidebar & divier & main -->
	<el-container>
		<sidebar @send-module="onSendModule" />
		<!-- divider -->
		<div>
			<el-divider
				direction="vertical"
				style="min-height: 100vh; height: 100%"
			></el-divider>
		</div>
		<!-- main -->
		<el-main>
			<div>
				<el-tabs
					v-model="moduleTabsValue"
					type="card"
					class="demo-tabs"
					closable
					@tab-remove="removeTab"
				>
					<el-tab-pane
						v-for="item in moduleTabs"
						:key="item.name"
						:label="item.title"
						:name="item.name"
					>
						<testPlan
							:selectedModule="item.content"
							v-if="isTestPlan"
						/>
						<testException :selectedModule="item.content" v-else />
					</el-tab-pane>
				</el-tabs>
			</div>
		</el-main>
	</el-container>
</template>

<script setup>
	import testPlan from "@/components/scga/testPlan.vue";
	import testException from "@/components/scga/testException.vue";
	import sidebar from "@/components/scga/sidebar/sidebar.vue";
	import axios from "axios";
	import { ref, provide, onMounted } from "vue";

	// scga list
	const data = ref([]);
	const baseline = ref("SCGA Workspace");
	const levels = ref(null);
	const selectedModule = ref();
	const testPlanModule = ref();
	const testExceptionModule = ref();

	const isTestPlan = ref(true);

	// tabs control
	let tabIndex = 0;
	const moduleTabsValue = ref("2");
	const moduleTabs = ref([]);

	const moduleAdded = (moduleValue) => {
		const tabs = moduleTabs.value;
		// console.log("tabs", tabs);
		// console.log("tabs length", tabs.length);
		// console.log(tabs);
		// see if the selected module already opened
		if (tabs) {
			for (const tab of tabs) {
				if (
					tab.title === moduleValue.label &&
					tab.root.name === moduleValue.root.name
				) {
					return true;
				}
			}
		}
		return false;
	};

	const addTab = (module) => {
		const newTabName = `${++tabIndex}`;
		moduleTabs.value.push({
			title: module.value.label,
			name: newTabName,
			content: module.value,
			root: module.value.root,
		});
		console.log(moduleTabs.value[moduleTabs.value.length - 1].content);
		// console.log(typeof(moduleTabs.value[0].content));
		moduleTabsValue.value = newTabName;
	};

	const removeTab = (targetName) => {
		const tabs = moduleTabs.value;
		let activeName = moduleTabsValue.value;
		if (activeName === targetName) {
			tabs.forEach((tab, index) => {
				if (tab.name === targetName) {
					const nextTab = tabs[index + 1] || tabs[index - 1];
					if (nextTab) {
						activeName = nextTab.name;
					}
				}
			});
		}
		moduleTabsValue.value = activeName;
		moduleTabs.value = tabs.filter((tab) => tab.name !== targetName);
	};

	// receive from sidebar treeview
	const onSendModule = (module) => {
		// for the first tab, selectedModule should be undefined
		if (!moduleAdded(module.value)) {
			// selectedModule.value = module.value;
			// console.log("on scga", selectedModule.value);
			// check if selected module from test plan or test exception
			if (module.value.root.name.includes("Test Plan")) {
				testPlanModule.value = module.value;
				// console.log("on scga", testPlanModule.value);
				isTestPlan.value = true;
				addTab(testPlanModule);
			} else {
				testExceptionModule.value = module.value;
				isTestPlan.value = false;
				addTab(testExceptionModule);
			}
		}
	};

	onMounted(async () => {
		await fetchScga();
	});

	const fetchScga = async () => {
		let url = "api/scgas";
		// get scga data
		await axios
			.get(url)
			.then((response) => {
				if (response.data) {
					data.value = locateCurrent(response.data.results)
					// console.log(data.value);
					baseline.value = data.value.baseline;
					levels.value = data.value.levels;
					levels.value.baseline = baseline.value;
				}
			})
			.catch((error) => {
				console.log(error);
			});
	};

	const locateCurrent = (scgasData) => {
		for (const scga of scgasData){
			if (scga.current === 'Y'){
				return scga
			}
		}
	}

	provide("baseline", baseline);
	provide("levels", levels);
	// provide("testPlanModule", testPlanModule);
	// provide("testExceptionModule", testExceptionModule);
	// provide("selectedModule", selectedModule);
</script>

<style lang="css" scoped>
	.demo-tabs > .el-tabs__content {
		padding: 32px;
		color: #6b778c;
		font-size: 32px;
		font-weight: 600;
	}
</style>
