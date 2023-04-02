import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Tutorial from '../views/Tutorial.vue'
import SOPanalyseSingle from '@/components/SOPanalyseSingle.vue'
import SOPanalyseAll from '@/components/SOPanalyseAll.vue'

const routes: Array<RouteRecordRaw> = [
  {
    // using the client's terms for the variables
    path: '/tool',
    name: 'Toolpage',
    component: Home
  },
  {
    path: '/tool/analyse-single',
    name: 'ToolAnalysepage',
    component: SOPanalyseSingle
  },
  {
    path: '/tool/analyse-all',
    name: 'ToolAnalysepages',
    component: SOPanalyseAll
  },
  {
    path: '/about',
    name: 'Aboutpage',
    component: About
  },
  {
    path: '/tutorial',
    name: 'Tutorialpage',
    component: Tutorial
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
