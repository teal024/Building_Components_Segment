<!-- 图像分割页面 -->
<template>
    <div>这是图像分割页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>
</template>

<script setup>
import router from "@/router/index.js"

const GoToDash = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'dashboard' 
        } 
    })
}
</script>

<style scoped>

</style>