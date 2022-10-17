import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.js'
import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrashCan, faPenToSquare, faSpinner, faRotate, faQrcode, faPlus, faMagnifyingGlass, faMagnifyingGlassChart, faLocationArrow, faGlobe } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

// Create a new store instance.
const store = createStore({
  state () {
    return {
      aanbevelingen: [],
      fileContents: [],
      fileURLS: [],
      fileNames: [],
      selectedIndex: 0,
      fileObjects: []

    }
  },
  mutations: {
    changeAanbevelingen (state: any, aanbevelingen: string[]) {
      (state.aanbevelingen as string[]) = aanbevelingen
    },
    changeFileContents (state: any, fileContents: string[][]) {
      (state.fileContents as string[][]) = fileContents
    },
    changeFileURLS (state: any, fileURLS: string[]) {
      (state.fileURLS as string[]) = fileURLS
    },
    changeFileNames (state: any, fileNames: string[]) {
      (state.fileNames as string[]) = fileNames
    },
    changeFileObjects (state: any, fileObjects: File[]) {
      (state.fileObjects as File[]) = fileObjects
    },
    changeIndex (state: any, index: number) {
      (state.selectedIndex as number) = index
    }
  }
})

library.add(faTrashCan, faPenToSquare, faRotate, faQrcode, faPlus, faMagnifyingGlass, faMagnifyingGlassChart, faLocationArrow, faSpinner, faGlobe)
const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)
app.component('VueSlider', VueSlider)
app.use(router)
// Install the store instance as a plugin
app.use(store)
app.mount('#app')
