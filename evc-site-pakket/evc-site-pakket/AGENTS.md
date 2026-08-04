# AGENTS.md : Bouwinstructies EVC-portfoliosite Rida

Jij bent de bouwagent. Bouw van de bestanden in `bron/` een samenhangende, statische multi-page website die als geheel naar Netlify wordt gedeployed (site: evc-dashboard-rida.netlify.app). De site is het persoonlijke voorbereidings- en werkstation van Rida Abouhayan voor het BVNT2 EVC-traject "Competent NT2-docent".

## Harde regels

1. Alles in het Nederlands.
2. Gebruik NOOIT het em dash-teken (het lange streepje). Gebruik een punt, komma of dubbele punt. Controleer dit in alle gegenereerde tekst.
3. Statische site, geen build-frameworks nodig: pure HTML/CSS/JS, geen externe dependencies of CDN's. Alles moet offline werken.
4. Behoud alle bestaande content en functionaliteit uit de bronbestanden. Niets weggooien, alleen herstructureren en verbinden.
5. Responsive (mobiel eerst testen) en print-vriendelijk (@media print per pagina).
6. Alle opslag loopt via de bestaande `StorageAdapter` (zit in bron/evc-dashboard.html). Til die op naar een gedeeld script en behoud het uitgecommentarieerde Firebase-skelet: later wordt localStorage vervangen door Firestore door alleen de adapter om te zetten. Gebruik één consistent sleutel-prefix `evc_` voor alle pagina's.

## Bronbestanden

- `bron/evc-dashboard.html`: het bestaande dashboard. Bevat: hero, voortgangsbalk, snake-roadmap met 6 fases, competentiekaarten, bewijsstukkentabel, 2 interactieve checklists (localStorage), STARR-uitleg met 2 uitgewerkte voorbeelden, lesobservatie, 360-graden vragen, logboek-sjabloon, tools, documentenkluis (upload naar localStorage), valkuilen, tips, bronnen.
- `bron/opdrachtenoverzicht-rida.html`: kleurgecodeerd overzicht per opdrachtgever (Basten groen, Square Mile blauw, STE amber, F9 rood, overig paars) met Excel-achtige kolomfilters (sorteren, zoeken, waarde-checkboxes per kolomkop).
- `bron/Pre-planning_info_v2.md`: projectinstructies, statusoverzicht per competentie (bron van waarheid), profiel van Rida, wekelijks ritme.

## Doelstructuur

```
site/
├── index.html          Landingspagina: welkom, totale voortgang, snelkoppelingen naar alle onderdelen, "volgende actie"-blok
├── dashboard.html      Het bestaande dashboard (roadmap, checklists, STARR-uitleg, observatie, 360, logboek, tools, valkuilen, tips, bronnen)
├── opdrachten.html     Het opdrachtenoverzicht met de Excel-filters, ongewijzigd overgenomen
├── status.html         Interactief statusoverzicht: de tabellen uit Pre-planning_info_v2.md per competentie, elk onderdeel met status-dropdown (Nog te doen / Bezig / Concept klaar / Definitief) die opslaat via StorageAdapter, plus voortgang per competentie
├── profiel.html        Het profiel van Rida uit de md, netjes opgemaakt, plus de werkervaringstabel
├── starrs/
│   ├── index.html      Overzicht van alle STARR's met status
│   └── sjabloon.html   Leeg STARR-invulformulier (S/T/A/R/R-velden, textarea's, opslaan via StorageAdapter, export naar klembord als platte tekst)
├── documenten.html     De documentenkluis uit het dashboard als eigen pagina
└── assets/
    ├── stijl.css       Gedeelde stijl
    └── kern.js         StorageAdapter (incl. Firebase-skelet), gedeelde nav-logica, voortgangsberekening
```

## Navigatie en linking

- Eén gedeelde sticky navigatiebalk op elke pagina met: Start, Dashboard, Status, Opdrachten, STARR's, Profiel, Documenten. Actieve pagina gemarkeerd.
- Kruislinks aanleggen waar inhoud elkaar raakt:
  - Elke competentiekaart in dashboard.html linkt naar het bijbehorende blok op status.html (anchors per competentie: #a2, #a3, enz.).
  - Elke rij "Bewijs + STARR" op status.html linkt naar starrs/sjabloon.html.
  - De portfolio-waarde blokken in opdrachten.html linken naar de genoemde competenties op status.html.
  - De roadmapfases in dashboard.html linken naar de relevante checklistsecties.
- De totale voortgangsbalk op index.html telt alle checkboxes (dashboard) plus alle statusvelden (status.html, waarbij Definitief = af) samen.

## Ontwerp

Gebruik exact het bestaande palet uit de bronbestanden: inktblauw #16324A, blauw #3D6FA5, groen #2E7D6B, papier #FBFAF7, amber #D98C2B, rood #B3543E. Georgia/Charter voor koppen, systeem-sans voor lopende tekst. Rustig en professioneel, geen decoratie die afleidt. Kaarten met zachte schaduwen, afgeronde hoeken 14px, consistent met de bron.

## Statusoverzicht: exacte inhoud

Neem de competentietabellen letterlijk over uit `bron/Pre-planning_info_v2.md` (sectie "Statusoverzicht"), inclusief alle notities en bewijsideeën. Elke rij krijgt een dropdown met de vier statussen en een vrij notitieveld (opslaan via StorageAdapter, sleutel per rij, bijv. `evc_status_a4_bewijs1`).

## Netlify

- Deploy-root is de map `site/`.
- Maak in de projectroot een `netlify.toml` met `publish = "site"` (staat al klaar, controleer hem).
- Geen serverfuncties nodig. Na het bouwen: `netlify deploy --prod` of drag & drop van de map `site/` in de Netlify UI, project "evc-dashboard-rida".

## Opleverchecklist voor jou als agent

- [ ] Alle pagina's delen assets/stijl.css en assets/kern.js, geen dubbele inline kopieën van de StorageAdapter
- [ ] Checkbox- en statusdata blijven bewaard na herladen (test in browser)
- [ ] Geen em dash in welke tekst dan ook
- [ ] Alle interne links werken (ook de anchors)
- [ ] Mobiel: nav scrollt horizontaal, tabellen scrollen binnen hun container
- [ ] Print: nav en knoppen verborgen, secties breken netjes
- [ ] De Excel-kolomfilters in opdrachten.html werken ongewijzigd
