import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routes = [
  {
    path: '*',
    redirect: '/liftdata'
  },
  {
    name: 'manage',
    redirect: '/manage/liftdata',
    // component: () => import('../views/lift_data_mgmt'),
    component: () => import('../layout/basic'),
    children: [
      {
        name: 'liftdata',
        path: '/liftdata',
        component: () => import('../views/lift_data_mgmt'),
        meta: {
          title: '数据管理'
        }
      }]
  }
]

// add route path
routes.forEach(route => {
  route.path = route.path || '/' + (route.name || '')
})

const router = new Router({ routes })

router.beforeEach((to, from, next) => {
  const title = to.meta && to.meta.title
  if (title) {
    document.title = title
  }
  next()
})

export default router
