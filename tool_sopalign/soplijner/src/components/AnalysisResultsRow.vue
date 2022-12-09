<template>
  <tr>
    <td> {{ value[0][0] }} </td>
    <td> {{ value[0][1] }} </td>
    <td> {{ value[1] }} </td>
    <td class="tdLabel"> {{ value[2] }} </td>
    <td> {{ probability }} </td>
    <td> <button @click="$emit('correct')" class="table-button" data-bs-toggle="tooltip" title="Corrigeer annotatie"><font-awesome-icon icon="wand-magic-sparkles" size="2x" /></button> </td>
    <td v-if="value.length === 5"> {{ value[4] }} </td>
</tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AnalysisResultsRow',
  props: ['value'],
  setup (props) {
    const labelToIndex: any = { 'niet conform': 0, neutraal: 1, conform: 2 }
    const probability = (props.value[3][labelToIndex[props.value[2]]] * 100).toFixed(2) + '%'
    // var allCells = document.getElementsByClassName('tdLabel')
    // for (let i = 0; i < allCells.length; i++) {
    //   var elem = allCells[i] as HTMLElement
    //   var currentText = elem.childNodes[0].nodeValue
    //   if (currentText === 'conform') {
    //     elem.style.backgroundColor = 'rgb(144, 238, 144, 0.5)'
    //   }
    //   if (currentText === 'niet conform') {
    //     elem.style.backgroundColor = 'rgb(255, 87, 51, 0.5)'
    //   }
    //   if (currentText === 'neutraal') {
    //     elem.style.backgroundColor = 'rgb(255, 195, 0, 0.5)'
    //   }
    // }
    return {
      probability
    }
  },
  methods: {
    getProbOfLabel (label: string, probs: number[]) {
      const labelToIndex: any = { 'niet conform': 0, neutraal: 1, conform: 2 }
      return (probs[labelToIndex[label]] * 100)
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";

</style>
