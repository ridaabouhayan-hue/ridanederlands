# -*- coding: utf-8 -*-
import json
import os

a1_topics = [
    # Categorie 1: Thema 1 & 2
    {
        "id": 1,
        "cat": "cat1",
        "title": "Ik, jij, wij (Persoonlijke voornaamwoorden)",
        "desc_nl": "De woorden die naar personen verwijzen als onderwerp van de zin (ik, jij, u, hij, zij, het, wij, jullie, zij).",
        "desc_en": "Subject pronouns pointing to people (ik, jij, u, hij, zij, het, wij, jullie, zij).",
        "desc_pl": "Zaimki osobowe w roli podmiotu (ik, jij, u, hij, zij, het, wij, jullie, zij).",
        "ex": "Ik leer Nederlands, zij woont in Delft."
    },
    {
        "id": 2,
        "cat": "cat1",
        "title": "Het werkwoord zijn",
        "desc_nl": "De vervoeging van het onregelmatige hulpwerkwoord zijn (ik ben, jij bent, hij/zij is, wij/jullie/zij zijn).",
        "desc_en": "Conjugation of the irregular verb zijn (to be).",
        "desc_pl": "Odmiana nieregularnego czasownika zijn (być).",
        "ex": "Ik ben moe. Wij zijn in de klas."
    },
    {
        "id": 3,
        "cat": "cat1",
        "title": "Het werkwoord hebben",
        "desc_nl": "De vervoeging van het onregelmatige hulpwerkwoord hebben (ik heb, jij hebt, hij/zij heeft, wij/jullie/zij hebben).",
        "desc_en": "Conjugation of the irregular verb hebben (to have).",
        "desc_pl": "Odmiana nieregularnego czasownika hebben (mieć).",
        "ex": "Ik heb een boek. Zij heeft pauze."
    },
    {
        "id": 4,
        "cat": "cat1",
        "title": "Vraagwoorden (Wie, wat, waar)",
        "desc_nl": "Vraagwoorden om informatie te vragen: wie (personen), wat (dingen), waar (plaatsen).",
        "desc_en": "Question words: wie (who), wat (what), waar (where).",
        "desc_pl": "Zaimki pytające: wie (kto), wat (co), waar (gdzie).",
        "ex": "Wie ben jij? Waar woon je?"
    },
    {
        "id": 5,
        "cat": "cat1",
        "title": "Tegenwoordige tijd: stam + t",
        "desc_nl": "Bij jij, u, hij, zij en het krijgt het werkwoord stam + t. Bij ik gebruiken we de stam.",
        "desc_en": "Present tense singular conjugation: stem + t for jij, u, hij, zij, het. Ik uses the stem.",
        "desc_pl": "Czas teraźniejszy l. poj.: temat + t dla jij, u, hij, zij, het. Ik używa czystego tematu.",
        "ex": "Hij drinkt thee. Jij werkt hard."
    },
    {
        "id": 6,
        "cat": "cat1",
        "title": "Tegenwoordige tijd: meervoud",
        "desc_nl": "Bij wij, jullie en zij gebruiken we het hele werkwoord (infinitive).",
        "desc_en": "Present tense plural: we use the infinitive (hele werkwoord) for wij, jullie, zij.",
        "desc_pl": "Czas teraźniejszy l. mn.: używamy bezokolicznika (hele werkwoord) dla wij, jullie, zij.",
        "ex": "Wij leren Nederlands. Jullie drinken koffie."
    },
    {
        "id": 7,
        "cat": "cat1",
        "title": "Klinkers en medeklinkers (maan - man)",
        "desc_nl": "Korte en lange klinkers in gesloten en open lettergrepen (maan - man, tak - taken).",
        "desc_en": "Short and long vowels in closed and open syllables (maan - man).",
        "desc_pl": "Długie i krótkie samogłoski w sylabach otwartych i zamkniętych (maan - man).",
        "ex": "Het is een grote maan. De man loopt op straat."
    },
    {
        "id": 8,
        "cat": "cat1",
        "title": "Spellingregels werkwoorden (wonen, spreken)",
        "desc_nl": "Klinkers behouden bij werkwoordsvervoeging (ik woon - wij wonen, ik spreek - wij spreken).",
        "desc_en": "Vowel spelling rules for verb conjugations (ik woon - wij wonen).",
        "desc_pl": "Zasady pisowni samogłosek przy odmianie czasowników (ik woon - wij wonen).",
        "ex": "Ik woon in Utrecht. Wij wonen in Nederland."
    },

    # Categorie 2: Thema 3 & 4
    {
        "id": 9,
        "cat": "cat2",
        "title": "Wisseling f -> v en s -> z",
        "desc_nl": "In het meervoud veranderen f in v en s in z (ik schrijf - wij schrijven, ik kies - wij kiezen).",
        "desc_en": "F changes to v, and s changes to z in plurals and infinitives.",
        "desc_pl": "Litery f i s przechodzą w v i z w liczbie mnogiej i bezokolicznikach.",
        "ex": "Ik schrijf een brief. Wij schrijven een e-mail."
    },
    {
        "id": 10,
        "cat": "cat2",
        "title": "Zinsbouw: Hoofdzin (SVO)",
        "desc_nl": "De basiswoordvolgorde in een Nederlandse hoofdzin: Onderwerp - Werkwoord - Rest.",
        "desc_en": "Basic word order in a main clause: Subject - Verb - Rest.",
        "desc_pl": "Podstawowy szyk zdania głównego: Podmiot - Czasownik - Reszta.",
        "ex": "De cursist leert Nederlands op school."
    },
    {
        "id": 11,
        "cat": "cat2",
        "title": "Korte en onregelmatige werkwoorden (komen, gaan, doen)",
        "desc_nl": "Vervoeging van veelgebruikte korte werkwoorden: komen (ik kom, hij komt), gaan (ik ga, hij gaat), doen (ik doe, hij doet).",
        "desc_en": "Conjugation of short, common irregular verbs like komen, gaan, doen.",
        "desc_pl": "Odmiana często używanych krótkich czasowników: komen, gaan, doen.",
        "ex": "Ik ga naar de markt. Wat doe jij?"
    },
    {
        "id": 12,
        "cat": "cat2",
        "title": "Ja/nee-vragen (Inversie)",
        "desc_nl": "Vragen zonder vraagwoord beginnen met het werkwoord, gevolgd door het onderwerp.",
        "desc_en": "Yes/no questions start with the verb, followed by the subject.",
        "desc_pl": "Pytania tak/nie zaczynają się od czasownika, po którym następuje podmiot.",
        "ex": "Werk jij vandaag? Gaan jullie mee?"
    },
    {
        "id": 13,
        "cat": "cat2",
        "title": "Vraagwoordvragen",
        "desc_nl": "Vragen met een vraagwoord: Vraagwoord - Werkwoord - Onderwerp - Rest.",
        "desc_en": "Information questions: Question word - Verb - Subject - Rest.",
        "desc_pl": "Pytania szczegółowe: Zaimek pytający - Czasownik - Podmiot - Reszta.",
        "ex": "Wanneer ga je naar de markt? Waar koopt Hans fruit?"
    },
    {
        "id": 14,
        "cat": "cat2",
        "title": "Meervoud met -en (lip - lippen)",
        "desc_nl": "Zelfstandige naamwoorden maken meervoud met -en, let op klinkerbehoud (lip - lippen, oor - oren).",
        "desc_en": "Plural of nouns ending in -en, maintaining short/long vowel sounds.",
        "desc_pl": "Liczba mnoga rzeczowników z końcówką -en, z zachowaniem krótkich/długich samogłosek.",
        "ex": "Ik heb twee oren en tien tenen."
    },
    {
        "id": 15,
        "cat": "cat2",
        "title": "Meervoud met wisseling f -> v en s -> z",
        "desc_nl": "Bij meervoud met -en verandert f in v en s in z (het huis - de huizen, de brief - de brieven).",
        "desc_en": "Plurals where f changes to v and s changes to z (het huis - de huizen).",
        "desc_pl": "Liczba mnoga, w której f zmienia się w v, a s w z (het huis - de huizen).",
        "ex": "Er zijn veel huizen in deze straat."
    },

    # Categorie 3: Thema 5 & 6
    {
        "id": 16,
        "cat": "cat3",
        "title": "Lidwoorden: de, het, een",
        "desc_nl": "Bepaalde lidwoorden (de/het) en onbepaald lidwoord (een). De voor mannelijk/vrouwelijk/meervoud, het voor onzijdig.",
        "desc_en": "Definite (de/het) and indefinite (een) articles.",
        "desc_pl": "Przedimki określone (de/het) i nieokreślony (een).",
        "ex": "De man eet het kindje een appel."
    },
    {
        "id": 17,
        "cat": "cat3",
        "title": "Jij of u? (Formeel vs Informeel)",
        "desc_nl": "Gebruik 'jij' voor vrienden, familie en collega's. Gebruik 'u' voor onbekenden, ouderen of formeel.",
        "desc_en": "Using informal 'jij' vs formal 'u'.",
        "desc_pl": "Używanie nieformalnego 'jij' oraz formalnego 'u'.",
        "ex": "Spreekt u Nederlands? Werk jij hier?"
    },
    {
        "id": 18,
        "cat": "cat3",
        "title": "Meervoud met -s",
        "desc_nl": "Woorden eindigend op el, em, en, er of onbepaalde klinkers krijgen vaak een -s in het meervoud (de sleutel - de sleutels, de dokter - de dokters).",
        "desc_en": "Plurals with -s for words ending in unstressed syllables.",
        "desc_pl": "Liczba mnoga z końcówką -s dla słów kończących się na nieakcentowane sylaby.",
        "ex": "De dokters hebben de sleutels."
    },
    {
        "id": 19,
        "cat": "cat3",
        "title": "Waarom en omdat (Bijzinvolgorde)",
        "desc_nl": "Vraag met 'waarom'. Geef antwoord met 'omdat'. In de bijzin na 'omdat' staan de werkwoorden achteraan.",
        "desc_en": "Asking why (waarom) and answering because (omdat). After 'omdat', verbs go to the end.",
        "desc_pl": "Pytanie o przyczynę (waarom) i odpowiedź (omdat). Po 'omdat' czasowniki idą na koniec zdania.",
        "ex": "Waarom ga je slapen? Omdat ik moe ben."
    },
    {
        "id": 20,
        "cat": "cat3",
        "title": "Welk? Welke?",
        "desc_nl": "Gebruik 'welke' voor de-woorden en meervoud. Gebruik 'welk' voor het-woorden.",
        "desc_en": "Which? Use 'welke' for de-words and plurals, 'welk' for het-words.",
        "desc_pl": "Który? Używaj 'welke' dla słów de i liczby mnogiej, 'welk' dla słów het.",
        "ex": "Welke schoenen koop je? Welk boek lees jij?"
    },
    {
        "id": 21,
        "cat": "cat3",
        "title": "Modale werkwoorden: willen",
        "desc_nl": "Het modale werkwoord willen (ik wil, jij wil/wilt, u wilt, wij willen) + hele werkwoord achteraan.",
        "desc_en": "Conjugating 'willen' (to want). The main verb goes to the end.",
        "desc_pl": "Odmiana czasownika 'willen' (chcieć) + główny czasownik na końcu.",
        "ex": "Ik wil graag een rode jas kopen."
    },
    {
        "id": 22,
        "cat": "cat3",
        "title": "De klok (Kwart, half, over, voor)",
        "desc_nl": "Tijd uitdrukken op de analoge klok: over, voor, half, kwart voor, kwart over.",
        "desc_en": "Telling time on the analog clock.",
        "desc_pl": "Określanie czasu na zegarze analogowym.",
        "ex": "Het is kwart over drie. Het is tien over half vier."
    },

    # Categorie 4: Thema 7 & 8
    {
        "id": 23,
        "cat": "cat4",
        "title": "Modale werkwoorden: kunnen en mogen",
        "desc_nl": "Kunnen (optie/capaciteit) en mogen (toestemming) vervoegen. Het hoofdwerkwoord staat achteraan.",
        "desc_en": "Conjugating 'kunnen' (can/ability) and 'mogen' (may/permission). Main verb goes to the end.",
        "desc_pl": "Odmiana czasowników 'kunnen' (móc/potrafić) i 'mogen' (mieć pozwolenie). Główny czasownik na końcu.",
        "ex": "U kunt hier oversteken. Mag ik hier fietsen?"
    },
    {
        "id": 24,
        "cat": "cat4",
        "title": "Voorzetsels van plaats",
        "desc_nl": "Voorzetsels die een locatie aanduiden (op, in, onder, boven, naast, achter, voor, tussen).",
        "desc_en": "Prepositions of place (on, in, under, next to, behind).",
        "desc_pl": "Przyimki miejsca (na, w, pod, obok, za, przed).",
        "ex": "De auto staat voor het huis. De sleutel ligt op de tafel."
    },
    {
        "id": 25,
        "cat": "cat4",
        "title": "Voorzetsels van tijd",
        "desc_nl": "Voorzetsels die tijd aangeven (voor, na, om, op, in, tijdens).",
        "desc_en": "Prepositions of time (before, after, at, on, in).",
        "desc_pl": "Przyimki czasu (przed, po, o, w).",
        "ex": "Ik ga op donderdag om negen uur naar de les."
    },
    {
        "id": 26,
        "cat": "cat4",
        "title": "Bezittelijk voornaamwoord (mijn, jouw, zijn...)",
        "desc_nl": "Bezitsvormen: mijn, jouw/je, uw, zijn, haar, ons/onze, jullie, hun.",
        "desc_en": "Possessive pronouns: my, your, his, her, our, their.",
        "desc_pl": "Zaimki dzierżawcze: mój, twój, jego, jej, nasz, ich.",
        "ex": "Zij draagt haar jas. Wij zetten onze fietsen weg."
    },
    {
        "id": 27,
        "cat": "cat4",
        "title": "Zinsbouw: Inversie door Tijd of Plaats",
        "desc_nl": "Als een zin begint met tijd (morgen) of plaats (in de klas), wissel je het onderwerp en het werkwoord om.",
        "desc_en": "Subject-verb inversion when a sentence starts with time or place.",
        "desc_pl": "Inwersja podmiotu i czasownika, gdy zdanie zaczyna się od czasu lub miejsca.",
        "ex": "Elke zaterdag gaat Richard sporten. Morgen reis ik naar Utrecht."
    },
    {
        "id": 28,
        "cat": "cat4",
        "title": "Ontkenning: geen of niet",
        "desc_nl": "Gebruik 'geen' bij onbepaalde zelfstandige naamwoorden (met een/zonder lidwoord). Gebruik 'niet' voor werkwoorden, bijvoeglijk naamwoorden, en bepaalde woorden.",
        "desc_en": "Use 'geen' for indefinite nouns. Use 'niet' for verbs, adjectives, and definite words.",
        "desc_pl": "Używaj 'geen' dla rzeczowników nieokreślonych. Używaj 'niet' dla czasowników, przymiotników i słów określonych.",
        "ex": "Ik drink geen bier. Ik ga niet op vakantie."
    },
    {
        "id": 29,
        "cat": "cat4",
        "title": "Aanwijzend voornaamwoord: dit, dat, deze, die",
        "desc_nl": "Dichtbij: deze (de-woord) en dit (het-woord). Ver weg: die (de-woord) en dat (het-woord).",
        "desc_en": "Demonstrative pronouns: close (deze/dit) vs far (die/dat).",
        "desc_pl": "Zaimki wskazujące: blisko (deze/dit) vs daleko (die/dat).",
        "ex": "Deze broek is mooi, maar dat t-shirt is te klein."
    }
]

a1_quizzes = {
    1: {
        "examples": ["Ik ben leraar.", "Jij leert Nederlands.", "Wij wonen in Delft."],
        "questions": [
            {"q": "Welk voornaamwoord past? '___ ben Julia.'", "o": ["Ik", "Jij", "Hij"], "c": 0, "e": "Bij 'ben' hoort altijd het onderwerp 'Ik'."},
            {"q": "Kies het juiste woord: 'Wonen ___ in Amsterdam?'", "o": ["hij", "jullie", "zij (sing)"], "c": 1, "e": "Bij een meervoudsvorm als 'wonen' past 'jullie' (of 'wij'/'zij' meervoud)."},
            {"q": "Wat is correct? '___ leert Nederlands.'", "o": ["Ik", "Zij", "Wij"], "c": 1, "e": "Bij 'leert' (stam + t) past een 3e persoon enkelvoud, zoals 'Zij'."}
        ]
    },
    2: {
        "examples": ["Ik ben blij.", "U bent vriendelijk.", "Zij zijn thuis."],
        "questions": [
            {"q": "Wat is de juiste vorm? 'Mijn vader ___ docent.'", "o": ["is", "bent", "zijn"], "c": 0, "e": "Mijn vader is 3e persoon enkelvoud (hij) -> is."},
            {"q": "Vul in: 'Hoe laat ___ het?'", "o": ["bent", "is", "zijn"], "c": 1, "e": "'Het' krijgt de vorm 'is' -> 'is het'."},
            {"q": "Kies de juiste zin:", "o": ["Wij ben cursisten.", "Wij bent cursisten.", "Wij zijn cursisten."], "c": 2, "e": "Bij 'wij' (meervoud) hoort 'zijn'."}
        ]
    },
    3: {
        "examples": ["Ik heb een kat.", "Hij heeft een auto.", "Jullie hebben een pen."],
        "questions": [
            {"q": "Vul in: 'Jij ___ een mooi huis.'", "o": ["hebt", "heeft", "hebben"], "c": 0, "e": "Bij 'jij' hoort de vorm 'hebt'."},
            {"q": "Welke vorm is goed? 'U ___ een vraag.'", "o": ["hebt", "heeft", "hebben"], "c": 1, "e": "Bij 'u' hoort de vorm 'heeft' (hoewel 'hebt' soms informeel kan, is 'heeft' de standaard)."},
            {"q": "Kies de juiste meervoudszin:", "o": ["Zij heeft vakantie.", "Zij hebben vakantie.", "Zij hebt vakantie."], "c": 1, "e": "'Zij' (meervoud) krijgt 'hebben' -> 'Zij hebben vakantie'."}
        ]
    },
    4: {
        "examples": ["Wie is dat?", "Wat zoek je?", "Waar is de klas?"],
        "questions": [
            {"q": "Vul in: '___ kom je vandaan?' - 'Uit Syrië.'", "o": ["Wat", "Wie", "Waar"], "c": 2, "e": "Voor herkomst/locatie gebruik je het vraagwoord 'Waar' (met vandaan)."},
            {"q": "Vul in: '___ is de docent?' - 'Dat is meneer Bakker.'", "o": ["Wat", "Wie", "Waar"], "c": 1, "e": "Voor personen gebruik je 'Wie'."},
            {"q": "Vul in: '___ kost dit boek?'", "o": ["Wat", "Wie", "Waar"], "c": 0, "e": "Voor objecten of prijzen gebruik je 'Wat'."}
        ]
    },
    5: {
        "examples": ["Ik werk.", "Jij werkt.", "Hij maakt een toets."],
        "questions": [
            {"q": "Vul de juiste vorm in: 'Bjorn ___ in het boek.' (schrijven)", "o": ["schrijft", "schrijf", "schrijven"], "c": 0, "e": "Bjorn is 'hij', dus stam + t -> 'schrijft'."},
            {"q": "Wat is correct? '___ je morgen ook?' (werken)", "o": ["Werk", "Werkt", "Werken"], "c": 0, "e": "Als 'je/jij' achter de persoonsvorm staat, vervalt de 't' -> 'Werk je'."},
            {"q": "Vul in: 'Leah ___ de baby.' (horen)", "o": ["hoor", "hoort", "horen"], "c": 1, "e": "Leah is 'zij' (enkelvoud), dus stam + t -> 'hoort'."}
        ]
    },
    6: {
        "examples": ["Wij leren veel.", "Jullie drinken water.", "Zij maken huiswerk."],
        "questions": [
            {"q": "Vul in: 'Stefan en Guido ___ zaterdag vrij zijn.' (willen)", "o": ["wil", "wilt", "willen"], "c": 2, "e": "Stefan en Guido zijn meervoud (zij), dus hele werkwoord -> 'willen'."},
            {"q": "Kies de juiste vorm: 'De cursisten ___ in de klas.' (zitten)", "o": ["zit", "zitten", "zittten"], "c": 1, "e": "Cursisten is meervoud -> hele werkwoord 'zitten'."},
            {"q": "Vul in: 'Jullie ___ een koekje.' (eten)", "o": ["eet", "eten", "eetn"], "c": 1, "e": "Bij 'juliie' hoort het hele werkwoord 'eten'."}
        ]
    },
    7: {
        "examples": ["Man -> Mannen", "Maan -> Manen", "Tak -> Taken"],
        "questions": [
            {"q": "Wat is het meervoud van 'man' (short vowel)?", "o": ["manen", "mannen", "mans"], "c": 1, "e": "Korte klinker blijft kort door dubbele medeklinker -> 'mannen'."},
            {"q": "Wat is het meervoud van 'maan' (long vowel)?", "o": ["mannen", "manen", "maanen"], "c": 1, "e": "Lange klinker wordt geschreven met één klinker in een open lettergreep -> 'manen'."},
            {"q": "Kies het correct gespelde meervoud van 'tas':", "o": ["tasen", "tassn", "tassen"], "c": 2, "e": "Korte klinker 'a' in 'tas' vereist verdubbeling van 's' -> 'tassen'."}
        ]
    },
    8: {
        "examples": ["Wonen -> ik woon, wij wonen", "Spreken -> ik spreek, wij spreken"],
        "questions": [
            {"q": "Wat is de ik-vorm van 'wonen'?", "o": ["woon", "won", "woone"], "c": 0, "e": "De stam heeft een lange klinker nodig in een gesloten lettergreep -> 'woon'."},
            {"q": "Wat is de hij-vorm van 'spreken'?", "o": ["spreekt", "sprekt", "spreekt"], "c": 0, "e": "Stam ('spreek') + t -> 'spreekt'."},
            {"q": "Vul in: 'Wij ___ in Utrecht.' (wonen)", "o": ["woon", "woont", "wonen"], "c": 2, "e": "Bij 'wij' gebruiken we de volledige vorm van het werkwoord -> 'wonen'."}
        ]
    },
    9: {
        "examples": ["Schrijven -> ik schrijf, wij schrijven", "Kiezen -> ik kies, wij kiezen"],
        "questions": [
            {"q": "Wat is de ik-vorm van 'schrijven'?", "o": ["schrijf", "schrijv", "schrijfe"], "c": 0, "e": "Aan het einde van een lettergreep verandert 'v' in 'f' -> 'schrijf'."},
            {"q": "Wat is de wij-vorm van 'kiezen'?", "o": ["kies", "kiezen", "kiezzn"], "c": 1, "e": "In het hele werkwoord (en meervoud) behouden we de 'z' -> 'kiezen'."},
            {"q": "Vul in: 'Jij ___ een stoel.' (kiezen)", "o": ["kies", "kiest", "kiezt"], "c": 1, "e": "Stam is 'kies' (van kiezen, s aan het eind). Stam + t -> 'kiest'."}
        ]
    },
    10: {
        "examples": ["Wij huren een huis.", "De straat is druk.", "De man kijkt op internet."],
        "questions": [
            {"q": "Zet in de juiste volgorde: 'een huis | Wij | huren'", "o": ["Wij huren een huis.", "Wij een huis huren.", "Huren wij een huis."], "c": 0, "e": "Hoofdzin volgorde is Onderwerp (Wij) + Werkwoord (huren) + Rest (een huis)."},
            {"q": "Kies de grammaticaal correcte zin:", "o": ["De man op internet kijkt.", "De man kijkt op internet.", "Kijkt de man op internet."], "c": 1, "e": "Het werkwoord 'kijkt' moet op positie 2 staan -> 'De man kijkt op internet.'"},
            {"q": "Zet in de juiste volgorde: 'druk | De straat | is'", "o": ["Is de straat druk.", "De straat druk is.", "De straat is druk."], "c": 2, "e": "Onderwerp (De straat) + Werkwoord (is) + Adjectief (druk)."}
        ]
    },
    11: {
        "examples": ["Ik ga naar de stad.", "Petra gaat naar de markt.", "Wat doe jij?"],
        "questions": [
            {"q": "Wat is de goede vorm? 'Petra ___ naar de markt.' (gaan)", "o": ["ga", "gaat", "gaan"], "c": 1, "e": "Petra is 'zij' (sing), dus stam + t -> 'gaat'."},
            {"q": "Vul in: 'Lars ___ uit school.' (komen)", "o": ["kom", "komt", "komen"], "c": 1, "e": "Lars (hij) -> 'komt'."},
            {"q": "Kies de juiste zin:", "o": ["Wat doen jij?", "Wat doe jij?", "Wat doet jij?"], "c": 1, "e": "Bij 'jij' achter het werkwoord vervalt de 't' bij 'doen' -> 'Wat doe jij?'."}
        ]
    },
    12: {
        "examples": ["Wilt u zegels?", "Gebruiken jullie mes en vork?", "Vindt Kim wortels lekker?"],
        "questions": [
            {"q": "Maak een vraag met: 'u | zegels | Wilt'", "o": ["Wilt u zegels?", "U wilt zegels?", "Zegels wilt u?"], "c": 0, "e": "Een ja/nee-vraag begint met het werkwoord (Wilt) + onderwerp (u) + rest (zegels)."},
            {"q": "Maak een vraag met: 'mes en vork | jullie | Gebruiken'", "o": ["Jullie gebruiken mes en vork?", "Gebruiken jullie mes en vork?", "Gebruiken mes en vork jullie?"], "c": 1, "e": "Werkwoord (Gebruiken) + onderwerp (jullie) + object (mes en vork)."},
            {"q": "Maak een vraag met: 'wortels lekker | Vindt | Kim'", "o": ["Vindt Kim wortels lekker?", "Kim vindt wortels lekker?", "Vindt wortels lekker Kim?"], "c": 0, "e": "Werkwoord (Vindt) + onderwerp (Kim) + rest (wortels lekker)."}
        ]
    },
    13: {
        "examples": ["Wat heb jij nodig?", "Waar koopt Hans fruit?", "Wanneer ga je naar de markt?"],
        "questions": [
            {"q": "Maak een vraag met: 'jij | nodig | Wat | heb'", "o": ["Wat heb jij nodig?", "Wat jij heb nodig?", "Heb jij wat nodig?"], "c": 0, "e": "Vraagwoord (Wat) + Werkwoord (heb) + Onderwerp (jij) + rest (nodig)."},
            {"q": "Maak een vraag met: 'fruit | Waar | Hans | koopt'", "o": ["Waar koopt Hans fruit?", "Waar Hans koopt fruit?", "Koopt Hans waar fruit?"], "c": 0, "e": "Vraagwoord (Waar) + Werkwoord (koopt) + Onderwerp (Hans) + object (fruit)."},
            {"q": "Maak een vraag met: 'Wanneer | naar de markt | ga | je'", "o": ["Wanneer je ga naar de markt?", "Wanneer ga je naar de markt?", "Ga je wanneer naar de markt?"], "c": 1, "e": "Vraagwoord (Wanneer) + Werkwoord (ga) + Onderwerp (je) + rest."}
        ]
    },
    14: {
        "examples": ["De kip -> de kippen", "Het bed -> de bedden", "De teen -> de tenen"],
        "questions": [
            {"q": "Wat is het meervoud van 'de kip'?", "o": ["de kipen", "de kippen", "de kips"], "c": 1, "e": "Korte klinker 'i' vereist verdubbeling van 'p' -> 'kippen'."},
            {"q": "Wat is het meervoud van 'het bed'?", "o": ["de bedden", "de beden", "de beds"], "c": 0, "e": "Korte klinker 'e' vereist verdubbeling van 'd' -> 'bedden'."},
            {"q": "Wat is het meervoud van 'de teen'?", "o": ["de tenen", "de teennen", "de teens"], "c": 0, "e": "Lange klinker 'ee' wordt 'e' in een open lettergreep -> 'tenen'."}
        ]
    },
    15: {
        "examples": ["Het huis -> de huizen", "De brief -> de brieven"],
        "questions": [
            {"q": "Wat is het meervoud van 'het huis'?", "o": ["de huisen", "de huizen", "de huizzn"], "c": 1, "e": "In het meervoud verandert 's' in 'z' -> 'huizen'."},
            {"q": "Wat is het meervoud van 'de brief'?", "o": ["de briefen", "de brieven", "de briefes"], "c": 1, "e": "In het meervoud verandert 'f' in 'v' -> 'brieven'."},
            {"q": "Kies de juiste meervoudsvorm voor 'het glas':", "o": ["de glasen", "de glazen", "de glassen"], "c": 1, "e": "De klinker wordt lang en s verandert in z -> 'glazen'."}
        ]
    },
    16: {
        "examples": ["De man, het kind, een appel."],
        "questions": [
            {"q": "Welk lidwoord hoort bij 'auto'?", "o": ["de", "het", "een (alleen)"], "c": 0, "e": "Het is 'de auto'."},
            {"q": "Welk lidwoord hoort bij 'boek'?", "o": ["de", "het", "een (alleen)"], "c": 1, "e": "Het is 'het boek'."},
            {"q": "Welke zin is correct?", "o": ["Mats heeft melk nodig.", "Mats heeft een melk nodig.", "Mats heeft de melk nodig (onbepaald)."], "c": 0, "e": "'Melk' is niet-telbaar, dus geen lidwoord 'een' -> 'Mats heeft melk nodig'."}
        ]
    },
    17: {
        "examples": ["Spreekt u Nederlands?", "Werk jij hier?"],
        "questions": [
            {"q": "Je praat met je docent. Welk pronomen gebruik je?", "o": ["jij", "u", "je"], "c": 1, "e": "Tegen een docent of onbekende volwassene zeg je uit beleefdheid 'u'."},
            {"q": "Je praat met je broer. Welk pronomen gebruik je?", "o": ["jij", "u", "ge"], "c": 0, "e": "Tegen familie en vrienden zeg je 'jij'."},
            {"q": "Kies de meest beleefde vraag aan een vreemde op straat:", "o": ["Hoe heet jij?", "Hoe heet u?", "Hoe heet je?"], "c": 1, "e": "'Hoe heet u?' is beleefd en formeel."}
        ]
    },
    18: {
        "examples": ["De sleutel -> de sleutels", "De dokter -> de dokters"],
        "questions": [
            {"q": "Wat is het meervoud van 'de sleutel'?", "o": ["de sleutelen", "de sleutels", "de sleutelz"], "c": 1, "e": "Woorden op -el krijgen een -s -> 'sleutels'."},
            {"q": "Wat is het meervoud van 'de dokter'?", "o": ["de dokters", "de dokteren", "de doktersen"], "c": 0, "e": "Woorden op -er krijgen een -s -> 'dokters'."},
            {"q": "Wat is het meervoud van 'de tafel'?", "o": ["de tafelen", "de tafels", "de tafelles"], "c": 1, "e": "Woord eindigt op -el -> 'tafels'."}
        ]
    },
    19: {
        "examples": ["Waarom leer je Nederlands? Omdat ik in Nederland woon."],
        "questions": [
            {"q": "Kies de juiste zin na 'omdat':", "o": ["Omdat ik moet naar de dokter.", "Omdat ik naar de dokter moet.", "Omdat moet ik naar de dokter."], "c": 1, "e": "'Omdat' introduceert een bijzin, dus alle werkwoorden gaan naar het einde -> 'omdat ik naar de dokter moet'."},
            {"q": "Vul in: '___ moet Suze naar de dokter? Omdat ze buikpijn heeft.'", "o": ["Waarom", "Wat", "Waar"], "c": 0, "e": "Bij een antwoord met 'omdat' hoort de vraag 'Waarom'."},
            {"q": "Kies het juiste einde van de zin: 'Ik ga niet werken omdat ik ziek ___.'", "o": ["ben", "is", "hebt"], "c": 0, "e": "Bijzin werkwoord achteraan: 'omdat ik (onderwerp) ziek ben (werkwoord)'."}
        ]
    },
    20: {
        "examples": ["Welke schoenen draagt zij?", "Welk shirt vind je leuk?"],
        "questions": [
            {"q": "Vul in: '___ boek lees jij?' (het boek)", "o": ["Welk", "Welke", "Welken"], "c": 0, "e": "Bij het-woorden hoort 'welk' -> 'Welk boek'."},
            {"q": "Vul in: '___ jas draag jij?' (de jas)", "o": ["Welk", "Welke", "Welker"], "c": 1, "e": "Bij de-woorden hoort 'welke' -> 'Welke jas'."},
            {"q": "Vul in: '___ oorbellen wil je?' (meervoud)", "o": ["Welk", "Welke", "Welkes"], "c": 1, "e": "Bij meervoud hoort altijd 'welke' -> 'Welke oorbellen'."}
        ]
    },
    21: {
        "examples": ["Stefan wil zaterdag vrij zijn.", "Ik wil naar huis gaan."],
        "questions": [
            {"q": "Vul in: 'Miranda ___ groene oorbellen.'", "o": ["wil", "wilt", "willen"], "c": 0, "e": "Miranda is 'zij' (enkelvoud). De vorm is 'wil' (zonder t)."},
            {"q": "Vul in: '___ u de kleren daar ophangen?'", "o": ["Wil", "Wilt", "Willen"], "c": 1, "e": "Bij 'u' hoort de vorm 'wilt' -> 'Wilt u'."},
            {"q": "Kies de juiste volgorde:", "o": ["Ik wil kopen een jas.", "Ik wil een jas kopen.", "Ik een jas kopen wil."], "c": 1, "e": "Het hulpwerkwoord 'wil' staat op positie 2, het hele werkwoord 'kopen' staat helemaal achteraan."}
        ]
    },
    22: {
        "examples": ["Het is kwart over drie.", "Het is tien over half vier."],
        "questions": [
            {"q": "Hoe laat is het als het 3.15 uur is?", "o": ["Het is kwart over drie.", "Het is kwart voor drie.", "Het is drie uur kwart."], "c": 0, "e": "15 minuten over drie is 'kwart over drie'."},
            {"q": "Hoe laat is het als het 17.55 uur is?", "o": ["Het is vijf voor zes.", "Het is vijf over zes.", "Het is tien over half zes."], "c": 0, "e": "5 minuten voor 6 is 'vijf voor zes'."},
            {"q": "Hoe laat is het als het 15.40 uur is?", "o": ["Het is tien over half vier.", "Het is tien voor half vier.", "Het is kwart voor vier."], "c": 0, "e": "15.30 is half vier, dus 15.40 is 10 minuten over half vier."}
        ]
    },
    23: {
        "examples": ["U kunt hier oversteken.", "Jij mag eerder naar huis."],
        "questions": [
            {"q": "Vul in: 'U ___ hier oversteken.' (kunnen)", "o": ["kan", "kunt", "kunnen"], "c": 1, "e": "Bij 'u' hoort de vorm 'kunt'."},
            {"q": "Vul in: 'De bus ___ 100 kilometer per uur rijden.' (mogen - toestemming)", "o": ["mag", "magt", "mogen"], "c": 0, "e": "De bus is 'hij/het', dus 'mag'."},
            {"q": "Kies de juiste meervoudszin:", "o": ["De kinderen mag vanavond laat naar bed.", "De kinderen mogen vanavond laat naar bed.", "De kinderen kunt vanavond laat naar bed."], "c": 1, "e": "Kinderen is meervoud, dus 'mogen' + hele werkwoord achteraan."}
        ]
    },
    24: {
        "examples": ["De pen ligt op de tafel.", "De auto staat voor de schuur."],
        "questions": [
            {"q": "De doos staat op de grond. De spullen liggen ___ de doos.", "o": ["in", "op", "onder"], "c": 0, "e": "Spullen stop je 'in' een doos."},
            {"q": "De kat zit ___ de stoel. (onder de zitting)", "o": ["op", "onder", "naast"], "c": 1, "e": "Onder de stoel is de juiste plaatsaanduiding."},
            {"q": "De schuur staat ___ de tuin.", "o": ["op", "in", "boven"], "c": 1, "e": "Een schuur staat 'in' een tuin."}
        ]
    },
    25: {
        "examples": ["Op donderdag.", "Om negen uur.", "In januari."],
        "questions": [
            {"q": "Vul in: 'Ik ga ___ donderdag naar de markt.'", "o": ["op", "om", "in"], "c": 0, "e": "Bij dagen van de week gebruik je 'op'."},
            {"q": "Vul in: 'De les begint ___ negen uur.'", "o": ["op", "om", "in"], "c": 1, "e": "Bij tijden gebruik je 'om'."},
            {"q": "Vul in: 'Mijn vakantie begint ___ juli.'", "o": ["op", "om", "in"], "c": 2, "e": "Bij maanden gebruik je 'in'."}
        ]
    },
    26: {
        "examples": ["Mijn auto, jouw jas, onze fietsen."],
        "questions": [
            {"q": "Vul in: 'De mensen gaan naar ___ werk.' (hun/ons)", "o": ["hun", "ons", "haar"], "c": 0, "e": "De mensen (zij meervoud) -> 'hun werk'."},
            {"q": "Vul in: 'Wij hebben een schuur in ___ tuintje.' (de-woord / het-woord: het tuintje)", "o": ["ons", "onze", "mijn"], "c": 0, "e": "Bij het-woorden (tuintje) hoort 'ons'."},
            {"q": "Vul in: 'Zij heeft een hoed op ___ hoofd.' (zij enkelvoud)", "o": ["haar", "zijn", "mijn"], "c": 0, "e": "Bij een vrouw (zij) hoort 'haar hoofd'."}
        ]
    },
    27: {
        "examples": ["Morgen ga ik sporten.", "Elke zaterdag werkt Richard."],
        "questions": [
            {"q": "Zet in de juiste volgorde: 'Richard | elke zaterdag | sporten | gaat'", "o": ["Elke zaterdag gaat Richard sporten.", "Elke zaterdag Richard gaat sporten.", "Richard gaat elke zaterdag sporten (ook goed, maar kies de inversievorm)."], "c": 0, "e": "Als 'Elke zaterdag' vooraan staat, volgt inversie: Werkwoord (gaat) + Onderwerp (Richard) + rest."},
            {"q": "Kies de juiste inversie-zin:", "o": ["Morgen ga ik naar de stad.", "Morgen ik ga naar de stad.", "Ik ga morgen naar de stad."], "c": 0, "e": "'Morgen' staat vooraan, dus werkwoord op positie 2 (ga) en onderwerp direct daarna (ich/ik)."},
            {"q": "Zet in de juiste volgorde: 'De docent | de opdracht | gaat | nu | uitleggen'", "o": ["Nu de docent gaat de opdracht uitleggen.", "Nu gaat de docent de opdracht uitleggen.", "De docent gaat nu de opdracht uitleggen."], "c": 1, "e": "'Nu' staat vooraan -> Werkwoord (gaat) + Onderwerp (de docent) + rest."}
        ]
    },
    28: {
        "examples": ["Ik drink geen bier.", "Jimmy gaat niet op vakantie."],
        "questions": [
            {"q": "Vul in: 'Ik ga ___ op vakantie.'", "o": ["geen", "niet", "geene"], "c": 1, "e": "'Op vakantie gaan' is een activiteit/werkwoord, dus ontkenning met 'niet'."},
            {"q": "Vul in: 'Jimmy drinkt ___ bier.'", "o": ["geen", "niet", "geene"], "c": 0, "e": "'Bier' is een zelfstandig naamwoord zonder bepaald lidwoord, dus 'geen'."},
            {"q": "Vul in: 'Wij hebben ___ huisdieren.'", "o": ["geen", "niet", "geene"], "c": 0, "e": "'Huisdieren' is een onbepaald meervoud -> 'geen'."}
        ]
    },
    29: {
        "examples": ["Deze man en dit kind.", "Die man en dat kind."],
        "questions": [
            {"q": "Vul in: '___ boek is hier.' (het-woord, dichtbij)", "o": ["Dit", "Dat", "Deze"], "c": 0, "e": "Het-woord dichtbij is 'dit'."},
            {"q": "Vul in: '___ huis is daar.' (het-woord, ver weg)", "o": ["Dit", "Dat", "Die"], "c": 1, "e": "Het-woord ver weg is 'dat'."},
            {"q": "Vul in: '___ flat is ver weg.' (de-flat, ver weg)", "o": ["Die", "Dat", "Deze"], "c": 0, "e": "De-woord ver weg is 'die'."}
        ]
    }
}
