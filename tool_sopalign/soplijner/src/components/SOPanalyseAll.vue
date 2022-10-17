<template>
      <div style="border-top: 2px solid black">
      <div v-if="!resultsNotLoaded" id="changeStrictness">
          <div class="panel panel-default">
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
                        <VueSlider v-model="strictnessValue" dragOnClick=true width="40%" dotSize=20 :value="'Normaal'" :data="['Erg Mild', 'Mild', 'Normaal', 'Strikt', 'Erg Strikt']"/>
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
        <div id="resultsSummary">
          <div class="panel panel-default">
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
                height="750px"
                style="display:none;"
                width="100%">
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
        <div class="panel panel-default">
          <div data-matchheights="t" class="panel-heading">
            <h3 class="panel-title">Tabel met gedetailleerde resultaten</h3>
          </div>
          <div data-matchheights="b" class="panel-body">
            <div class="container-small" >
              <div data-matchheights="d" class="description">
                <div v-if="!resultsNotLoaded">
                <div class="form-check" style="width: 20%">
                  <input class="form-check-input" type="checkbox" value="" id="checkCurrentPDF" v-model="onlyCurrentPDFSelector" @change ="filterTable">
                  <label class="form-check-label" for="checkCurrentPDF">
                    Laat alleen huidige PDF zien
                  </label>
                </div>
                <div class="form-check" style="width: 20%">
                  <input class="form-check-input" type="checkbox" value="" id="checkAanb" v-model="onlyEnteredAanb" @change="filterTable">
                  <label class="form-check-label" for="checkCurrentPDF">
                    Laat alleen ingevulde aanbeveling zien
                  </label>
                  <input type="text" value="" name="filterAanb" id="filterAanb" placeholder="Aanbeveling ID om te filteren..." style="width: 250px;">
                </div>
                  <div class="form-check" style="width: 20%">
                  <input class="form-check-input" type="checkbox" value="" id="nietConformFilter" v-model="showNietConform" @change ="filterTable" checked>
                  <label class="form-check-label" for="NietConformFilter">
                    Niet conform
                  </label>
                  </div>
                  <div class="form-check" style="width: 20%">
                  <input class="form-check-input" type="checkbox" value="" id="conformFilter" v-model="showConform" @change ="filterTable" checked>
                  <label class="form-check-label" for="conformFilter">
                    Conform
                  </label>
                  </div>
                  <div class="form-check" style="width: 20%">
                  <input class="form-check-input" type="checkbox" value="" id="neutraalFilter" v-model="showNeutraal" @change ="filterTable" checked>
                  <label class="form-check-label" for="neutraalFilter">
                    Neutraal
                  </label>
                  </div>
                </div>
                <table class="table table-bordered">
                  <thead style="text-align: center; background-color: #E0F2F2;">
                      <tr class="table_head">
                      <th scope="col">Aanbeveling</th>
                      <th scope="col">SOP-passage</th>
                      <th scope="col">Aanbeveling ID</th>
                      <th scope="col">Label</th>
                      <th scope="col">Probability</th>
                      <th scope="col">Filename</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
                      <tr v-if="resultsNotLoaded">
                        <td align="center" colspan="6"><font-awesome-icon icon="spinner" spin/></td>
                      </tr>
                      <AnalysisResultsRow
                          v-bind:value="value"
                          v-bind:key="index"
                          v-for="(value, index) in filteredResults"
                      />
                  </tbody>
              </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <AanbevelingenAnalysis
              v-bind:aanbevelingen="aanbevelingen"
              v-bind:results="allResultsAnalyser"
              v-bind:resultsNotLoaded="resultsNotLoaded"
          />
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
    this.resultsNotLoaded = true
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
          const newLabelCounts = this.getLabelCounts(this.resultsAnalyser)
          this.labelCounts = (this.labelCounts.map(function (num, idx) {
            return num + newLabelCounts[idx]
          }) as [number, number, number])
          const newSTSCounts = data.sts_counts
          this.totalCount += newSTSCounts[2]
          console.log('STS counts: ' + data.sts_counts)
          this.timeTaken += data.time
        })
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
    // At this point, all results are loaded.
    this.resultsNotLoaded = false
    document.getElementById('PDFdisplay')!.style.display = 'block'
    this.renderPDF(this.currentIndex)
    console.log(this.allResultsAnalyser)
  },
  methods: {
    async renderPDF (index: number) {
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[index])
    },
    changePage () {
      const page = parseInt((document.getElementById('goToPage') as HTMLInputElement).value)
      console.log(page)
      var newPage = page
      if (newPage < 0) {
        newPage = 0
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
    resetVars () {
      this.resultsNotLoaded = true
      this.currentIndex = 0
      this.totalCount = 0
      this.labelCounts = [0, 0, 0]
      this.timeTaken = 0
      this.allResultsAnalyser = []
      this.filteredResults = []
      this.indexCurrentPDFUploading = 0
    },
    async analyseWithStrictness (strictness: string) {
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
      var bar: HTMLElement = document.querySelector('.progress-bar') as HTMLElement;
      (bar! as HTMLElement).style.width = (current) / total * 100 + '%';
      (bar! as HTMLElement).innerText = ((current) / total * 100).toFixed(0) + '%'
    },
    goToPrevious () {
      this.currentIndex = Math.max(0, this.currentIndex - 1)
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURLs[this.currentIndex])
      // If only showing the current PDF, the table has to be updated when moving to a new PDF
      if (this.onlyCurrentPDFSelector) {
        this.filterTable()
      }
      (document.getElementById('goToPage') as HTMLInputElement).value = (this.currentIndex + 1).toString()
    },
    goToNext () {
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
    const currentIndex = 0
    const fileURLs: string[] = this.$store.state.fileURLS
    const fileContents: string[][] = this.$store.state.fileContents
    const fileObjects: File[] = this.$store.state.fileObjects
    const fileNames: string[] = this.$store.state.fileNames
    const aanbevelingen: string[] = this.$store.state.aanbevelingen
    const resultsAnalyser: any[] = []
    const allResultsAnalyser: any[] = []
    const totalCount = 0
    const resultsNotLoaded = ref(true)
    const annotatedFile: File = {} as File
    const timeTaken = 0
    const labelCounts: [number, number, number] = [0, 0, 0]
    const strictnessValue = 'Normaal'
    const indexCurrentPDFUploading = 0
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

</style>
