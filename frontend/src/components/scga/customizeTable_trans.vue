<template>
	<el-table-v2
		fixed
		:columns="fixedColumns"
		:data="data"
		:header-height="[50, 40, 50]"
		:header-class="headerClass"
		:width="700"
		:height="400">
		<template #header="props">
			<customized-header v-bind="props" />
		</template>
	</el-table-v2>
</template>

<script setup>
	import { ref } from "vue";
	import { TableV2FixedDir, TableV2Placeholder } from "element-plus";

	// 生成列的函数
	const generateColumns = (length = 10, prefix = "column-", props) =>
		Array.from({ length }).map((_, columnIndex) => ({
			...props,
			key: `${prefix}${columnIndex}`,
			dataKey: `${prefix}${columnIndex}`,
			title: `Column ${columnIndex}`,
			width: 150,
		}));

	// 生成数据的函数
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

	// 生成固定列和数据
	const columns = generateColumns(10);
	const data = generateData(columns, 200);
	// 固定前3列在左，14列及以上的在右，宽度为100
	const fixedColumns = columns.map((column, columnIndex) => {
		let fixed = undefined;
		if (columnIndex < 3) fixed = TableV2FixedDir.LEFT;
		if (columnIndex > 12) fixed = TableV2FixedDir.RIGHT;
		return { ...column, fixed, width: 100 };
	});

	// 表头类名函数
	const headerClass = (headerIndex) => {
		return headerIndex === 0 ? "first-header" : "other-header";
	};

	// 自定义表头组件
	const CustomizedHeader = {
		functional: true, // defined as a functional component of which render only depends on the props injected. 

		props: ["cells", "columns", "headerIndex"], // attributes that component received
		// cells: array of header cell
		// columns: array of columns
		// headerIndex: header row index
		render(h, { props }) { // render() is a render method in Vue
			// h used to create visual DOM
			const { cells, columns, headerIndex } = props;
			if (headerIndex === 2) return cells;

			const groupCells = [];
			let width = 0;
			let idx = 0;

			columns.forEach((column, columnIndex) => {
				if (column.placeholderSign === TableV2Placeholder)
					groupCells.push(cells[columnIndex]);
				else {
					width += cells[columnIndex].props.column.width;
					idx++;

					const nextColumn = columns[columnIndex + 1];
					if (
						columnIndex === columns.length - 1 ||
						nextColumn.placeholderSign === TableV2Placeholder ||
						idx === (headerIndex === 0 ? 4 : 2)
					) {
						groupCells.push(
							h(
								"div",
								{
									class: "flex items-center justify-center custom-header-cell",
									role: "columnheader",
									style: {
										...cells[columnIndex].props.style,
										width: `${width}px`,
									},
								},
								`Group width ${width}`
							)
						);
						width = 0;
						idx = 0;
					}
				}
			});

			return groupCells;
		},
	};
</script>
