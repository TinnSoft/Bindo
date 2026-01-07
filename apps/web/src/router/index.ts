import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Requests from '../pages/Requests.vue'
import NewRequest from '../pages/NewRequest.vue'
import RequestDetail from '../pages/RequestDetail.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/requests', component: Requests },
  { path: '/requests/new', component: NewRequest },
  { path: '/requests/:id', component: RequestDetail },
]

const router = createRouter({ history: createWebHistory(), routes })
export default router