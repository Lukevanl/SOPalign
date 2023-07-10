<template>
<div class="row justify-content-md-center" style="background-color: #fafafa;">
      <div class="col-8">
        <div class="panel panel-default" style="min-height: 400px">
              <div data-matchheights="t" class="panel-heading">
                <h3 class="panel-title">Uitleg van de tool</h3>
              </div>
              <div data-matchheights="b" class="panel-body">
                <div class="container-small ">
                  <div data-matchheights="d" class="description" style="word-wrap: break-word; text-align: left;">
                    <h3>Wat is SOPalign</h3>
                    <p>SOPalign is een tool die protcollen, werkinstructies en beleidsstukken vergelijkt met aanbevelingen uit een richtlijn.
                      Zo kan je controleren of je werkinstructies nog overeenkomen met een richtlijn. Wanneer een richtlijn verandert kan je de tool gebruiken om de instructies op te zoeken die je moet aanpassen. </p>
                    <h3>Inladen van de richtlijn</h3>
                    <p> Voor het inladen van de richtlijn zijn er 2 opties:  </p>
                    <ol>
                      <li><b>Het gebruiken van een richtlijn die al in de tool zit:</b> In onderstaande tabel kan een bestaande richtlijn worden ingeladen door op het icoontje met de pijl te drukken.  </li>
                      <img alt="Tabel bestaande richtlijnen" src="@/assets/img/tut1.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <li><b>Zelf een richtlijn toevoegen:</b> <p>Klik op het plusje om handmatig de aanbevelingen uit een richtlijn toe te voegen. Vul telkens één aanbeveling in. Als in een richtlijn in één alinea of onder één kopje meerdere aanbevelingen opgesomd zijn, vul je deze één voor één in. </p>
                      <p>Vul de letterlijke tekst van de aanbeveling in en een ID waarmee je de aanbeveling identificeert. Klik vervolgens op 'voeg aanbeveling toe' om de aanbeveling op te slaan. </p></li>
                      <img alt="Individuele aanbeveling toevoegen" src="@/assets/img/tut2.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <p> <b><i>Belangrijk: Sla een richtlijn op na het handmatig toevoegen van de aanbevelingen en geef hem een naam door op de blauwe 'Sla richtlijn op' knop te klikken. Als je dit niet doet verdwijnt de richtlijn zodra je van pagina wisselt. </i></b></p>
                    </ol>
                    <p>Wanneer een richtlijn is ingeladen kan je de individuele aanbevelingen aanpassen. Dit doe je door op het pennetje te klikken en de aanpassing te maken en op te slaan. Aanbevelingen kan je verwijderen door op het prullenbakje te klikken.</p>
                    <p>Een hele richtlijn kan je ook weggooien door op het prullenbakje te klikken. <br> <b>LET OP:</b> doe dit alleen bij zelf-ingevoerde richtlijnen. Als je dit doet met een vooraf ingevoerde richtlijn is deze ook voor andere gebruikers weg. </p>

                    <h3>Uploaden van de Standard Operating Procedures (SOPs)</h3>
                    <p>SOPs zijn alle werkinstructies, protocollen, checklists en beleidsstukken die iets zeggen over hoe het werk gedaan wordt. In ziekenhuizen zijn deze over het algemeen verzameld in een kwaliteitssysteeem.
                      Je hebt de PDFs nodig van de SOPs die je wilt analyseren. </p>
                    <p>Het uploaden van de SOPs is erg eenvoudig, klik op de 'Browse...' knop en selecteer de PDFs van de SOPs die je wil analyseren.</p>
                    <p><b>TIP:</b> gebruik de toetscombinatie Ctrl+A om alle bestanden in een folder te selecteren. Dit scheelt een hoop tijd wanneer je alle SOP's uit een folder wil uploaden.</p>
                    <p>Zodra de richtlijn is ingeladen, en de SOPs geüpload zijn, kun je op de 'Analyseer' knop drukken om de tool te starten.</p>

                    <h3>Interpreteren resultaten</h3>
                    <p>Zodra de tool klaar is, worden de resultaten op vier verschillende manieren getoond:</p>
                    <ol>
                      <li><b>Samenvatting:</b> Bovenaan de pagina staat een korte samenvatting van de resultaten. Hierin staat hoeveel aanbevelingen er in totaal zijn gekoppeld, de tijd dat dit kostte en de conformiteit van de SOP passage met de gekoppelde aanbeveling.
                        Er zijn drie mogelijke labels die word geplakt aan elke koppeling: <b>conform</b> (de SOP passage is conform met de gekoppelde aanbeveling), <b>niet conform</b> (de SOP passage is <i>niet</i> conform met de gekoppelde aanbeveling) en
                        <b>neutraal</b> (de gekoppelde aanbeveling is niet relevant, en hoort niet gekoppeld te zijn aan de SOP passage).
                      </li> <br>
                      <li><b>Geannoteerde PDF:</b> Onder de samenvatting zie je de ingevoerde PDFs met markeringen die aangeven waar tekst is gekoppeld aan aanbevelingen.
                        Bij elke gele markeringen staat een notitie die informatie geeft over de gemaakte koppeling.
                        Eerst wordt per SOP passage aangegeven hoeveel aanbevelingen hier aan gekoppeld zijn.
                        Vervolgens staat per koppeling aangegeven: aan welke aanbeveling de passage is gekoppeld, de conformiteit van de koppeling, en hoe zeker het model is (in %) over deze confomiteits label.</li>
                      <img alt="Annotatie van tool" src="@/assets/img/tut3.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <br>
                      <li><p><b>Tabel met alle resultaten:</b> Onder de PDF vind je een tabel met alle resultaten. Boven deze tabel vind je filters waarmee je naar specifieke informatie kan zoeken.
                        Zo kan je bijvoorbeeld alleen de annotaties van de huidige PDF bekijken, of alleen de conforme labels, of alleen de annotaties voor één aanbeveling door de ID van deze aanbeveling in te voeren.
                      </p><b>Belangrijk:</b> de tool is nog niet foutloos, maar je kan helpen deze te verbeteren. Door op het toverstafje te klikken kan je de label van de gemarkeerde tekst aanpassen.
                        Klik op 'herlaad met correcties' als je klaar bent met verbeteren. De tool leert van deze correcties en wordt daardoor slimmer.
                        In onderstaande afbeelding zie je een voorbeeld waar het model een SOP passage incorrect classificeert als niet conform. Door nu op het toverstafje te klikken, wordt de label aangepast.
                        Door vervolgens op de 'Herlaad met correcties' knop te drukken, wordt de aanpassing ook in de PDF gemaakt en opgeslagen zodat het model hier later van kan leren.
                      </li>
                      <img alt="Correctie met toverstafje" src="@/assets/img/tut5.png" style="background-color: #f8f5f5; display: block; width: 98%;margin-bottom: 10px; margin-top: 12px;">
                      <li><b>Tabel met resultaten per aanbeveling:</b> In deze tabel, helemaal onderaan de pagina, staan de resultaten per aanbeveling weergegeven. Met behulp van deze tabel zie je of aanbevelingen verwerkt zijn in je SOPs.
                        Daarnaast zie je ook welke aanbevelingen vaak zijn gekoppeld aan tekst die 'niet conform' is gelabeld. Dit kan aanleiding zijn om eens goed te kijken naar de manier waarop een aanbeveling is vertaald naar een werkinstructie of protocol.
                        Een onduidelijke of onjuiste instructie kan hier de oorzaak van zijn. Of het beleid van het ziekenhuis wijkt bewust af van de richtlijn, dat is natuurlijk ook mogelijk.
                      </li>
                    </ol>
                    <p>
                    Naast de resultaten staat ook nog helemaal bovenaan de pagina een <b>slider</b>:
                    </p>
                    <img alt="Slider voor striktheid van de tool" src="@/assets/img/tut4.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                    <p>Soms markeert de tool te veel of te weinig tekst. Door deze slider te verschuiven kan je dit oplossen. Door hem naar links te schuiven (minder strikt) markeert de tool meer tekst. Je krijgt juist minder gemarkeerde tekst als je hem naar rechts verschuift.
                    Klik na het verschuiven van de slider op de knop 'Analyseer opnieuw met...' om de nieuwe markeringen en analyse te krijgen.
                    </p>
                    <h3>Disclaimers</h3>
                    <p>De tool is in een vroege ontwikkeling en is zeker nog niet perfect. De tool maakt vaak foute koppelingen dus de tool moet worden gezien als <b>hulpmiddel</b> om de compliance check van SOPs en richtlijnen makkelijker te maken.
                    <u><b>Het doel van de huidige tool is daarom (nog) niet om het hele proces te automatiseren, en een handmatige check van de annotaties van het model is nodig.</b></u></p>

                    <h3>Contact en vragen</h3>
                    <p>Bij vragen, onduidelijkheden of een niet werkende tool kunt u per mail contact opnemen via het mailadres <a href = "mailto: Luke.vanLeijenhorst@ru.nl">Luke.vanLeijenhorst@ru.nl</a>.</p>

                  </div>
                </div>
              </div>
            </div>
      </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Tutorial',
  setup () {
    return {
    }
  }
})

</script>

<style lang = "scss" scoped>
@import "../assets/css/main.scss";

a:link, a:visited {
  color: #000;
}

a:hover {
  color: #999999;
}

</style>
