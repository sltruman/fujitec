import http from './http'
/*http 数据配置请求接口*/
let proxyUrl = 'http://dungbeetles.xyz:60000/fujitec/'
if (process.env.NODE_ENV === 'development') {
	proxyUrl = process.env.API_URL ? 'proxyUrl/' : 'static/mock/';
	// proxyUrl = 'proxyUrl/';
}
export default {
	getElevators: () => http.get(proxyUrl + 'elevators.json'),
	setElevators: (params) => http.post(proxyUrl + 'elevator-set.json', params),
}
