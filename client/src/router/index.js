import Vue from 'vue'
import Router from 'vue-router'
import Books from '../components/Books.vue'
import Hotels from '../components/Hotels.vue'
import Hotels2 from '../components/Hotels2.vue'
import Bookings from '../components/Bookings.vue'
import Login from '../components/Login.vue'
import About from '../components/About.vue'
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
      path: '/hotels2',
      name: 'Hotels2',
      component: Hotels2
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
      path: '/about',
      name: 'About',
      component: About
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
