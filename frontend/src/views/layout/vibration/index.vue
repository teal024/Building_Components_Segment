<template>
    <div>这是图像分割页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>
        <el-upload
            ref="uploadRef"
            class="upload-container"
            v-model:file-list="fileList"
            accept=".csv"
            action="/api"
            :auto-upload="false"
            :limit="1"
            :on-exceed="handleExceed"
    >
        <el-button type="primary">选择文件</el-button>
        <el-button type="success" @click="submitUpload">
            上传文件
        </el-button>
        <template #tip>
        <div class="el-upload__tip">
            请选择csv格式文件
        </div>
        </template>
    </el-upload>
</template>

<script setup>
    import router from "@/router/index.js"
    import { ref } from 'vue'

    const uploadRef = ref(null);

    const GoToDash = () => {
        //跳转仪表盘页面
        router.push({ 
            name: 'layout', 
            params:{ 
                choice:'dashboard' 
            } 
        })
    }

    const handleExceed = (files) => {
        uploadRef.value.clearFiles()
        const file = files[0]
        file.uid = genFileId()
        uploadRef.value.handleStart(file)
    }

    const submitUpload = () =>{
        uploadRef.value.submit();
    }

</script>

<style>

    .upload-container{
        margin:30px;
    }

</style>