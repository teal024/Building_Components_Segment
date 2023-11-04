import Request from "@/utils/Request.js";  // 在每个 api 文件里都要引入这两个文件
import Message from "@/utils/Message.js"  // 在每个 api 文件里都要引入这两个文件
import router from "@/router/index.js"

// 图像上传
export function UploadImg(params) {  // 在 src/views/login/index.vue 里调用，可以去看看是如何调用的
    return Request({  // 发送请求
        method: 'POST',
        url: '/segmentation/saveimage/',  // 与后端接口对应！！！
        params: params
    }).then(function (response) {  // then 表示成功接收到响应后的操作
        if (response.data.code === 200) {
            Message.success("分割成功");
            
            // console.log(response.data); // 检查返回的数据
            return response;  //  // 正确响应，返回数据
        } else {
            Message.error("分割失败");
        }
    }).catch(function (error) {  // catch 表示接收到错误响应后的操作
        console.log(error);
    });
}