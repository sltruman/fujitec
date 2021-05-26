import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routes = [
  {
    path: '*',
    redirect: '/manage/liftdata'
  },
  {
    name: 'liftdata',
    path: '/manage/liftdata',
    component: () => import('../views/lift_data_mgmt'),
    meta: {
      title: '电梯管理'
    }
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
