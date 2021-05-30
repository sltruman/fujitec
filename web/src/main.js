import Vue from 'vue';
import App from './App';
import "@/assets/styles/common.css"
import VueAMap from 'vue-amap';
import http from './request/api'
import tools from './utils/tools.js'
import {
  router
} from './router';
import {
  NavBar,
  Icon,
  Popover,
	popup,
  Form,
  Field,
	Picker,
	Stepper,
	Button,
	List,
	Cell
} from 'vant';

// 全局注册
Vue.use(NavBar);
Vue.use(Icon);
Vue.use(Popover);
Vue.use(popup);
Vue.use(Form);
Vue.use(Field);
Vue.use(Picker);
Vue.use(Stepper);
Vue.use(Button);
Vue.use(List);
Vue.use(Cell);
Vue.use(VueAMap);

VueAMap.initAMapApiLoader({
  key: '466ba813c8cfcc75f1638484ce44643b',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  v: '1.4.4'
});
Vue.prototype.$http = http
Vue.prototype.$tools = tools
new Vue({
  router,
  el: '#app',
  render: h => h(App)
});
