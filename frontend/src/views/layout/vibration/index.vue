<template>
    <div>这是振动数据风震图页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>

    <div>
        <input type="file" ref="fileInput"  accept=".csv" @change="handleFileInputChange" />
        <button @click="uploadFile" :disabled="!selectedFile">上传文件</button>
    </div>
</template>

<script setup>
    import router from "@/router/index.js"
    import { UploadCsv } from '@/api/vibration.js'
    import { ref } from 'vue'

    
    const fileInputRef = ref(null);
    const selectedFile = ref(null); //已选文件

    const GoToDash = () => {
        //跳转仪表盘页面
        router.push({ 
            name: 'layout', 
            params:{ 
                choice:'dashboard' 
            } 
        })
    }


    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        selectedFile.value = file;
        console.log(selectedFile.value);
    };
    const uploadFile =  () => {
        if (selectedFile.value) {
            let formData = new FormData();
            formData.append('csv', selectedFile.value);
            UploadCsv(formData)
            .then(function (result) {  
                console.log(result)
                // after_upload(result);
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    };

</script>

<style>

    .upload-container{
        margin:30px;
    }

</style>