# NT2 Leerplatform — Toetsen Ontwikkeling Standaard (2026)

Dit document bevat de strikte richtlijnen en standaarden voor het ontwikkelen, onderhouden en toevoegen van nieuwe oefentoetsen (zoals voor Thema 1, 2, etc.) binnen dit project. Deze regels moeten door elke AI-ontwikkelaar en programmeur strikt worden nageleefd om bugs met achtergrondkleuren, mediaspelers en nakijkfouten te voorkomen.

---

## 1. Naamgeving & Bestandsstructuur
- **Oefentoetsen**: Plaats oefentoetsen voor een specifiek thema in de map `/A1/` met de naamgeving: `thema[Nummer]-oefentoets[ToetsNummer].html` (bijv. `thema1-oefentoets1.html`).
- **Thema-index**: De indexpagina van het thema is altijd `/A1/thema[Nummer].html` (bijv. `thema8.html`). Oefentoetsen worden onderaan deze pagina getoond onder het kopje **Oefentoetsen**.
- **Dashboard**: Het docentendashboard bevindt zich in `/TOETSEN/dashboard.html`.

---

## 2. Centrale Antwoordsleutels & Synchronisatie
Bij het maken van oefentoetsen moeten de antwoordsleutels op **twee** plaatsen exact identiek zijn:
1. **Lokaal**: In het HTML-bestand van de oefentoets zelf (in het scriptgedeelte onder `const answerKeys = { ... };`).
2. **Dashboard**: In `/TOETSEN/dashboard.html` in het globale `answerKeys` object:
   ```javascript
   const answerKeys = {
       thema8: {
           toets1: { ... },
           toets2: { ... }
       },
       thema1: { // NIEUW THEMA HIER TOEVOEGEN
           toets1: {
               sec1: [...],
               sec2: [...],
               sec3: [...],
               sec4: [...],
               sec5: [...]
           }
       }
   };
   ```
- **Strikte Regel**: De volgorde en waarden in het dashboard moeten 100% overeenkomen met wat de student hoort en invult. Voeg alternatieve antwoorden (bijv. met of zonder punt/hoofdletter) toe als sub-arrays (bijv. `["antwoord", "antwoord."]`).

---

## 3. Achtergrondkleuren & Donkere Modus (Dark Mode)
Om te zorgen dat de unieke achtergrondkleur van elke oefentoets goed werkt en ook netjes meekleurt in de donkere modus, moeten de volgende CSS-regels gebruikt worden in het `<style>` blok van de oefentoets:

```css
:root {
    --toets-bg: #fff5f5; /* Unieke lichte pastelkleur per oefentoets */
    --toets-accent: #FF6B6B; /* Unieke accentkleur */
}
[data-theme="dark"] {
    --toets-bg: #0f1729 !important; /* Standaard donkere achtergrond */
}
html, body {
    background: var(--toets-bg) !important;
    background-color: var(--toets-bg) !important;
}
main.page-container {
    background: var(--toets-bg) !important;
}
.language-bar {
    background: var(--toets-bg) !important;
}
.quiz-card { 
    border-left: 4px solid var(--toets-accent) !important; 
}
.choice-btn:hover, .choice-btn.selected { 
    border-color: var(--toets-accent) !important; 
    background: rgba(255, 107, 107, 0.08) !important; 
}
.page-header h1 { 
    color: var(--toets-accent) !important; 
}
.back-link { 
    color: var(--toets-accent) !important; 
}
```
- **Strikte Regel**: Gebruik **nooit** inline styles op het `<body>`-element (dus altijd een schone `<body>` tag). Anders wordt de donkere modus geblokkeerd.

---

## 4. Mediaspeler & Spraaksynthese (Audio)
Wanneer er gebruik wordt gemaakt van de ingebouwde spraaksynthese (`SpeechSynthesis`) voor de luistertekst of het dictee, moeten de volgende regels worden toegepast om vastlopen van de browser te voorkomen:

1. **Race-conditions voorkomen (setTimeout)**:
   Bij het starten van de audio moet er altijd een kleine pauze zitten na het annuleren van eerdere spraak om de spraak-engine van de browser te resetten:
   ```javascript
   if (!isSpeaking) {
       window.speechSynthesis.cancel();
       setTimeout(() => {
           speechUtterance = new SpeechSynthesisUtterance(text);
           // ... configuratie ...
           window.speechSynthesis.speak(speechUtterance);
       }, 100); // 100ms vertraging voorkomt vastlopen
   }
   ```
2. **Dictee (Geen meervoud/enkelvoud tegelijk uitspreken)**:
   Tekst tussen haakjes mag nooit uitgesproken of getoond worden in het dictee. Gebruik de volgende regex om tekst tussen haakjes te verwijderen vóór het uitspreken:
   ```javascript
   const cleanText = text.replace(/\([^)]+\)/g, '').trim();
   ```

---

## 5. AI Feedbackbrieven & Docentnaam
- **Ondertekening**: Alle door AI gegenereerde feedbackbrieven moeten persoonlijk ondertekend worden met **Rida**. Het prompt in `/TOETSEN/dashboard.html` moet dit expliciet afdwingen (vervang `[Je docent]` door `Rida`).
- **Dictee Beoordeling**: De AI mag in de brief nooit alternatieve meervoudsvormen noemen als de cursist een fout maakt. Dit verwart de cursist.

---

## 6. Woordenlijst Beperking
- **Strikte Regel**: Alle dicteewoorden en zinnen die in de oefentoetsen worden gebruikt, moeten uitsluitend afkomstig zijn uit de officiële woordenlijst van het desbetreffende A1 thema. Introduceer geen onbekende woorden.

---

## 7. ElevenLabs Audio Generatie (Dictee & Luisteren)
- **Strikte Regel**: Alle met ElevenLabs (of andere API's) gegenereerde audiobestanden voor dictee en luisteropdrachten moeten voldoen aan de **NT2 Nederlands examen A1/A2-standaard**. Dit houdt in:
  - Uiterst duidelijke, rustige en heldere uitspraak.
  - Een langzamer spreektempo zodat het voor cursisten goed te volgen is en oneerlijkheden worden voorkomen.
  - In de generatiescripts (bijv. [genereer_toets_audio.py](file:///c:/Users/Rabou/Mijn%20Drive/HTML%20FILES/genereer_toets_audio.py)) moeten de steminstellingen voor stabiliteit en gelijkenis (`stability` en `similarity_boost`) ingesteld zijn op ten minste `0.85` voor dicteewoorden om een stabiele en rustige intonatie te garanderen.

