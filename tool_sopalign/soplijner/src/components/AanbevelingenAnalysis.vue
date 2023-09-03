<template>
  <!-- Table containing the content of all the annotationg -->
  <div class="panel panel-default">
          <div data-matchheights="t" class="panel-heading">
            <h3 class="panel-title">Analyse per aanbeveling</h3>
          </div>
          <div data-matchheights="b" class="panel-body">
          <div class="container-small ">
            <div data-matchheights="d" class="description">
              <!-- If results not loaded yet, display a loader. -->
              <div v-if="resultsNotLoaded">
                <font-awesome-icon id="loaderBig" style="text-align: center; left: 50px; margin-top: 30px; margin-bottom: 30px;" icon="spinner" size="4x" spin/>
              </div>
            <div v-else style="display: flex; justify-content: space-between; margin-top: 30px; margin-bottom: 30px;">
              <div id="aanbevelingenAnalysisTable">
                <table class="table table-bordered">
                    <thead style="text-align: center; background-color: #E0F2F2;">
                        <tr class="table_head">
                        <th scope="col">Aanbeveling</th>
                        <th scope="col">ID</th>
                        <th scope="col">Geschatte compliance score</th>
                        <th scope="col">Aantal koppelingen</th>
                        <th scope="col">Conform</th>
                        <th scope="col">Neutraal</th>
                        <th scope="col">Niet conform</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="display:none;"></tr> <!--Else the colors don't alternate properly-->
                        <AanbevelingenAnalysisRow
                            v-bind:aanbeveling="aanbeveling"
                            v-bind:results="results"
                            v-for="(aanbeveling, index) in aanbevelingen"
                            :key="index"
                        />
                    </tbody>
                    </table>
                </div>
            </div>
            </div>
            </div>
        </div>
      </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AanbevelingenAnalysisRow from './AanbevelingenAnalysisRow.vue'

export default defineComponent({
  name: 'FileHandler',
  props: ['results', 'aanbevelingen', 'resultsNotLoaded'],
  components: { AanbevelingenAnalysisRow },
  methods: {
  },
  setup () {
    const fileContents = ref([] as string[][])
    return {
      fileContents
    }
  }
})
</script>

<style lang="scss" scoped>
@import "../assets/css/main.scss";
@import "../assets/css/colors.scss";
  </style>
