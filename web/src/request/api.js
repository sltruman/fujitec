import http from './http'
/*http 数据配置请求接口*/
let proxyUrl = 'http://dungbeetles.xyz:60000/fujitec/'
// if (process.env.NODE_ENV === 'development') {
// 	proxyUrl = process.env.API_URL ? 'proxyUrl/' : 'static/mock/';
// 	// proxyUrl = 'proxyUrl/';
// }
/*-----json数据序列化-----*/
function serialize(params) {
	if (!params || Object.prototype.toString.call(params) != "[object Object]") {
		return ""
	}
	let str = "?",
		keys = Object.keys(params);
	keys.forEach(k => {
		if (Object.prototype.toString.call(params[k]) === "[object Object]" || Object.prototype.toString.call(
				params[
					k]) ===
			"[object Array]") {
			str += k + "=" + JSON.stringify(params[k]) + "&"
		} else {
			str += k + "=" + params[k] + "&"
		}

	})
	return str.substr(0, str.length - 1)
}
export default {
	getSyncedStatus: () => http.get(proxyUrl + 'elevators-sync-date'),
	getElevatorsStatus: () => http.get(proxyUrl + 'elevators-less'),
	getElevators: (params) => http.get(proxyUrl + 'elevator' + serialize(params)),
	setElevators: (params) => http.put(proxyUrl + 'elevator-set', params),
}
