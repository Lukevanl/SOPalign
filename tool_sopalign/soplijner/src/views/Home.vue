<template>
  <div class="home" style="background-color: #FAFAFA;">
    <div class="row">
      <div class="col-6">
        <div class="panel panel-default" style="min-height: 400px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title">Aanbevelingen toevoegen</h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <AanbevelingenRetriever />
                  </div>
                </div>
              </div>
            </div>
      </div>
      <div class="col-6">
        <div class="panel panel-default" style="min-height: 400px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title">Bestanden toevoegen (pdf)</h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <FileHandler/>
                  </div>
                </div>
              </div>
            </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import FileHandler from '../components/FileHandler.vue'
import AanbevelingenRetriever from '../components/AanbevelingenRetriever.vue'

export default defineComponent({
  components: { FileHandler, AanbevelingenRetriever },
  name: 'Home',
  setup () {
    const aanbevelingen: string[] = []
    return {
      aanbevelingen
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";
@import "../assets/css/colors.scss";
</style>
