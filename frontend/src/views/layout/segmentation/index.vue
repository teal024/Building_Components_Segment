<!-- 图像分割页面 -->
<template>
    <div>这是图像分割页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>
    <!-- 上传图片begin -->
    <!-- action为文件上传地址，也可通过https-request自定义上传方式，上传到哪里有待解决 -->
    <el-upload
    v-model:file-list="fileList"
    action=''
    :limit="1"
    accept=".jpg, .png"
    :http-request="uploadHttpRequest"
    :on-remove="handleRemove"
    :before-upload="beforeUpload">
        <el-button type="primary">上传图片</el-button>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files.
            </div>
        </template>
    </el-upload>
    <!-- 上传图片end -->
</template>

<script setup>
import { ref }from 'vue'
import axios from 'axios'
import router from "@/router/index.js"
import Message from "@/utils/Message.js"

const fileList = ref();
const GoToDash = () => {
    //跳转仪表盘页面
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'dashboard' 
        } 
    })
}
const beforeUpload = (file) => {
  // 在上传前进行一些处理，如判断文件类型、大小等
  // 如果不希望上传这个文件，返回 false；如果希望上传这个文件，返回 true
    return true;
}
const uploadHttpRequest = (param) => {
  //自定义上传方法
    console.log(param.file);//查看是否选取到文件
    
}
const handleRemove = (file, fileList) => {
    //  文件列表移除文件时的钩子
    Message.warning("文件已移除");
}

</script>

<style scoped>

</style>