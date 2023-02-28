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
    <table class="table table-bordered">
          <thead style="text-align: center; background-color: #E0F2F2;">
              <tr class="table_head">
              <th scope="col">Richtlijn</th>
              <th scope="col">Inladen</th>
              <th scope="col">Verwijder</th>
              </tr>
          </thead>
          <tbody>
              <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
              <RichtlijnRow
                  v-bind:name="name"
                  v-for="(name, index) in names"
                  :key="index"
                  @remove="removeRichtlijn(name)"
                  @load="loadRichtlijn(index)"
              />
          </tbody>
    </table>
    <button type="button" class="btn btn-primary" @click="openAddingRichtlijnModal()" style="color:white;">Sla richtlijn op</button>
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

    <div class="modal fade" id="richtlijnModal" tabindex="-1" aria-labelledby="richtlijnModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title" id="richtlijnModalLabel">Voeg richtlijn toe</h2>
            <button type="button" id="closeModalRichtlijn" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form class="needs-validation" id="formRichtlijn" name="formRichtlijn" ref="formRichtlijn" @submit.prevent="addRichtlijn(nameRichtlijn)">
            <div class="modal-body">
              <div class="AddingRichtlijn">
                <div class="form-floating mb-3 mt-3">
                  <input
                  type="text"
                  class="form-control"
                  id='RichtlijnInput'
                  name='RichtlijnInput'
                  placeholder='Naam voor richtlijn...'
                  v-model='nameRichtlijn'
                  required/>
                  <label for="RichtlijnInput">Naam richtlijn:</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Voeg toe</button>
            </div>
          </form>
          </div>
        </div>
    </div>
    <div>
    <button id="openModalRichtlijn" style="visibility:hidden;" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#richtlijnModal">
    Launch modal
    </button>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AanbevelingenRow from './AanbevelingenRow.vue'
import RichtlijnRow from './RichtlijnRow.vue'

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
  components: { AanbevelingenRow, RichtlijnRow },
  mounted: async function () {
    var results: any[] = []
    await fetch('http://127.0.0.1:8000/richtlijn/')
      .then(res => res.json())
      .then(data => {
        results = data
      })
    for (let i = 0; i < results.length; i++) {
      const aanb = results[i].aanbevelingen
      const ids = results[i].aanbevelingen_ids
      const zipped: [string, string][] = aanb.map(function (e: any, i: any) {
        return [e, ids[i]]
      })
      this.richtlijnenList.push(zipped)
      this.names.push(results[i].name)
    }
  },
  methods: {
    saveChanges () {
      this.$store.commit('changeAanbevelingen', this.aanbevelingen)
    },
    async getRichtlijnen () {
      this.aanbevelingen = []
      this.names = []
      var results: any[] = []
      await fetch('http://127.0.0.1:8000/richtlijn/')
        .then(res => res.json())
        .then(data => {
          results = data
        })
      for (let i = 0; i < results.length; i++) {
        const aanb = results[i].aanbevelingen
        const ids = results[i].aanbevelingen_ids
        const zipped: [string, string][] = aanb.map(function (e: any, i: any) {
          return [e, ids[i]]
        })
        this.richtlijnenList.push(zipped)
        this.names.push(results[i].name)
      }
    },
    loadRichtlijn (index: number) {
      this.aanbevelingen = this.richtlijnenList[index]
      console.log(this.richtlijnenList)
      this.saveChanges()
    },
    async addRichtlijn (name: string) {
      const aanbevelingenSentences = this.aanbevelingen.map(function (e: any, i: any) {
        return [e[0]]
      })
      const aanbevelingenIDs = this.aanbevelingen.map(function (e: any, i: any) {
        return [e[1]]
      })
      await fetch('http://127.0.0.1:8000/richtlijn_post', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ aanbevelingen: aanbevelingenSentences, aanbevelingen_ids: aanbevelingenIDs, name: name }) // body data type must match "Content-Type" header
      })
      this.getRichtlijnen()
      this.closeModal()
    },
    async removeRichtlijn (name: string) {
      var results: any[] = []
      await fetch('http://127.0.0.1:8000/rem_richtlijn/' + name)
        .then(res => res.json())
        .then(data => {
          results = data
        })
      this.richtlijnenList = []
      this.names = []
      for (let i = 0; i < results.length; i++) {
        const aanb = results[i].aanbevelingen
        const ids = results[i].aanbevelingen_ids
        const zipped: [string, string][] = aanb.map(function (e: any, i: any) {
          return [e, ids[i]]
        })
        this.richtlijnenList.push(zipped)
        this.names.push(results[i].name)
      }
    },
    closeModal () {
        document.getElementById('closeModalAanbevelingen')!.click()
        document.getElementById('closeModalRichtlijn')!.click()
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
    openAddingRichtlijnModal () {
       document.getElementById('openModalRichtlijn')!.click()
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
    const richtlijnenList = ref([] as [string, string][][])
    const names = ref([] as string[])
    const isEditing = ref(false)
    const nameRichtlijn = ref('')
    const selectedIndex = ref(0)
    var newAanbeveling = ref('')
    var newID = ref('')
    return {
      aanbevelingen,
      isEditing,
      selectedIndex,
      newAanbeveling,
      newID,
      richtlijnenList,
      names,
      nameRichtlijn
    }
  }
})
</script>
