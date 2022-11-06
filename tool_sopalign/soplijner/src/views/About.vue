<template>
  <div class="row justify-content-md-center">
    <h2 style="text-align: center; margin-top: 20px; margin-bottom: 20px; color: black; font-weight: 600;"> Ontwikkeld door:</h2>
    <div class="col-3">
       <div class="panel panel-default" style="min-height: 150px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title"> Radboud Universiteit </h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <img src="../assets/img/ru.png" alt="Company logo" style="max-height: 150px">
                    <br>
                  </div>
                </div>
              </div>
              <div class="panel-footer">
                  <font-awesome-icon icon="globe"/> <a href="https://www.ru.nl" target="_blank">https://www.ru.nl</a>
                </div>
            </div>
    </div>
    <div class="col-3">
       <div class="panel panel-default" style="min-height: 150px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title"> Radboudumc </h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <img src="../assets/img/rumc.png" alt="Company logo" style="max-height: 150px">
                    <br>
                  </div>
                </div>
              </div>
              <div class="panel-footer">
                  <font-awesome-icon icon="globe"/> <a href="https://www.radboudumc.nl" target="_blank">https://www.radboudumc.nl</a>
                </div>
            </div>
    </div>
  </div>
  <div class="row justify-content-md-center">
    <h2 style="text-align: center; margin-top: 20px; margin-bottom: 20px; color: black; font-weight: 600;"> Gefinancierd door:</h2>
    <div class="col-3">
       <div class="panel panel-default" style="min-height: 150px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title"> ABR zorgnetwerk Utrecht </h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <img src="../assets/img/abr.png" alt="Company logo" style="max-height: 150px">
                    <br>
                  </div>
                </div>
              </div>
              <div class="panel-footer">
                  <font-awesome-icon icon="globe"/> <a href="https://www.abrzorgnetwerkutrecht.nl/" target="_blank">https://www.abrzorgnetwerkutrecht.nl/</a>
                </div>
            </div>
    </div>
    <div class="col-3">
       <div class="panel panel-default" style="min-height: 150px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title"> Zorgnetwerk GAIN </h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <img src="../assets/img/gain.jpg" alt="Company logo" style="max-height: 150px">
                    <br>
                  </div>
                </div>
              </div>
              <div class="panel-footer">
                  <font-awesome-icon icon="globe"/> <a href="https://www.zorgnetwerk-gain.nl/home" target="_blank">https://www.zorgnetwerk-gain.nl/home</a>
                </div>
            </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'About',
  setup () {
    return {
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";

</style>
