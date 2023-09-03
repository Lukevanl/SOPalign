<template>
  <!-- Simple row template for the table used for displaying, loading and removing guidelines. -->
    <tr>
      <td class="table-filename"> {{ name }} </td>
      <td> <button @click="$emit('load')" class="table-button" data-bs-toggle="tooltip" title="Laad richtlijn"><font-awesome-icon icon="upload" /></button> </td>
      <td> <button @click="$emit('remove')" class="table-button" data-bs-toggle="tooltip" title="Verwijder richtlijn"><font-awesome-icon icon="trash-can" /></button> </td>
  </tr>
  </template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RichtlijnRow',
  props: ['name'],
  setup () {
    return {
    }
  }
})

</script>

  <style lang = "scss" scoped>
  @import "../assets/css/main.scss";

  </style>
