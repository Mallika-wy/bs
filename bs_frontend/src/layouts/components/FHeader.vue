<template>
    <div class="f-header">
        <span class="logo">
            <el-icon>
                <eleme-filled />
            </el-icon>
            ZJU B/S 商品比价网站
        </span>
        <el-icon class="icon-btn">
            <Fold />
        </el-icon>
        <el-icon class="icon-btn">
            <Refresh />
        </el-icon>
        <el-icon class="icon-btn">
            <FullScreen />
        </el-icon>
    </div>
</template>

<style>
.f-header {
    @apply flex items-center bg-indigo-700 text-light-50 fixed top-0 left-0 right-0;
    height: 80px;
    z-index: 1;
}

.logo {
    width: 250px;
    @apply flex justify-center items-center text-xl font-thin;
}

.icon-btn {
    @apply flex justify-center items-center;
    width: 42px;
    height: 80px;
    cursor: pointer;
}

.icon-btn:hover {
    @apply bg-indigo-600;
}

</style>