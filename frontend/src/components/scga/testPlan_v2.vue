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

	const props = defineProps({
		selectedModule: {
			type: Object,
		},
	});

	// 双向绑定： 将props中的selectdModule 和 该组件的selectedModule 双向绑定，让数据改变同步
	const selectedModule = toRef(props, "selectedModule");
	const functions = ref(selectedModule.value.functions);
	const columns = ref([]);
	const data = ref([]);
	
	// console.log("testplan functions", functions.value);
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
			title: `${curValue}`,
			width: 180,
		}));
	};

	const generateData = (columns, functions, prefix = "row-") =>
		// 为每一行建立数据
		Array.from({ length }).map((_, rowIndex) => {
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
					rowData[
						column.dataKey
					] = `Row ${rowIndex} - Col ${columnIndex}`;

					return rowData;
				},
				// 数组本身的元素 即 initialValue
				{
					id: `${prefix}${rowIndex}`,
					parentId: null,
				}
			);
		});

	const extract_nested = (dict) => {
		let keys = [];
		let value = [];
		function recurseObject(obj) {
			for (const [key, val] of Object.entries(dict)) {
				
			}
		}
	};

	const generateTable = () => {
		let keys = [];
		let values = [];
		if (functions.value != null && typeof functions.value === "object") {
			for (arr of functions.value) {
			}
			keys = Object.keys(functions.value[0]);
			values = Object.values(functions.value[0]);
		}
		console.log("keys", keys);
		console.log("values", values);
		columns.value = generateColumns(keys);
		console.log(columns.value);
		const data = generateData(columns.value, 200);
	};
	generateTable();
</script>

<style lang="css" scoped></style>
