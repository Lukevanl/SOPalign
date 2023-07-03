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
                    <h3>Inladen van de richtlijn</h3>
                    <p> Voor het inladen van de richtlijn zijn er 2 opties:  </p>
                    <ol>
                      <li><b>Het gebruiken van een bestaande richtlijn:</b> In onderstaande tabel kan een bestaande richtlijn worden ingeladen door op het icoontje met de pijl te drukken.  </li>
                      <img alt="Tabel bestaande richtlijnen" src="@/assets/img/tut1.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <li><b>Zelf een richtlijn toevoegen:</b> Door op het plusje te drukken kan je zelf een richtlijn handmatig toevoegen door de aanbevelingen er één voor één in te zetten.
                        Bij het invullen van de aanbeveling wordt gevraagd om de tekst van de aanbeveling, en een ID waarmee je die aanbeveling wil identificeren.
                        Door deze uit te vullen en vervolgens op de 'Voeg aanbeveling toe' knop te drukken, wordt een aanbeveling toegevoegd</li>
                      <img alt="Individuele aanbeveling toevoegen" src="@/assets/img/tut2.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <p> <b><i>Belangrijk: Sla een richtlijn op na hem handmatig aangemaakt te hebben en geef hem een naam door op de blauwe 'Sla richtlijn op' knop te drukken, hij verdwijnt anders namelijk zodra je van pagina wisselt. </i></b></p>
                    </ol>
                    <p>Zodra een richtlijn is ingeladen heb je ook nog de optie om individuele aanbevelingen aan te passen door op het pennetje te klikken en de aanpassingen te maken. Aanbevelingen kunnen ook weggegooid worden door op het prullenbakje te drukken.
                      Hele richtlijnen kunnen ook weggegooid worden door op het prullenbakje te drukken, gebruik deze alleen om zelf-gemaakte richtlijnen te verwijderen en niet één van de al bestaande richtlijnen.  </p>

                    <h3>Uploaden van de SOPs</h3>
                    <p>Het uploaden van de SOPs is erg eenvoudig, klik op de 'Browse...' knop en selecteer de <b>PDFs</b> van de SOPs die je wil analyseren (alleen PDFs worden geaccepteerd).</p>
                    <p><b>TIP:</b> gebruik de toetscombinatie Ctrl+A om alle bestanden in een folder te selecteren, scheelt een hoop tijd als je alle SOPs in een folder wil uploaden.</p>
                    <p>Zodra de richtlijn is ingeladen, en de SOPs geüpload zijn, kun je op de 'Analyseer' knop drukken om de tool te starten.</p>

                    <h3>Interpreteren resultaten</h3>
                    <p>Zodra de tool klaar is, worden de resultaten op vier verschillende manier getoond:</p>
                    <ol>
                      <li><b>Samenvatting:</b> Bovenaan de pagina staat een korte samenvatting van de resultaten. Hierin staat hoeveel aanbevelingen er gekoppeld zijn in totaal, de tijd die dit kostte en de conformiteit labels.
                        Er zijn drie mogelijke labels: <b>conform</b> (de SOP passage is conform met de gekoppelde aanbeveling), <b>niet conform</b> (de SOP passage is <i>niet</i> conform met de gekoppelde aanbeveling) en
                        <b>neutraal</b> (de gekoppelde aanbeveling is niet relevant).
                      </li> <br>
                      <li><b>Geannoteerde PDF:</b> Onder de samenvatting zie je de geüploade PDFs terug maar nu met annotaties met de gekoppelde aanbevelingen uit de richtlijn.
                        De gele annotaties hebben een notitie ernaast die informatie geeft over de gemaakte koppeling. Eerst wordt het totaal aantal gekoppelde aanbevelingen aan de geannoteerde SOP passage genoemd,
                      gevolgd door al deze koppelingen. Voor elke koppeling wordt de aanbeveling genoemd, de conformiteit label en hoe zeker het onderliggende model is (in %) over deze label (zie voorbeeld in afbeelding beneden).</li>
                      <img alt="Annotatie van tool" src="@/assets/img/tut3.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                      <br>
                      <li><p><b>Tabel met alle resultaten:</b> Onder de PDF vind je een tabel met alle resultaten. Boven deze tabel vind je filters waarmee je naar specifieke informatie kan zoeken.
                        Zo kan je bijvoorbeeld alleen de annotaties van de huidige PDF bekijken, of alleen de conforme labels, of alleen de annotaties voor één aanbeveling door de ID van deze aanbeveling in te voeren.
                      </p><b>Belangrijk:</b> de kolom 'Corrigeer' is bedoeld om de tool te corrigeren. Door op het toverstafje te klikken pas je de label aan van de annotatie.
                        Het is erg nuttig voor de effectiviteit van de tool om deze correcties te maken naar de correcte label en dan vervolgens op 'Herlaad met correcties' te drukken.
                        Het model dat de tool in de achtergrond gebruikt leert van data, deze correcties worden gebruikt door het model om 'slimmer' te worden. Dus hoe meer je de tool corrigeert, hoe beter die in de toekomst wordt.
                        In onderstaande afbeelding zie je een voorbeeld waar het model aan SOP passage incorrect classificeert als niet conform. Door nu op het toverstafje te klikken, wordt de label aangepast.
                        Door vervolgens op de 'Herlaad met correcties' knop te drukken, wordt de aanpassing ook in de PDF gemaakt en opgeslagen zodat het model hier later van kan leren.
                      </li>
                      <img alt="Correctie met toverstafje" src="@/assets/img/tut5.png" style="background-color: #f8f5f5; display: block; width: 98%;margin-bottom: 10px; margin-top: 12px;">
                      <li><b>Tabel met resultaten per aanbeveling:</b> In deze tabel helemaal onderaan de pagina worden de resultaten per aanbeveling geïllustreerd. Deze tabel kan gebruikt worden om te kijken welke aanbevelingen wel en niet voor lijken te komen in de SOPs.
                        Daarnaast kan ook gekeken worden naar welke aanbeveling vaak wordt gemarkeerd als 'niet conform'. Dit kan mogelijk aanleiding zijn om eens goed naar de implementatie van deze aanbeveling in de SOPs te kijken. Een incorrecte of onduidelijke implementatie kan mogelijk hier de oorzaak van zijn.
                      </li>
                    </ol>
                    <p>
                    Naast de resultaten staat ook nog helemaal bovenaan de pagina een <b>slider</b>:
                    </p>
                    <img alt="Slider voor striktheid van de tool" src="@/assets/img/tut4.png" style="background-color: #f8f5f5; display: block; width: 58%;margin-bottom: 10px; margin-top: 12px;">
                    <p>Soms maakt de tool te veel of te weinig annotaties. Door deze slider te verschuiven kan je dit mogelijk oplossen. Door hem naar links te schuiven maakt de tool meer annotaties terwijl die juist minder annotaties maakt als je hem naar rechts verschuift.
                    Om de nieuwe annotaties te krijgen verschuif je eerst de slider en dan druk je op de knop 'Analyseer opnieuw met...'.
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
