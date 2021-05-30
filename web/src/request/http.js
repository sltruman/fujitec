/**
 * http配置
 */
// 引入axios以及element ui中的loading和message组件
import axios from 'axios'

/*http拦截请求*/
axios.interceptors.request.use(config => {

	return config;
}, error => {
	/*返回错误信息*/
	return Promise.reject(error)
});

/*http响应拦截*/
axios.interceptors.response.use(res => {
	if (res.data.result == 'error') {
		return Promise.reject(res)
	} else {
		return Promise.resolve(res)
	}

}, error => {
	return Promise.reject(error)
})

export default axios
