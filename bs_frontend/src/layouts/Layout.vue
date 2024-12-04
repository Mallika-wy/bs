<template>
    <el-container class="layout-container">
        <el-header>
            <f-header />
        </el-header>
        <el-row class="row-container">
            <el-col class="hidden-sm-and-down menuV-col" :lg="4" :md="4" :sm="24" :xs="24" >
                <f-menu-v></f-menu-v>
            </el-col>
            <el-col class="hidden-md-and-up menuH-col":lg="4" :md="4" :sm="24" :xs="24">
                <f-menu-h></f-menu-h>
            </el-col>
            <el-col class="main":lg="20" :md="20" :sm="24" :xs="24">
                <router-view>
                </router-view>
            </el-col>
        </el-row>
    </el-container>
</template>

<script setup>
import FHeader from './components/FHeader.vue'
import FMenuH from './components/FMenuH.vue'
import FMenuV from './components/FMenuV.vue'
import 'element-plus/theme-chalk/display.css'
</script>

<style>
.layout-container {
    height: 100vh;
}

.layout-container .el-header {
    height: 80px;
}

.row-container {
    width: 100%;
    height: calc(100% - 80px);
}

.menuH-col {
  height: 10vh; /* 水平菜单列的高度为视口高度的10% */
  display: flex;
  justify-content: flex-end;
  align-items: center; /* 使菜单在其列中居中 */
  background-color: #ffffff; /* 菜单背景颜色 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 轻微的阴影 */
}

.menuV-col {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 使内容在垂直方向上分散对齐 */
  height: calc(100% - 80px);
}

.main {
    height: calc(100% - 80px); 
}

.fade-enter-from {
    opacity: 0;
}

.fade-enter-to {
    opacity: 1;
}

.fade-leave-from {
    opacity: 1;
}

.fade-leave-to {
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: all 0.3s;
}

.fade-enter-active {
    transition-delay: 0.3s;
}
</style>