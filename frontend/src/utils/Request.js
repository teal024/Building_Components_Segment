import axios from 'axios'

const baseURL = 'https://mock.apifox.com/m1/3531201-0-default';
// const baseURL = 'http://124.220.110.93:5045/api'

const request = axios.create({  // 创建axios实例
    baseURL: baseURL,
    timeout: 5000
})

export default request;