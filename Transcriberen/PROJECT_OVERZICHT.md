# Transcribeer-tool: overzicht en stand van zaken

Laatste update: 16 juni 2026. Dit document vat samen wat de tool doet, wat er is
gebouwd en aangepast, hoe je hem draait, en wat de volgende stap is. Bedoeld om op
een andere pc verder te kunnen.

## Wat de tool doet

Je uploadt audio (of video) van spreekoefeningen van NT2-cursisten. De tool maakt:

1. een letterlijke transcriptie met sprekers,
2. objectieve uitspraakscores,
3. een zin-voor-zin analyse (uitspraak, grammatica, logica),
4. een warme, tweetalige WhatsApp-feedbackbrief per cursist.

Er zijn twee manieren om hem te draaien:

- De webpagina `index.html` (wat jij gebruikt, gepusht naar Netlify via Antigravity).
- Het Python-script `transcribe.py` (batchverwerking op je pc; gebruik je niet actief).

## De gelaagde opzet (welke tool doet wat)

1. ElevenLabs Scribe v2: letterlijke transcriptie + sprekers + woord-tijdstempels.
2. Azure Pronunciation Assessment (nl-NL): objectieve uitspraakscores per zin, woord en klank.
3. Gemini 2.5 Pro: combineert alles tot de zin-voor-zin analyse en de feedbackbrieven.
4. (Nog te doen) LanguageTool: objectieve grammaticacheck.

Elke laag doet een ding goed. De objectieve metingen (ElevenLabs, Azure) maken de
feedback van Gemini nauwkeuriger en moeilijker te "verzinnen".

## Sleutels en instellingen (webpagina)

Alle sleutels staan lokaal in je browser (localStorage), niet in de code. Vul ze in
via het tandwiel (instellingen) op de pagina:

- Gemini API key
- ElevenLabs API key
- Azure Speech key + regio (`westeurope`)

Belangrijk: localStorage is per browser en per apparaat. Op een nieuwe pc of browser
vul je de sleutels opnieuw in via het tandwiel. Zet sleutels NOOIT in een bestand dat
je naar Netlify pusht; alles op Netlije is openbaar.

Azure aan/uit staat links onder de engine-keuze. Azure staat standaard AAN en werkt
alleen met ElevenLabs als engine.

## Wat er is gebouwd en gerepareerd

Betrouwbaarheid (Python-script `transcribe.py`):
- Retry-lus begrensd (MAX_ATTEMPTS) zodat het script nooit eindeloos blijft hangen.
- Echt verschillend fallback-model bij een 404.
- max_output_tokens ingesteld zodat lange gesprekken niet afkappen.
- Schema-controle: nooit een half/leeg resultaat opslaan.
- Standaard ElevenLabs als transcriptie-engine (scribe_v2).
- Optionele lagen ingebouwd (LanguageTool, Azure) achter vlaggen, standaard uit.

Webpagina (`index.html`):
- ElevenLabs Scribe v2 is de aanbevolen/standaard engine.
- max_output_tokens toegevoegd op alle generatiepaden (geen afgekapte brieven meer).
- Azure-uitspraaklaag volledig ingebouwd in de browser:
  - Sleutel/regio in instellingen, aan/uit-schakelaar links (standaard aan).
  - Meet per zin, per woord en per klank; scores opgeslagen bij de opname.
- Vijf tabbladen in de viewer, in deze volgorde:
  Azure (uitspraak), ElevenLabs (gehoord), Transcript gesprek, Feedbackbrief,
  Complete brief & Vertaling.
- Azure-tabblad toont kleuren (groen/oranje/rood), totaalscores en per woord de klanken.
- Gemini legt in de feedback uit "het klonk als X, het moet Y zijn" voor zwakke woorden.
- Als ElevenLabs faalt, stopt de verwerking met een duidelijke fout in plaats van
  Gemini de tekst te laten verzinnen.
- WAV-conversie gerepareerd (header stond op de verkeerde plek en negeerde stereo;
  daardoor wees ElevenLabs mp4's af als "corrupted"). Nu correct.
- Verwerkingslus pakt na een fout niet meer eindeloos hetzelfde bestand op.
- Altijd-zichtbare stopknop ("Stop / wis wachtrij") zolang er onverwerkte bestanden zijn.

Zelf toegevoegd (op je andere pc), blijft behouden:
- Voorlees-knop (luidsprekericoon) met Nederlandse stem (nl-NL), om de juiste
  uitspraak te horen.
- Audio-extractie naar WAV voor mp4/video voordat het wordt geupload.
- Betere data.js-afhandeling: verbindingsstatus, opnieuw inladen, download-fallback,
  en handmatig audio lokaliseren.

## Bekende grenzen

- Azure geeft voor Nederlands GEEN leesbare klanknamen (het fonetische IPA-alfabet
  werkt alleen voor een paar talen zoals Engels). In het Azure-tabblad zie je daarom
  "klank 1, 2, 3" met scores, niet "ui" of "g". De leesbare uitleg komt van Gemini
  in de feedbackbrief.
- Azure meet de hele opname tegen een referentietekst. Het meest betrouwbaar voor
  monologen; bij twee sprekers zijn de scores een ruwe indicatie voor het geheel.
- Werkt het best in Chrome (audio decoderen van .ogg en mp4).

## Hoe je verder werkt op een andere pc

1. De projectmap staat in Google Drive en synct automatisch mee.
2. Bewerk/deploy altijd DEZE `index.html` uit de Drive-map. Als je vanaf een andere
   pc een eigen kopie deployt, mis je de laatste fixes.
3. Push naar Netlify via Antigravity, ververs hard (Ctrl+Shift+R).
4. Vul op de live site de sleutels in via het tandwiel (eenmalig per browser).

## Volgende stap: de grammatica-laag (LanguageTool)

Doel: een objectieve, regelgebaseerde grammaticacheck toevoegen, net zoals Azure dat
voor uitspraak doet. Resultaten gaan dan mee in de Gemini-feedback zodat de
grammatica-opmerkingen op regels gebaseerd zijn in plaats van een inschatting.

Belangrijke keuze:
- Self-hosted LanguageTool (gratis, via Docker) werkt NIET met een Netlify-site,
  want je openbare website kan niet bij een servertje op je eigen laptop.
- Voor de webpagina heb je dus de betaalde LanguageTool-cloud nodig (ongeveer 5 euro
  per maand), met een API-sleutel die je in het tandwiel zet (zoals bij Azure).

Te beslissen voordat we bouwen: gaan we voor de betaalde LanguageTool-cloud in de
webpagina, of doen we de grammaticacheck alleen in het Python-script (gratis,
self-hosted) voor batchverwerking?
