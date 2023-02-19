<template>
  <div class="row" id="handleInputPDFs">
    <div id="PDFtable">
      <table class="table table-bordered">
          <thead style="text-align: center; background-color: #E0F2F2;">
              <tr class="table_head">
              <th scope="col">Filename</th>
              <th scope="col">Verwijder</th>
              </tr>
          </thead>
          <tbody>
              <tr style="display:none;"></tr> <!--Else the colors dont alternate properly-->
              <PDFTableRow
                  v-bind:fileName="fileName"
                  v-for="(fileName, index) in fileNames"
                  :key="index"
                  @remove="removePDFAtIndex(index)"
              />
          </tbody>
        </table>
    </div>
    <input type="file" id="pdfuploader" accept=".pdf" @change="getAllTextsFromFiles()" multiple>
  </div>
  <button type="button" class="btn btn-primary" @click="analyseAll()" style="color:white;">Analyseer alles</button>

</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import PDFTableRow from './PDFTableRow.vue'
const pdfjs = (async () => {
  const pdfjs = await import('pdfjs-dist/legacy/build/pdf')
  const pdfjsWorker = await import('pdfjs-dist/legacy/build/pdf.worker.entry')
  pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker
  return pdfjs
})()

export default defineComponent({
  name: 'FileHandler',
  components: { PDFTableRow },
  methods: {
    isUpperCase (stringToCheck: string) {
      const strUpper = stringToCheck.toUpperCase()
      const strLower = stringToCheck.toLowerCase()
      return stringToCheck === strUpper && stringToCheck !== strLower
    },
    saveChanges () {
      this.$store.commit('changeFileContents', this.fileContents)
      this.$store.commit('changeFileURLS', this.fileURLS)
      this.$store.commit('changeFileNames', this.fileNames)
      this.$store.commit('changeFileObjects', this.fileObjects)
    },
    openAnalyser (index: number) {
      this.$store.commit('changeIndex', index)
      this.$router.push('/tool/analyse-single')
    },
    analyseAll () {
      this.$router.push('/tool/analyse-all')
    },
    async extractTextFromPage (page: any) {
      return (await page).getTextContent()
    },
    async getText (object: File) {
      const url = URL.createObjectURL(object)
      this.fileURLS.push(url)
      console.log(url)
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
      const allPagesFlattened = allPages.flat()
      return allPagesFlattened
    },
    async getAllTextsFromFiles () {
      const inputFiles: FileList = (document.getElementById('pdfuploader') as HTMLInputElement).files!
      console.log(this.fileNames)
      for (let i = 0; i < inputFiles.length; i++) {
        var item = inputFiles.item(i)!
        this.fileObjects.push(item)
        const fileName = item.name
        console.log(fileName)
        const text = await this.getText(item)
        const cleanedText = this.cleanSentences(text)
        this.fileContents.push(cleanedText)
        this.fileNames.push(fileName)
        this.saveChanges()
        console.log(cleanedText.map(c => [c, []]))
      }
    },
    cleanSentences (sentences: string[]) {
      var cleanedSentences = []
      for (const [i, sentence] of sentences.entries()) {
        const cleanedSentence = sentence.trim()
        // Concat sentences if most likely wrongly separated (checked by below conditions)
        // Attempt 1:
        if (((!('.-?!"·o'.includes(sentence[sentence.length - 1]))) || (sentence.slice(-3) === 'dr.')) && (i + 1 !== sentences.length)) {
          sentences[i + 1] = cleanedSentence + ' ' + sentences[i + 1].trim()
          continue
        }
        // Attempt 2:
        // if (((!('.-?!"·o*#<>[]:|@123456789'.includes(sentence[sentence.length - 1]))) ||
        //   (!('.-?!"·o*#<>[]:|@123456789'.includes(sentence[sentence.length - 2]))) ||
        //   (sentence.slice(-3) === 'dr.')) &&
        //   (i + 1 !== sentences.length)) {
        //   if (sentences[i + 1].length < 1) {
        //     sentences[i + 1] = sentence + sentences[i + 1]
        //     console.log(sentences[i + 1])
        //     continue
        //   }
        //   const nextChar = sentences[i + 1][0]
        //   const charUpper = nextChar.toUpperCase()
        //   const charLower = nextChar.toLowerCase()
        //   // Check if next sentence starts with capital, if yes, dont concat.
        //   if (nextChar === charUpper && nextChar !== charLower) {
        //     cleanedSentences.push(sentence)
        //     continue
        //   }
        //   sentences[i + 1] = sentence.trim() + ' ' + sentences[i + 1].trim()
        //   console.log(sentences[i + 1])
        //   continue
        // }
        cleanedSentences.push(sentence)
      }
      return cleanedSentences
    },
    removePDFAtIndex (index: number) {
      console.log(this.fileNames)
      this.fileNames.splice(index, 1)
      this.fileContents.splice(index, 1)
      this.fileURLS.splice(index, 1)
      this.fileObjects.splice(index, 1)
      this.saveChanges()
    }
    // getItems("./samples/MRSA besmetting.pdf")
  },
  setup () {
    const fileContents = ref([] as string[][])
    const fileURLS = ref([] as string[])
    const selectedIndex = 0
    const fileNames = ref([] as string[])
    const fileObjects = ref([] as File[])
    return {
      fileContents,
      fileURLS,
      selectedIndex,
      fileNames,
      fileObjects
    }
  }
})
</script>

<style lang="scss" scoped>
  #pdf-viewer {
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.1);
    overflow: auto;
  }

  .pdf-page-canvas {
    display: block;
    margin: 5px auto;
    border: 1px solid rgba(0, 0, 0, 0.2);
  }
  </style>
