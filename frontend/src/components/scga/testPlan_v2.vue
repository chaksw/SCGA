<template>
	<div style="height: 100vh">
		<el-auto-resizer>
			<template #default="{ height, width }">
				<el-table-v2
					:columns="columns"
					:data="data"
					:width="width"
					:height="height"
					fixed>
				</el-table-v2>
			</template>
		</el-auto-resizer>
	</div>
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
    console.log("testplan functions", selectedModule.value.functions);
	const generateColumns = (length = 10, prefix = "col-", props) =>
		Array.from({ length }).map((_, columnIndex) => ({
			...props,
			key: `${prefix}${columnIndex}`,
			dataKey: `${prefix}${columnIndex}`,
			title: `col ${columnIndex}`,
			width: 150,
		}));

	const generateData = (columns, length = 200, prefix = "row-") =>
		Array.from({ length }).map((_, rowIndex) => {
			return columns.reduce(
				(rowData, column, columnIndex) => {
					rowData[
						column.dataKey
					] = `Row ${rowIndex} - Col ${columnIndex}`;

					return rowData;
				},
				{
					id: `${prefix}${rowIndex}`,
					parentId: null,
				}
			);
		});

	const columns = generateColumns(10);
	const data = generateData(columns, 200);
	// console.log(columns);
	// console.log(data);
</script>

<style lang="css" scoped></style>
