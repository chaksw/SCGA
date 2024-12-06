<template>
    <div>
        <el-table-v2
            fixed 
            :columns="fixedColumns" 
            :data="data"
            :header-height="[50, 40, 50]"
            :header-class="headerClass"
            :width="700"
            :height="400">
        <template #header="props">
            <customized-header v-bind="props"/>
        </template>

        </el-table-v2>
    </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>