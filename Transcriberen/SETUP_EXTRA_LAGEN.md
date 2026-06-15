# Setup: extra analyselagen (LanguageTool + Azure)

Deze twee lagen zijn al in `transcribe.py` ingebouwd, maar staan standaard **uit**.
Je script werkt dus gewoon zonder dat je iets doet. Zet een laag pas aan als de
bijbehorende dienst draait. Beide lagen werken alleen in de **ElevenLabs-modus**
(`TRANSCRIPTION_SERVICE = "elevenlabs"`), want ze hebben de letterlijke
transcriptie als basis nodig.

Samengevat:

| Laag | Wat het toevoegt | Kosten | Aanzetten met |
|---|---|---|---|
| LanguageTool | Objectieve, regelgebaseerde grammatica-/spelcheck | Gratis (self-hosted) | `ENABLE_LANGUAGETOOL = True` |
| Azure Pronunciation | Objectieve uitspraakscores per klank (0-100) | Gratis tot 5 uur/maand, daarna ca. 0,15-0,18 euro/uur | `ENABLE_AZURE_PRONUNCIATION = True` |

---

## 1. LanguageTool (self-hosted, gratis)

LanguageTool draait als een klein servertje op je eigen computer. Niets gaat naar
internet, dus dit is ook de privacy-vriendelijke keuze.

### Stap 1: Docker installeren
Installeer **Docker Desktop** (eenmalig): https://www.docker.com/products/docker-desktop

### Stap 2: De server starten
Open een terminal en draai:

```
docker run -d -p 8081:8010 --name languagetool erikvl87/languagetool
```

Dit start LanguageTool op poort **8081** op je computer. De server blijft draaien
op de achtergrond (ook na herstart van Docker). Controleer in je browser:
http://localhost:8081/v2/languages zou een lijst met talen moeten tonen.

Stoppen kan met `docker stop languagetool`, weer starten met `docker start languagetool`.

### Stap 3: Aanzetten in het script
Zet boven in `transcribe.py`:

```python
ENABLE_LANGUAGETOOL = True
```

De waarde `LANGUAGETOOL_URL = "http://localhost:8081/v2/check"` klopt al met de
Docker-poort hierboven. Als de server niet draait, slaat het script deze stap
netjes over (zonder te crashen).

---

## 2. Azure Pronunciation Assessment (gratis tier)

Dit geeft objectieve uitspraakscores per woord en per klank voor Nederlands
(nl-NL): accuratesse, vloeiendheid en volledigheid. Dat is precies wat grote
taal-apps gebruiken om uitspraak te beoordelen.

> Let op: het meet de hele opname tegen een referentietekst. Voor **monologen**
> is dit heel betrouwbaar. Bij **twee sprekers** zijn de scores een ruwe
> indicatie van het geheel.

### Stap 1: Een gratis Speech-resource maken
1. Maak een (gratis) account op https://azure.microsoft.com
2. Ga in de Azure-portal naar **Create a resource** en zoek op **Speech**.
3. Kies bij prijscategorie **Free F0** (5 audio-uur per maand gratis).
4. Kies een regio dicht bij huis, bijvoorbeeld **West Europe**.
5. Na het aanmaken vind je onder **Keys and Endpoint** je **Key** en **Location/Region**.

### Stap 2: Sleutel opslaan
Maak in de **hoofdmap** (een map boven deze projectmap, naast `API.txt`) een
bestand `API_AZURE.txt` met deze inhoud:

```
AZURE_SPEECH_KEY=jouw_sleutel_hier
AZURE_SPEECH_REGION=westeurope
```

(Gebruik de regio-code zonder spaties, bijv. `westeurope`, `northeurope`.)

### Stap 3: Benodigde software
Azure heeft een Python-pakket en ffmpeg nodig (voor het omzetten van .ogg naar wav):

```
pip install azure-cognitiveservices-speech
```

ffmpeg installeren: https://ffmpeg.org/download.html (op Windows: voeg de map met
`ffmpeg.exe` toe aan je PATH). Controleer met `ffmpeg -version`.

### Stap 4: Aanzetten in het script
Zet boven in `transcribe.py`:

```python
ENABLE_AZURE_PRONUNCIATION = True
```

Ontbreekt de sleutel, het pakket of ffmpeg, dan slaat het script de stap netjes
over zonder te stoppen.

---

## Hoe het samenwerkt

1. **ElevenLabs Scribe v2** maakt de letterlijke transcriptie + sprekersherkenning.
2. **LanguageTool** controleert de grammatica van die tekst (objectief).
3. **Azure** meet de uitspraak van de opname (objectief, per klank).
4. **Gemini 2.5 Pro** krijgt alles binnen (transcriptie + grammaticameldingen +
   uitspraakscores + jouw opdracht-context) en schrijft de warme, tweetalige
   WhatsApp-feedbackbrief. De objectieve cijfers maken de feedback nauwkeuriger
   en moeilijker te "verzinnen".
5. **Jouw web-UI** blijft het controlepunt: je leest de transcriptie na voordat
   je de brieven definitief maakt.

## Privacy (AVG)

Je verwerkt herkenbare stemmen van cursisten. Vraag toestemming, zet geen volledige
echte namen in bestandsnamen die naar een clouddienst gaan, en check per dienst of
audio wordt bewaard. LanguageTool self-hosted houdt grammaticacontrole volledig
lokaal; Azure verwerkt audio in de gekozen EU-regio (West Europe / North Europe).

## Kosten kort

- LanguageTool self-hosted: 0 euro.
- Azure: gratis tot 5 audio-uur per maand, daarna enkele centen per uur.
- Gemini en ElevenLabs: dat betaal je al.

Voor normale lesvolumes blijft dit dus rond de 0 euro per maand bovenop wat je nu hebt.
