<template>
    <div class="f-menuv">
        <el-menu :default-active="2" @select="handleSelect" mode="vertical">
            <el-menu-item index="/document">
                <el-icon>
                    <Document />
                </el-icon>
                <span>说明文档</span>
            </el-menu-item>
            <el-menu-item index="/search">
                <el-icon>
                    <Search />
                </el-icon>
                <span>搜索</span>
            </el-menu-item>
            <el-menu-item index="/history">
                <el-icon>
                    <Folder />
                </el-icon>
                <span>商品库</span>
            </el-menu-item>
            <el-menu-item index="/user">
                <el-icon>
                    <setting />
                </el-icon>
                <span>用户中心</span>
            </el-menu-item>
            <el-menu-item index="/loginTJ">
                <el-icon>
                    <setting />
                </el-icon>
                <span>淘宝京东登录</span>
            </el-menu-item>
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
/* .f-menu {
    transition: all 0.5s;
    top: 80px;
    bottom: 0px;
    left: 0;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    @apply shadow-md fixed bg-light-50;
}

.f-menu::-webkit-scrollbar {
    width: 0px;
} */


/* 默认样式，适用于小屏幕 */
/* .horizontal {
    flex-direction: row;
} */

/* 大屏幕样式 */
/* .vertical {
    flex-direction: column;
} */

/* 媒体查询，适用于小屏幕 */
/* @media only screen and (max-width: 992px) {
    .f-menu .el-menu.horizontal {
        flex-direction: row !important;
    }
} */
</style>