<template>
  <!-- Row template for displaying a single annotation -->
  <tr>
    <td class="table-cell"> {{ aanbeveling[0] }} </td>
    <td class="table-cell"> {{ aanbeveling[1] }} </td>
    <td class="compliance-cell"> {{ ifNaN((resultsForAanbevelingConform.length / (resultsForAanbevelingNietConform.length + resultsForAanbevelingConform.length)).toFixed(2)) }} </td>
    <td class="table-cell"> {{ resultsForAanbeveling.length }} </td>
    <td class="table-cell"> {{ resultsForAanbevelingConform.length }} </td>
    <td class="table-cell"> {{ resultsForAanbevelingNeutraal.length }} </td>
    <td class="table-cell"> {{ resultsForAanbevelingNietConform.length }} </td>
</tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PDFTableRow',
  props: ['aanbeveling', 'results'],
  setup (props) {
    const resultsForAanbeveling = props.results.filter((x: any[]) => x[1] === props.aanbeveling[1])
    const resultsForAanbevelingConform = resultsForAanbeveling.filter((x: any[]) => x[2] === 'conform')
    const resultsForAanbevelingNietConform = resultsForAanbeveling.filter((x: any[]) => x[2] === 'niet conform')
    const resultsForAanbevelingNeutraal = resultsForAanbeveling.filter((x: any[]) => x[2] === 'neutraal')
    return {
      resultsForAanbeveling,
      resultsForAanbevelingConform,
      resultsForAanbevelingNietConform,
      resultsForAanbevelingNeutraal
    }
  },
  methods: {
    // If dividing by zero, replace by '-'
    ifNaN (x: number) {
      if (isNaN(x)) {
        return '-'
      } else {
        return x
      }
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";
@import "../assets/css/colors.scss";
</style>
