<template>
  <tr>
    <td class="table-filename"> {{ aanbeveling[0] }} </td>
    <td class="table-filename"> {{ aanbeveling[1] }} </td>
    <td> <button @click="$emit('edit')" class="table-button" data-bs-toggle="tooltip" title="Pas aanbeveling aan"><font-awesome-icon icon="pen-to-square" /></button> </td>
    <td> <button @click="$emit('remove')" class="table-button" data-bs-toggle="tooltip" title="Verwijder aanbeveling"><font-awesome-icon icon="trash-can" /></button> </td>
</tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PDFTableRow',
  props: ['aanbeveling'],
  setup () {
    return {
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";

</style>
