<template>
	<div class="nav">
		<el-menu mode="horizontal" default-active="1">
			<el-menu-item index="0" alt="logo" class="menu-item">
				<a href="/">
					<el-icon><Menu /></el-icon>
				</a>
			</el-menu-item>
			<el-menu-item index="1" class="menu-item">
				<a href="/scga">
					SCGA
				</a>
			</el-menu-item>
			<el-menu-item index="2" class="menu-item">TRS</el-menu-item>

			<el-menu-item index="3" class="menu-item">RA</el-menu-item>
		</el-menu>
	</div>
</template>

<script setup></script>

<style lang="css" scoped>
	.nav {
		margin-left: -20px;
	}
	.el-menu {
		padding-left: 10px;
	}

	.el-menu--horizontal {
		--el-menu-horizontal-height: 60px;
	}
	.menu-item {
		font-size: 16px !important;
	}
	.sub-menu-item {
		font-size: 14px !important;
	}
</style>
