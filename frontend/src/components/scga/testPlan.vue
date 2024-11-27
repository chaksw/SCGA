<template>
	<el-table
		:data="functions"
		style="width: 100%"
		max-height="800"
		table-layout="auto">
		<el-table-column prop="process" label="Process" fixed />
		<el-table-column fixed prop="function_name" label="Function Name" />
		<el-table-column prop="analyst" label="Analyst" />
		<el-table-column prop="site" label="Site" />
		<el-table-column prop="start_date" label="Start Date" />
		<el-table-column prop="coverage" label="Coverage">
			<el-table-column
				prop="coverage.percent_coverage_MCDC"
				label="Percent MC/DC"
				:formatter="
					(value) =>
						(value.coverage.percent_coverage_MCDC * 100).toFixed(
							2
						) + '%'
				" />
			<el-table-column
				prop="coverage.percent_coverage_Analysis"
				label="Percent Analysis"
				:formatter="
					(value) =>
						(
							value.coverage.percent_coverage_Analysis * 100
						).toFixed(2) + '%'
				" />
			<el-table-column
				prop="coverage.total_coverage"
				label="Total by SC Tool"
				:formatter="
					(value) =>
						(value.coverage.total_coverage * 100).toFixed(2) + '%'
				" />
		</el-table-column>
		<el-table-column
			prop=""
			label="Module Structure Data (Conditions, Decisions and statements)">
			<el-table-column prop="covered" label="Covered">
				<el-table-column prop="covered.branches" label="Branches" />
				<el-table-column prop="covered.pairs" label="Pairs" />
				<el-table-column prop="covered.statement" label="Statements" />
			</el-table-column>
			<el-table-column prop="total" label="Total">
				<el-table-column
					prop="total.branches"
					label="Branches" />
				<el-table-column
					prop="total.pairs"
					label="Pairs" />
				<el-table-column prop="total.statement" label="Statements" />
			</el-table-column>
		</el-table-column>
		<el-table-column prop="oversight" label="Oversight" />
		<el-table-column
			prop="defect_classification"
			label="Defect Classification">
			<el-table-column prop="defect_classification.tech" label="Tech" />
			<el-table-column
				prop="defect_classification.non_tech"
				label="No-Tech" />
			<el-table-column
				prop="defect_classification.process"
				label="Process" />
		</el-table-column>
	</el-table>
</template>

<script setup>
	import { ref, toRef } from "vue";

	const props = defineProps({
		selectedModule: {
			type: Object,
		},
	});
	const functions = ref();
	const selectedModule = toRef(props, "selectedModule");
	functions.value = selectedModule.value.functions;
	console.log("testplan", selectedModule.value);
	console.log("testplan functions", selectedModule.value.functions);

	// const functions = ref();
	// onMounted(() => {
	// 	if (props.selectedModuleValue) {
	// 		functions.value = props.selectedModuleValue.functions;
	// 	}
	// });

	const processFcuntions = (funcs) => {};
</script>

<style lang="css" scoped></style>
