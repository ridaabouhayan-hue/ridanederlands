import re

file_path = r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\niet_geen.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Language Button
if 'onclick="setLang(\'pl\')"' not in content:
    content = content.replace(
        '<button class="lang-btn" id="btn-en" onclick="setLang(\'en\')">🇬🇧 English</button>',
        '<button class="lang-btn" id="btn-en" onclick="setLang(\'en\')">🇬🇧 English</button>\n        <button class="lang-btn" id="btn-pl" onclick="setLang(\'pl\')">🇵🇱 Polski</button>'
    )

# 2. Add Translations
# Strict mapping of text to replace -> text to replace with
replacements = [
    (
        '<span lang="en">Rules</span>', 
        '<span lang="en">Rules</span>\n<span lang="pl">Zasady</span>'
    ),
    (
        '<span lang="en">Mistakes</span>',
        '<span lang="en">Mistakes</span>\n<span lang="pl">Błędy</span>'
    ),
    (
        '<span lang="en">Practice</span>',
        '<span lang="en">Practice</span>\n<span lang="pl">Ćwiczenia</span>'
    ),
    (
        '<span lang="en">Voice Memo</span>',
        '<span lang="en">Voice Memo</span>\n<span lang="pl">Notatka głosowa</span>'
    ),
    (
        '<span lang="en">Niet or Geen?</span>',
        '<span lang="en">Niet or Geen?</span>\n            <span lang="pl">Niet czy Geen?</span>'
    ),
    (
        '<span lang="en">Learn the most important rules for negation in Dutch. Specially designed for work and office!</span>',
        '<span lang="en">Learn the most important rules for negation in Dutch. Specially designed for work and office!</span>\n            <span lang="pl">Poznaj najważniejsze zasady przeczeń w języku holenderskim. Specjalnie do pracy i biura!</span>'
    ),
    (
        '<span lang="en">💡 The Rules</span>',
        '<span lang="en">💡 The Rules</span>\n                <span lang="pl">💡 Zasady</span>'
    ),
    (
        '<span lang="en">Use <strong>geen</strong> before nouns (people, things, plans).</span>',
        '<span lang="en">Use <strong>geen</strong> before nouns (people, things, plans).</span>\n                        <span lang="pl">Użyj <strong>geen</strong> przed rzeczownikami (ludzie, rzeczy, plany).</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(I have no company computer.)</span>',
        '<span class="translation-sub" lang="en">(I have no company computer.)</span>\n                            <span class="translation-sub" lang="pl">(Nie mam służbowego komputera.)</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(We have no break today.)</span>',
        '<span class="translation-sub" lang="en">(We have no break today.)</span>\n                            <span class="translation-sub" lang="pl">(Nie mamy dzisiaj przerwy.)</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(She speaks no Dutch with colleagues.)</span>',
        '<span class="translation-sub" lang="en">(She speaks no Dutch with colleagues.)</span>\n                            <span class="translation-sub" lang="pl">(Ona nie mówi po holendersku z kolegami.)</span>'
    ),
    (
        '<span lang="en">💡 <strong>Rule:</strong> geen + noun. It replaces \'een\' (a/an) or a plural without an article.</span>',
        '<span lang="en">💡 <strong>Rule:</strong> geen + noun. It replaces \'een\' (a/an) or a plural without an article.</span>\n                        <span lang="pl">💡 <strong>Zasada:</strong> geen + rzeczownik. Zastępuje \'een\' lub liczbę mnogą.</span>'
    ),
    (
        '<span lang="en">Use <strong>niet</strong> for the rest (verbs, adjectives, adverbs, specific things, <strong>prepositions</strong>, and <strong>possessives</strong>).</span>',
        '<span lang="en">Use <strong>niet</strong> for the rest (verbs, adjectives, adverbs, specific things, <strong>prepositions</strong>, and <strong>possessives</strong>).</span>\n                        <span lang="pl">Użyj <strong>niet</strong> dla reszty (czasowniki, przymiotniki, przysłówki, konkretne rzeczy, <strong>przyimki</strong> i <strong>zaimki dzierżawcze</strong>).</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(I am not working today. - negating a verb)</span>',
        '<span class="translation-sub" lang="en">(I am not working today. - negating a verb)</span>\n                            <span class="translation-sub" lang="pl">(Dzisiaj nie pracuję. - przeczenie czasownika)</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(This office is not big. - negating an adjective)</span>',
        '<span class="translation-sub" lang="en">(This office is not big. - negating an adjective)</span>\n                            <span class="translation-sub" lang="pl">(To biuro nie jest duże. - przeczenie przymiotnika)</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(I do not understand the instruction. - negating a specific noun with \'de\')</span>',
        '<span class="translation-sub" lang="en">(I do not understand the instruction. - negating a specific noun with \'de\')</span>\n                            <span class="translation-sub" lang="pl">(Nie rozumiem instrukcji. - przeczenie konkretnego rzeczownika z \'de/het\')</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(I am not at the office. - negating a preposition / voorzetsel)</span>',
        '<span class="translation-sub" lang="en">(I am not at the office. - negating a preposition / voorzetsel)</span>\n                            <span class="translation-sub" lang="pl">(Nie jestem w biurze. - przeczenie przyimka)</span>'
    ),
    (
        '<span class="translation-sub" lang="en">(This is not my computer. - negating a possessive / possessief)</span>',
        '<span class="translation-sub" lang="en">(This is not my computer. - negating a possessive / possessief)</span>\n                            <span class="translation-sub" lang="pl">(To nie jest mój komputer. - przeczenie zaimka dzierżawczego)</span>'
    ),
    (
        '<span lang="en">💡 <strong>Rule:</strong> niet = for the rest (verbs, adjectives, prepositions, and specific nouns / possessives).</span>',
        '<span lang="en">💡 <strong>Rule:</strong> niet = for the rest (verbs, adjectives, prepositions, and specific nouns / possessives).</span>\n                        <span lang="pl">💡 <strong>Zasada:</strong> niet = dla reszty (czasowniki, przymiotniki, przyimki, konkretne rzeczowniki / dzierżawcze).</span>'
    ),
    (
        '<span lang="en">⚠️ Common Mistakes</span>',
        '<span lang="en">⚠️ Common Mistakes</span>\n                <span lang="pl">⚠️ Częste błędy</span>'
    ),
    (
        '<h4 lang="en">1. Nouns</h4>',
        '<h4 lang="en">1. Nouns</h4>\n                    <h4 lang="pl">1. Rzeczowniki</h4>'
    ),
    (
        '<span class="translation-sub" lang="en">Explanation: In Dutch, we never say \'niet een\'. We replace it with \'geen\'.</span>',
        '<span class="translation-sub" lang="en">Explanation: In Dutch, we never say \'niet een\'. We replace it with \'geen\'.</span>\n                        <span class="translation-sub" lang="pl">Wyjaśnienie: W języku holenderskim nigdy nie mówimy \'niet een\'. Zastępujemy to przez \'geen\'.</span>'
    ),
    (
        '<h4 lang="en">2. Verbs & Adverbs</h4>',
        '<h4 lang="en">2. Verbs & Adverbs</h4>\n                    <h4 lang="pl">2. Czasowniki i Przysłówki</h4>'
    ),
    (
        '<span class="translation-sub" lang="en">Explanation: \'Vandaag\' (today) and \'werken\' (to work) are not nouns. So we must use \'niet\'.</span>',
        '<span class="translation-sub" lang="en">Explanation: \'Vandaag\' (today) and \'werken\' (to work) are not nouns. So we must use \'niet\'.</span>\n                        <span class="translation-sub" lang="pl">Wyjaśnienie: \'Vandaag\' (dzisiaj) i \'werken\' (pracować) nie są rzeczownikami. Dlatego musimy użyć \'niet\'.</span>'
    ),
    (
        '<span lang="en">✍️ Practice</span>',
        '<span lang="en">✍️ Practice</span>\n                    <span lang="pl">✍️ Ćwiczenia</span>'
    ),
    (
        '<span lang="en">Type <strong>niet</strong> or <strong>geen</strong> in the blank spaces. Get instant feedback!</span>',
        '<span lang="en">Type <strong>niet</strong> or <strong>geen</strong> in the blank spaces. Get instant feedback!</span>\n                    <span lang="pl">Wpisz <strong>niet</strong> lub <strong>geen</strong> w puste miejsca. Otrzymaj natychmiastową informację zwrotną!</span>'
    ),
    (
        '<span lang="en">Voice Memo Task: A terrible workday!</span>',
        '<span lang="en">Voice Memo Task: A terrible workday!</span>\n                            <span lang="pl">Zadanie Voice Memo: Okropny dzień w pracy!</span>'
    ),
    (
        '<span lang="en">Record a voice memo and use as many instances of <strong>niet</strong> and <strong>geen</strong> as possible.</span>',
        '<span lang="en">Record a voice memo and use as many instances of <strong>niet</strong> and <strong>geen</strong> as possible.</span>\n                            <span lang="pl">Nagraj wiadomość głosową i użyj jak najwięcej słów <strong>niet</strong> i <strong>geen</strong>.</span>'
    ),
    (
        '<span lang="en">Strict criteria for your story:</span>',
        '<span lang="en">Strict criteria for your story:</span>\n                        <span lang="pl">Ścisłe kryteria dla twojej opowieści:</span>'
    ),
    (
        '<span lang="en">Use \'geen\' for nouns</span>',
        '<span lang="en">Use \'geen\' for nouns</span><span lang="pl">Użyj \'geen\' przed rzeczownikami</span>'
    ),
    (
        '<span lang="en">Use \'niet\' for the rest</span>',
        '<span lang="en">Use \'niet\' for the rest</span><span lang="pl">Użyj \'niet\' w innych przypadkach</span>'
    ),
    (
        '<span lang="en">Record for 1 minute on your phone</span>',
        '<span lang="en">Record for 1 minute on your phone</span><span lang="pl">Nagrywaj przez 1 minutę na telefonie</span>'
    ),
    (
        '<span lang="en">Example of a terrible office story:</span>',
        '<span lang="en">Example of a terrible office story:</span>\n                        <span lang="pl">Przykład okropnej historii z biura:</span>'
    ),
    (
        '<p style="font-size: 1.1rem; font-weight: 500; color: var(--text-light); line-height: 1.6; margin: 0; font-style: italic;" lang="en">\n                        "Today is a terrible day at the office. I have <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> coffee and <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> internet. My colleague is <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> there to help. The printer is also <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> working. I have <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> motivation left today. I am really <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> happy!"\n                    </p>',
        '<p style="font-size: 1.1rem; font-weight: 500; color: var(--text-light); line-height: 1.6; margin: 0; font-style: italic;" lang="en">\n                        "Today is a terrible day at the office. I have <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> coffee and <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> internet. My colleague is <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> there to help. The printer is also <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> working. I have <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">no</span> motivation left today. I am really <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">not</span> happy!"\n                    </p>\n                    <p style="font-size: 1.1rem; font-weight: 500; color: var(--text-light); line-height: 1.6; margin: 0; margin-top: 10px; font-style: italic;" lang="pl">\n                        "Dzisiaj jest okropny dzień w biurze. Nie mam <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">żadnej</span> kawy i <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">żadnego</span> internetu. Mojego kolegi <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">nie</span> ma, żeby pomóc. Drukarka również <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">nie</span> działa. Nie mam dzisiaj <span style="color: var(--geen-main); text-decoration: underline; text-underline-offset: 3px;">żadnej</span> motywacji. Naprawdę <span style="color: var(--niet-main); text-decoration: underline; text-underline-offset: 3px;">nie</span> jestem zadowolony!"\n                    </p>'
    ),
    (
        '<h4 style="font-weight: 800; font-size: 1.2rem; margin-bottom: 4px;" lang="en">How to submit this assignment?</h4>',
        '<h4 style="font-weight: 800; font-size: 1.2rem; margin-bottom: 4px;" lang="en">How to submit this assignment?</h4>\n                        <h4 style="font-weight: 800; font-size: 1.2rem; margin-bottom: 4px;" lang="pl">Jak przesłać to zadanie?</h4>'
    ),
    (
        '<li lang="en">Create your own story about a day where everything goes wrong (at work, school, or home).</li>',
        '<li lang="en">Create your own story about a day where everything goes wrong (at work, school, or home).</li>\n                            <li lang="pl">Wymyśl własną historię o dniu, w którym wszystko idzie źle (w pracy, w szkole lub w domu).</li>'
    ),
    (
        '<li lang="en">Open the recording app on your phone or record a voice message in WhatsApp.</li>',
        '<li lang="en">Open the recording app on your phone or record a voice message in WhatsApp.</li>\n                            <li lang="pl">Otwórz aplikację dyktafonu w telefonie lub nagraj wiadomość głosową na WhatsApp.</li>'
    ),
    (
        '<li lang="en">Speak for at least 1 minute and pay close attention to the difference between <strong>niet</strong> and <strong>geen</strong>!</li>',
        '<li lang="en">Speak for at least 1 minute and pay close attention to the difference between <strong>niet</strong> and <strong>geen</strong>!</li>\n                            <li lang="pl">Mów przez co najmniej 1 minutę i zwróć szczególną uwagę na różnicę między <strong>niet</strong> a <strong>geen</strong>!</li>'
    ),
    (
        '<li lang="en">Send the voice memo directly to your teacher via WhatsApp for feedback! 🚀</li>',
        '<li lang="en">Send the voice memo directly to your teacher via WhatsApp for feedback! 🚀</li>\n                            <li lang="pl">Wyślij notatkę głosową bezpośrednio przez WhatsApp do swojego nauczyciela, aby otrzymać feedback! 🚀</li>'
    )
]

for src, tgt in replacements:
    if tgt not in content:
        content = content.replace(src, tgt)

# 3. Replace the questions array with 20 questions including Polish hints
new_questions_str = """const questions = [
            {
                parts: ["Ik heb ", " computer van de zaak."],
                hint: { nl: "Ik heb (geen) computer van de zaak.", en: "I have no company computer.", pl: "Nie mam służbowego komputera." },
                answer: "geen"
            },
            {
                parts: ["De fabriek van VDL is vandaag ", " open."],
                hint: { nl: "De fabriek van VDL is vandaag (niet) open.", en: "The VDL factory is not open today.", pl: "Fabryka VDL nie jest dzisiaj otwarta." },
                answer: "niet"
            },
            {
                parts: ["Wij drinken ", " koffie in de pauze."],
                hint: { nl: "Wij drinken (geen) koffie in de pauze.", en: "We drink no coffee during the break.", pl: "Nie pijemy kawy podczas przerwy." },
                answer: "geen"
            },
            {
                parts: ["Mijn collega spreekt ", " snel Nederlands."],
                hint: { nl: "Mijn collega spreekt (niet) snel Nederlands.", en: "My colleague does not speak Dutch quickly.", pl: "Mój kolega nie mówi szybko po holendersku." },
                answer: "niet"
            },
            {
                parts: ["Er zijn vandaag ", " vergaderingen gepland."],
                hint: { nl: "Er zijn vandaag (geen) vergaderingen gepland.", en: "There are no meetings scheduled today.", pl: "Na dzisiaj nie zaplanowano żadnych spotkań." },
                answer: "geen"
            },
            {
                parts: ["Ik kan vanmiddag helaas ", " werken."],
                hint: { nl: "Ik kan vanmiddag helaas (niet) werken.", en: "I unfortunately cannot work this afternoon.", pl: "Niestety nie mogę dzisiaj po południu pracować." },
                answer: "niet"
            },
            {
                parts: ["Zij heeft ", " vast contract bij VDL."],
                hint: { nl: "Zij heeft (geen) vast contract bij VDL.", en: "She has no permanent contract at VDL.", pl: "Ona nie ma stałej umowy w VDL." },
                answer: "geen"
            },
            {
                parts: ["Dit rapport is nog ", " klaar."],
                hint: { nl: "Dit rapport is nog (niet) klaar.", en: "This report is not ready yet.", pl: "Ten raport nie jest jeszcze gotowy." },
                answer: "niet"
            },
            {
                parts: ["Hij begrijpt de nieuwe machine ", "."],
                hint: { nl: "Hij begrijpt de nieuwe machine (niet).", en: "He does not understand the new machine.", pl: "On nie rozumie nowej maszyny." },
                answer: "niet"
            },
            {
                parts: ["Er is ", " papier meer in de printer."],
                hint: { nl: "Er is (geen) papier meer in de printer.", en: "There is no more paper in the printer.", pl: "W drukarce nie ma już papieru." },
                answer: "geen"
            },
            {
                parts: ["Wij hebben morgen ", " tijd voor een meeting."],
                hint: { nl: "Wij hebben morgen (geen) tijd voor een meeting.", en: "We have no time for a meeting tomorrow.", pl: "Jutro nie mamy czasu na spotkanie." },
                answer: "geen"
            },
            {
                parts: ["Mijn baas is vandaag ", " op kantoor."],
                hint: { nl: "Mijn baas is vandaag (niet) op kantoor.", en: "My boss is not at the office today.", pl: "Mojego szefa nie ma dzisiaj w biurze." },
                answer: "niet"
            },
            {
                parts: ["Deze e-mail is ", " voor jou bestemd."],
                hint: { nl: "Deze e-mail is (niet) voor jou bestemd.", en: "This email is not intended for you.", pl: "Ten e-mail nie jest przeznaczony dla ciebie." },
                answer: "niet"
            },
            {
                parts: ["Ik heb ", " auto, ik kom met de fiets."],
                hint: { nl: "Ik heb (geen) auto, ik kom met de fiets.", en: "I have no car, I come by bicycle.", pl: "Nie mam samochodu, przyjeżdżam rowerem." },
                answer: "geen"
            },
            {
                parts: ["De nieuwe stagiair spreekt nog ", " goed Nederlands."],
                hint: { nl: "De nieuwe stagiair spreekt nog (niet) goed Nederlands.", en: "The new intern does not speak Dutch well yet.", pl: "Nowy stażysta jeszcze nie mówi dobrze po holendersku." },
                answer: "niet"
            },
            {
                parts: ["Heb jij ", " vragen over het project?"],
                hint: { nl: "Heb jij (geen) vragen over het project?", en: "Do you have no questions about the project?", pl: "Nie masz żadnych pytań dotyczących projektu?" },
                answer: "geen"
            },
            {
                parts: ["Wij kunnen dit probleem ", " oplossen."],
                hint: { nl: "Wij kunnen dit probleem (niet) oplossen.", en: "We cannot solve this problem.", pl: "Nie możemy rozwiązać tego problemu." },
                answer: "niet"
            },
            {
                parts: ["Zij zoeken ", " nieuwe medewerkers op dit moment."],
                hint: { nl: "Zij zoeken (geen) nieuwe medewerkers op dit moment.", en: "They are looking for no new employees at the moment.", pl: "Obecnie nie szukają nowych pracowników." },
                answer: "geen"
            },
            {
                parts: ["Het is ", " moeilijk om dit te leren."],
                hint: { nl: "Het is (niet) moeilijk om dit te leren.", en: "It is not difficult to learn this.", pl: "Nie jest trudno się tego nauczyć." },
                answer: "niet"
            },
            {
                parts: ["Hij heeft ", " zin om over te werken."],
                hint: { nl: "Hij heeft (geen) zin om over te werken.", en: "He has no desire to work overtime.", pl: "On nie ma ochoty na nadgodziny." },
                answer: "geen"
            }
        ];"""

# Replace the questions array
content = re.sub(r'const questions = \[.*?\];', new_questions_str, content, flags=re.DOTALL)

# 4. Update the translation sub in JS rendering
if '<span class="translation-sub" lang="en">Translation: ${q.hint.en}</span>' in content:
    content = content.replace(
        '<span class="translation-sub" lang="en">Translation: ${q.hint.en}</span>',
        '<span class="translation-sub" lang="en">Translation: ${q.hint.en}</span>\n                        <span class="translation-sub" lang="pl">Tłumaczenie: ${q.hint.pl}</span>'
    )

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done properly injecting Polish and adding 10 extra exercises!")
