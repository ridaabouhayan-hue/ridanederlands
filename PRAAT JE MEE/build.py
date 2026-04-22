import re
import os

input_file = r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-1-1.html"
output_file = r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html"

with open(input_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Title and Topbar
html = html.replace("<title>Praat je mee – Thema 1.1 ⭐</title>", "<title>Praat je mee – Thema 5.1 ⭐</title>")
html = html.replace('<div class="topbar-title">Thema 1.1 ⭐ — Kennismaken</div>', '<div class="topbar-title">Thema 5.1 ⭐ — Kleding</div>')
html = html.replace('Thema 1.1 ⭐', 'Thema 5.1 ⭐')
html = html.replace('thema 1.1', 'thema 5.1')

# 2. Words Data
words_data_new = """const wordsData = [
  {nl:'Kan ik u helpen?', en:'Can I help you?', emoji:'🛍️'},
  {nl:'de trui', en:'the sweater', emoji:'👕'},
  {nl:'de broek', en:'the trousers', emoji:'👖'},
  {nl:'de jas', en:'the coat/jacket', emoji:'🧥'},
  {nl:'klein', en:'small', emoji:'🔽'},
  {nl:'groot', en:'big / large', emoji:'🔼'},
  {nl:'Ik kijk even.', en:'I\\'m just looking.', emoji:'👀'},
  {nl:'Heeft u … ?', en:'Do you have … ?', emoji:'🤝'},
  {nl:'Nee, dank u.', en:'No, thank you.', emoji:'🙏'},
  {nl:'Jammer.', en:'What a pity.', emoji:'😔'},
  {nl:'Bedankt.', en:'Thank you.', emoji:'🙏'},
  {nl:'Tot ziens.', en:'Goodbye.', emoji:'👋'},
];"""
html = re.sub(r"const wordsData = \[\s*.*?\s*\];", words_data_new, html, flags=re.DOTALL)

# 3. Repeat Phrases
repeat_phrases_new = """const repeatPhrases = [
  {nl:'Kan ik u helpen?', emoji:'🛍️'},
  {nl:'Nee, dank u. Ik kijk even.', emoji:'👀'},
  {nl:'Heeft u een trui voor mij?', emoji:'👕'},
  {nl:'Deze trui is te groot.', emoji:'🔼'},
  {nl:'Ik heb geen trui voor u.', emoji:'❌'},
  {nl:'Jammer. En heeft u een broek?', emoji:'👖'},
  {nl:'Bedankt. Tot ziens.', emoji:'👋'},
];"""
html = re.sub(r"const repeatPhrases = \[\s*.*?\s*\];", repeat_phrases_new, html, flags=re.DOTALL)

# 4. Copy Phrases
copy_phrases_new = """const copyPhrases = [
  'Kan ik u helpen?',
  'Nee, dank u. Ik kijk even.',
  'Heeft u een trui voor mij?',
  'Deze trui is te groot.',
  'Ik heb geen trui voor u.',
  'Jammer. En heeft u een broek?',
  'Bedankt. Tot ziens.',
];"""
html = re.sub(r"const copyPhrases = \[\s*.*?\s*\];", copy_phrases_new, html, flags=re.DOTALL)

# 5. Sort Exercises
sort_exercises_new = """const sortExercisesBase = [
  {words:['u','Kan','helpen','ik','?'], answer:'Kan ik u helpen ?'},
  {words:['trui','Heeft','mij','u','een','voor','?'], answer:'Heeft u een trui voor mij ?'},
  {words:['te','trui','groot','is','Deze','.'], answer:'Deze trui is te groot .'},
  {words:['broek','En','een','u','heeft','?'], answer:'En heeft u een broek ?'},
  {words:['heb','Ik','voor','geen','u','trui','.'], answer:'Ik heb geen trui voor u .'},
];"""
html = re.sub(r"const sortExercisesBase = \[\s*.*?\s*\];", sort_exercises_new, html, flags=re.DOTALL)

# 6. Conversation Sets
conv_sets_new = """const convSetsBase = [
  {label:'Gesprek 1 — Trui', lines:[
    {speaker:'Medewerker', text:'Kan ik u helpen?'},
    {speaker:'Klant', text:'Nee, dank u. Ik kijk even.'},
    {speaker:'Klant', text:'Heeft u een trui voor mij?'},
    {speaker:'Medewerker', text:'Deze trui is te groot.'},
    {speaker:'Medewerker', text:'En deze trui is te klein.'},
    {speaker:'Klant', text:'En heeft u een broek?'},
    {speaker:'Medewerker', text:'Ja hoor, een broek.'},
    {speaker:'Klant', text:'Bedankt. Tot ziens.'},
  ]},
  {label:'Gesprek 2 — Jas', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Heeft u een jas?'},
    {speaker:'Medewerker', text:'Nee, die heb ik niet.'},
    {speaker:'Klant', text:'Jammer.'},
    {speaker:'Medewerker', text:'Sorry.'},
    {speaker:'Klant', text:'Heeft u een broek?'},
    {speaker:'Medewerker', text:'Ja hoor.'},
    {speaker:'Klant', text:'Bedankt. Tot ziens.'},
  ]},
  {label:'Gesprek 3 — Bril', lines:[
    {speaker:'Medewerker', text:'Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Ik wil graag een nieuwe bril.'},
    {speaker:'Medewerker', text:'Welke kleur wilt u?'},
    {speaker:'Klant', text:'Paars. Paars is mooi.'},
    {speaker:'Medewerker', text:'Alstublieft. Wat vindt u hiervan?'},
    {speaker:'Klant', text:'Nee, ik wil een blauwe bril.'},
    {speaker:'Medewerker', text:'Ja hoor, een blauwe bril.'},
    {speaker:'Klant', text:'Ja, dat is mooi. Dank u.'},
  ]},
  {label:'Gesprek 4 — Kleur kiezen', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Ik zoek een trui.'},
    {speaker:'Medewerker', text:'Welke kleur?'},
    {speaker:'Klant', text:'Rood.'},
    {speaker:'Medewerker', text:'Sorry, ik heb geen rode trui.'},
    {speaker:'Klant', text:'En blauw?'},
    {speaker:'Medewerker', text:'Ja hoor, een blauwe trui.'},
    {speaker:'Klant', text:'Heel fijn. Dank u.'},
  ]},
  {label:'Gesprek 5 — Schoenen', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Nee hoor, ik kijk even.'},
    {speaker:'Klant', text:'Mag ik iets vragen?'},
    {speaker:'Medewerker', text:'Natuurlijk. Zegt u het maar.'},
    {speaker:'Klant', text:'Heeft u deze schoen in maat 38?'},
    {speaker:'Medewerker', text:'Één moment.'},
    {speaker:'Medewerker', text:'Ik heb de donkerbruine niet in maat 38.'},
    {speaker:'Klant', text:'Kunt u ze bestellen?'},
  ]},
];"""
html = re.sub(r"const convSetsBase = \[\s*.*?\s*\];", conv_sets_new, html, flags=re.DOTALL)

# 7. Q5A Base
q5a_new = """const q5aBase = [
  {prompt:'Kan ik u helpen?', options:[
    {text:'Helpen ik u kan.', correct:false},
    {text:'Kan ik u helpen?', correct:true},
    {text:'Ik kan helpen u.', correct:false},
  ]},
  {prompt:'Heeft u een trui voor mij?', options:[
    {text:'Trui heeft u mij voor een.', correct:false},
    {text:'Voor mij heeft u een trui.', correct:false},
    {text:'Heeft u een trui voor mij?', correct:true},
  ]},
  {prompt:'Wat zeg je als je binnenkomt en niet geholpen wilt worden?', options:[
    {text:'Bedankt. Tot ziens.', correct:false},
    {text:'Nee, dank u. Ik kijk even.', correct:true},
    {text:'Jammer. En heeft u een broek?', correct:false},
  ]},
  {prompt:'Hoe vraag je om een andere kleur?', options:[
    {text:'Welke kleur wilt u?', correct:true},
    {text:'Wilt kleur welke u?', correct:false},
    {text:'U wilt welke kleur?', correct:false},
  ]},
];"""
html = re.sub(r"const q5aBase = \[\s*.*?\s*\];", q5a_new, html, flags=re.DOTALL)

# 8. Q5B Base
q5b_new = """const q5bBase = [
  {prompt:'Kan ik u helpen?', options:[
    {text:'Ik kom uit Marokko.', correct:false},
    {text:'Nee, dank u. Ik kijk even.', correct:true},
    {text:'Tot ziens!', correct:false},
  ], feedback:'In een winkel zeg je "Nee, dank u. Ik kijk even." of "Ja, ik zoek…"'},
  {prompt:'Heeft u een trui in maat 38?', options:[
    {text:'Mijn naam is Kim.', correct:false},
    {text:'Ja hoor, één moment.', correct:true},
    {text:'Ik ben de docent.', correct:false},
  ], feedback:'De medewerker reageert met "Ja hoor" of "Sorry, die heb ik niet."'},
  {prompt:'Sorry, ik heb geen trui voor u.', options:[
    {text:'Bedankt. Tot ziens.', correct:false},
    {text:'Jammer. En heeft u een broek?', correct:true},
    {text:'Kan ik u helpen?', correct:false},
  ], feedback:'Na "ik heb dat niet" vraag je door: "En heeft u … ?"'},
  {prompt:'Welke kleur wilt u?', options:[
    {text:'Ik woon in Utrecht.', correct:false},
    {text:'Ik wil graag een blauwe.', correct:true},
    {text:'Ik ben ziek.', correct:false},
  ], feedback:'Bij "Welke kleur?" zeg je de kleur die je wilt.'},
  {prompt:'Kunt u de schoenen bestellen?', options:[
    {text:'Nee, dank u. Ik kijk even.', correct:false},
    {text:'Ja hoor, ik heb ze dan op zaterdag.', correct:true},
    {text:'Eén moment.', correct:false},
  ], feedback:'Na "kunt u bestellen?" zegt de medewerker wanneer ze klaar zijn.'},
];"""
html = re.sub(r"const q5bBase = \[\s*.*?\s*\];", q5b_new, html, flags=re.DOTALL)

# 9. Conv Fill Sets
conv_fill_sets_new = """const convFillSets = [
  {label:'Gesprek 1', lines:[
    {speaker:'Medewerker', fixed:'Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg dat je even rondkijkt', hint_en:'Say you are taking a look around', example:'Nee, dank u. Ik kijk even.'},
    {speaker:'Medewerker', fixed:'Heeft u een trui?'},
    {speaker:'Jij', input:true, hint_nl:'Vraag naar een kledingstuk', hint_en:'Ask for a piece of clothing', example:'Ja. Heeft u een trui voor mij?'},
    {speaker:'Medewerker', fixed:'Sorry, ik heb geen trui voor u.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer en vraag iets anders', hint_en:'Respond and ask for something else', example:'Jammer. En heeft u een broek?'},
    {speaker:'Medewerker', fixed:'Ja hoor, een broek.'},
    {speaker:'Jij', input:true, hint_nl:'Sluit het gesprek af', hint_en:'Close the conversation', example:'Bedankt. Tot ziens.'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Medewerker', fixed:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg wat je zoekt', hint_en:'Say what you are looking for', example:'Ja. Ik zoek een jas.'},
    {speaker:'Medewerker', fixed:'Welke kleur?'},
    {speaker:'Jij', input:true, hint_nl:'Noem een kleur', hint_en:'Name a colour', example:'Blauw.'},
    {speaker:'Medewerker', fixed:'Een blauwe jas. Alstublieft.'},
    {speaker:'Jij', input:true, hint_nl:'Sluit af beleefd', hint_en:'Close politely', example:'Dank u. Tot ziens.'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Medewerker', fixed:'Goedemiddag. Kunt u het vinden?'},
    {speaker:'Jij', input:true, hint_nl:'Vraag toestemming', hint_en:'Ask for permission to speak', example:'Mag ik iets vragen?'},
    {speaker:'Medewerker', fixed:'Natuurlijk. Zegt u het maar.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag naar de maat', hint_en:'Ask for the size', example:'Heeft u deze schoen in maat 38?'},
    {speaker:'Medewerker', fixed:'Één moment. Sorry, die heb ik niet.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag of ze het kunnen bestellen', hint_en:'Ask if they can order it', example:'Kunt u ze bestellen?'},
    {speaker:'Medewerker', fixed:'Ja hoor, op zaterdag.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer blij en sluit af', hint_en:'React happily and close', example:'Heel fijn. Dank u wel.'},
  ]},
];"""
html = re.sub(r"const convFillSets = \[\s*.*?\s*\];", conv_fill_sets_new, html, flags=re.DOTALL)


a_tasks_nl = ['1️⃣ Begroet en zeg dat je kijkt: "Nee, dank u. Ik kijk even."', '2️⃣ Vraag naar een kledingstuk: "Heeft u een … ?"', '3️⃣ Reageer op het antwoord: "Jammer." of "Ja, mooi."', '4️⃣ Sluit af: "Bedankt. Tot ziens."']
a_tasks_en = ['1️⃣ Greet and say you are looking: "Nee, dank u. Ik kijk even."', '2️⃣ Ask for clothing: "Heeft u een … ?"', '3️⃣ React to answer: "Jammer." or "Ja, mooi."', '4️⃣ Close: "Bedankt. Tot ziens."']
b_tasks_nl = ['1️⃣ Begroet de klant: "Goedemiddag. Kan ik u helpen?"', '2️⃣ Reageer op de vraag: "Ja hoor." of "Sorry, die heb ik niet."', '3️⃣ Stel een vervolgvraag: "Welke kleur wilt u?"', '4️⃣ Sluit af: "Graag gedaan. Tot ziens."']
b_tasks_en = ['1️⃣ Greet the customer: "Goedemiddag. Kan ik u helpen?"', '2️⃣ React to question: "Ja hoor." or "Sorry, die heb ik niet."', '3️⃣ Ask follow-up question: "Welke kleur wilt u?"', '4️⃣ Close: "Graag gedaan. Tot ziens."']

html = re.sub(
    r"const aTasks=isEN\s*\?[^:]+:\s*\[[^\]]+\];",
    f"const aTasks=isEN ? {a_tasks_en} : {a_tasks_nl};",
    html
)
html = re.sub(
    r"const bTasks=isEN\s*\?[^:]+:\s*\[[^\]]+\];",
    f"const bTasks=isEN ? {b_tasks_en} : {b_tasks_nl};",
    html
)

html = html.replace("Person A — You are new", "Person A — Customer")
html = html.replace("Persoon A — Jij bent nieuw", "Persoon A — Klant")
html = html.replace("Person B — You are the teacher", "Person B — Store employee")
html = html.replace("Persoon B — Jij bent de docent", "Persoon B — Winkelmedewerker")

text_replacements_nl = [
    ("'Begroet de persoon'", "'Begroet de winkelmedewerker'"),
    ("'Zeg wie jij bent'", "'Zeg wat je zoekt'"),
    ("'Zeg waar jij vandaan komt'", "'Vraag naar kleur of maat'"),
    ("'Vraag wie de ander is'", "'Reageer op het antwoord'"),
    ("'Sluit het gesprek af'", "'Sluit het gesprek beleefd af'"),
]
text_replacements_en = [
    ("'Greet the person'", "'Greet the store employee'"),
    ("'Say who you are'", "'Say what you are looking for'"),
    ("'Say where you come from'", "'Ask about color or size'"),
    ("'Ask who the other person is'", "'React to the answer'"),
    ("'End the conversation'", "'Close the conversation politely'"),
]

for nl_old, nl_new in text_replacements_nl:
    html = html.replace(nl_old, nl_new)
    
for en_old, en_new in text_replacements_en:
    html = html.replace(en_old, en_new)

html = html.replace(
    '<div class="speech-step-example">"Hallo!" / "Goedemorgen!"</div>',
    '<div class="speech-step-example">"Goedemiddag. Kan ik u helpen?"</div>'
)
html = html.replace(
    '<div class="speech-step-example">"Ik ben [naam]."</div>',
    '<div class="speech-step-example">"Ik zoek een …"</div>'
)
html = html.replace(
    '<div class="speech-step-example">"Ik kom uit [land]."</div>',
    '<div class="speech-step-example">Kleur/maat: "Hebt u rood?"</div>'
)
html = html.replace(
    '<div class="speech-step-example">"Wie ben jij?"</div>',
    '<div class="speech-step-example">"Leuk!" / "Jammer."</div>'
)
html = html.replace(
    '<div class="speech-step-example">"Bedankt! Dag!"</div>',
    '<div class="speech-step-example">"Bedankt. Tot ziens."</div>'
)

html = html.replace("Druk op 🔊 om het woord te horen. Zeg het daarna zelf na!",
                    "<strong>Leerdoel 5.1 ⭐: De cursist kan een gesprek voeren in een winkel over kleding — vragen stellen, reageren op de medewerker, en het gesprek afsluiten.</strong><br>Druk op 🔊 om het woord te horen. Zeg het daarna zelf na!")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)
    
print('Success')
