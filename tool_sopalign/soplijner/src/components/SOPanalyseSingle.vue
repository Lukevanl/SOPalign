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
                        <p style="text-align: center; color:gray; left: 50px; margin-top: 10px; opacity: 0.65;">Een hogere striktheid geeft over het algemeen minder overbodige annotaties maar mist ook meer belangrijke annotaties. <br>Mocht het analyseren te lang duren, zet de striktheid dan hoger.</p>
                      </div>
                      <div class="slidecontainer" align="center" justify="center" style="margin-top: 10px;">
                        <VueSlider v-model="strictnessValue" dragOnClick=true width="30%" dotSize=20 :value="'Normaal'" :data="['Erg Mild', 'Mild', 'Normaal', 'Strikt', 'Erg Strikt']"/>
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
                      <font-awesome-icon id="loaderBig" style="text-align: center; left: 50px; margin-top: 30px; margin-bottom: 30px;" icon="spinner" size="4x" spin/>
                    </div>
                    <div v-else>
                      <div class="row">
                        <div class="col-3">
                            <h4 tyle="text-align: center; color:gray; left: 50px; margin-top: 30px;">Resultaten geladen in {{ timeTaken.toFixed(2) }} seconden</h4>
                        </div>
                        <div class="col-9">
                            <h5 tyle="text-align: center; color:gray; left: 50px; margin-top: 10px;"> Totaal aantal gekoppelde aanbevelingen: {{ resultsAnalyser.length }}</h5>
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
                    <div v-if="resultsNotLoaded">
                      <h4 style="text-align: center; color:gray; left: 50px; margin-top: 30px; opacity: 0.5;">Please wait...</h4>
                      <font-awesome-icon id="loaderBig" style="text-align: center; left: 50px; margin-top: 30px; margin-bottom: 30px;" icon="spinner" size="4x" spin/>
                    </div>
                    <embed seamless
                      id="PDFdisplay"
                      src=""
                      type="application/pdf"
                      height="750px"
                      style="display:none;"
                      width="100%">
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
            <div class="container-small ">
              <div data-matchheights="d" class="description">
                <div v-if="!resultsNotLoaded">
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
                      <th scope="col">Corrigeer</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
                      <tr v-if="resultsNotLoaded">
                        <td align="center" colspan="6"><font-awesome-icon icon="spinner" spin/></td>
                      </tr>
                      <AnalysisResultsRow
                          v-bind:value="value"
                          v-for="(value, index) in filteredResults"
                          :key="index"
                          @correct="swapLabel(value)"
                          @goto="goToText(index)"
                      />
                  </tbody>
              </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- <h3>Extracted text:</h3>
       <textarea
        class="form-control"
        name="displayPDFText"
        id="displayPDFText"
        oninput='this.style.height = "";this.style.height = this.scrollHeight + 3 + "px"'
      ></textarea> -->
        <AanbevelingenAnalysis
          v-bind:aanbevelingen="aanbevelingen"
          v-bind:results="resultsAnalyser"
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
    const formData = new FormData()
    formData.append('file', this.fileObject)
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
      body: JSON.stringify({ sentences_list: this.fileContent }) // body data type must match "Content-Type" header
    })
    await fetch('http://127.0.0.1:8000/post_aanbevelingen', {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ aanbevelingen_list: this.aanbevelingen }) // body data type must match "Content-Type" header
    })
    await fetch('http://127.0.0.1:8000/get_sentence_pairs')
      .then(res => res.json())
      .then(data => {
        console.log(data)
        this.resultsAnalyser = data.results
        this.filteredResults = this.resultsAnalyser
        this.labelCounts = this.getLabelCounts(this.resultsAnalyser)
        this.stsCounts = data.sts_counts
        this.timeTaken = data.time
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
        // console.log('Found url in fetch: ' + url)
        this.fileURL = url
      })
    // At this point, all results are loaded.
    this.resultsNotLoaded = false
    document.getElementById('PDFdisplay')!.style.display = 'block'
    console.log(this.fileURL)
    this.renderPDF()
    console.log(this.resultsAnalyser, this.aanbevelingen, this.stsCounts, this.annotatedFile, this.labelCounts)
  },
  methods: {
    async renderPDF () {
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURL)
    },
    filterTable () {
      console.log(this.showNietConform, this.showConform, this.showNeutraal)
      var intermedResults = this.resultsAnalyser
      if (!this.showConform) {
        intermedResults = intermedResults.filter(x => x[2] !== 'conform')
      }
      if (!this.showNietConform) {
        intermedResults = intermedResults.filter(x => x[2] !== 'niet conform')
      }
      if (!this.showNeutraal) {
        intermedResults = intermedResults.filter(x => x[2] !== 'neutraal')
      }
      console.log(intermedResults)
      this.filteredResults = intermedResults
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
    async analyseWithStrictness (strictness: string) {
      this.strictnessValue = strictness
      this.resultsNotLoaded = true
      const formData = new FormData()
      console.log('Fileobject:')
      console.log(this.fileObject)
      formData.append('file', this.fileObject)
      await fetch('http://127.0.0.1:8000/post_pdf', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        body: formData // body data type must match "Content-Type" header
      })
      await fetch('http://127.0.0.1:8000/get_sentence_pairs?' + new URLSearchParams({ chosen_strictness: this.strictnessValue }))
        .then(res => res.json())
        .then(data => {
          console.log(data)
          this.resultsAnalyser = data.results
          this.filteredResults = this.resultsAnalyser
          this.labelCounts = this.getLabelCounts(this.resultsAnalyser)
          this.stsCounts = data.sts_counts
          this.timeTaken = data.time
        })
      await fetch('http://127.0.0.1:8000/get_ann_pdf')
        .then(res => {
          return res.blob()
        })
        .then(blob => {
          var url = window.URL.createObjectURL(blob)
          console.log('Found url in fetch: ' + url)
          this.fileURL = url
        })
      // At this point, all results are loaded.
      this.resultsNotLoaded = false
      document.getElementById('PDFdisplay')!.style.display = 'block'
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURL)
    },
    async extractTextFromPage (page: any) {
      return (await page).getTextContent()
    },
    async getText () {
      const url = this.fileURL
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
    },
    async goToText (index: number) {
      const pageContents = await this.getText()
      var pageNumber = 0
      for (let i = 0; i < pageContents.length; i++) {
        if (pageContents[i].includes(this.resultsAnalyser[0][1])) {
          pageNumber = i
        }
      }
      document.getElementById('PDFdisplay')!.setAttribute('src', this.fileURL + '#page=' + pageNumber.toString() + '&zoom=70')
      const elem = (document.getElementById('PDFdisplay')! as HTMLIFrameElement)
      elem.contentDocument!.location.reload()
      //   const viewer = document.getElementById('pdf-viewer')
      const scrollingElement = (document.scrollingElement || document.body)
      scrollingElement.scrollTop = scrollingElement.scrollHeight
      // const windowIframe = (elem.contentWindow as any)
      const windowAny = (window as any)
      windowAny.find(this.resultsAnalyser[index][0][1], true, true)
    },
    swapLabel (value: any) {
      alert('testing...')
    }
  },
  data () {
    const index: number = this.$store.state.selectedIndex
    const fileURL: string = this.$store.state.fileURLS[index]
    const fileContent: string[] = this.$store.state.fileContents[index]
    const fileObject: File = this.$store.state.fileObjects[index]
    const fileName: string = this.$store.state.fileNames[index]
    const aanbevelingen: string[] = this.$store.state.aanbevelingen
    const resultsAnalyser: any[] = []
    const stsCounts: [number, number, number] = [0, 0, 0]
    const resultsNotLoaded = ref(true)
    const annotatedFile: File = {} as File
    const timeTaken = 0
    const labelCounts: [number, number, number] = [0, 0, 0]
    const strictnessValue = 'Normaal'
    const showConform = true
    const showNietConform = true
    const showNeutraal = true
    const filteredResults: any[] = []
    // document.getElementById('PDFdisplay')
    // console.log(fileURL, fileContent, fileName, index, aanbevelingen)
    return {
      fileURL,
      fileContent,
      fileName,
      fileObject,
      index,
      aanbevelingen,
      resultsAnalyser,
      stsCounts,
      resultsNotLoaded,
      annotatedFile,
      timeTaken,
      labelCounts,
      strictnessValue,
      showConform,
      showNietConform,
      showNeutraal,
      filteredResults
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
