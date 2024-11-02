<template>
    <el-container class="layout-container">
        <el-header>
            <f-header />
        </el-header>
        <el-container class="small-container">
            <el-aside>
                <f-menu></f-menu>
            </el-aside>
            <el-main>
                <router-view>
                </router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import FHeader from './components/FHeader.vue'
import FMenu from './components/FMenu.vue'
</script>

<style>
.layout-container {
    height: 100vh;
}

.layout-container .el-header {
    height: 80px;
}
.layout-container .el-aside {
    transition: all 0.2s;
    width: 170px;
    bottom: 0px;
}
.layout-container .el-menu {
    width: 170px;
}
.layout-container .el-main {
    bottom: 0px;
}

.small-container {
    bottom: 0px;
}

.fade-enter-from{
    opacity: 0;
}
.fade-enter-to{
    opacity: 1;
}
.fade-leave-from{
    opacity: 1;
}
.fade-leave-to{
    opacity: 0;
}
.fade-enter-active,
.fade-leave-active{
    transition: all 0.3s;
}
.fade-enter-active{
    transition-delay: 0.3s;
}
</style>