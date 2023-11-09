<template>
    <el-container class="result-container">

      <el-main class="result-gallery" v-loading="isload">
        <!-- 行 -->
        <el-row v-for="(row, index) in imageRows" :key="index" class="resultrow" :gutter="20">
          <!-- 列 -->
          <el-col v-for="(result, i) in row" :key="i" :span="6" class="resultcol" style="max-width:none;">
              <el-card class="result">
                <img :src="result.url" class="image" alt="图片加载失败" />
                <el-button type="primary" :icon="ZoomIn" @click="dialogVisible=true" circle/>
                <el-button type="success" :icon="Download" @click="savePicture(result.url)" circle />
              </el-card>
              <el-dialog v-model="dialogVisible">
                <div class="picture-container">
                    <img w-full :src="result.url" alt="图片预览" class="picture"/>
                </div>
            </el-dialog>
          </el-col>
        </el-row>
        <!-- 分页栏 -->
        <el-row class="pagination">
          <el-pagination v-model:currentPage="currentPage" v-model:pageSize="pageSize" :small="small" :disabled="disabled"
            :background="background" layout="prev, pager, next, jumper" :total="total"
            @current-change="handleCurrentChange" />
        </el-row>
      </el-main>
    </el-container>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { ref } from 'vue'
  import { ZoomIn, Download } from '@element-plus/icons-vue';

  
  const isload = ref(false);
  const dialogVisible = ref(false) //缩略图是否可见
  const showShadow = ref(false);//是否显示阴影块
  
  
//   const resultList = ref([]);

  const resultList = ref([
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
    {url:'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
  ])
  
  // 分页栏用到的数据
  const currentPage = ref(1) //当前页数，默认为第1页
  const pageSize = 20 //每页的图片数量，设置为20
  const rowSize = 4
  let total = ref(1);
  
  // 计算属性，计算resultList中图片对应的行；每行3列
  const imageRows = computed(() => {
    const start = 0; //当前页的起始数据编号
    const end = start + pageSize;//当前页的最后数据号
    const paginatedShopRows = resultList.value.slice(start, end);
    const rows = []  //二维数组，rows[i]存储第i行的店铺卡牌（4个）
    const rowCount = pageSize / rowSize; //行数
    for (let i = 0; i < rowCount; i++) {
      rows.push(paginatedShopRows.slice(i * rowSize, (i + 1) * rowSize))
    }
    return rows;
  })

  const savePicture = (url) =>{
    console.log(url);
  }

  

  </script>
  
  
  <style scoped>
  .result-container {
    padding: 3%;
    margin: 0 5% 5% 5%;
  }
  
  .result-gallery {
    position: relative;
  }
  
  .resultrow {
    margin-bottom: 30px;
  }
  
  .resultcol {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  
  .result {
    width: 200px;
    height: 200px;
    text-align: center;
    padding-bottom:30px;
  }
  
  .result-gallery .result .image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    margin-bottom: 0;
  }
  
  .pagination {
    margin-top: 20px;
    justify-content: center;
    text-align: center;
    width: 100%;
  }

  .picture-container {
    margin:0 auto; 
    width:60vh;
    height:60vh;
    overflow: hidden; /* 隐藏超出容器的部分 */
  }

  .picture-container .picture {
    /* display: block; */
    width:100%;
    height:100%;
    object-fit:cover;
    object-position: center;
  }
  
  </style>