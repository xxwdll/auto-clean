import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Welcome from '../components/Welcome.vue'
import Users from '../components/user/Users.vue'
import ResetPassword from '../components/user/ResetPassword.vue'
import DataMange from '../components/datamanage/DataManage.vue'
import ScriptManage from '../components/scriptmanage/ScriptManage.vue'
import AppManage from '../components/applistmanage/AppManage.vue'
import ScriptTemp from '../components/scripttemp/ScriptTemp.vue'
import UpdateData from '../components/execmanage/UpdateData.vue'
// 导入全局样式表
import '../assets/css/global.css'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/home',
    component: Home,
    redirect: '/welcome',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/users', component: Users },
      { path: '/data_list', component: DataMange },
      { path: '/script_list', component: ScriptManage },
      { path: '/app_list', component: AppManage },
      { path: '/script_temp', component: ScriptTemp },
      { path: '/reset_password', component: ResetPassword },
      { path: '/update_data', component: UpdateData }
    ]
  }
]

const router = new VueRouter({
  routes
})

// 挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 从哪个路径跳转而来
  // next 是个函数，表示放行 next() 放行, next('/login') 强制跳转
  if (to.path === '/login') return next()
  // 获取token
  const tokenStr = sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})

export default router
