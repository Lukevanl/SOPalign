<template>
  <!-- Where the magic happens, this component is loaded when pressing the 'ANalyse all' button. It analyses all the SOPs through API request
  and returns all the annotated PDFs and all other relevant information. -->
      <div style="border-top: 2px solid black">
        <div id="resultsSummary">
          <div class="panel panel-default">
            <!-- Panel displaying a summary of the results -->
                <div data-matchheights="t" class="panel-heading">
                  <h3 class="panel-title">Samenvatting resultaten</h3>
                </div>
                <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description">
                    <div v-if="resultsNotLoaded">
                      <h4 style="text-align: center; color:gray; left: 50px; margin-top: 30px; opacity: 0.5;">Loading results...</h4>
                      <div class="progress" style="text-align: center; margin:0 auto; left: 50px; margin-top: 30px; width: 75%">
                        <div id="progBar" class="progress-bar bg-info" role="progressbar" style="text-align: center; width: 0%" aria-valuenow="1" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <h4 style="text-align: center; color:gray; left: 50px; margin-top: 30px; opacity: 0.5;">PDF {{ indexCurrentPDFUploading + 1 }} van {{ fileObjects.length }} aan het analyseren</h4>
                      <font-awesome-icon id="loaderBig" style="text-align: center; left: 50px; margin-top: 30px; margin-bottom: 30px;" icon="spinner" size="4x" spin/>
                    </div>
                    <div v-else>
                      <div class="row">
                        <div class="col-3">
                            <h4 tyle="text-align: center; color:gray; left: 50px; margin-top: 30px;">Resultaten geladen in {{ timeTaken.toFixed(2) }} seconden</h4>
                        </div>
                        <div class="col-9">
                            <h5 tyle="text-align: center; color:gray; left: 50px; margin-top: 10px;"> Totaal aantal gekoppelde aanbevelingen: {{ totalCount }}</h5>
                            <h5 tyle="text-align: center; color:gray; left: 50px; margin-top: 10px;"> Voor deze sop passages waren {{ labelCounts[0] }} <u>niet</u> conform met de aanbeveling, {{ labelCounts[1] }} waren neutraal en {{ labelCounts[2] }} waren conform</h5>
                            <h4> Geschatte compliance score: {{ (labelCounts[2] / (labelCounts[0] + labelCounts[2])).toFixed(2) }}</h4>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                </div>
            </div>
          </div>
      <div class="panel panel-default">
        <!-- Panel containing the annotated PDFs and buttons + a text field to navigate between the PDFs -->
          <div data-matchheights="t" class="panel-heading">
            <h3 class="panel-title">PDF met highlights</h3>
          </div>
          <div data-matchheights="b" class="panel-body">
          <div class="container-small ">
            <div data-matchheights="d" class="description">
                <embed seamless allowfullscreen webkitallowfullscreen mozallowfullscreen
                id="PDFdisplay"
                src=""
                type="application/pdf"
                height="1250px"
                style="display:none; text-align: center; margin: auto;"
                width="95%">
              <div v-if="resultsNotLoaded">
                <h4 style="text-align: center; color:gray; left: 50px; margin-top: 30px; opacity: 0.5;">Please wait...</h4>
                <font-awesome-icon id="loaderBig" style="text-align: center; left: 50px; margin-top: 30px; margin-bottom: 30px;" icon="spinner" size="4x" spin/>
              </div>
            <div v-else id="pdfs-navigator" style="display: flex; justify-content: space-between; margin-top: 30px; margin-bottom: 30px;">
              <button type="button" class="btn btn-primary" @click="goToPrevious()" style="color:white; height: 70%;">Vorige</button>
              <div id="pdfNav">
                <h5>PDF <input type="number" value="1" name="goToPage" id="goToPage" v-on:keyup.enter="changePage()" style="width: 75px;"> van {{ fileObjects.length }}: <br> {{ fileNames[currentIndex] }} <br> {{ allResultsAnalyser.filter(value => value[4] == fileNames[currentIndex]).length }} koppelingen </h5>
              </div>
              <button type="button" class="btn btn-primary" @click="goToNext()" style="color:white; height: 70%;">Volgende</button>
            </div>
            </div>
            </div>
        </div>
      </div>
      <div id="resultsTable">
        <!-- Panel with a large table with all the results. Abovethe table there are numerous options to filter the table. On every filter change, the filterTable function is called which refilters the table based on all the selected filters -->
        <div class="panel panel-default">
          <div data-matchheights="t" class="panel-heading">
            <h3 class="panel-title">Tabel met gedetailleerde resultaten</h3>
          </div>
          <div data-matchheights="b" class="panel-body">
            <div class="container-small" >
              <div data-matchheights="d" class="description">
                <div class="row justify-content-md-center">
                <div class="col-5">
                <div class="panel panel-default panel-small" v-if="!resultsNotLoaded" style="margin: 0 auto;">
                  <div data-matchheights="t" class="panel-heading">
                    <h4 class="panel-title"> <b>Filter de tabel </b></h4>
                  </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="checkCurrentPDF" v-model="onlyCurrentPDFSelector" @change ="filterTable">
                  <label class="form-check-label" for="checkCurrentPDF">
                    Laat alleen huidige PDF zien
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="checkAanb" v-model="onlyEnteredAanb" @change="filterTable">
                  <label class="form-check-label" for="checkCurrentPDF">
                    Laat alleen ingevulde aanbeveling zien:
                  </label>
                  <input type="text" value="" name="filterAanb" id="filterAanb" placeholder="Aanbeveling ID om te filteren..." style="width: 225px; margin-left: 10px;">
                </div>
                  <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="nietConformFilter" v-model="showNietConform" @change ="filterTable" checked>
                  <label class="form-check-label" for="NietConformFilter">
                    Niet conform
                  </label>
                  </div>
                  <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="conformFilter" v-model="showConform" @change ="filterTable" checked>
                  <label class="form-check-label" for="conformFilter">
                    Conform
                  </label>
                  </div>
                  <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="neutraalFilter" v-model="showNeutraal" @change ="filterTable" checked>
                  <label class="form-check-label" for="neutraalFilter">
                    Neutraal
                  </label>
                  </div>
                </div>
              </div>
            </div>
                <div style="padding: 5px;">
                  <button type="button" id="reloadButton" class="btn btn-primary" @click="reloadAllWithChanges()" disabled style="color:white; padding-bottom: 5px;">Herlaad tabel met correcties</button>
                </div>
                <table class="table table-bordered">
                  <!-- The actual table -->
                  <thead style="text-align: center; background-color: #E0F2F2;">
                      <tr class="table_head">
                      <th scope="col">Aanbeveling</th>
                      <th scope="col">SOP-passage</th>
                      <th scope="col">Aanbeveling ID</th>
                      <th scope="col">Label</th>
                      <th scope="col">Probability</th>
                      <th scope="col">Corrigeer</th>
                      <th scope="col">Bestandsnaam</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
                      <tr v-if="resultsNotLoaded">
                        <td align="center" colspan="7"><font-awesome-icon icon="spinner" spin/></td>
                      </tr>
                      <!-- Functionality and content for each row in separate component. -->
                      <AnalysisResultsRow
                          v-bind:value="value"
                          v-bind:key="index"
                          @correct="swapLabel(value, index)"
                          v-for="(value, index) in filteredResults"
                      />
                  </tbody>
              </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Table with results where each row represent the results for a single recommendation instead of the previous table where each row is a single annotation. -->
      <AanbevelingenAnalysis
              v-bind:aanbevelingen="aanbevelingen"
              v-bind:results="allResultsAnalyser"
              v-bind:resultsNotLoaded="resultsNotLoaded"
          />
      <div v-if="!resultsNotLoaded" id="changeStrictness">
      <div class="panel panel-default">
        <!-- Panel where users can change the thresholds of the STS and cosine similarity scores by dragging the slider. -->
            <div data-matchheights="t" class="panel-heading">
              <h3 class="panel-title">Pas striktheid aan</h3>
            </div>
            <div data-matchheights="b" class="panel-body">
            <div class="container-small ">
              <div data-matchheights="d" class="description">
                <div>
                  <div>
                    <p style="text-align: center; color:gray; left: 50px; margin-top: 10px; opacity: 0.8;">Een hogere striktheid geeft over het algemeen minder overbodige annotaties maar mist ook meer belangrijke annotaties. <br>Mocht het analyseren te lang duren, zet de striktheid dan hoger.</p>
                  </div>
                  <div class="slidecontainer" align="center" justify="center" style="margin-top: 10px;">
                    <VueSlider v-model="strictnessValue" dragOnClick=true width="40%" dotSize=20 :value="'Normaal'" :data="['Extreem Mild', 'Erg Mild', 'Mild', 'Normaal', 'Strikt', 'Erg Strikt', 'Extreem Strikt']"/>
                  </div>
                  <div style="margin-top: 25px;">
                    <button type="button" class="btn btn-primary" @click="analyseWithStrictness(strictnessValue)" style="color:white;">Analyseer opnieuw met striktheid: {{ strictnessValue }}</button>
                  </div>
                </div>
              </div>
            </div>
            </div>
        </div>
      </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import AnalysisResultsRow from './AnalysisResultsRow.vue'
import AanbevelingenAnalysis from './AanbevelingenAnalysis.vue'
import 'vue-slider-component/theme/antd.css'

const pdfjs = (async () => {
  const pdfjs = await import('pdfjs-dist/legacy/build/pdf')
  const pdfjsWorker = await import('pdfjs-dist/legacy/build/pdf.worker.entry')
  pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker
  return pdfjs
})()

export default defineComponent({
  name: 'SOPanalyser',
  components: { AnalysisResultsRow, AanbevelingenAnalysis },
  created: async function () {
    // While this variable is true, no results will be displayed and instead a loading bar will be shown.
    this.resultsNotLoaded = true
    // Perform the API requests
    await fetch('http://127.0.0.1:8000/post_aanbevelingen', {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ aanbevelingen_list: this.aanbevelingen }) // body data type must match "Content-Type" header
    })
    const nrOfFiles = this.fileContents.length
    for (let index = 0; index < nrOfFiles; index++) {
      const formData = new FormData()
      formData.append('file', this.fileObjects[index])
      // Send PDF to API
      await fetch('http://127.0.0.1:8000/post_pdf', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        body: formData // body data type must match "Content-Type" header
      })
      // Send PDF contents to API
      await fetch('http://127.0.0.1:8000/post_sop', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sentences_list: this.fileContents[index] }) // body data type must match "Content-Type" header
      })
      // Load results from the models from the API
      await fetch('http://127.0.0.1:8000/get_sentence_pairs')
        .then(res => res.json())
        .then(data => {
          console.log(data)
          const resultsWithFilename = data.results.map((num: number, idx: any) => {
            return data.results[idx].concat(this.fileNames[index])
          }, this)
          console.log('Res with fn: ' + resultsWithFilename)
          this.resultsAnalyser = resultsWithFilename
          for (let i = 0; i < this.resultsAnalyser.length; i++) {
            this.allResultsAnalyser.push(this.resultsAnalyser[i])
          }
          console.log('Total results:')
          console.log(this.allResultsAnalyser)
          this.filteredResults = this.allResultsAnalyser
          this.unchangedResults = JSON.parse(JSON.stringify(this.allResultsAnalyser))
          const newLabelCounts = this.getLabelCounts(this.resultsAnalyser)
          this.labelCounts = (this.labelCounts.map(function (num, idx) {
            return num + newLabelCounts[idx]
          }) as [number, number, number])
          const newSTSCounts = data.sts_counts
          this.totalCount += newSTSCounts[2]
          console.log('STS counts: ' + data.sts_counts)
          this.timeTaken += data.time
        })
      // Load the original PDF but now annotated with the results.
      await fetch('http://127.0.0.1:8000/get_ann_pdf', {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        headers: {
          'Content-Type': 'application/pdf'
        }
      })
        .then(res => {
          return res.blob()
        })
        .then(blob => {
          var url = window.URL.createObjectURL(blob)
          console.log('Found url in fetch: ' + url)
          this.fileURLs[index] = url
        })
      this.indexCurrentPDFUploading += 1
      this.makeProgress(this.indexCurrentPDFUploading, nrOfFiles)
    }
    // At this point, all results are loaded, so results are displayed.
    this.resultsNotLoaded = false
    document.getElementById('PDFdisplay')!.style.display = 'block'
    // Show PDF
    this.renderPDF(this.currentIndex)
    console.log(this.allResultsAnalyser)
  },
  methods: {
    async renderPDF (index: number) {
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[index])
    },
    changePage () {
      // Navigate to new page based on current value of textbox
      const page = parseInt((document.getElementById('goToPage') as HTMLInputElement).value)
      console.log(page)
      var newPage = page
      if (newPage < 1) {
        newPage = 1
      } else {
        newPage = Math.min(page - 1, this.fileNames.length - 1)
      }
      console.log(newPage);
      (document.getElementById('goToPage') as HTMLInputElement).value = (newPage + 1).toString()
      this.currentIndex = newPage
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[newPage])
      // If only showing the current PDF, the table has to be updated when moving to a new PDF
      if (this.onlyCurrentPDFSelector) {
        this.filterTable()
      }
    },
    filterTable () {
      // Checks whether each filter has been applied and filter table in accordance with these filters.
      console.log(this.onlyCurrentPDFSelector, this.showNietConform, this.showConform, this.showNeutraal)
      var intermedResults = this.allResultsAnalyser
      if (!this.showConform) {
        intermedResults = intermedResults.filter(x => x[2] !== 'conform')
      }
      if (!this.showNietConform) {
        intermedResults = intermedResults.filter(x => x[2] !== 'niet conform')
      }
      if (!this.showNeutraal) {
        intermedResults = intermedResults.filter(x => x[2] !== 'neutraal')
      }
      if (this.onlyCurrentPDFSelector) {
        intermedResults = intermedResults.filter(x => x[4] === this.fileNames[this.currentIndex])
      }
      if (this.onlyEnteredAanb) {
        const aanbId = (document.getElementById('filterAanb')! as HTMLInputElement).value
        intermedResults = intermedResults.filter(x => x[1] === aanbId)
      }
      this.filteredResults = intermedResults
    },
    async reloadAllWithChanges () {
      // When user pressed the reload button, its corrections are saved to a database and the PDF is then reloaded with the changes made.
      await this.saveChangesToDatabase()
      await this.reloadPDFsWithChanges()
    },
    async saveChangesToDatabase () {
      // API calls to save the changes made to a database, these values can later be used to retrain the model for better performance.
      const nliLabelsCurrent: string[] = JSON.parse(JSON.stringify(this.allResultsAnalyser.map(function (value, index) { return value[2] })))
      const nliLabelsOrig: string[] = JSON.parse(JSON.stringify(this.unchangedResults.map(function (value, index) { return value[2] })))
      nliLabelsOrig.forEach(async (origLabel, index) => {
        const newLabel = nliLabelsCurrent[index]
        if (origLabel !== newLabel) {
          console.log('change found, saving to database')
          await fetch('http://127.0.0.1:8000/feedback', {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ aanbeveling: this.allResultsAnalyser[index][0][0], aanbeveling_id: this.allResultsAnalyser[index][1], sop_passage: this.allResultsAnalyser[index][0][1], nli_label: newLabel }) // body data type must match "Content-Type" header
          })
        }
      })
    },
    async reloadPDFsWithChanges () {
      // Reloads PDF with the changes that were made
      const groupedMap = this.allResultsAnalyser.reduce(
        (entryMap, e) => entryMap.set(e[4], [...entryMap.get(e[4]) || [], e]),
        new Map()
      )
      const resultsGrouped: any[] = Array.from(groupedMap.entries())
      console.log(resultsGrouped)
      const nrOfFiles = this.fileContents.length
      this.resultsNotLoaded = true
      this.currentIndex = 0
      this.indexCurrentPDFUploading = 0
      this.labelCounts = [0, 0, 0]
      for (let index = 0; index < nrOfFiles; index++) {
        const formData = new FormData()
        formData.append('file', this.fileObjects[index])
        // Send unannotated PDF to API
        await fetch('http://127.0.0.1:8000/post_pdf', {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          body: formData // body data type must match "Content-Type" header
        })
        console.log(resultsGrouped[index][1].map((x: any[]) => x[0][1]), resultsGrouped[index][1].map((x: any[]) => x[0][0]), resultsGrouped[index][1].map((x: any[]) => x[1]), resultsGrouped[index][1].map((x: any[]) => x[2]), resultsGrouped[index][1].map((x: any[]) => Math.max(...x[3])))
        // Re-annotate PDF with the changed values
        await fetch('http://127.0.0.1:8000/get_and_ann_pdf?' + new URLSearchParams({
          sop_sentences: resultsGrouped[index][1].map((x: any[]) => x[0][1].replace(new RegExp(',', 'g'), '$#$')),
          aanbevelingen: resultsGrouped[index][1].map((x: any[]) => x[0][0].replace(new RegExp(',', 'g'), '$#$')),
          aanbeveling_ids: resultsGrouped[index][1].map((x: any[]) => x[1]),
          labels: resultsGrouped[index][1].map((x: any[]) => x[2]),
          probabilities: resultsGrouped[index][1].map((x: any[]) => Math.max(...x[3]))
        }),
        {
          method: 'GET', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          headers: {
            'Content-Type': 'application/pdf'
          }
        })
          .then(res => {
            return res.blob()
          })
          .then(blob => {
            var url = window.URL.createObjectURL(blob)
            console.log('Found url in fetch: ' + url)
            this.fileURLs[index] = url
          })
      }
      this.indexCurrentPDFUploading += 1
      this.makeProgress(this.indexCurrentPDFUploading, nrOfFiles)
      const newLabelCounts = this.getLabelCounts(this.allResultsAnalyser)
      this.labelCounts = (this.labelCounts.map(function (num, idx) {
        return num + newLabelCounts[idx]
      }) as [number, number, number])
      // Done, reload pdf.
      this.resultsNotLoaded = false
      document.getElementById('PDFdisplay')!.style.display = 'block'
      this.renderPDF(this.currentIndex)
      this.goToPrevious()
    },
    resetVars () {
      // When the user wants to reanalyse but with different strictness, all variables are reset.
      this.resultsNotLoaded = true
      this.currentIndex = 0
      this.totalCount = 0
      this.labelCounts = [0, 0, 0]
      this.timeTaken = 0
      this.allResultsAnalyser = []
      this.filteredResults = []
      this.indexCurrentPDFUploading = 0
    },
    swapLabel (value: any, index: number) {
      // Function which loops through the conformity labels, used when the user corrects the model.
      const currentLabel = value[2]
      const labels = ['conform', 'niet conform', 'neutraal']
      const currentIndex = labels.indexOf(currentLabel)
      const nextIndex = (currentIndex + 1) % 3
      value[2] = labels[nextIndex]
      console.log(this.labelsUnchanged())
      if (this.labelsUnchanged()) {
        (document.getElementById('reloadButton')! as HTMLButtonElement).disabled = true
      } else {
        (document.getElementById('reloadButton')! as HTMLButtonElement).disabled = false
      }
    },
    labelsUnchanged () {
      // Function that checks whether any changes have been made to the labels. Button only becomes active when this is the case.
      const nliLabelsCurrent: string[] = JSON.parse(JSON.stringify(this.allResultsAnalyser.map(function (value, index) { return value[2] })))
      const nliLabelsOrig: string[] = JSON.parse(JSON.stringify(this.unchangedResults.map(function (value, index) { return value[2] })))
      var isTheSame = true
      nliLabelsOrig.forEach((num1, index) => {
        const num2 = nliLabelsCurrent[index]
        if (num1 !== num2) {
          isTheSame = false
        }
      })
      return isTheSame
    },
    async analyseWithStrictness (strictness: string) {
      // API calls just like in the 'created' function before but now with a different strictness.
      this.resetVars()
      this.strictnessValue = strictness
      const nrOfFiles = this.fileContents.length
      for (let index = 0; index < nrOfFiles; index++) {
        const formData = new FormData()
        formData.append('file', this.fileObjects[index])
        await fetch('http://127.0.0.1:8000/post_pdf', {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          body: formData // body data type must match "Content-Type" header
        })
        await fetch('http://127.0.0.1:8000/post_sop', {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ sentences_list: this.fileContents[index] }) // body data type must match "Content-Type" header
        })
        await fetch('http://127.0.0.1:8000/get_sentence_pairs?' + new URLSearchParams({ chosen_strictness: this.strictnessValue }))
          .then(res => res.json())
          .then(data => {
            console.log(data)
            const resultsWithFilename = data.results.map((num: number, idx: any) => {
              return data.results[idx].concat(this.fileNames[index])
            }, this)
            console.log('Res with fn: ' + resultsWithFilename)
            this.resultsAnalyser = resultsWithFilename
            for (let i = 0; i < this.resultsAnalyser.length; i++) {
              this.allResultsAnalyser.push(this.resultsAnalyser[i])
            }
            this.unchangedResults = JSON.parse(JSON.stringify(this.allResultsAnalyser))
            this.filteredResults = this.allResultsAnalyser
            console.log('Total results:')
            console.log(this.allResultsAnalyser)
            const newLabelCounts = this.getLabelCounts(this.resultsAnalyser)
            this.labelCounts = (this.labelCounts.map(function (num, idx) {
              return num + newLabelCounts[idx]
            }) as [number, number, number])
            const newSTSCounts = data.sts_counts
            this.totalCount += newSTSCounts[2]
            console.log('STS counts: ' + data.sts_counts)
            this.timeTaken += data.time
          })
        await fetch('http://127.0.0.1:8000/get_ann_pdf')
          .then(res => {
            return res.blob()
          })
          .then(blob => {
            var url = window.URL.createObjectURL(blob)
            console.log('Found url in fetch: ' + url)
            this.fileURLs[index] = url
          })
        this.indexCurrentPDFUploading += 1
        this.makeProgress(this.indexCurrentPDFUploading, nrOfFiles)
      }
      // At this point, all results are loaded.
      this.resultsNotLoaded = false
      document.getElementById('PDFdisplay')!.style.display = 'block'
      this.renderPDF(this.currentIndex)
      this.goToPrevious()
    },
    makeProgress (current: number, total: number) {
      // Simple functionality for a loading bar which progressed after a single PDF is loaded.
      var bar: HTMLElement = document.querySelector('.progress-bar') as HTMLElement;
      (bar! as HTMLElement).style.width = (current) / total * 100 + '%';
      (bar! as HTMLElement).innerText = ((current) / total * 100).toFixed(0) + '%'
    },
    goToPrevious () {
      // Goes to previous PDF, with boundary checks
      this.currentIndex = Math.max(0, this.currentIndex - 1)
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[this.currentIndex])
      // If only showing the current PDF, the table has to be updated when moving to a new PDF
      if (this.onlyCurrentPDFSelector) {
        this.filterTable()
      }
      (document.getElementById('goToPage') as HTMLInputElement).value = (this.currentIndex + 1).toString()
    },
    goToNext () {
      // Goes to next PDF, with boundary checks
      this.currentIndex = Math.min(this.fileObjects.length - 1, this.currentIndex + 1)
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[this.currentIndex])
      console.log(this.fileContents[this.currentIndex])
      // If only showing the current PDF, the table has to be updated when moving to a new PDF
      if (this.onlyCurrentPDFSelector) {
        this.filterTable()
      }
      (document.getElementById('goToPage') as HTMLInputElement).value = (this.currentIndex + 1).toString()
    },
    getLabelCounts (results: any[]) {
      // Collects summary information about the conformity labels.
      var labels = results.map(function (row) { return row[2] })
      console.log(labels)
      const conformCount = labels.filter(x => x === 'conform').length
      const neutraalCount = labels.filter(x => x === 'neutraal').length
      const nietConformCount = labels.filter(x => x === 'niet conform').length
      console.log('Counts:')
      console.log(conformCount, neutraalCount, nietConformCount)
      return [nietConformCount, neutraalCount, conformCount] as [number, number, number]
    },
    async extractTextFromPage (page: any) {
      return (await page).getTextContent()
    },
    async getText (index: number) {
      // Extracts text from the PDFs
      const url = this.fileURLs[index]
      const doc = (await pdfjs).getDocument(url).promise
      const nrofPages = (await doc).numPages
      console.log(nrofPages)
      var allPages = []
      for (let i = 1; i <= nrofPages; i++) {
        const page = (await doc).getPage(i)
        const content = await this.extractTextFromPage(page)
        const items: string[] = content.items.map((item: any) => item.str)
        allPages.push(items)
      }
      return allPages
    }
  },
  data () {
    // Current index of the PDF that is being looked at
    const currentIndex = 0
    // Information about the PDFs of the SOPs
    const fileURLs: string[] = this.$store.state.fileURLS
    const fileContents: string[][] = this.$store.state.fileContents
    const fileObjects: File[] = this.$store.state.fileObjects
    const fileNames: string[] = this.$store.state.fileNames
    const aanbevelingen: string[] = this.$store.state.aanbevelingen
    const annotatedFile: File = {} as File

    // Keeps track of current results and original results
    const resultsAnalyser: any[] = []
    const allResultsAnalyser: any[] = []
    const unchangedResults: any[] = []

    // While true, results are not displayed. Instead a loading bar is shown.
    const resultsNotLoaded = ref(true)

    // Some summary statistics
    const totalCount = 0
    const timeTaken = 0
    const labelCounts: [number, number, number] = [0, 0, 0]

    // Used strictness when analysing the SOPs
    const strictnessValue = 'Normaal'

    // Used for the progress bar
    const indexCurrentPDFUploading = 0

    // Table filter variables.
    const onlyCurrentPDFSelector = false
    const onlyEnteredAanb = false
    const showConform = true
    const showNietConform = true
    const showNeutraal = true
    const filteredResults: any[] = []
    // document.getElementById('PDFdisplay')
    // console.log(fileURL, fileContent, fileName, index, aanbevelingen)
    return {
      currentIndex,
      fileURLs,
      fileContents,
      fileNames,
      fileObjects,
      aanbevelingen,
      resultsAnalyser,
      allResultsAnalyser,
      totalCount,
      resultsNotLoaded,
      annotatedFile,
      timeTaken,
      labelCounts,
      strictnessValue,
      indexCurrentPDFUploading,
      onlyCurrentPDFSelector,
      showConform,
      showNietConform,
      showNeutraal,
      filteredResults,
      unchangedResults,
      onlyEnteredAanb
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";
@import "../assets/css/colors.scss";

$newbuttoncolor: $rumc-light;
.btn-primary {
    @include button-variant($newbuttoncolor, darken($newbuttoncolor, 7.5%), darken($newbuttoncolor, 10%), lighten($newbuttoncolor,5%), lighten($newbuttoncolor, 10%), darken($newbuttoncolor,30%));
}

.panel-small {
    text-align: center;
    -webkit-box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.05);
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.05);
    margin: 18px;
    background-color: #FFFFFF;
  }

</style>

function x(x: any, arg1: any, arg2: any): any {
  throw new Error('Function not implemented.')
}

function x(x: any, arg1: any, arg2: any): any {
  throw new Error('Function not implemented.')
}
