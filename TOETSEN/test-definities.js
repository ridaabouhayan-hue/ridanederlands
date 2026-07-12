/* =====================================================================
   TEST-DEFINITIES — enige bron van waarheid voor het Toetsen Dashboard
   =====================================================================

   Waarom dit bestand bestaat:
   Elke toets (thema + versie) heeft zijn EIGEN aantal vragen, eigen
   sectie-betekenis en eigen puntentelling. Vroeger stond dat verspreid
   over drie plekken (de toetspagina zelf, een losse kopie in
   dashboard.html, en nog een keer hardcoded in de AI-promptteksten) en
   die raakten uit sync — vandaar bugs zoals "Sectie 4 = Geen/Niet" bij
   thema 1 (dat is fout, thema 1 sectie 4 is vraagwoorden) en "iedereen
   sloeg dictee-vraag 10 over" (bij toetsen met maar 9 dictee-items werd
   toch een 10e verwacht).

   Dit bestand is de ENIGE plek waar labels, vragen, antwoorden en
   punten bij elkaar horen. dashboard.html leest hier alles uit voor
   scoring, AI-promptopbouw en het tonen van "Vraag N: ... -> antwoord".

   NIEUWE TOETS TOEVOEGEN — kopieer dit sjabloon en vul in:

   TEST_DEFINITIES.themaX.toetsY = {
     jaar: 2026,                 // of het jaar/versie van de toets
     secties: [
       {
         id: "sec1",             // moet overeenkomen met answers.sec1 uit Firestore
         label: "Luisteren",     // wat de docent en de AI te zien krijgen
         type: "keuze",          // "keuze" | "invul" | "dictee" | "woordenschat-plaatje" | "open-ai"
         vaardigheid: "luisteren", // "luisteren" | "lezen" | "grammatica" | "schrijven"
         puntenPerVraag: 1,
         context: null,          // gedeelde leestekst/luistertekst, indien van toepassing
         vragen: ["Vraag 1 tekst...", "..."],   // exact zoveel items als antwoorden[]
         antwoorden: ["b", "a", "c", "b", "c"]  // zelfde antwoordvorm als voorheen
       },
       // ... meer secties
     ]
   };

   totaalPunten wordt NOOIT hardcoded — die wordt in dashboard.html
   berekend uit sectie.antwoorden.length * sectie.puntenPerVraag (of
   sectie.aantalZinnen voor "open-ai" secties). Zo kan een totaal nooit
   meer los raken van het echte aantal vragen.

   Vaardigheid-indeling (voor de 4 diagnostische percentages die het
   dashboard naast het totaalpercentage toont): dit is een inhoudelijke
   indeling per sectietype (luisteren/lezen/grammatica/schrijven), NIET
   een 1-op-1 kopie van de papieren Scoreformulieren — die gebruiken een
   andere opdracht-indeling (opdr. 1-7) die niet overeenkomt met de
   secties van deze digitale toetsen. "Spreekvaardigheid" komt in deze
   digitale toetsen niet voor (dat is een mondeling onderdeel) en wordt
   daarom nergens als vaardigheid gebruikt. Pas de vaardigheid-tag per
   sectie gerust aan als je een andere indeling wilt.
   ===================================================================== */

const TEST_DEFINITIES = {

    // ============================= THEMA 1 — Hallo =============================
    thema1: {
        toets1: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: "Hallo, ik heet Julia. Ik ben dertig jaar oud. Ik kom uit Spanje. Ik woon nu in Nederland, in Utrecht. Ik heb een man en twee kinderen. Mijn man heet Thomas. Mijn zoon heet Max en mijn dochter heet Emma. Ik spreek Spaans en een beetje Nederlands.",
                    vragen: [
                        "Hoe oud is Julia?",
                        "Waar komt Julia vandaan?",
                        "Waar woont Julia nu?",
                        "Hoe heet haar man?",
                        "Hoeveel kinderen heeft ze?"
                    ],
                    antwoorden: ["b", "a", "c", "b", "c"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Beste Julia, Hoe gaat het met jou? Met mij gaat het goed. Mijn naam is Anna. Ik woon in Rotterdam. Rotterdam is een grote stad in Nederland. Ik woon samen met mijn vriend. Hij heet Mark. Wij hebben geen kinderen. Ik heb wel een zus en twee broers. Mijn zus heet Sophie. Sophie woont in Utrecht. Mijn broers wonen nog in Duitsland. Groetjes, Anna",
                    vragen: [
                        "Wie schrijft de brief?",
                        "Waar woont Anna?",
                        "Met wie woont Anna samen?",
                        "Hoeveel broers heeft Anna?",
                        "Waar wonen haar broers?"
                    ],
                    antwoorden: ["b", "c", "a", "c", "b"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(heten) Ik ___ Julia.",
                        "(zijn) ___ jij getrouwd?",
                        "(komen) Wij ___ uit Spanje.",
                        "(wonen) Hij ___ in Utrecht.",
                        "(hebben) Zij ___ twee kinderen.",
                        "(zijn) Hoe oud ___ uw dochter?",
                        "(spreken) Jullie ___ goed Nederlands.",
                        "(zijn) Wij ___ erg blij.",
                        "(hebben) ___ jij een broer?",
                        "(leren) Zij ___ Nederlands op school."
                    ],
                    antwoorden: [["heet"], ["ben", "bent"], ["komen"], ["woont"], ["heeft"], ["is"], ["spreekt", "spreken"], ["zijn"], ["heb", "hebt"], ["leren", "leert"]]
                },
                {
                    id: "sec4", label: "Vul het vraagwoord in", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "___ woon jij? - Ik woon in Utrecht.",
                        "___ is dat? - Dat is mijn broer.",
                        "___ spreek jij? - Ik spreek Spaans en Nederlands.",
                        "___ kom je vandaan? - Ik kom uit Spanje.",
                        "___ is jouw docent? - Mijn docent heet Rida."
                    ],
                    antwoorden: [["waar"], ["wie"], ["wat"], ["waar"], ["wie"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["naam", "wonen", "gezin", "moeder", "getrouwd", "kind", "Ik kom uit Spanje.", "Hoe heet jouw broer?", "Mijn vader woont in Utrecht."],
                    antwoorden: [["naam"], ["wonen"], ["gezin"], ["moeder"], ["getrouwd"], ["kind"], ["ik kom uit spanje", "ik kom uit spanje."], ["hoe heet jouw broer", "hoe heet jouw broer?"], ["mijn vader woont in utrecht", "mijn vader woont in utrecht."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        toets2: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: "Hoi, ik ben Karim. Ik ben vijfentwintig jaar oud. Ik kom uit Syrië. Ik woon nu in Amsterdam. Ik ben niet getrouwd. Ik heb geen kinderen. Ik heb wel een broer en een zus. Mijn broer heet Samir en mijn zus heet Leyla. Ik spreek Arabisch en een beetje Nederlands. Ik leer Nederlands op school.",
                    vragen: [
                        "Hoe heet de man?",
                        "Hoe oud is Karim?",
                        "Waar woont Karim nu?",
                        "Is Karim getrouwd?",
                        "Hoe heet zijn broer?"
                    ],
                    antwoorden: ["b", "c", "a", "b", "c"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Mijn naam is Ali. Ik ben dertig jaar oud. Ik ben getrouwd met Fatima. Wij hebben een zoon en een dochter. Mijn zoon heet Omar. Omar is zes jaar oud. Mijn dochter heet Sara. Sara is drie jaar oud. Wij wonen in een klein huis in Haarlem. Fatima komt uit Marokko en ik kom uit Turkije. Wij praten thuis Nederlands en Turks.",
                    vragen: [
                        "Hoe heet de vrouw van Ali?",
                        "Hoeveel kinderen hebben Ali en Fatima?",
                        "Hoe oud is de dochter van Ali?",
                        "Waar woont de familie?",
                        "Welke talen praten ze thuis?"
                    ],
                    antwoorden: ["a", "c", "b", "a", "c"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    // LET OP — DATAPROBLEEM GEVONDEN, NOG NIET OPGELOST (zie opmerking onderaan dit bestand):
                    // de zinnen hieronder zijn precies wat er in A1/thema1-oefentoets2.html staat, maar de
                    // bijbehorende antwoorden (hieronder, ongewijzigd overgenomen uit de bestaande answerKeys)
                    // passen grammaticaal niet bij de werkwoord-cue van bijna elke zin (bv. item 2 heeft de cue
                    // "hebben" bij "Mijn broer ___ een grote auto", maar het opgeslagen antwoord is "zijn").
                    // Dit is een bug die al in de live toetspagina zelf zit, niet iets dat door deze module is
                    // veroorzaakt. Ik heb de bestaande antwoorden bewust NIET aangepast/gegokt — dat is een
                    // inhoudelijke beslissing die aan Rida is. Zie de opmerking aan het einde van dit bestand.
                    vragen: [
                        "(zijn) Ik ___ Karim.",
                        "(hebben) Mijn broer ___ een grote auto.",
                        "(heten) Hoe ___ uw man?",
                        "(wonen) ___ jij in Amsterdam?",
                        "(zijn) Zij ___ niet getrouwd.",
                        "(komen) Waar ___ je vandaan?",
                        "(hebben) Wij ___ geen kinderen.",
                        "(spreken) Hij ___ Spaans.",
                        "(zijn) ___ u meneer Bakker?",
                        "(hebben) ___ jullie een gezin?"
                    ],
                    antwoorden: [["ben"], ["zijn"], ["bent"], ["is"], ["bent", "ben"], ["hebben"], ["heb"], ["heeft"], ["hebben"], ["heeft"]]
                },
                {
                    id: "sec4", label: "Vul het vraagwoord in", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "___ leer jij op school? - Ik leer Nederlands.",
                        "___ woont jouw familie? - Mijn familie woont in Marokko.",
                        "___ is jouw zus? - Haar naam is Reem.",
                        "___ is Omar? - Omar is mijn zoon.",
                        "___ spreekt er Turks? - Ali spreekt Turks."
                    ],
                    antwoorden: [["wat"], ["waar"], ["wie"], ["wie"], ["wie"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["vader", "dochter", "praten", "school", "broer", "mevrouw", "Ik leer Nederlands op school.", "Waar woont jouw familie?", "Zij spreekt een beetje Nederlands."],
                    antwoorden: [["vader"], ["dochter"], ["praten"], ["school"], ["broer"], ["mevrouw"], ["ik leer nederlands op school", "ik leer nederlands op school."], ["waar woont jouw familie", "waar woont jouw familie?"], ["zij spreekt een beetje nederlands", "zij spreekt een beetje nederlands."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        }
    },

    // ============================= THEMA 7 — Reizen (officieel 2026) =============================
    thema7: {
        toets1: {
            jaar: 2026,
            officieel: true,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: null, // geen transcript beschikbaar; audio-only (Luistertekst - Toets Thema 7.mp3)
                    vragen: [
                        "Welke bus moet Eva nemen?",
                        "Hoe laat vertrekt de bus?",
                        "Hoelang moet Eva lopen naar het huis van Koen?",
                        "Waar moet Eva naar rechts?",
                        "Waar moet Eva linksaf?"
                    ],
                    antwoorden: ["b", "d", "b", "b", "b"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Aster reist meestal met de trein naar haar werk. Ze woont in Amersfoort en ze werkt in Amsterdam. Ze moet eerst twaalf minuten met de fiets naar het station. Dan zit ze een half uur in de trein. De trein rijdt 130 kilometer per uur. Daarna moet ze in Amsterdam nog vijf minuten lopen. Vandaag rijdt de trein niet. Dus Aster gaat met de auto. Ze gaat over de snelweg. Ze mag daar 100 kilometer per uur. Vandaag is het rustig. Aster moet drie kwartier rijden. Soms is het heel druk. Dan moet Aster een uur rijden. Aster vindt rijden in de file heel vervelend.",
                    vragen: [
                        "Waar woont Aster?",
                        "Hoe snel rijdt de trein?",
                        "Hoelang moet Aster nog lopen in Amsterdam?",
                        "Waarom reist Aster vandaag met de auto?",
                        "Hoelang rijdt Aster vandaag met de auto?"
                    ],
                    antwoorden: ["b", "c", "a", "a", "b"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(kunnen) We ___ hier oversteken.",
                        "(mogen) Je ___ hier niet lopen.",
                        "(kunnen) Olga ___ de metro nemen.",
                        "(kunnen) ___ u het goede spoor vinden?",
                        "(mogen) Ik ___ niet autorijden.",
                        "(kunnen) ___ je dit doorgeven aan mijn collega?",
                        "(kunnen) Snel! Jullie ___ de trein nog halen.",
                        "(mogen) Kleine kinderen ___ niet zelf reizen met het vliegtuig.",
                        "(mogen) Samir ___ niet op het fietspad rijden met zijn auto.",
                        "(kunnen) Jing en Ricardo ___ hun fiets niet vinden."
                    ],
                    antwoorden: [["kunnen"], ["mag"], ["kan"], ["kunt", "kan"], ["mag"], ["kun", "kan"], ["kunnen"], ["mogen"], ["mag"], ["kunnen"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (van wie is het?)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Van wie is die hond? (Aron en Zora)",
                        "Van wie zijn de schoenen? (jij)",
                        "Van wie is de kaart? (hij)",
                        "Van wie is de afspraak? (wij)",
                        "Van wie zijn de potloden? (jullie)"
                    ],
                    antwoorden: [["is hun hond"], ["zijn jouw schoenen", "zijn je schoenen"], ["is zijn kaart"], ["is onze afspraak"], ["zijn jullie potloden"]]
                },
                {
                    id: "sec5", label: "Woordenschat (plaatjes)", type: "woordenschat-plaatje", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["Plaatje 1", "Plaatje 2", "Plaatje 3", "Plaatje 4", "Plaatje 5", "Plaatje 6", "Plaatje 7", "Plaatje 8", "Plaatje 9", "Plaatje 10"],
                    antwoorden: [["kruispunt"], ["wachten"], ["chauffeur"], ["denken"], ["boot", "zeilboot"], ["rennen"], ["bord", "verkeersbord"], ["eiland"], ["instappen"], ["slapen"]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        }
    },

    // ============================= THEMA 8 — Vrije tijd =============================
    thema8: {
        toets1: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: null,
                    vragen: [
                        "Wat wil Lars dit weekend doen?",
                        "Wanneer gaat Lars hardlopen?",
                        "Waar gaat Lars wandelen op zondag?",
                        "Wat doet Lars op zaterdagmiddag?",
                        "Waarom gaat Lars niet zwemmen?"
                    ],
                    antwoorden: ["b", "a", "c", "b", "b"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Anna heeft volgende week vakantie. Ze gaat niet naar het buitenland, maar ze gaat leuke dingen doen in Nederland. Op maandag gaat ze met haar zus naar een museum in Amsterdam. Op woensdag gaat ze wandelen in het bos. Vrijdag gaat ze tennissen met haar vriendin Sofia. Zaterdag gaat ze naar haar ouders op de boerderij. Zondag blijft ze thuis om te rusten.",
                    vragen: [
                        "Wanneer heeft Anna vakantie?",
                        "Waar gaat ze op maandag naartoe?",
                        "Met wie gaat Anna tennissen?",
                        "Wanneer gaat ze naar haar ouders?",
                        "Wat doet ze op zondag?"
                    ],
                    antwoorden: ["b", "b", "b", "c", "b"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(gaan) ___ jij morgen tennissen?",
                        "(dansen) Emine houdt niet van ___.",
                        "(moeten) Ik ___ vandaag mijn kamer opruimen.",
                        "(komen) ___ je morgen op mijn feestje?",
                        "(willen) Wij ___ een nieuwe hobby beginnen.",
                        "(mogen) Je ___ hier niet roken.",
                        "(wandelen) Gaan jullie in het park ___?",
                        "(spelen) Julan en Tim ___ zaterdag tennis.",
                        "(kunnen) ___ u dat herhalen?",
                        "(zwemmen) Ik ga graag in de zee ___."
                    ],
                    antwoorden: [["ga", "gaat"], ["dansen"], ["moet"], ["kom", "komt"], ["willen"], ["mag"], ["wandelen"], ["spelen"], ["kunt", "kan"], ["zwemmen"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Ga jij een cursus doen?",
                        "Houdt hij van dansen?",
                        "Heeft zij een hond?",
                        "Voetballen zij zaterdag?",
                        "Is taart gezond?"
                    ],
                    antwoorden: [["ik ga geen cursus doen", "ik ga geen cursus volgen"], ["hij houdt niet van dansen"], ["zij heeft geen hond"], ["zij voetballen niet op zaterdag", "zij voetballen zaterdag niet"], ["taart is niet gezond"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["vakantie", "boerderij", "wandelen", "hobby", "vriend", "weekend", "Ik ga in het weekend wandelen.", "Wij houden van muziek en dansen.", "Wij gaan in het weekend op vakantie."],
                    antwoorden: [["vakantie"], ["boerderij"], ["wandelen"], ["hobby"], ["vriend"], ["weekend"], ["ik ga in het weekend wandelen", "ik ga in het weekend wandelen."], ["wij houden van muziek en dansen", "wij houden van muziek en dansen."], ["wij gaan in het weekend op vakantie", "wij gaan in het weekend op vakantie."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        toets2: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: null,
                    vragen: [
                        "Wat doet Thomas op maandag?",
                        "Welke dag is Thomas vrij?",
                        "Waar gaat Thomas op woensdag naartoe?",
                        "Met wie gaat Thomas tennissen?",
                        "Wat doet Thomas op zaterdag?"
                    ],
                    antwoorden: ["b", "b", "b", "b", "a"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Sarah houdt van muziek. Ze speelt gitaar in een band. Ze oefenen elke dinsdagavond in een studio. Op vrijdagavond geeft de band een concert in het café. Sarah houdt ook van sport. Ze gaat twee keer per week hardlopen in het bos. Op zondag wandelt ze met haar man in het park. Ze vindt het leuk om buiten te zijn.",
                    vragen: [
                        "Welk instrument speelt Sarah?",
                        "Wanneer oefent de band?",
                        "Waar is het concert op vrijdag?",
                        "Hoe vaak gaat Sarah hardlopen?",
                        "Met wie wandelt Sarah op zondag?"
                    ],
                    antwoorden: ["b", "a", "b", "b", "a"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(willen) Ik ___ graag een hond kopen.",
                        "(fietsen) Wij gaan morgen in de natuur ___.",
                        "(moeten) ___ jij vandaag werken?",
                        "(komen) Zij ___ vanavond ook op bezoek.",
                        "(mogen) ___ ik hier mijn auto parkeren?",
                        "(koken) Mijn moeder houdt van ___.",
                        "(spelen) De kinderen ___ in de tuin.",
                        "(kunnen) Hij ___ heel goed voetballen.",
                        "(opstaan) Wij moeten morgen vroeg ___."
                    ],
                    antwoorden: [["wil"], ["fietsen"], ["moet"], ["komen"], ["mag"], ["koken"], ["spelen"], ["kan"], ["opstaan"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Ga je morgen werken?",
                        "Woont zij in Amsterdam?",
                        "Drinkt hij melk?",
                        "Spelen zij buiten?",
                        "Is de winkel open?"
                    ],
                    antwoorden: [["ik ga morgen niet werken"], ["zij woont niet in amsterdam"], ["hij drinkt geen melk"], ["zij spelen niet buiten"], ["de winkel is niet open"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["sporten", "club", "team", "fietsen", "wedstrijd", "trainen", "Wij gaan sporten met het team.", "Ik speel graag met mijn vrienden.", "Wij eten vanavond in een gezellig restaurant."],
                    antwoorden: [["sporten"], ["club"], ["team"], ["fietsen"], ["wedstrijd"], ["trainen"], ["wij gaan sporten met het team", "wij gaan sporten met het team."], ["ik speel graag met mijn vrienden", "ik speel graag met mijn vrienden."], ["wij eten vanavond in een gezellig restaurant", "wij eten vanavond in een gezellig restaurant."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        toets3: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: null,
                    vragen: [
                        "Waar gaat Eva zaterdag naartoe?",
                        "Met wie gaat Eva?",
                        "Hoe reizen ze naar Zandvoort?",
                        "Waarom wil Maria niet zwemmen?",
                        "Wat eten ze 's avonds?"
                    ],
                    antwoorden: ["b", "b", "b", "a", "b"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Jan is een boer. Hij woont en werkt op een grote boerderij. Er zijn veel dieren op de boerderij. Jan heeft tien koeien, twintig kippen en twee paarden. Hij moet elke dag om vijf uur opstaan om de dieren te voeren. Op zaterdag kunnen mensen melk en eieren kopen op de boerderij. Jan vindt zijn werk zwaar maar erg leuk.",
                    vragen: [
                        "Wat is het beroep van Jan?",
                        "Hoeveel paarden heeft Jan?",
                        "Hoe laat moet Jan opstaan?",
                        "Wat kunnen mensen kopen op zaterdag?",
                        "Wat vindt Jan van zijn werk?"
                    ],
                    antwoorden: ["b", "b", "a", "b", "b"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(kunnen) ___ jij gitaar spelen?",
                        "(koken) Zij gaan vanavond samen ___.",
                        "(moeten) Wij ___ morgen studeren.",
                        "(mogen) Kinderen ___ hier gratis spelen.",
                        "(willen) Hij ___ geen koffie drinken.",
                        "(gaan) ___ u morgen op vakantie?",
                        "(zwemmen) Mijn broer houdt van ___.",
                        "(opstaan) Zij gaan morgen om zeven uur ___.",
                        "(bellen) Kan ik je vanavond ___?",
                        "(leren) Cursisten ___ Nederlands op school."
                    ],
                    antwoorden: [["kun", "kan"], ["koken"], ["moeten"], ["mogen"], ["wil"], ["gaat"], ["zwemmen"], ["opstaan"], ["bellen"], ["leren"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Heb jij een fiets?",
                        "Is hij vandaag vrij?",
                        "Gaan zij tennissen?",
                        "Eet jij vlees?",
                        "Komt de bus nu?"
                    ],
                    antwoorden: [["ik heb geen fiets"], ["hij is vandaag niet vrij"], ["zij gaan niet tennissen"], ["ik eet geen vlees"], ["de bus komt nu niet"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["bioscoop", "feest", "afspreken", "verjaardag", "muziek", "spelen", "Wij gaan samen naar de bioscoop.", "Wij luisteren naar klassieke muziek.", "Hij viert zijn verjaardag in de tuin."],
                    antwoorden: [["bioscoop"], ["feest"], ["afspreken"], ["verjaardag"], ["muziek"], ["spelen"], ["wij gaan samen naar de bioscoop", "wij gaan samen naar de bioscoop."], ["wij luisteren naar klassieke muziek", "wij luisteren naar klassieke muziek."], ["hij viert zijn verjaardag in de tuin", "hij viert zijn verjaardag in de tuin."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        toets4: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: "Mark en zijn vrienden gaan dit weekend kamperen. Ze vertrekken op vrijdagmiddag. Ze reizen met de auto naar de camping. Op zaterdag gaan ze fietsen in de omgeving. 's Avonds maken ze een vuur en gaan ze barbecueën bij de tent.",
                    vragen: [
                        "Waar gaan Mark en zijn vrienden dit weekend naartoe?",
                        "Wanneer vertrekken ze?",
                        "Waarmee reizen ze?",
                        "Wat doen ze op zaterdag?",
                        "Wat doen ze op zaterdagavond?"
                    ],
                    antwoorden: ["b", "a", "c", "b", "c"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Sara houdt heel veel van wandelen en van de natuur. Elke zaterdagochtend gaat ze naar het bos met haar hond Max. Ze wandelen samen ongeveer twee uur. Na de wandeling is Sara moe en drinkt ze een lekker kopje thee. Op zondag blijft Sara graag thuis. Dan leest ze een boek op de bank.",
                    vragen: [
                        "Wat vindt Sara erg leuk?",
                        "Met wie gaat ze zaterdagochtend naar het bos?",
                        "Hoelang wandelen ze in het bos?",
                        "Wat doet Sara na de wandeling?",
                        "Wat doet Sara op zondag?"
                    ],
                    antwoorden: ["c", "b", "b", "b", "a"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(kunnen) Wij ___ goed gitaar spelen.",
                        "(willen) ___ jij vanavond naar de film?",
                        "(mogen) Kinderen ___ hier gratis naar binnen.",
                        "(gaan) Hij ___ morgen vissen met zijn vader.",
                        "(komen) ___ jullie vanavond ook op het feest?",
                        "(tennissen) Gaan wij morgen samen ___?",
                        "(moeten) Ik ___ nu echt naar huis gaan.",
                        "(hardlopen) Lars houdt van ___ in het park.",
                        "(kunnen) ___ u mij helpen met dit formulier?",
                        "(sporten) Wij ___ elke woensdag in de sportschool."
                    ],
                    antwoorden: [["kunnen"], ["wil", "wilt"], ["mogen"], ["gaat"], ["komen"], ["tennissen"], ["moet"], ["hardlopen"], ["kunt", "kan"], ["sporten"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Speel jij piano?",
                        "Is de film leuk?",
                        "Ga je vandaag sporten?",
                        "Heeft Jan een auto?",
                        "Is bier gezond?"
                    ],
                    antwoorden: [["ik speel geen piano"], ["de film is niet leuk"], ["ik ga vandaag niet sporten", "ik ga niet sporten vandaag"], ["jan heeft geen auto"], ["bier is niet gezond"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["kamperen", "hobby", "vriend", "gezellig", "wandelen", "weekend", "Mark gaat in het weekend kamperen.", "Wij luisteren graag naar muziek.", "Ik wil graag met mijn vriend wandelen."],
                    antwoorden: [["kamperen"], ["hobby"], ["vriend"], ["gezellig"], ["wandelen"], ["weekend"], ["mark gaat in het weekend kamperen", "mark gaat in het weekend kamperen."], ["wij luisteren graag naar muziek", "wij luisteren graag naar muziek."], ["ik wil graag met mijn vriend wandelen", "ik wil graag met mijn vriend wandelen."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        toets5: {
            jaar: 2024,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: "Lisa en Thomas willen hun vakantie plannen. Lisa wil graag twee weken naar Italië. Thomas wil liever in Nederland blijven en gaan vissen en zeilen. Ze praten er lang over. Uiteindelijk besluiten ze om samen te gaan kamperen in de Ardennen.",
                    vragen: [
                        "Wat willen Lisa en Thomas plannen?",
                        "Waar wil Lisa naartoe?",
                        "Wat wil Thomas in Nederland doen?",
                        "Wat besluiten ze uiteindelijk te gaan doen?",
                        "Hoelang wil Lisa in Italië blijven?"
                    ],
                    antwoorden: ["b", "a", "c", "b", "b"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "De sportclub van Emma organiseert vandaag een sportdag. Emma doet mee aan drie onderdelen: hardlopen, zwemmen en tennissen. Het tennissen begint om tien uur 's ochtends. Emma vindt zwemmen het allerleukst. Aan het einde van de dag krijgt iedereen een prijs. Emma is heel blij, want zij krijgt een gouden medaille.",
                    vragen: [
                        "Wat organiseert de club van Emma vandaag?",
                        "Aan hoeveel onderdelen doet Emma mee?",
                        "Hoe laat begint het tennissen?",
                        "Wat vindt Emma het allerleukst?",
                        "Wat krijgt Emma aan het einde van de dag?"
                    ],
                    antwoorden: ["b", "c", "a", "b", "c"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(mogen) Cursisten ___ hier gratis parkeren.",
                        "(kunnen) ___ jij morgen met mij mee naar de markt?",
                        "(willen) Wij ___ volgend jaar een reis maken.",
                        "(vissen) Mijn opa houdt erg van ___ in het kanaal.",
                        "(moeten) Jij ___ je huiswerk vandaag afmaken.",
                        "(gaan) Morgen ___ wij zwemmen in de zee.",
                        "(komen) Wie ___ er vanavond op bezoek?",
                        "(zeilen) Zij gaan in de vakantie ___ op de meren.",
                        "(kunnen) Hij ___ heel goed Nederlands spreken.",
                        "(spelen) De kinderen ___ buiten in de tuin."
                    ],
                    antwoorden: [["mogen"], ["kan", "kun"], ["willen"], ["vissen"], ["moet"], ["gaan"], ["komt", "komen"], ["zeilen"], ["kan"], ["spelen"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Woont zij in Utrecht?",
                        "Heb jij een fiets?",
                        "Kookt hij vanavond?",
                        "Is dit jouw boek?",
                        "Heeft Ali een gitaar?"
                    ],
                    antwoorden: [["zij woont niet in utrecht"], ["ik heb geen fiets"], ["hij kookt vanavond niet", "hij kookt niet vanavond"], ["dit is niet mijn boek"], ["ali heeft geen gitaar"]]
                },
                {
                    id: "sec5", label: "Dictee", type: "dictee", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["sporten", "wedstrijd", "team", "weekend", "vakantie", "samen", "Wij gaan samen op vakantie.", "Emma doet mee aan de wedstrijd.", "Ik wil graag sporten in het weekend."],
                    antwoorden: [["sporten"], ["wedstrijd"], ["team"], ["weekend"], ["vakantie"], ["samen"], ["wij gaan samen op vakantie", "wij gaan samen op vakantie."], ["emma doet mee aan de wedstrijd", "emma doet mee aan de wedstrijd."], ["ik wil graag sporten in het weekend", "ik wil graag sporten in het weekend."]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        },
        officieel2026: {
            jaar: 2026,
            officieel: true,
            secties: [
                {
                    id: "sec1", label: "Luisteren", type: "keuze", vaardigheid: "luisteren", puntenPerVraag: 1,
                    context: null, // geen transcript beschikbaar; audio-only (Luistertekst - Toets Thema 8.mp3)
                    vragen: [
                        "Wat doet Sanne op zondagavond?",
                        "Waarom wil Sanne niet naar de zee?",
                        "Waar gaan Sanne en Naima wandelen?",
                        "Hoe laat gaat Naima naar Sanne?",
                        "Waar woont Sanne?"
                    ],
                    antwoorden: ["a", "c", "b", "a", "b"]
                },
                {
                    id: "sec2", label: "Lezen", type: "keuze", vaardigheid: "lezen", puntenPerVraag: 1,
                    context: "Samir is volgende week vrij. Hij gaat niet op vakantie, maar hij gaat wel veel leuke dingen doen. Maandag gaat hij op bezoek bij zijn moeder. Ze woont op een boerderij in Bloemendaal. Zijn moeder is oud. Samir helpt met de dieren. Op dinsdag gaat hij sporten met een vriend. Ze gaan 's avonds uit eten in een restaurant in Haarlem. Samir traint op woensdag met zijn team in Alkmaar. Ze spelen op zaterdag een wedstrijd. Samir is dus nog vrij op donderdag en vrijdag. Hij wil op donderdag naar een museum. Op vrijdag blijft hij thuis.",
                    vragen: [
                        "Waar woont de moeder van Samir?",
                        "Wanneer helpt Samir op de boerderij?",
                        "Met wie gaat Samir uit eten?",
                        "Wanneer speelt het team een wedstrijd?",
                        "Wanneer wil Samir naar het museum?"
                    ],
                    antwoorden: ["b", "a", "a", "d", "b"]
                },
                {
                    id: "sec3", label: "Grammatica", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 1,
                    vragen: [
                        "(gaan) ___ jij je inschrijven?",
                        "(dansen) Emine houdt niet van ___.",
                        "(komen) ___ Nahom ook voetballen?",
                        "(moeten) Ik ___ het huis schoonmaken.",
                        "(tekenen) Nahom kan goed ___.",
                        "(mogen) Je ___ vandaag niet in de zee zwemmen.",
                        "(trainen) Het team gaat veel ___.",
                        "(sporten) Julan en Tim gaan zaterdag ___.",
                        "(gaan) Ik ___ met vrienden fietsen.",
                        "(kunnen) ___ u dat herhalen?"
                    ],
                    antwoorden: [["ga"], ["dansen"], ["komt"], ["moet"], ["tekenen"], ["mag"], ["trainen"], ["sporten"], ["ga"], ["kunt"]]
                },
                {
                    id: "sec4", label: "Geef antwoord (niet/geen)", type: "invul", vaardigheid: "grammatica", puntenPerVraag: 3,
                    vragen: [
                        "Ga jij een cursus doen?",
                        "Houdt hij van dansen?",
                        "Heeft zij een hond?",
                        "Voetballen zij zaterdag?",
                        "Is taart gezond?"
                    ],
                    antwoorden: [["ik ga geen cursus doen", "ik ga geen cursus volgen"], ["hij houdt niet van dansen"], ["zij heeft geen hond"], ["zij voetballen zaterdag niet", "zij voetballen niet op zaterdag"], ["taart is niet gezond"]]
                },
                {
                    id: "sec5", label: "Woordenschat (plaatjes)", type: "woordenschat-plaatje", vaardigheid: "schrijven", puntenPerVraag: 3,
                    vragen: ["Plaatje 1", "Plaatje 2", "Plaatje 3", "Plaatje 4", "Plaatje 5", "Plaatje 6", "Plaatje 7", "Plaatje 8", "Plaatje 9: niet de heer, maar ___", "Plaatje 10"],
                    antwoorden: [["kat"], ["bal"], ["tent"], ["zwembad"], ["kletsen", "zij kletsen"], ["bloem", "bloemen"], ["zingen", "hij zingt"], ["wandelen", "zij wandelen"], ["dame"], ["schaap"]]
                },
                {
                    id: "sec6", label: "Schrijven (Praatplaat)", type: "open-ai", vaardigheid: "schrijven", puntenPerVraag: 3,
                    aantalZinnen: 4,
                    instructie: "Kijk naar de praatplaat. Wat zie je? Geef vier antwoorden. Maak hele zinnen."
                }
            ]
        }
    }
};

/* -----------------------------------------------------------------------
   OPEN PUNT VOOR RIDA — nog niet opgelost, bewust niet gegokt:
   In thema1.toets2, sectie 3 ("Vul in") passen de opgeslagen antwoorden
   niet bij de werkwoord-cues in de zinnen (bv. item 2 heeft cue "hebben"
   bij "Mijn broer ___ een grote auto", maar het opgeslagen antwoord is
   "zijn" — dat klopt grammaticaal niet). Dit zit al zo in de live
   toetspagina A1/thema1-oefentoets2.html zelf (regels 294-322 vs
   982-993), dus cursisten die deze toets al hebben gemaakt zijn mogelijk
   al verkeerd nagekeken. Ik heb de bestaande antwoorden hier bewust NIET
   gewijzigd/gegokt, omdat alleen jij kunt beoordelen wat de bedoelde
   correcte antwoorden per zin zijn. Corrigeer de "antwoorden"-array
   hierboven (thema1.toets2.secties[2]) zodra je de juiste antwoorden
   hebt vastgesteld — de rest van het dashboard leest automatisch de
   bijgewerkte waarden.
   ----------------------------------------------------------------------- */

/* Vaardigheid-labels voor de UI (diagnostische vaardigheidsbalkjes) */
const VAARDIGHEID_LABELS = {
    luisteren: "Luisteren",
    lezen: "Lezen",
    grammatica: "Grammatica",
    schrijven: "Schrijven"
};

/* -----------------------------------------------------------------------
   Helper: haal de juiste testdefinitie op voor een submission.
   Regels: thema7 heeft maar 1 versie ("toets1"); thema8's officiële
   2026-toets wordt herkend via testNum die "OFFICIEEL" bevat; alle
   andere gevallen matchen op "toets" + testNum (bv. testNum "2" -> toets2).
   ----------------------------------------------------------------------- */
function getTestDefinitie(theme, testNum) {
    const themaDef = TEST_DEFINITIES[theme];
    if (!themaDef) return null;

    if (theme === "thema7") {
        return themaDef.toets1 || null;
    }

    if (testNum && String(testNum).toUpperCase().includes("OFFICIEEL")) {
        return themaDef.officieel2026 || themaDef["toets" + testNum] || null;
    }

    const key = "toets" + (testNum || "1");
    return themaDef[key] || null;
}

/* Totaalpunten van een testdefinitie: NOOIT hardcoded, altijd berekend
   uit de secties zelf zodat het totaal nooit los kan raken van het
   werkelijke aantal vragen. */
function getTotaalPunten(testDef) {
    if (!testDef) return 0;
    return testDef.secties.reduce((sum, sec) => {
        const aantal = sec.type === "open-ai" ? (sec.aantalZinnen || 0) : (sec.antwoorden ? sec.antwoorden.length : 0);
        return sum + aantal * sec.puntenPerVraag;
    }, 0);
}
