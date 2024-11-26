<template>
	<el-table :data="uncoverages" style="width: 100%" max-height="750">
		<el-table-column fixed prop="root.root.name" label="Module" />

		<el-table-column fixed prop="root.name" label="Function Name" />

		<el-table-column type="expand">
			<template #default="props">
				<div m="4">
					<h3>Uncovered Instrumented SW Line:</h3>
					<p m="t-0 b-2">
						{{ props.row.uncovered_instrument_sw_line }}
					</p>
				</div>
			</template>
		</el-table-column>

		<el-table-column prop="uncovered_sw_line" label="Uncovered SW Line #" />

		<!-- <el-table-column
			prop="uncovered_instrument_sw_line"
			label="Uncovered Instrumented SW Line #"
			
		/> -->
		<el-table-column prop="requirement_id" label="Requirement ID" />
		<el-table-column prop="coverage" label="Analyst" />

		<el-table-column prop="_class" label="Class" />

		<el-table-column prop="analysis_summary" label="Analysis Summary" />

		<el-table-column
			prop="correction_summary"
			label="Corrective Action Summary"
		/>
		<el-table-column prop="" label="Issue" />
		<el-table-column prop="PAR_SCR" label="Accplicable" />
		<el-table-column prop="comment" label="Comment" />
	</el-table>
</template>

<script setup>
	import { inject, ref, watch, toRef, onMounted } from "vue";
	// const module = inject("testExceptionModule");
	const props = defineProps({
		selectedModule: {
			type: Object,
		},
	});
	const selectedModule = toRef(props, "selectedModule");
	// console.log("test exception", selectedModule);
	
	const functions = ref();
	const uncoverages = ref([]);

	const processFunctions = (module) => {
		let funcs = [];
		for (const function_ of module.functions) {
			let func = function_;
			func.root = {};
			func.root.name = module.label;
			func.root.root = module.root;
			funcs.push(func);
			uncoverages.value = uncoverages.value.concat(
				processUnCoverages(func)
			);
		}
		console.log("uncoverage", uncoverages);
		return funcs;
	};

	const processUnCoverages = (func) => {
		let uncoverages = [];
		for (let i = 0; i < func.uncoverages.length; i++) {
			let uncoverage = func.uncoverages[i];
			uncoverage.root = {};
			uncoverage.root.name = func.function_name;
			uncoverage.root.root = func.root;
			uncoverages.push(uncoverage);
		}
		return uncoverages;
	};
	
	onMounted(() => {
		if (selectedModule) {
			console.log("test exception", selectedModule.value);
			functions.value = processFunctions(selectedModule.value);
			// console.log(functions.value);
		}
	});
</script>

<style lang="scss" scoped></style>
