# Systeem Instructies voor NOS in Makkelijke Taal

**Beste AI (Antigravity),**

Wanneer de gebruiker vraagt om een **nieuw NOS-transcript** te verwerken, volg je ALTIJD deze exacte stappen. De gebruiker hoeft alleen de onbewerkte transcript-tekst en de YouTube-link in de chat te plakken. Jij doet de rest!

## 1. Doel & Opzet
Het doel is om een interactieve HTML-pagina te genereren gebaseerd op `transcript_template.html`.
*   We gebruiken `transcript_style.css` voor alle opmaak.
*   De gebruiker navigeert via een taalbalk (`.lang-switcher`) om **ENG**, **TR**, **AR**, **Farsi**, **Dari** of **VN** te selecteren.
*   Moeilijke en belangrijke woorden worden klikbaar gemaakt met een zwevende tooltip.

## 2. Bestanden die je moet aanmaken/updaten
*   Kopieer de inhoud van `transcript_template.html`.
*   Sla dit op als een nieuw bestand, bijvoorbeeld `transcript_nos_10mei.html`.
*   Voeg de link naar dit nieuwe bestand toe aan `index.html`.

## 3. Vertalingen & Tooltips (CRUCIAAL)
Wanneer je de tekst van het transcript in de HTML plaatst, moet je de belangrijkste **5 tot 15 moeilijke steekwoorden** markeren. 
*   Vertaal niet té veel woorden (de student moet zelf ook moeite doen).
*   Kies woorden die essentieel zijn voor het begrijpen van het onderwerp.

Je wikkelt deze woorden in een `<span>` tag met de class `vocab` en de benodigde data-attributen voor **Engels (en)**, **Turks (tr)**, **Arabisch (ar)**, **Farsi (fa)**, **Dari (da)** en **Vietnamees (vi)**.

**Voorbeeld format:**
```html
<p>De problemen met het <span class="vocab" data-en="power grid" data-tr="elektrik şebekesi" data-ar="شبكة الكهرباء" data-fa="شبکه برق" data-da="شبکه برق" data-vi="lưới điện">stroomnet</span> zijn niet alleen in Utrecht.</p>
```

**Let op:**
*   De `data-en`, `data-tr`, `data-ar`, `data-fa`, `data-da` en `data-vi` attributen zijn verplicht voor elk gemarkeerd woord.
*   Gebruik géén `<span class="dict-word">` of inline `onclick` functies meer; het nieuwe systeem draait volledig op `.vocab` en de script-logica die in de template staat.

## 4. YouTube Video & Structuur
*   Plaats de YouTube-ID in de `<iframe>` bovenaan.
*   Verdeel de tekst logisch over `<div class="topic-card">` blokken, met een passende emoji in de `.topic-icon`.
*   Gebruik de `<div class="quote-box">` als er mensen geïnterviewd worden.
*   Als alles erin staat, zorg er dan voor dat het `<script>` blok onderaan de body staat (zoals in het sjabloon) zodat de tooltips werken.

Volg dit systeem altijd strikt op, zodat we elke week snel en efficiënt nieuwe lesmaterialen kunnen toevoegen!
