import Vue from 'vue'
import Router from 'vue-router'
import Books from '../components/Books.vue'
import Hotels from '../components/Hotels.vue'
import Bookings from '../components/Bookings.vue'
import Login from '../components/Login.vue'
import NotFound from '../components/NotFound.vue'
import Ping from '../components/Ping.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/hotels',
      name: 'Hotels',
      component: Hotels
    },
    {
      path: '/books',
      name: 'Books',
      component: Books
    },
    {
      path: '/bookings',
      name: 'Bookings',
      component: Bookings
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      redirect: '/Hotels'
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '*',
      component: NotFound
    }
  ]
})
