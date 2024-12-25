<template>
    <div class="f-menuH">
        <el-menu :default-active="2" @select="handleSelect" mode="horizontal" :ellipsis="false">
            <el-sub-menu index="2">
                <template #title>导航</template>
                <el-menu-item index="/document">说明文档</el-menu-item>
                <el-menu-item index="/search">搜索</el-menu-item>
                <el-menu-item index="/history">商品库</el-menu-item>
                <el-menu-item index="/subscribe">订阅管理</el-menu-item>
                <el-menu-item index="/user">用户中心</el-menu-item>
                <el-menu-item index="/loginTJ">淘宝京东登录</el-menu-item>
            </el-sub-menu>
        </el-menu>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter();
const handleSelect = (e) => {
    router.push(e);
};
</script>

<style>
.f-menuH {
    height: 10vh;
    /* 高度占屏幕的10% */
    display: flex;
    justify-content: flex-start;
    align-items: center;
    /* 居中 */
    background-color: #ffffff;
    /* 背景颜色 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* 轻微的阴影 */
    position: relative;
    z-index: 10;
    /* 确保菜单在其他内容之上 */
}
</style>