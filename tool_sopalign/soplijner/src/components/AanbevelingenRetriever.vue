<template>
  <table class="table table-bordered">
          <thead style="text-align: center; background-color: #E0F2F2;">
              <tr class="table_head">
              <th scope="col">Aanbeveling</th>
              <th scope="col">ID</th>
              <th scope="col">Aanpassen</th>
              <th scope="col">Verwijder</th>
              </tr>
          </thead>
          <tbody>
              <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
              <AanbevelingenRow
                  v-bind:aanbeveling="aanbeveling"
                  v-for="(aanbeveling, index) in aanbevelingen"
                  :key="index"
                  @remove="removeAanbeveling(index)"
                  @edit="openEditingModal(index)"
              />
              <tr>
                <td align="center" colspan="4"><button style='background-color: inherit; border : 0; color: #96D2DA;;' @click="openAddingModal" class="table-button-plus" data-bs-toggle="tooltip" title="Voeg aanbeveling toe"><font-awesome-icon id="table-icon-plus" icon="plus" size="2x" /></button></td>
              </tr>
          </tbody>
    </table>
    <h3>Upload aanbevelingen vanaf tsv bestand</h3>
    <form id="csvForm">
    <input type="file" accept=".tsv" id="aanbevelingenFile"/>
    <br>
    <input type="button" value="Submit file" @click="tsvHandler"/>
    </form>
    <!-- Modal -->
    <div class="modal fade" id="aanbevelingenModal" tabindex="-1" aria-labelledby="aanbevelingenModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 v-if="isEditing" class="modal-title" id="aanbevelingenModalLabel">Wijzig aanbeveling</h2>
            <h2 v-else class="modal-title" id="aanbevelingenModalLabel">Voeg aanbeveling toe</h2>
            <button type="button" id="closeModalAanbevelingen" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form v-if="isEditing" class="needs-validation" id="formAanbeveling" name="formAanbeveling" ref="formAanbevelingen" @submit.prevent="editAanbeveling(selectedIndex, newAanbeveling, newID)">
            <div class="modal-body">
              <div class="AddingAanbevelingen">
                <div class="form-floating mb-3 mt-3">
                  <input
                  type="text"
                  class="form-control"
                  id='AanbevelingInput'
                  name='AanbevelingInput'
                  placeholder='Nieuwe aanbeveling...'
                  v-model="newAanbeveling"
                  />
                  <label for="AanbevelingInput">Aanbeveling:</label>
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                  class="form-control"
                  id='IDInput'
                  name="IDInput"
                  type='text'
                  placeholder='ID voor aanbeveling...'
                  v-model='newID'
                  />
                  <label for="IDInput">ID:</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Sla aanpassingen op</button>
            </div>
          </form>
          <form v-else class="needs-validation" id="formAanbeveling" name="formAanbeveling" ref="formAanbevelingen" @submit.prevent="addAanbeveling(newAanbeveling, newID)">
            <div class="modal-body">
              <div class="AddingAanbevelingen">
                <div class="form-floating mb-3 mt-3">
                  <input
                  type="text"
                  class="form-control"
                  id='AanbevelingInput'
                  name='AanbevelingInput'
                  placeholder='Nieuwe aanbeveling...'
                  v-model="newAanbeveling"
                  />
                  <label for="AanbevelingInput">Aanbeveling:</label>
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                  class="form-control"
                  id='IDInput'
                  name="IDInput"
                  type='text'
                  placeholder='ID voor aanbeveling...'
                  v-model='newID'
                  />
                  <label for="IDInput">ID:</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Voeg aanbeveling toe</button>
            </div>
          </form>
          </div>
        </div>
    </div>
    <div>
    <button id="openModalAanbevelingen" style="visibility:hidden;" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#aanbevelingenModal">
    Launch modal
    </button>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AanbevelingenRow from './AanbevelingenRow.vue'

function tsvToArray (str: string, delimiter = '\t') {
  const headers: string[] = str.slice(0, str.indexOf('\n') - 1).split(delimiter)
  console.log(headers)
  const rows = str.slice(str.indexOf('\n') + 1).split('\n')
  console.log(rows)
  const arr = rows.map(function (row) {
    console.log(row)
    const values: string[] = row.split(delimiter)
    const el = headers.reduce(function (object: any, header, index) {
      object[header] = values[index].replace('\r', '')
      return object
    }, {})
    return el
  })

  // return the array
  return arr
}
export default defineComponent({
  name: 'AanbevelingenRetriever',
  components: { AanbevelingenRow },
  methods: {
    saveChanges () {
      this.$store.commit('changeAanbevelingen', this.aanbevelingen)
    },
    closeModal () {
        document.getElementById('closeModalAanbevelingen')!.click()
    },
    removeAanbeveling (index: number) {
      this.aanbevelingen.splice(index, 1)
      this.saveChanges()
    },
    addAanbeveling (newAanbeveling: string, newId: string) {
      this.aanbevelingen.push([newAanbeveling, newId])
      this.saveChanges()
      this.closeModal()
    },
    editAanbeveling (index: number, newAanbeveling: string, newId: string) {
      this.aanbevelingen[index] = [newAanbeveling, newId]
      this.saveChanges()
      this.closeModal()
    },
    openAddingModal () {
      this.isEditing = false
       document.getElementById('openModalAanbevelingen')!.click()
    },
    openEditingModal (index: number) {
      this.isEditing = true
      this.selectedIndex = index
        document.getElementById('openModalAanbevelingen')!.click()
    },
    tsvHandler () {
      const fileElem = document.getElementById('aanbevelingenFile') as HTMLInputElement
      const file = fileElem.files![0]
      const reader = new FileReader()
      var comp: any = null
      // Assign state to var so aanbevelingen can be changed inside onload
      comp = this
      var data: any[] = []
      reader.onload = function (event) {
        const text: string = (event.target!.result as string)
        data = tsvToArray(text)
        console.log(data)
        for (let i = 0; i < data.length; i++) {
          comp.aanbevelingen.push([data[i].Aanbeveling, data[i].Identifier])
          comp.saveChanges()
        }
      }
      reader.readAsText(file, 'ISO-8859-1')
      this.aanbevelingen = comp.aanbevelingen
    }

  },
  setup () {
    const aanbevelingen = ref([] as [string, string][])
    const isEditing = ref(false)
    const selectedIndex = ref(0)
    var newAanbeveling = ref('')
    var newID = ref('')
    return {
      aanbevelingen,
      isEditing,
      selectedIndex,
      newAanbeveling,
      newID
    }
  }
})
</script>
