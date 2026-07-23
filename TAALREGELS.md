# Taalregels — geen vaste brugtaal, ooit

Dit bestand is bindend voor elke AI (Claude Code, Antigravity, Lovable) die
content, oefeningen of teksten maakt of aanpast op dit platform. Lees dit
**voordat** je een woordenschat- of vertaaloefening schrijft.

## Het probleem dat dit voorkomt

Bestaande content bevat oefeningen zoals:

```json
{"prompt": "Hoe zeg je \"name\" in het Nederlands?", "options": ["naam", "jaar", "man"]}
{"prompt": "Hoe zeg je \"good morning\" in het Nederlands?", ...}
```

Het Engelse woord staat hier **letterlijk en vast** in de tekst, ongeacht
welke taal de cursist zelf heeft ingesteld (`profiles.display_language_code`).
Een cursist met Turks, Arabisch of gewoon Nederlands als voorkeurstaal krijgt
alsnog Engels te zien. Dat is nooit de bedoeling geweest — Engels is hier
zonder reden als "universele brugtaal" gebruikt.

## De harde regel

1. **Nederlandstalige content bevat nooit een andere taal**, tenzij die tekst
   expliciet en correct gekoppeld is aan de taal die de cursist zelf heeft
   gekozen — en dan **alleen** die ene taal, nooit standaard Engels.
2. **Engels is nooit de standaard-brugtaal.** Als een vertaling nodig is,
   wordt die per cursist bepaald door `profiles.display_language_code` —
   niet hardgecodeerd in de content.
3. **Vertaling is vaak niet eens nodig.** Bij de meeste woordenschat-oefeningen
   kan een vertaalvraag vervangen worden door een taalneutrale synoniem-,
   context- of definitievraag in het Nederlands zelf. Dat heeft de voorkeur
   boven vertalen, want het werkt voor iedereen ongeacht taalinstelling.

## Hoe het wel moet

**Optie A — voorkeur: maak vertaling overbodig.**
In plaats van:
> "Hoe zeg je 'bread' in het Nederlands?" → naam / jaar / man

Gebruik een Nederlandse context- of definitievraag:
> "Wat koop je bij de bakker, gemaakt van meel?" → brood / melk / kaas
> "___ is te koop bij de bakker." (cloze, antwoord: brood)

**Optie B — als vertaling echt nodig is: per taal, dynamisch getoond.**
Sla de vertaling op zoals `explanations.body_translations` dat al doet: een
JSONB-object met één sleutel per taalcode uit de `languages`-tabel
(`nl`, `en`, `tr`, `ar`, `fa`, `zh`, `pl`, ...), en toon in de UI **alleen**
de sleutel die hoort bij `profiles.display_language_code` van de ingelogde
cursist. Nooit een vaste taal in de hoofdtekst van de oefening zelf.

```json
{
  "prompt_nl": "Wat betekent dit woord?",
  "word": "brood",
  "translations": { "en": "bread", "tr": "ekmek", "ar": "خبز", "fa": "نان" }
}
```

De frontend kiest dan zelf `translations[profile.display_language_code]` —
nooit een vast veld dat toevallig Engels bevat.

## Bekende, nog openstaande gerelateerde bug

De taal-dropdown in de app slaat `display_language_code` wel op, maar
**niets in de lespagina leest dat veld momenteel uit** om de juiste
vertaling te tonen — ook de al goed opgeslagen `body_translations` bij
uitlegteksten worden nooit gefilterd op de taal van de cursist. Dit moet
samen met de contentfix hierboven aangepakt worden, anders blijft het
mechanisme correct opgeslagen maar functioneel dood.

## Controle op bestaande content

`/admin/curriculum` (of een vergelijkbaar overzicht) hoort een lijst te
tonen van oefeningen waarvan de prompt/opties verdacht Engels bevatten
(heuristisch — quotes rond een Engels woord, "Hoe zeg je", "What does...",
veelvoorkomende Engelse functiewoorden). Dit is een detectiehulpmiddel, geen
garantie — uiteindelijk is menselijke review nodig per gevonden item.
