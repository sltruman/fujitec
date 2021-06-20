// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router/index'
import { Tabbar, TabbarItem, NavBar, Icon, Popover, Col, Row, Dialog, Field, Form } from 'vant';
// 全局注册
Vue.use(Dialog);
Vue.use(Tabbar);
Vue.use(TabbarItem);
Vue.use(NavBar);
Vue.use(Icon);
Vue.use(Popover);
Vue.use(Col);
Vue.use(Row);

Vue.config.productionTip = false
// Vue.prototype.$axios = axios
// axios.defaults.baseURL = '/api'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
