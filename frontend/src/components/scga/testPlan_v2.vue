<template>
	<div style="height: 800px">
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
	import { onMounted, ref, toRef } from "vue";

	const keyMap = {
		id: "ID",
		module: 'File Name',
		functions_name: 'Function',
		function: "Function",
		analyst: 'Analyst',
		site: "Site",
		start_date: "Start Date",
		coverage: "Coverage",
		percent_coverage_Analysis: "Percent Analysis",
		percent_coverage_MCDC: "Percent MC/DC",
		total_coverage: "Total by SC Tool",
		covered: "Covered",
		branches: "Branches",
		pairs: "Pairs",
		statement: "Statements",
		total: 'Total',
		defect_classification: "Defect Classification",
		non_tech: "Non-Tech",
		process: "Process",
		tech: "Tech",
		oversight: "Oversight",

	}

	const props = defineProps({
		selectedModule: {
			type: Object,
		},
	});

	// 双向绑定： 将props中的selectdModule 和 该组件的selectedModule 双向绑定，让数据改变同步
	const selectedModule = toRef(props, "selectedModule");
	const functions = ref(selectedModule.value.functions);
	// let headers = []
	const columns = ref([]);
	const data = ref([]);

	const generateColumns = (headers, props) => {
		// Array.from 主要用于从类数组对象或可迭代对象创建一个新的数组
		// 如 Array.form({ 10 }) = [1,2,3,4,5,6,7,8,9]
		// Array.from(arrayLike, mapFn, thisArg)
		// arrayLike: 类数组对象或可迭代对象
		// mapFn （可选）： 一个函数，用来对每个元素执行某种操作，相当于数组的.map()
		// thisArg(可选)： 执行mapFn时的上下文
		// 用花括号包围 { 10 } 是因为Array.form需要接受一个类数组对象
		// map 是数组的实例方法，用于对数组的每个元素执行指定操作，并返回一个新的数组。
		// array.map(callback(currentValue, index, array), thisArg)
		// callback: 处理数组中每个元素的函数
		// thisArg(可选)：执行 callback 时绑定的上下文
		return headers.map((curValue, columnIndex) => ({
			...props, // 将 props 解构到列的配置对象中
			key: `${curValue}-${columnIndex}`,
			dataKey: `${curValue}-${columnIndex}`,
			title: `${keyMap[curValue]}`,
			// title: `${curValue}`,
			width: 180,
		}));
	};

	const generateData = (columns, values) =>
		// 为每一行建立数据
		Array.from(values).map((_, rowIndex) => {
			// reduce 语法,
			// array.reduce(callback, initialValue)
			// callback(accumularotr, currentValue, currentIndex, array)
			// accumulator: 累积值，表示上一次回调函数的返回值
			// currentValue： 当前正在处理的数组元素
			// currentIndex: 当前元素的索引 （可选）
			// array: 调用 reduce的数组本身
			return columns.reduce(
				// 为每一行的列元素建立（累积）数据
				(rowData, column, columnIndex) => {
					rowData[column.dataKey] = values[rowIndex][columnIndex];

					return rowData;
				},
				// 数组本身的元素 即 initialValue
				{
					id: `${rowIndex}`,
					parentId: null,
				}
			);
		});

	const extractKeysAndValues = (obj) => {
		let keys = [];
		let values = [];
		function recurseKeys(o) {
			for (let key in o) {
				// deconstruct automatically the object{}
				if (o.hasOwnProperty(key)) {
					keys.push(key);
					if (typeof o[key] === "object" && o[key] !== null) {
						recurseKeys(o[key]);
					} else {
						values.push(o[key]);
					}
				}
			}
		}
		recurseKeys(obj);
		return [keys, values];
	};

	const extractTableValue = (array) => {
		let valuesList = [];
		let keys = [];
		for (const obj of array) {
			let values = [];
			let curKeys = [];
			if (typeof obj === "object" && obj !== null) {
				[curKeys, values] = extractKeysAndValues(obj);
				if (!keys.length) keys = curKeys;
				// console.log(curKeys);
				// console.log(values);
				valuesList.push(values);
			}
		}
		return [keys, valuesList];
	};
	onMounted(() => {
		const [headers, values] = extractTableValue(functions.value);
		columns.value = generateColumns(headers);
		data.value = generateData(columns.value, values);
		// console.log("data", data);
	});
</script>

<style lang="css" scoped></style>
