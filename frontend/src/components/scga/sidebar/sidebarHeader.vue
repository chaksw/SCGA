<template>
	<div>
		<!-- sidebar header -->
		<el-container class="sidebar-horizontal-header">
			<!-- Title & buttons -->
			<el-container class="sidebar-horizontal-header-content">
				<p>{{ baseline }}</p>
				<el-tooltip
					class="box-item"
					effect="dark"
					content="Import SCGA"
					placement="bottom"
					><el-button
						circle
						v-if="!isImported"
						@click="importScgaDialogVisible = true"
						><el-icon><Plus /></el-icon></el-button
				></el-tooltip>

				<!-- configure buttons -->
				<el-dropdown trigger="click" v-if="isImported">
					<span class="el-dropdown-link">
						<el-icon><MoreFilled /></el-icon>
					</span>
					<template #dropdown>
						<el-dropdown-menu>
							<el-dropdown-item
								@click="configureDrawerVisible = true"
								style="
									width: 150px;
									display: flex;
									justify-content: space-between;
								">
								Configure
								<el-icon style="font-size: 18px"
									><Setting /></el-icon
							></el-dropdown-item>
							<el-dropdown-item
								style="
									width: 150px;
									color: red;
									display: flex;
									justify-content: space-between;
								">
								Delete
								<el-icon style="font-size: 18px"
									><DocumentDelete
								/></el-icon>
							</el-dropdown-item>
						</el-dropdown-menu>
					</template>
				</el-dropdown>
			</el-container>
			<!-- import button -->
			<!-- ref 是 Vue 提供的一个指令，用来直接引用 DOM 元素或组件实例，便于在脚本中操作它们。可以理解为一种快捷的方式来访问特定的 DOM 或组件。 -->
			<!-- ref="upload" 会将当前的 el-upload 组件实例引用到 setup 或 data 中定义的 ref 对象上。 -->

			<el-divider style="margin: 10px 0 0 0"></el-divider>
		</el-container>

		<!-- current scga import dialog -->
		<el-dialog v-model="importScgaDialogVisible" width="500">
			<template #header>
				<div class="drawer-header">
					<el-icon style="padding-right: 7px; font-size: 24px"
						><Plus
					/></el-icon>
					<h4>SCGA Import</h4>
				</div>
			</template>
			<el-form ref="ruleFormRef" :model="scgaForm" :rules="rules">
				<el-form-item
					prop="project"
					label="Project: "
					:label-width="importFormLabelWidth"
					label-position="left">
					<el-select
						clearable
						v-model="scgaForm.project"
						placeholder="Please select the Project">
						<el-option label="CA22" value="CA22" />
						<el-option label="GS" value="GS" />
					</el-select>
				</el-form-item>
				<el-form-item
					prop="function"
					label="Function: "
					:label-width="importFormLabelWidth"
					label-position="left">
					<el-select
						clearable
						v-model="scgaForm.function"
						placeholder="Please select the Function">
						<el-option label="GGF" value="GGF" />
						<el-option label="MWF" value="MWF" />
						<el-option label="UTIL" value="UTIL" />
					</el-select>
				</el-form-item>
				<el-form-item
					prop="file"
					label=""
					:label-width="0"
					label-position="left">
					<el-upload
						ref="upload"
						:on-change="handleChange"
						:on-exceed="handleExceed"
						:before-remove="beforeRemove"
						:limit="1"
						list-type="text"
						accept=".pkl, .xlsm"
						:auto-upload="false">
						<template #trigger>
							<el-button type="success">Select file</el-button>
						</template>
						<template #tip>
							<div class="el-upload__tip">
								SCGA file with format *.pkl | *.xlsm
							</div>
						</template>
					</el-upload>
					<!-- <p v-for="(item, index) in fileList" :key="index">
						<span>{{ item.name }}</span>
					</p> -->
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="handleCancel('Import')">
						Cancel
					</el-button>
					<el-button
						type="primary"
						@click="handleSubmitImport(ruleFormRef)">
						Confirm
					</el-button>
				</div>
			</template>
		</el-dialog>

		<!-- pas scga configuration drawer -->
		<el-drawer
			v-model="configureDrawerVisible"
			:direction="direction"
			size="30%">
			<template #header>
				<div class="drawer-header">
					<el-icon style="padding-right: 5px; font-size: 28px"
						><Setting
					/></el-icon>
					<h4>PAS SCGA Configuration</h4>
				</div>
			</template>
			<el-form ref="ruleFormRef" :model="pasScgasForm" :rules="rules">
				<el-form-item
					prop="project"
					label="Project: "
					:label-width="configFormLabelWidth"
					label-position="left">
					<el-select
						clearable
						v-model="pasScgasForm.project"
						placeholder="Please select the Project">
						<el-option label="CA22" value="CA22" />
						<el-option label="GS" value="GS" />
					</el-select>
				</el-form-item>
				<el-form-item
					prop="function"
					label="Function: "
					:label-width="configFormLabelWidth"
					label-position="left">
					<el-select
						clearable
						v-model="pasScgasForm.function"
						placeholder="Please select the Function">
						<el-option label="GGF" value="GGF" />
						<el-option label="MWF" value="MWF" />
						<el-option label="UTIL" value="UTIL" />
					</el-select>
				</el-form-item>
				<el-form-item
					prop="path"
					label="SCGAs Path: "
					:label-width="configFormLabelWidth"
					label-position="left">
					<el-input
						clearable
						v-model="pasScgasForm.path"
						autocomplete="off" />
				</el-form-item>
				<el-form-item style="flex: auto">
					<el-button @click="handleCancel('Configuration')">
						Cancel
					</el-button>
					<el-button
						type="primary"
						@click="handleSumbitConfig(ruleFormRef)">
						Confirm
					</el-button>
				</el-form-item>
			</el-form>
			<!-- <template #footer>
			<el-form-item style="flex: auto">
				<el-button @click="handleCancel('Configuration')">
					Cancel
				</el-button>
				<el-button type="primary" @click="handleSumbitConfig">
					Confirm
				</el-button>
			</el-form-item>
		</template> -->
		</el-drawer>
	</div>
</template>

<script setup>
	import axios, { AxiosError } from "axios";
	import { ref, inject, onMounted, watch, reactive, nextTick } from "vue";
	import { ElMessage, ElMessageBox, genFileId } from "element-plus";
	// v-model 和 ref 的核心区别
	// v-model 是用于 双向绑定数据 的。它通常绑定组件的值或者用户输入的值。
	// ref 是为了获取 DOM 或组件实例的引用。
	// 这里的upload只作为组件实例，只包含一些clearFiles(), submit()等方法，不能用于发送请求
	const upload = ref(null); // instance of import
	let importFile = null; // 存储选中的文件
	const fileName = ref(null);
	const baseline = inject("baseline");
	const isImported = ref(false);
	const fileList = ref([]);
	const ruleFormRef = ref();
	const rules = reactive({
		project: [
			{
				required: true,
				message: "Please choose a porject",
				trigger: "blur",
			},
		],
		function: [
			{
				required: true,
				message: "Please select a function",
				trigger: "blur",
			},
		],
		path: [
			{
				required: true,
				message: "Please entre a valid path",
				trigger: "blur",
			},
		],
		file: [
			{
				required: true,
				message: "Please choose the scga file",
				trigger: "blur",
			},
		],
	});
	const configFormLabelWidth = "120px";
	const importFormLabelWidth = "120px";

	// current scga import dialog
	const importScgaDialogVisible = ref(false);
	const scgaForm = reactive({
		project: "",
		function: "",
		file: "",
		current: true,
	});

	// pas scga configuration drawer
	const configureDrawerVisible = ref(false);

	const pasScgasForm = reactive({
		project: "",
		function: "",
		path: "",
		current: false,
	});

	const handleChange = (uploadFile, uploadFiles) => {
		importFile = uploadFile.raw;
		fileName.value = uploadFile.name;
		console.log("filename object", fileName);
		console.log("filename", fileName.value);
	};

	const handleExceed = (files) => {
		upload.value.clearFiles();
		const file = files[0];
		file.uid = genFileId();
		upload.value.handleStart(file);
	};

	const submitImport = async () => {
		await ElMessageBox.confirm(`Confirm the import of ${fileName.value} ?`);

		// create form
		const formData = new FormData();
		console.log(importFile);
		formData.append("file", importFile); // `raw` 是 ElUpload 文件对象的实际文件数据

		// send to backend
		await axios
			.post("api/upload-scgas/", formData, {
				headers: {
					"Content-Type": "multipart/form-data", // must have
				},
			})
			.then((response) => {
				// console.log(upload.value);
				ElMessage.success(
					`File ${fileName.value} import successfully!`
				);
				// get response
				console.log("Response from server: ", response.data);
				location.reload();
				// upload.clearFiles(); //clear upload component
				// reset status
			})
			.catch((error) => {
				// handle cancel or fail of import
				if (axios.isCancel(error) || error === "cancel") {
					ElMessage.info("File upload canceled");
				} else {
					console.error("Upload error: ", error.data.detail);
					ElMessage.error("Fail to upload file.", error.data.detail);
				}
			});
	};

	const beforeRemove = (uploadFile, uploadFiles) => {
		return ElMessageBox.confirm(
			`Cancel the import of ${uploadFile.name} ?`
		).then(
			() => {
				upload.value.clearFiles();
				ElMessage.info("File upload canceled");
				true;
			},
			() => false
		);
	};

	const handleCancel = (cancelInfo) => {
		configureDrawerVisible.value = false;
		importScgaDialogVisible.value = false;
		ElMessage({
			type: "info",
			message: `${cancelInfo} cancaled.`,
		});
	};

	const handleSumbitConfig = async (formEl) => {
		if (!formEl) return;
		await formEl.validate((valid, fields) => {
			if (valid) {
				ElMessageBox.confirm(
					"Confirm the configure PAS SCGAs on this path ?"
				)
					.then(() => {
						console.log("scga", pasScgasForm);
						axios
							.post("api/upload-scgas/", pasScgasForm, {
								headers: {
									"Content-Type": "application/json",
									// Authorization: "Bearer your_token_here", // 如果需要身份验证的话
								},
							})
							.then((response) => {
								ElMessage.success(`Configure successfully!`);
								// get response
								console.log(
									"Response from server: ",
									response.data
								);
							}) // axios post request error
							.catch((error) => {
								console.error(
									"Configure error: ",
									error.response.data
								);
								ElMessage.error(
									`Fail to configure. ${error.response.data}`
								);
							});
					}) // submit error
					.catch((error) => {
						// do nothing
						ElMessage.error(error);
						console.log(error);
					});
			} else {
				console.log("error submit", fields);
			}
		});
	};

	const handleSubmitImport = async (formEl) => {
		if (!formEl) return;
		await formEl.validate((valid, fields) => {
			if (valid) {
				submitImport();
			} else {
				console.log("error submit", fields);
			}
		});
	};

	onMounted(() => {
		isImported.value = baseline.value === "SCGA Workspace" ? false : true;
	});

	watch(() => {
		isImported.value = baseline.value === "SCGA Workspace" ? false : true;
	});
</script>

<style lang="css" scoped>
	.sidebar-horizontal-header {
		display: flex;
		flex-direction: column;
		font-size: 15px;
	}
	.sidebar-horizontal-header-content {
		display: flex;
		justify-content: space-between;
		padding: 0 10px;
		align-items: center;
		font-weight: 600;
	}
	.import-area {
		justify-content: space-between;
		align-items: center;
		padding: 0 10px;
		padding-top: 10px;
	}
	.drawer-header {
		display: flex;
		align-items: center;
		font-weight: bold;
		font-size: 20px;
	}
	.el-button {
		font-weight: 500;
		font-size: 14px;
	}
</style>
