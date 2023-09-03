<template>
  <!-- Simple row template for displaying and removing PDFs from the table -->
  <tr>
    <td class="table-filename"> {{ fileName }} </td>
    <td> <button @click="$emit('remove')" class="table-button" data-bs-toggle="tooltip" title="Verwijder pdf"><font-awesome-icon icon="trash-can" /></button> </td>
</tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PDFTableRow',
  props: ['fileName'],
  setup () {
    return {
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";

</style>
