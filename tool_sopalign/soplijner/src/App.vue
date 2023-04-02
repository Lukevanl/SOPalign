<template>
  <div>
    <div class="logo">
    <img alt="Radboudumc logo" src="@/assets/img/sopalign.png" style="margin-left: auto;margin-right: auto;display: block;width: 18%;margin-bottom: 10px; margin-top: 12px;">
    </div>
    <div>
      <div class="nav">
        <div> <router-link class="router-link" tag= "li" :to="{name: 'Aboutpage'}">About</router-link> </div>
        <div> <router-link class="router-link" tag= "li" :to="{name: 'Tutorialpage'}">Tutorial</router-link> </div>
        <div> <router-link class="router-link" tag= "li" :to="{name: 'Toolpage'}">Tool</router-link> </div>
      </div>
      <router-view/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})

</script>

<style lang = "scss" scoped>
  @import "assets/css/main.scss";

</style>
