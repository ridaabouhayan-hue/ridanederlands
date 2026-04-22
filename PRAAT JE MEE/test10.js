
// ── CONFIG ──────────────────────────────────────────────────────────
const TEACHER_WA = '31626211106';
const TOTAL = 13;

// ── DATA ────────────────────────────────────────────────────────────
const wordsData = [
  {nl:'de vakantie',     en:'the holiday',        tr:'tatil',          ar:'العطلة',         om:'boqonnaa',     ps:'رخصتي',          zh:'假期',           desc_nl:'Vrije dagen, bijv. je gaat op vakantie',  emoji:'🏖️'},
  {nl:'het vliegtuig',   en:'the airplane',       tr:'uçak',           ar:'الطائرة',        om:'xiyyaara',     ps:'الوتکه',         zh:'飞机',           desc_nl:'Je vliegt hiermee naar een ander land',    emoji:'✈️'},
  {nl:'de trein',        en:'the train',          tr:'tren',           ar:'القطار',         om:'baabura',      ps:'اورګاډی',        zh:'火车',           desc_nl:'Rijdt op het spoor van stad naar stad',    emoji:'🚂'},
  {nl:'de boot',         en:'the boat',           tr:'tekne / gemi',   ar:'القارب',         om:'doonii',       ps:'کشتي',           zh:'船',             desc_nl:'Vaart over het water',                     emoji:'⛴️'},
  {nl:'de auto',         en:'the car',            tr:'araba',          ar:'السيارة',        om:'konkolaataa',  ps:'موټر',           zh:'汽车',           desc_nl:'Rijdt op de weg, je hebt een rijbewijs nodig', emoji:'🚗'},
  {nl:'het vliegveld',   en:'the airport',        tr:'havalimanı',     ar:'المطار',         om:'buufata xiyyaaraa', ps:'هوايي ډګر',  zh:'机场',           desc_nl:'Hier vertrekken vliegtuigen',              emoji:'🛫'},
  {nl:'het buitenland',  en:'abroad',             tr:'yurt dışı',      ar:'الخارج',         om:'biyya alaa',   ps:'بهرنی هېواد',    zh:'国外',           desc_nl:'Een ander land buiten Nederland',          emoji:'🌍'},
  {nl:'de reis',         en:'the trip / journey',  tr:'yolculuk',       ar:'الرحلة',         om:'imala',        ps:'سفر',            zh:'旅行',           desc_nl:'Van A naar B reizen',                      emoji:'🧳'},
  {nl:'Waar ga je naartoe?',   en:'Where are you going?',  tr:'Nereye gidiyorsun?',   ar:'إلى أين تذهب؟',   om:'Eessa deemta?',  ps:'چېرته ځې؟',     zh:'你去哪里？',     desc_nl:'Vraag om te weten waar iemand heen gaat', emoji:'🗺️'},
  {nl:'Fijne vakantie!',       en:'Have a nice holiday!',  tr:'İyi tatiller!',         ar:'إجازة سعيدة!',     om:'Boqonnaa gaarii!', ps:'ښه رخصتي!',   zh:'假期愉快！',     desc_nl:'Dit zeg je als iemand op vakantie gaat',  emoji:'👋'},
];

const repeatPhrases = [
  {nl:'Waar ga je naartoe?',                             emoji:'🗺️'},
  {nl:'Ik ga op vakantie.',                              emoji:'🏖️'},
  {nl:'Ik ga naar Spanje.',                              emoji:'🇪🇸'},
  {nl:'Hoe ga je naar Spanje?',                          emoji:'🤔'},
  {nl:'Met het vliegtuig.',                              emoji:'✈️'},
  {nl:'Ik ga eerst met de trein naar het vliegveld.',    emoji:'🚂'},
  {nl:'Ik ga met de boot naar Ameland.',                 emoji:'⛴️'},
  {nl:'Mijn trein gaat bijna.',                          emoji:'⏰'},
  {nl:'Fijne vakantie!',                                 emoji:'👋'},
  {nl:'Wat leuk!',                                       emoji:'😊'},
];

const copyPhrases = [
  'Waar ga je naartoe?',
  'Ik ga op vakantie.',
  'Hoe ga je naar Spanje?',
  'Met het vliegtuig.',
  'Ik ga met de trein naar het vliegveld.',
  'Ik ga met de boot naar Ameland.',
  'Fijne vakantie!',
];

const sortExercisesBase = [
  {words:['ga','naartoe','je','Waar','?'],                      answer:'Waar ga je naartoe ?'},
  {words:['vakantie','ga','Ik','op','.'],                       answer:'Ik ga op vakantie .'},
  {words:['vliegtuig','Met','het','.'],                         answer:'Met het vliegtuig .'},
  {words:['trein','de','ga','naar','Ik','met','vliegveld','het','.'], answer:'Ik ga met de trein naar het vliegveld .'},
  {words:['boot','ga','Ik','de','met','Ameland','naar','.'],    answer:'Ik ga met de boot naar Ameland .'},
  {words:['vakantie','Fijne','!'],                              answer:'Fijne vakantie !'},
  {words:['bijna','trein','gaat','Mijn','.'],                   answer:'Mijn trein gaat bijna .'},
];

const convSetsBase = [
  {label:'Gesprek 1 — Nina & Daan', lines:[
    {speaker:'Daan', text:'Hey Nina, wat leuk om je te zien.'},
    {speaker:'Nina', text:'Hey hallo, Daan. Hoe gaat het met je?'},
    {speaker:'Daan', text:'Goed, en met jou?'},
    {speaker:'Nina', text:'Ook goed. Waar ga je naartoe?'},
    {speaker:'Daan', text:'Ik ga op vakantie.'},
    {speaker:'Nina', text:'Wat leuk, ga je naar het buitenland?'},
    {speaker:'Daan', text:'Ja, ik ga naar mijn zus. Zij woont in Spanje.'},
    {speaker:'Nina', text:'Fijne vakantie!'},
    {speaker:'Daan', text:'Dankjewel, jij ook. Doei.'},
  ]},
  {label:'Gesprek 2 — Op het station', lines:[
    {speaker:'Ahmed', text:'Hallo! Waar ga jij naartoe?'},
    {speaker:'Sara', text:'Ik ga naar Breda. En jij?'},
    {speaker:'Ahmed', text:'Ik ga naar Amsterdam. Ik heb daar een afspraak.'},
    {speaker:'Sara', text:'Hoe ga je? Met de trein?'},
    {speaker:'Ahmed', text:'Ja, met de trein. En jij?'},
    {speaker:'Sara', text:'Ik ga ook met de trein.'},
    {speaker:'Ahmed', text:'Fijne reis!'},
    {speaker:'Sara', text:'Jij ook. Doei!'},
  ]},
  {label:'Gesprek 3 — Vakantie plannen', lines:[
    {speaker:'Lisa', text:'Ik ga volgende week op vakantie!'},
    {speaker:'Karim', text:'Wat leuk! Waar ga je naartoe?'},
    {speaker:'Lisa', text:'Ik ga naar Turkije. Met het vliegtuig.'},
    {speaker:'Karim', text:'Leuk! Hoe lang ga je weg?'},
    {speaker:'Lisa', text:'Twee weken.'},
    {speaker:'Karim', text:'Wat ga je daar doen?'},
    {speaker:'Lisa', text:'Naar het strand en lekker eten.'},
    {speaker:'Karim', text:'Fijne vakantie!'},
  ]},
];

const q5aBase = [
  {prompt:'Waar ga je naartoe?', options:[
    {text:'Ik ga op vakantie.',              correct:true},
    {text:'Op vakantie ga ik.',              correct:false},
    {text:'Vakantie ga ik op.',              correct:false},
  ]},
  {prompt:'Hoe ga je naar Spanje?', options:[
    {text:'Met het vliegtuig.',              correct:true},
    {text:'Vliegtuig met het.',              correct:false},
    {text:'Het met vliegtuig.',              correct:false},
  ]},
  {prompt:'Welke zin klopt?', options:[
    {text:'Ik ga met de trein naar het vliegveld.', correct:true},
    {text:'Met trein ik ga vliegveld naar het.',     correct:false},
    {text:'Naar vliegveld het ga ik trein met de.',  correct:false},
  ]},
  {prompt:'Hoe neem je afscheid?', options:[
    {text:'Fijne vakantie!',                correct:true},
    {text:'Vakantie fijne!',                correct:false},
    {text:'Fijne de vakantie!',             correct:false},
  ]},
  {prompt:'Welke zin klopt?', options:[
    {text:'Mijn trein gaat bijna.',          correct:true},
    {text:'Gaat bijna mijn trein.',          correct:false},
    {text:'Trein mijn bijna gaat.',          correct:false},
  ]},
];

const q5bBase = [
  {prompt:'Waar ga jij naartoe?', options:[
    {text:'Ik heet Ahmed.',                  correct:false},
    {text:'Ik ga naar Spanje.',             correct:true},
    {text:'Het gaat goed.',                 correct:false},
  ], feedback:'Bij "Waar ga je naartoe?" zeg je een plek of land.'},
  {prompt:'Hoe ga je naar Turkije?', options:[
    {text:'Met het vliegtuig.',             correct:true},
    {text:'Ik woon in Utrecht.',            correct:false},
    {text:'Het is mooi weer.',              correct:false},
  ], feedback:'Bij "Hoe ga je?" zeg je het vervoermiddel: trein, vliegtuig, auto of boot.'},
  {prompt:'Ga je naar het buitenland?', options:[
    {text:'Ja, ik ga naar Marokko.',        correct:true},
    {text:'Ik houd van voetbal.',           correct:false},
    {text:'Nee, ik heet Sara.',             correct:false},
  ], feedback:'Bij "Ga je naar het buitenland?" antwoord je ja/nee + het land.'},
  {prompt:'Mijn trein gaat bijna!', options:[
    {text:'Fijne reis! Doei!',              correct:true},
    {text:'Ik ben ziek.',                   correct:false},
    {text:'Welke kleur?',                   correct:false},
  ], feedback:'Als iemand haast heeft, zeg je: "Fijne reis!" of "Doei!"'},
  {prompt:'Ik ga op vakantie naar Spanje.', options:[
    {text:'Wat leuk! Hoe ga je daarheen?',  correct:true},
    {text:'Ik kom uit Syrië.',              correct:false},
    {text:'Goedemorgen.',                   correct:false},
  ], feedback:'Reageer op vakantieplannen met: "Wat leuk!" en stel een vraag.'},
  {prompt:'Hoe lang ga je weg?', options:[
    {text:'Twee weken.',                    correct:true},
    {text:'Met de auto.',                   correct:false},
    {text:'Ik ga naar Turkije.',            correct:false},
  ], feedback:'Bij "Hoe lang?" antwoord je met een periode: dagen, weken, maanden.'},
];

const convFillSets = [
  {label:'Gesprek 1', lines:[
    {speaker:'Vriend', fixed:'Hallo! Waar ga jij naartoe?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg waar je naartoe gaat', hint_en:'Say where you are going', hint_tr:'Nereye gittiğini söyle', hint_ar:'قل إلى أين تذهب', hint_om:'Eessa akka deemtu himi', hint_ps:'ووایه چېرته ځې', hint_zh:'说你要去哪里', example:'Ik ga naar Spanje.'},
    {speaker:'Vriend', fixed:'Wat leuk! Hoe ga je daarheen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg hoe je reist', hint_en:'Say how you travel', hint_tr:'Nasıl seyahat ettiğini söyle', hint_ar:'قل كيف تسافر', hint_om:'Akkamiin akka deemtu himi', hint_ps:'ووایه څنګه سفر کوې', hint_zh:'说你怎么旅行', example:'Met het vliegtuig.'},
    {speaker:'Vriend', fixed:'Ga je alleen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg met wie je gaat', hint_en:'Say who you go with', hint_tr:'Kiminle gittiğini söyle', hint_ar:'قل مع من تذهب', hint_om:'Eenyu wajjin akka deemtu himi', hint_ps:'ووایه له چا سره ځې', hint_zh:'说你和谁一起去', example:'Nee, ik ga met mijn gezin.'},
    {speaker:'Vriend', fixed:'Fijne vakantie!'},
    {speaker:'Jij', input:true, hint_nl:'Zeg bedankt en afscheid', hint_en:'Say thank you and goodbye', hint_tr:'Teşekkür et ve vedalaş', hint_ar:'قل شكراً ووداعاً', hint_om:'Galatoomii fi nagaatti jedhi', hint_ps:'مننه ووایه او جلا شه', hint_zh:'说谢谢并告别', example:'Dankjewel! Doei!'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Jij', input:true, hint_nl:'Begin het gesprek — begroet en stel een vraag', hint_en:'Start the conversation — greet and ask a question', hint_tr:'Konuşmayı başlat — selamla ve bir soru sor', hint_ar:'ابدأ المحادثة — سلم واسأل سؤالاً', hint_om:'Haasawa jalqabi — nagaa gaafadhii fi gaaffii gaafadhu', hint_ps:'خبرې پیل کړه — سلام او پوښتنه وکړه', hint_zh:'开始对话——打招呼并提问', example:'Hey! Waar ga jij naartoe?'},
    {speaker:'Vriend', fixed:'Ik ga naar Friesland. Met de trein en dan met de boot naar Ameland.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer en vertel waar jij naartoe gaat', hint_en:'React and tell where you are going', hint_tr:'Tepki ver ve nereye gittiğini anlat', hint_ar:'تفاعل وأخبر إلى أين تذهب', hint_om:'Deebii kennii fi eessa akka deemtu himi', hint_ps:'ځواب ورکړه او ووایه چېرته ځې', hint_zh:'回应并说你要去哪里', example:'Wat leuk! Ik ga naar Turkije.'},
    {speaker:'Vriend', fixed:'Leuk! Hoe ga je daarheen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg hoe je reist', hint_en:'Say how you travel', hint_tr:'Nasıl seyahat ettiğini söyle', hint_ar:'قل كيف تسافر', hint_om:'Akkamiin akka deemtu himi', hint_ps:'ووایه څنګه سفر کوې', hint_zh:'说你怎么旅行', example:'Met het vliegtuig. Ik ga eerst met de trein naar het vliegveld.'},
    {speaker:'Vriend', fixed:'Fijne reis!'},
    {speaker:'Jij', input:true, hint_nl:'Neem afscheid', hint_en:'Say goodbye', hint_tr:'Vedalaş', hint_ar:'ودع', hint_om:'Nagaatti jedhi', hint_ps:'جلا شه', hint_zh:'告别', example:'Dankjewel, jij ook! Doei!'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Collega', fixed:'Ik ga volgende week op vakantie!'},
    {speaker:'Jij', input:true, hint_nl:'Reageer en vraag waar', hint_en:'React and ask where', hint_tr:'Tepki ver ve nereye gittiğini sor', hint_ar:'تفاعل واسأل إلى أين', hint_om:'Deebii kennii fi eessa akka deemu gaafadhu', hint_ps:'ځواب ورکړه او پوښتنه وکړه چېرته', hint_zh:'回应并问去哪里', example:'Wat leuk! Waar ga je naartoe?'},
    {speaker:'Collega', fixed:'Naar Marokko. Met het vliegtuig.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag hoe lang', hint_en:'Ask how long', hint_tr:'Ne kadar süre olduğunu sor', hint_ar:'اسأل كم المدة', hint_om:'Hammam akka turu gaafadhu', hint_ps:'پوښتنه وکړه تر څو وخته', hint_zh:'问去多久', example:'Leuk! Hoe lang ga je weg?'},
    {speaker:'Collega', fixed:'Drie weken. Ik heb er zin in!'},
    {speaker:'Jij', input:true, hint_nl:'Wens een fijne vakantie', hint_en:'Wish a nice holiday', hint_tr:'İyi tatiller dile', hint_ar:'تمنى إجازة سعيدة', hint_om:'Boqonnaa gaarii hawwi', hint_ps:'ښه رخصتي هیله کړه', hint_zh:'祝假期愉快', example:'Super! Fijne vakantie!'},
  ]},
];

// ── STATE ────────────────────────────────────────────────────────────
let currentScreen = 1;
let lang = 'nl';
let sortIdx = 0, sortExercises = [], sortSlots = [], sortChipBtns = [];
let convIdx = 0, convSets = [], convSelected = null;
let q5aIdx = 0, q5a = [];
let q5bIdx = 0, q5b = [];
let convFillIdx = 0;
let drillMode = 'mc_meaning';
let drillQueue = [], drillCurrent = 0, drillCorrect = 0;
let copyIdx = 0;

// ── UTILS ────────────────────────────────────────────────────────────
function shuffle(arr){ const a=[...arr]; for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; }
function deepShuffle(arr){ return shuffle(arr).map(q=>({...q,options:shuffle(q.options)})); }

// ── LANGUAGE ────────────────────────────────────────────────────────
const T = {
  nl:{
    progress:'Voortgang',
    s1num:'Stap 1 van 13 · Woorden leren',s1title:'Kijk en lees de woorden',
    s1desc:'<strong>Leerdoel 8.1 ⭐⭐: Je kunt een gesprek voeren over reizen en vakantie — vertellen waar je naartoe gaat, hoe je reist en afscheid nemen.</strong><br>Druk op 🔊 om het woord te horen. Zeg het daarna zelf na!',
    s2num:'Stap 2 van 13 · Herhalen',s2title:'Zeg het na! 🗣️',s2desc:'Druk op 🔊 en zeg de zin hardop na. Zo vaak als je wilt!',
    s2info:'💡 Herhaal elke zin minimaal 3 keer. Hoe vaker, hoe beter!',
    s3b_num:'Stap 3 van 13 · Schrijf de zinnen over',s3b_title:'Schrijf de zin over ✏️',s3b_desc:'Schrijf elke zin precies over. Let op: hoofdletter aan het begin en punt of vraagteken aan het einde!',
    s3num:'Stap 4 van 13 · Woordentraining',s3title:'Ken jij de woorden? 🧠',s3desc:'Oefen de woorden. Maak geen fouten! Als je een fout maakt, begin je opnieuw.',
    s4num:'Stap 5 van 13 · Zinnen maken',s4title:'Maak de zin! 🧩',s4desc:'Tik de woorden in de juiste volgorde.',
    s5num:'Stap 6 van 13 · Gespreksvolgorde',s5title:'Zet het gesprek in de goede volgorde 💬',s5desc:'Tik een zin aan → tik dan op de juiste plek.',
    s6num:'Stap 7 van 13 · Goede zin kiezen',s6title:'Welke zin is goed? ✅',s6desc:'Kies de zin met de goede woordvolgorde.',
    s7num:'Stap 8 van 13 · Juist antwoord kiezen',s7title:'Wat is het goede antwoord? 🤔',s7desc:'Iemand stelt een vraag. Kies het juiste antwoord.',
    s8num:'Stap 9 van 13 · Schrijf over jouw reis',s8title:'Schrijf over jouw reis ✍️',s8desc:'Beantwoord de vragen hieronder in het Nederlands. Schrijf alles in het tekstvak en stuur het naar de docent.',
    ftlabel:'Vertel over jouw reis',
    fthint:'📝 Voorbeeld: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 Stuur mijn tekst naar de docent',
    waConv:'📲 Stuur dit gesprek naar de docent',
    s9num:'Stap 10 van 13 · Gesprek invullen',s9title:'Maak het gesprek compleet 📝',s9desc:'Vul in wat jij zegt. Gebruik de hint als je hulp nodig hebt.',
    s10num:'Stap 11 van 13 · Praten met een klasgenoot',s10title:'Oefen samen! 👥',s10desc:'Ga naast een klasgenoot zitten. Jullie gaan samen een gesprek oefenen over reizen.',
    s11num:'Stap 12 van 13 · Opnemen en sturen',s11title:'Neem het gesprek op! 🎤',s11desc:'Doe dit samen met jouw klasgenoot. Stuur de opname naar de docent.',
    s12num:'Stap 13 van 13 · Vrij gesprek',s12title:'Praat voor de klas! 🌟',s12desc:'Nu doe jij het zelf, zonder hulp. Je kunt dit!',
    sgTitle:'Stappenplan',sg1:'Begroet de ander: "Hallo!" of "Hey!"',sg2:'Vraag: "Waar ga jij naartoe?"',sg3:'Vertel hoe je reist: "Ik ga met de trein."',sg4:'Reageer op het antwoord: "Wat leuk!"',sg5:'Sluit af: "Fijne vakantie! Doei!"',
    congratsTitle:'Goed gedaan!',congratsSub:'Je hebt alle stappen van thema 8.1 gedaan!',
    learnedTitle:'📚 Woorden die je hebt geleerd',restart:'↺ Opnieuw oefenen',
    convOrderTitle:'Zet in de goede volgorde',beginLabel:'BEGIN 🟢',endLabel:'EINDE 🔴',
    questionLabel:'Vraag:',convFillTitle:'Vul in wat jij zegt',
    waFreeMsg:'Hallo docent! Dit is mijn tekst over reizen (thema 8.1):\n',
    waVoiceTip:'\n\n🎤 Ik stuur nu ook een voice memo!',
    drillCorrectMsg:'✅ Goed zo!',drillWrongMsg:'❌ Fout! Opnieuw van het begin.',
    drillDoneMsg:'🎉 Alle woorden goed! Probeer nu een andere modus.',
    drillScore:'Correct:',drillReset:'↺ Opnieuw (nieuwe volgorde)',
    checkBtn:'✓ Controleer',resetBtn:'↺ Opnieuw beginnen',
    prevSentence:'Vorige zin',nextSentence:'Volgende zin',
    writeQuestions:['1️⃣ Waar ga jij naartoe op vakantie?','2️⃣ Hoe ga je daarheen? (vliegtuig, trein, auto, boot?)','3️⃣ Met wie ga je op vakantie?','4️⃣ Wat ga je doen op vakantie?','5️⃣ Hoe lang ga je weg?','6️⃣ Ben je weleens naar het buitenland geweest? Waar naartoe?'],
  },
  en:{
    progress:'Progress',
    s1num:'Step 1 of 13 · Learn words',s1title:'Look and read the words',
    s1desc:'Press 🔊 to hear the word. Then say it yourself!',
    s2num:'Step 2 of 13 · Repeat',s2title:'Repeat out loud! 🗣️',s2desc:'Press 🔊 and say the sentence out loud. As many times as you like!',
    s2info:'💡 Repeat each sentence at least 3 times. The more, the better!',
    s3b_num:'Step 3 of 13 · Copy the sentences',s3b_title:'Copy the sentence ✏️',s3b_desc:'Write each sentence exactly. Pay attention to capital letters and the dot or question mark!',
    s3num:'Step 4 of 13 · Word training',s3title:'Do you know the words? 🧠',s3desc:'Practise the words. No mistakes! If you make a mistake, start again.',
    s4num:'Step 5 of 13 · Build sentences',s4title:'Build the sentence! 🧩',s4desc:'Tap the words in the correct order.',
    s5num:'Step 6 of 13 · Conversation order',s5title:'Put the conversation in the right order 💬',s5desc:'Tap a sentence → then tap the correct spot.',
    s6num:'Step 7 of 13 · Choose correct sentence',s6title:'Which sentence is correct? ✅',s6desc:'Choose the sentence with the correct word order.',
    s7num:'Step 8 of 13 · Choose correct answer',s7title:'What is the correct answer? 🤔',s7desc:'Someone asks a question. Choose the right answer.',
    s8num:'Step 9 of 13 · Write about your trip',s8title:'Write about your trip ✍️',s8desc:'Answer the questions below in Dutch. Write everything in the text box and send it to the teacher.',
    ftlabel:'Tell about your trip',
    fthint:'📝 Example: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 Send my text to the teacher',
    waConv:'📲 Send this conversation to the teacher',
    s9num:'Step 10 of 13 · Fill in the conversation',s9title:'Complete the conversation 📝',s9desc:'Fill in what you say. Use the hint if you need help.',
    s10num:'Step 11 of 13 · Talk with a classmate',s10title:'Practise together! 👥',s10desc:'Sit next to a classmate. You will practise a conversation about travel together.',
    s11num:'Step 12 of 13 · Record and send',s11title:'Record the conversation! 🎤',s11desc:'Do this together with your classmate. Send the recording to the teacher.',
    s12num:'Step 13 of 13 · Free conversation',s12title:'Talk in front of the class! 🌟',s12desc:'Now you do it yourself, without help. You can do this!',
    sgTitle:'Step-by-step',sg1:'Greet the other person: "Hallo!" or "Hey!"',sg2:'Ask: "Waar ga jij naartoe?"',sg3:'Tell how you travel: "Ik ga met de trein."',sg4:'React: "Wat leuk!"',sg5:'End: "Fijne vakantie! Doei!"',
    congratsTitle:'Well done!',congratsSub:'You completed all steps of theme 8.1!',
    learnedTitle:'📚 Words you have learned',restart:'↺ Practise again',
    convOrderTitle:'Put in the correct order',beginLabel:'START 🟢',endLabel:'END 🔴',
    questionLabel:'Question:',convFillTitle:'Fill in what you say',
    waFreeMsg:'Hello teacher! This is my text about travel (theme 8.1):\n',
    waVoiceTip:'\n\n🎤 I will also send a voice memo!',
    drillCorrectMsg:'✅ Correct!',drillWrongMsg:'❌ Wrong! Start again.',
    drillDoneMsg:'🎉 All words correct! Try another mode.',
    drillScore:'Correct:',drillReset:'↺ Try again (new order)',
    checkBtn:'✓ Check',resetBtn:'↺ Start over',
    prevSentence:'Previous',nextSentence:'Next',
    writeQuestions:['1️⃣ Where are you going on holiday?','2️⃣ How do you get there? (plane, train, car, boat?)','3️⃣ Who are you going with?','4️⃣ What are you going to do?','5️⃣ How long will you be away?','6️⃣ Have you ever been abroad? Where to?'],
  },
  tr:{
    progress:'İlerleme',
    s1num:'Adım 1 / 13 · Kelime öğrenme',s1title:'Kelimelere bak ve oku',
    s1desc:'Kelimeyi duymak için 🔊 düğmesine bas. Sonra kendin tekrar et!',
    s2num:'Adım 2 / 13 · Tekrar',s2title:'Tekrar et! 🗣️',s2desc:'🔊 düğmesine bas ve cümleyi sesli tekrar et. İstediğin kadar!',
    s2info:'💡 Her cümleyi en az 3 kez tekrar et. Ne kadar çok olursa o kadar iyi!',
    s3b_num:'Adım 3 / 13 · Cümleleri yaz',s3b_title:'Cümleyi kopyala ✏️',s3b_desc:'Her cümleyi tam olarak yaz. Büyük harf ve noktalama işaretlerine dikkat et!',
    s3num:'Adım 4 / 13 · Kelime alıştırması',s3title:'Kelimeleri biliyor musun? 🧠',s3desc:'Kelimeleri çalış. Hata yapma! Hata yaparsan baştan başla.',
    s4num:'Adım 5 / 13 · Cümle kur',s4title:'Cümleyi kur! 🧩',s4desc:'Kelimeleri doğru sıraya koy.',
    s5num:'Adım 6 / 13 · Konuşma sırası',s5title:'Konuşmayı doğru sıraya koy 💬',s5desc:'Bir cümleye dokun → sonra doğru yere yerleştir.',
    s6num:'Adım 7 / 13 · Doğru cümle',s6title:'Hangi cümle doğru? ✅',s6desc:'Doğru kelime sırasına sahip cümleyi seç.',
    s7num:'Adım 8 / 13 · Doğru cevap',s7title:'Doğru cevap ne? 🤔',s7desc:'Biri bir soru soruyor. Doğru cevabı seç.',
    s8num:'Adım 9 / 13 · Seyahatini yaz',s8title:'Seyahatini yaz ✍️',s8desc:'Aşağıdaki soruları Hollandaca olarak cevapla. Her şeyi metin kutusuna yaz ve öğretmene gönder.',
    ftlabel:'Seyahatini anlat',
    fthint:'📝 Örnek: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 Metnimi öğretmene gönder',
    waConv:'📲 Bu konuşmayı öğretmene gönder',
    s9num:'Adım 10 / 13 · Konuşmayı doldur',s9title:'Konuşmayı tamamla 📝',s9desc:'Ne söylediğini doldur. İpucunu kullan.',
    s10num:'Adım 11 / 13 · Sınıf arkadaşınla konuş',s10title:'Birlikte alıştırma yap! 👥',s10desc:'Sınıf arkadaşının yanına otur. Birlikte seyahat hakkında konuşma alıştırması yapacaksınız.',
    s11num:'Adım 12 / 13 · Kaydet ve gönder',s11title:'Konuşmayı kaydet! 🎤',s11desc:'Bunu sınıf arkadaşınla birlikte yap. Kaydı öğretmene gönder.',
    s12num:'Adım 13 / 13 · Serbest konuşma',s12title:'Sınıfın önünde konuş! 🌟',s12desc:'Şimdi kendin yap, yardım almadan. Yapabilirsin!',
    sgTitle:'Adım adım',sg1:'Karşındakini selamla: "Hallo!" veya "Hey!"',sg2:'Sor: "Waar ga jij naartoe?"',sg3:'Nasıl seyahat ettiğini anlat: "Ik ga met de trein."',sg4:'Tepki ver: "Wat leuk!"',sg5:'Bitir: "Fijne vakantie! Doei!"',
    congratsTitle:'Aferin!',congratsSub:'Tema 8.1\'in tüm adımlarını tamamladın!',
    learnedTitle:'📚 Öğrendiğin kelimeler',restart:'↺ Tekrar alıştırma yap',
    convOrderTitle:'Doğru sıraya koy',beginLabel:'BAŞLANGIÇ 🟢',endLabel:'SON 🔴',
    questionLabel:'Soru:',convFillTitle:'Ne söylediğini doldur',
    waFreeMsg:'Merhaba öğretmenim! Bu benim seyahat hakkındaki yazım (tema 8.1):\n',
    waVoiceTip:'\n\n🎤 Sesli mesaj da göndereceğim!',
    drillCorrectMsg:'✅ Doğru!',drillWrongMsg:'❌ Yanlış! Baştan başla.',
    drillDoneMsg:'🎉 Tüm kelimeler doğru! Başka bir mod dene.',
    drillScore:'Doğru:',drillReset:'↺ Tekrar dene (yeni sıra)',
    checkBtn:'✓ Kontrol et',resetBtn:'↺ Baştan başla',
    prevSentence:'Önceki',nextSentence:'Sonraki',
    writeQuestions:['1️⃣ Tatile nereye gidiyorsun?','2️⃣ Oraya nasıl gidiyorsun? (uçak, tren, araba, gemi?)','3️⃣ Tatile kiminle gidiyorsun?','4️⃣ Tatilde ne yapacaksın?','5️⃣ Ne kadar süre gideceksin?','6️⃣ Hiç yurt dışına gittin mi? Nereye?'],
  },
  ar:{
    progress:'التقدم',
    s1num:'الخطوة 1 من 13 · تعلم الكلمات',s1title:'انظر واقرأ الكلمات',
    s1desc:'اضغط على 🔊 لسماع الكلمة. ثم قلها بنفسك!',
    s2num:'الخطوة 2 من 13 · التكرار',s2title:'كرر بصوت عالٍ! 🗣️',s2desc:'اضغط على 🔊 وقل الجملة بصوت عالٍ. بقدر ما تريد!',
    s2info:'💡 كرر كل جملة 3 مرات على الأقل. كلما كان أكثر، كان أفضل!',
    s3b_num:'الخطوة 3 من 13 · انسخ الجمل',s3b_title:'انسخ الجملة ✏️',s3b_desc:'اكتب كل جملة بالضبط. انتبه إلى الأحرف الكبيرة والنقطة أو علامة الاستفهام!',
    s3num:'الخطوة 4 من 13 · تدريب الكلمات',s3title:'هل تعرف الكلمات؟ 🧠',s3desc:'تدرب على الكلمات. لا أخطاء! إذا أخطأت، ابدأ من جديد.',
    s4num:'الخطوة 5 من 13 · بناء الجمل',s4title:'ابنِ الجملة! 🧩',s4desc:'اضغط على الكلمات بالترتيب الصحيح.',
    s5num:'الخطوة 6 من 13 · ترتيب المحادثة',s5title:'ضع المحادثة في الترتيب الصحيح 💬',s5desc:'اضغط على جملة → ثم اضغط على المكان الصحيح.',
    s6num:'الخطوة 7 من 13 · اختر الجملة الصحيحة',s6title:'أي جملة صحيحة؟ ✅',s6desc:'اختر الجملة ذات ترتيب الكلمات الصحيح.',
    s7num:'الخطوة 8 من 13 · اختر الإجابة الصحيحة',s7title:'ما هي الإجابة الصحيحة؟ 🤔',s7desc:'شخص يسأل سؤالاً. اختر الإجابة الصحيحة.',
    s8num:'الخطوة 9 من 13 · اكتب عن رحلتك',s8title:'اكتب عن رحلتك ✍️',s8desc:'أجب عن الأسئلة أدناه بالهولندية. اكتب كل شيء في مربع النص وأرسله إلى المعلم.',
    ftlabel:'أخبر عن رحلتك',
    fthint:'📝 مثال: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 أرسل نصي إلى المعلم',
    waConv:'📲 أرسل هذه المحادثة إلى المعلم',
    s9num:'الخطوة 10 من 13 · املأ المحادثة',s9title:'أكمل المحادثة 📝',s9desc:'املأ ما تقوله. استخدم التلميح إذا احتجت إلى مساعدة.',
    s10num:'الخطوة 11 من 13 · تدرب مع زميل',s10title:'تدربا معاً! 👥',s10desc:'اجلس بجانب زميل. ستتدربان على محادثة عن السفر معاً.',
    s11num:'الخطوة 12 من 13 · سجل وأرسل',s11title:'سجل المحادثة! 🎤',s11desc:'افعل هذا مع زميلك. أرسل التسجيل إلى المعلم.',
    s12num:'الخطوة 13 من 13 · محادثة حرة',s12title:'تحدث أمام الفصل! 🌟',s12desc:'الآن افعلها بنفسك، بدون مساعدة. أنت تستطيع!',
    sgTitle:'خطوة بخطوة',sg1:'سلِّم على الآخر: "Hallo!" أو "Hey!"',sg2:'اسأل: "Waar ga jij naartoe?"',sg3:'أخبر كيف تسافر: "Ik ga met de trein."',sg4:'تفاعل: "Wat leuk!"',sg5:'أنهِ: "Fijne vakantie! Doei!"',
    congratsTitle:'أحسنت!',congratsSub:'لقد أكملت جميع خطوات الموضوع 8.1!',
    learnedTitle:'📚 الكلمات التي تعلمتها',restart:'↺ تدرب مرة أخرى',
    convOrderTitle:'ضع في الترتيب الصحيح',beginLabel:'ابدأ 🟢',endLabel:'نهاية 🔴',
    questionLabel:'سؤال:',convFillTitle:'املأ ما تقوله',
    waFreeMsg:'مرحباً أستاذ! هذا نصي عن السفر (موضوع 8.1):\n',
    waVoiceTip:'\n\n🎤 سأرسل أيضاً رسالة صوتية!',
    drillCorrectMsg:'✅ صحيح!',drillWrongMsg:'❌ خطأ! ابدأ من جديد.',
    drillDoneMsg:'🎉 جميع الكلمات صحيحة! جرب وضعاً آخر.',
    drillScore:'صحيح:',drillReset:'↺ حاول مرة أخرى',
    checkBtn:'✓ تحقق',resetBtn:'↺ ابدأ من جديد',
    prevSentence:'السابق',nextSentence:'التالي',
    writeQuestions:['1️⃣ إلى أين تذهب في العطلة؟','2️⃣ كيف تصل إلى هناك؟ (طائرة، قطار، سيارة، قارب؟)','3️⃣ مع من تذهب في العطلة؟','4️⃣ ماذا ستفعل في العطلة؟','5️⃣ كم ستكون مدة الغياب؟','6️⃣ هل سبق أن سافرت للخارج؟ إلى أين؟'],
  },
  om:{
    progress:'Adeemsa',
    s1num:'Tarkaanfii 1 / 13 · Jechoota barachuu',s1title:'Jechoota ilaalii dubbisi',
    s1desc:'Jecha dhaggeeffachuuf 🔊 cuqaasi. Achi booda ofii kee irra deebi\'i jedhi!',
    s2num:'Tarkaanfii 2 / 13 · Irra deebi\'uu',s2title:'Irra deebi\'ii jedhi! 🗣️',s2desc:'🔊 cuqaasii hima sagaleen ol jedhi. Si fedhetti irra deddeebi\'i!',
    s2info:'💡 Hima hunda yoo xiqqaate si\'a 3 irra deebi\'i. Irra baay\'atte, irra gaariidha!',
    s3b_num:'Tarkaanfii 3 / 13 · Himawwan barreessi',s3b_title:'Hima barreessi ✏️',s3b_desc:'Hima hunda sirriitti barreessi. Qubee guddaa jalqabaa fi tuqaa yookiin mallattoo gaaffii xumuraa irratti xiyyeeffadhu!',
    s3num:'Tarkaanfii 4 / 13 · Shaakala jechootaa',s3title:'Jechoota beektaa? 🧠',s3desc:'Jechoota shaakali. Dogoggora hin godhin! Yoo dogoggora goote, irra deebi\'ii jalqabi.',
    s4num:'Tarkaanfii 5 / 13 · Hima ijaaruu',s4title:'Hima ijaari! 🧩',s4desc:'Jechoota tartiiba sirrii ta\'een cuqaasi.',
    s5num:'Tarkaanfii 6 / 13 · Tartiiba haasawaa',s5title:'Haasawa tartiiba sirriitiin kaa\'i 💬',s5desc:'Hima cuqaasi → achi booda iddoo sirrii cuqaasi.',
    s6num:'Tarkaanfii 7 / 13 · Hima sirrii fili',s6title:'Hima kami sirriidha? ✅',s6desc:'Hima tartiiba jechootaa sirrii qabu fili.',
    s7num:'Tarkaanfii 8 / 13 · Deebii sirrii fili',s7title:'Deebiin sirrii maali? 🤔',s7desc:'Namni tokko gaaffii gaafata. Deebii sirrii fili.',
    s8num:'Tarkaanfii 9 / 13 · Waa\'ee imala keetii barreessi',s8title:'Waa\'ee imala keetii barreessi ✍️',s8desc:'Gaaffiiwwan armaan gadii Afaan Holandiin deebisi. Waan hunda sanduuqa barreeffamaa keessa barreessii barsiisaatti ergi.',
    ftlabel:'Waa\'ee imala keetii himi',
    fthint:'📝 Fakkeenya: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 Barreeffama koo barsiisaatti ergi',
    waConv:'📲 Haasawa kana barsiisaatti ergi',
    s9num:'Tarkaanfii 10 / 13 · Haasawa guuti',s9title:'Haasawa guutuu godhi 📝',s9desc:'Waan ati jettu guuti. Gargaarsa yoo barbaadde yaadachiisa fayyadami.',
    s10num:'Tarkaanfii 11 / 13 · Hiriyyaa waliin dubbisi',s10title:'Waliin shaakali! 👥',s10desc:'Hiriyyaa kee cinaa taa\'i. Waliin haasawa imala irratti shaakaltania.',
    s11num:'Tarkaanfii 12 / 13 · Waraabii ergi',s11title:'Haasawa waraabi! 🎤',s11desc:'Kana hiriyyaa kee waliin godhi. Waraabbii barsiisaatti ergi.',
    s12num:'Tarkaanfii 13 / 13 · Haasawa bilisa',s12title:'Fuula daree duratti dubbadhu! 🌟',s12desc:'Amma ofii kee godhi, gargaarsa malee. Dandeessa!',
    sgTitle:'Tarkaanfii tarkaanfiin',sg1:'Nama biraa nagaa gaafadhu: "Hallo!" yookiin "Hey!"',sg2:'Gaafadhu: "Waar ga jij naartoe?"',sg3:'Akkamiin akka deemtu himi: "Ik ga met de trein."',sg4:'Deebii kenni: "Wat leuk!"',sg5:'Xumuri: "Fijne vakantie! Doei!"',
    congratsTitle:'Hojii gaarii!',congratsSub:'Tarkaanfii mata duree 8.1 hunda xumurte!',
    learnedTitle:'📚 Jechoota baratte',restart:'↺ Irra deebi\'ii shaakali',
    convOrderTitle:'Tartiiba sirriitiin kaa\'i',beginLabel:'JALQABA 🟢',endLabel:'XUMURA 🔴',
    questionLabel:'Gaaffii:',convFillTitle:'Waan ati jettu guuti',
    waFreeMsg:'Barsiisaa koo nagaa! Kun barreeffama koo imala irratti (mata duree 8.1):\n',
    waVoiceTip:'\n\n🎤 Ergaa sagalee illee nan erga!',
    drillCorrectMsg:'✅ Sirriidha!',drillWrongMsg:'❌ Dogoggora! Irra deebi\'ii jalqabi.',
    drillDoneMsg:'🎉 Jechootni hundi sirriidha! Haala biraa yaali.',
    drillScore:'Sirrii:',drillReset:'↺ Irra deebi\'ii yaali (tartiiba haaraa)',
    checkBtn:'✓ Mirkaneessi',resetBtn:'↺ Irra deebi\'ii jalqabi',
    prevSentence:'Dura',nextSentence:'Itti aanee',
    writeQuestions:['1️⃣ Boqonnaaf eessa deemta?','2️⃣ Akkamiin achii deemta? (xiyyaara, baabura, konkolaataa, doonii?)','3️⃣ Eenyu wajjin boqonnaaf deemta?','4️⃣ Boqonnaa irratti maal gootaa?','5️⃣ Hammam turta?','6️⃣ Biyya alaa deemtee beektaa? Eessa?'],
  },
  ps:{
    progress:'پرمختګ',
    s1num:'ګام 1 له 13 · توکي زده کول',s1title:'وګوره او توکي ولوله',
    s1desc:'د توکو د اورېدلو لپاره 🔊 کېکاږه. بیا یې پخپله ووایه!',
    s2num:'ګام 2 له 13 · تکرار',s2title:'پس یې ووایه! 🗣️',s2desc:'🔊 کېکاږه او جمله په لوړ غږ ووایه. هرڅومره چې غواړې!',
    s2info:'💡 هره جمله لږ تر لږه 3 ځله تکرار کړه. هرڅومره ډېر، هومره ښه!',
    s3b_num:'ګام 3 له 13 · جملې ولیکه',s3b_title:'جمله ولیکه ✏️',s3b_desc:'هره جمله دقیقه ولیکه. پام وکړه: لوی توری په پیل کې او ټکی یا د پوښتنې نښه په پای کې!',
    s3num:'ګام 4 له 13 · د توکو تمرین',s3title:'ایا ته توکي پېژنې؟ 🧠',s3desc:'توکي تمرین کړه. غلطي مه کوه! که غلطي وکړې، بیا له سره پیل کوه.',
    s4num:'ګام 5 له 13 · جملې جوړول',s4title:'جمله جوړه کړه! 🧩',s4desc:'توکي په سمه ترتیب کېکاږه.',
    s5num:'ګام 6 له 13 · د خبرو ترتیب',s5title:'خبرې په سمه ترتیب کېږده 💬',s5desc:'یوه جمله کېکاږه → بیا سم ځای کېکاږه.',
    s6num:'ګام 7 له 13 · سمه جمله وټاکه',s6title:'کومه جمله سمه ده؟ ✅',s6desc:'هغه جمله وټاکه چې سم ترتیب لري.',
    s7num:'ګام 8 له 13 · سم ځواب وټاکه',s7title:'سم ځواب کوم دی؟ 🤔',s7desc:'یو څوک پوښتنه کوي. سم ځواب وټاکه.',
    s8num:'ګام 9 له 13 · د خپل سفر په اړه ولیکه',s8title:'د خپل سفر په اړه ولیکه ✍️',s8desc:'لاندې پوښتنو ته په هالنډي ځواب ورکړه. ټول یې د متن په بکس کې ولیکه او ښوونکي ته یې ولېږه.',
    ftlabel:'د خپل سفر په اړه ووایه',
    fthint:'📝 بېلګه: "Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 زما متن ښوونکي ته ولېږه',
    waConv:'📲 دا خبرې ښوونکي ته ولېږه',
    s9num:'ګام 10 له 13 · خبرې ډکې کړه',s9title:'خبرې بشپړې کړه 📝',s9desc:'هغه څه ډک کړه چې ته یې وایې. که مرسته پکار وه لارښود وکاروه.',
    s10num:'ګام 11 له 13 · له ملګري سره خبرې وکړه',s10title:'یوځای تمرین وکړئ! 👥',s10desc:'د ملګري تر څنګ کېنه. تاسو به یوځای د سفر خبرې تمرین کوئ.',
    s11num:'ګام 12 له 13 · ضبط کړه او ولېږه',s11title:'خبرې ضبط کړه! 🎤',s11desc:'دا له ملګري سره وکړه. ضبط شوی ښوونکي ته ولېږه.',
    s12num:'ګام 13 له 13 · آزادې خبرې',s12title:'د ټولګي مخې ته خبرې وکړه! 🌟',s12desc:'اوس پخپله وکړه، پرته له مرستې. ته کولی شې!',
    sgTitle:'ګام په ګام',sg1:'بل ته سلام ورکړه: "Hallo!" یا "Hey!"',sg2:'پوښتنه وکړه: "Waar ga jij naartoe?"',sg3:'ووایه چې څنګه سفر کوې: "Ik ga met de trein."',sg4:'غبرګون وکړه: "Wat leuk!"',sg5:'پای ته یې ورسوه: "Fijne vakantie! Doei!"',
    congratsTitle:'آفرین!',congratsSub:'ته د موضوع 8.1 ټولې مرحلې بشپړې کړې!',
    learnedTitle:'📚 هغه توکي چې دې زده کړل',restart:'↺ بیا تمرین وکړه',
    convOrderTitle:'په سمه ترتیب کېږده',beginLabel:'پیل 🟢',endLabel:'پای 🔴',
    questionLabel:'پوښتنه:',convFillTitle:'هغه څه ډک کړه چې ته یې وایې',
    waFreeMsg:'سلام ښوونکی! دا زما د سفر متن دی (موضوع 8.1):\n',
    waVoiceTip:'\n\n🎤 زه به یو غږیز پیغام هم ولېږم!',
    drillCorrectMsg:'✅ سم دی!',drillWrongMsg:'❌ غلط! بیا له سره پیل کړه.',
    drillDoneMsg:'🎉 ټول توکي سم دي! بله طریقه هم آزمایه.',
    drillScore:'سم:',drillReset:'↺ بیا هڅه وکړه (نوی ترتیب)',
    checkBtn:'✓ وګوره',resetBtn:'↺ بیا له سره پیل کړه',
    prevSentence:'مخکینی',nextSentence:'بل',
    writeQuestions:['1️⃣ ته په رخصتي کې چېرته ځې؟','2️⃣ هلته څنګه ځې؟ (الوتکه، اورګاډی، موټر، کشتي؟)','3️⃣ له چا سره رخصتي ته ځې؟','4️⃣ په رخصتي کې به څه کوې؟','5️⃣ تر څو وخته ځې؟','6️⃣ ته کله بهرنۍ هېواد ته تللی یې؟ چېرته؟'],
  },
  zh:{
    progress:'进度',
    s1num:'第1步/共13步 · 学习词汇',s1title:'看一看，读一读',
    s1desc:'按 🔊 听单词发音。然后自己跟读！',
    s2num:'第2步/共13步 · 重复',s2title:'跟读！🗣️',s2desc:'按 🔊 然后大声跟读句子。想读几遍就读几遍！',
    s2info:'💡 每个句子至少重复3遍。越多越好！',
    s3b_num:'第3步/共13步 · 抄写句子',s3b_title:'抄写句子 ✏️',s3b_desc:'准确抄写每个句子。注意：开头大写字母，结尾句号或问号！',
    s3num:'第4步/共13步 · 词汇训练',s3title:'你认识这些词吗？🧠',s3desc:'练习词汇。不要犯错！如果犯错，从头开始。',
    s4num:'第5步/共13步 · 造句',s4title:'造句！🧩',s4desc:'按正确顺序点击单词。',
    s5num:'第6步/共13步 · 对话排序',s5title:'把对话排成正确顺序 💬',s5desc:'点击一个句子 → 然后点击正确的位置。',
    s6num:'第7步/共13步 · 选择正确句子',s6title:'哪个句子是正确的？✅',s6desc:'选择词序正确的句子。',
    s7num:'第8步/共13步 · 选择正确答案',s7title:'正确答案是什么？🤔',s7desc:'有人提了一个问题。选择正确答案。',
    s8num:'第9步/共13步 · 写一写你的旅行',s8title:'写一写你的旅行 ✍️',s8desc:'用荷兰语回答以下问题。写在文本框中，发给老师。',
    ftlabel:'讲讲你的旅行',
    fthint:'📝 示例："Ik ga op vakantie naar Turkije. Ik ga met het vliegtuig. Ik ga met mijn gezin. We gaan twee weken."',
    waFree:'📲 把我的文字发给老师',
    waConv:'📲 把这段对话发给老师',
    s9num:'第10步/共13步 · 填写对话',s9title:'完成对话 📝',s9desc:'填写你说的内容。如果需要帮助，请使用提示。',
    s10num:'第11步/共13步 · 和同学练习',s10title:'一起练习！👥',s10desc:'坐在同学旁边。你们将一起练习关于旅行的对话。',
    s11num:'第12步/共13步 · 录音并发送',s11title:'录下对话！🎤',s11desc:'和同学一起完成。把录音发给老师。',
    s12num:'第13步/共13步 · 自由对话',s12title:'在全班面前说话！🌟',s12desc:'现在自己来，不需要帮助。你可以的！',
    sgTitle:'步骤指南',sg1:'和对方打招呼："Hallo!" 或 "Hey!"',sg2:'问："Waar ga jij naartoe?"',sg3:'说你怎么旅行："Ik ga met de trein."',sg4:'回应："Wat leuk!"',sg5:'告别："Fijne vakantie! Doei!"',
    congratsTitle:'做得好！',congratsSub:'你完成了主题8.1的所有步骤！',
    learnedTitle:'📚 你学到的词汇',restart:'↺ 再练习一次',
    convOrderTitle:'按正确顺序排列',beginLabel:'开始 🟢',endLabel:'结束 🔴',
    questionLabel:'问题：',convFillTitle:'填写你说的内容',
    waFreeMsg:'老师您好！这是我关于旅行的文字（主题8.1）：\n',
    waVoiceTip:'\n\n🎤 我也会发一条语音消息！',
    drillCorrectMsg:'✅ 正确！',drillWrongMsg:'❌ 错误！从头开始。',
    drillDoneMsg:'🎉 所有词汇都正确！试试另一种模式。',
    drillScore:'正确：',drillReset:'↺ 再试一次（新顺序）',
    checkBtn:'✓ 检查',resetBtn:'↺ 重新开始',
    prevSentence:'上一个',nextSentence:'下一个',
    writeQuestions:['1️⃣ 你假期去哪里？','2️⃣ 你怎么去？（飞机、火车、汽车、船？）','3️⃣ 你和谁一起去度假？','4️⃣ 你在假期做什么？','5️⃣ 你去多长时间？','6️⃣ 你去过国外吗？去了哪里？'],
  }
};

function t(k){ return T[lang][k] || T['en'][k] || k; }

function setLang(l){
  lang = l;
  ['nl','en','tr','ar','om','ps','zh'].forEach(x => document.getElementById('btn-'+x).classList.toggle('active-lang', l===x));
  document.body.setAttribute('dir', (l==='ar'||l==='ps') ? 'rtl' : 'ltr');
  document.body.style.fontFamily = l==='zh' ? "'Noto Sans SC','Microsoft YaHei','Nunito',sans-serif" : "'Nunito',sans-serif";
  rebuildAll();
}

// ── NAV ─────────────────────────────────────────────────────────────
let currentIndex = 0;
function updateUI() {
  const screens = document.querySelectorAll('.screen');
  screens.forEach((s, i) => s.classList.toggle('active', i === currentIndex));
  updateProgress();
  buildDots();
  const act = screens[currentIndex];
  if(act.id==='screen-4a') { drillMode='mc_meaning'; initDrill(); }
  else if(act.id==='screen-4b') { drillMode='mc_reverse'; initDrill(); }
  else if(act.id==='screen-4c') { drillMode='write'; initDrill(); }
  else if(act.id==='screen-3') { copyIdx=0; initCopyDrill(); }
  else if(act.id==='screen-5') { initSort(); }
  else if(act.id==='screen-6') { initConv(); }
  else if(act.id==='screen-7') { initQ5a(); }
  else if(act.id==='screen-8') { initQ5b(); }
  else if(act.id==='screen-10') { initConvFill(); }
  window.scrollTo(0,0);
}

function nextLoc() { 
  const screens=document.querySelectorAll('.screen'); 
  if(currentIndex < screens.length-1) { currentIndex++; updateUI(); }
}
function prevLoc() {
  if(currentIndex > 0) { currentIndex--; updateUI(); }
}

function updateProgress(){
  const screens = document.querySelectorAll('.screen');
  const total = screens.length;
  const pct=Math.round((currentIndex/(total-1))*100);
  document.getElementById('progress-fill').style.width=pct+'%';
  document.getElementById('progress-pct').textContent=pct+'%';
  document.getElementById('step-label').textContent=(currentIndex+1);
}


const bottomNavEmojis = ["👋","🗣️","✍️","📖","🧩","📝","🧩","🔄","🧐","🤔","✍️","📝","👥","🎙️","🎉"];

function buildDots(){
  const tDots=document.getElementById('step-dots');
  const bDots=document.getElementById('bottom-dots');
  if(tDots) tDots.innerHTML='';
  if(bDots) bDots.innerHTML='';
  const screens=document.querySelectorAll('.screen');
  const total=screens.length;
  for(let i=0;i<total;i++){
    if(tDots){
      const d=document.createElement('div');
      d.className='step-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      tDots.appendChild(d);
    }
    if(bDots){
      const bd=document.createElement('button');
      bd.className='b-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      bd.textContent=bottomNavEmojis[i] || "🔹";
      bd.onclick=()=>{ currentIndex=i; updateUI(); };
      bDots.appendChild(bd);
    }
  }
}
function speak(text,btn){
  if(!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang='nl-NL'; u.rate=0.82; u.pitch=1;
  if(btn){ btn.classList.add('playing'); u.onend=()=>btn.classList.remove('playing'); u.onerror=()=>btn.classList.remove('playing'); }
  window.speechSynthesis.speak(u);
}
function audioBtn(text){
  return `<button class="audio-btn" onclick="speak('${text.replace(/'/g,"\\'")}',this)">🔊</button>`;
}

// ── S1: WORDS ───────────────────────────────────────────────────────
function buildWordGrid(){
  const c=document.getElementById('word-grid'); c.innerHTML='';
  wordsData.forEach(w=>{
    const card=document.createElement('div'); card.className='word-card';
    let translation = '';
    if(lang==='en') translation = `<div class="word-en">${w.en}</div>`;
    else if(lang==='tr') translation = `<div class="word-en">${w.tr}</div>`;
    else if(lang==='ar') translation = `<div class="word-en" style="font-family:Arial;direction:rtl;text-align:right;">${w.ar||''}</div>`;
    else if(lang==='om') translation = `<div class="word-en">${w.om}</div>`;
    else if(lang==='ps') translation = `<div class="word-en" style="font-family:Arial;direction:rtl;text-align:right;">${w.ps||''}</div>`;
    else if(lang==='zh') translation = `<div class="word-en">${w.zh}</div>`;
    else translation = `<div class="word-en" style="color:var(--muted);font-size:0.82rem;">${w.desc_nl||''}</div>`;
    card.innerHTML=`<div class="word-main-row"><div class="word-emoji">${w.emoji}</div><div><div class="word-nl">${w.nl}</div>${translation}</div></div>${audioBtn(w.nl)}`;
    c.appendChild(card);
  });
}

// ── S2: REPEAT ──────────────────────────────────────────────────────
function buildRepeatGrid(){
  const c=document.getElementById('repeat-grid'); c.innerHTML='';
  repeatPhrases.forEach(p=>{
    const card=document.createElement('div'); card.className='word-card';
    card.innerHTML=`<div class="word-main-row"><div class="word-emoji">${p.emoji}</div><div class="word-nl">${p.nl}</div></div>${audioBtn(p.nl)}`;
    c.appendChild(card);
  });
}

// ── COPY DRILL ──────────────────────────────────────────────────────
function initCopyDrill(){ copyIdx=0; renderCopyDrill(); }
function renderCopyDrill(){
  const c=document.getElementById('copy-drill-container'); if(!c) return; c.innerHTML='';
  if(copyIdx>=copyPhrases.length){
    const done=document.createElement('div'); done.className='drill-card';
    done.innerHTML='<div style="font-size:3rem;margin-bottom:10px;">🎉</div><div style="font-size:1.2rem;font-weight:900;color:var(--green);">'+(lang==='nl'?'Alle zinnen overschreven! Goed gedaan!':lang==='tr'?'Tüm cümleler kopyalandı! Aferin!':lang==='ar'?'تم نسخ جميع الجمل! أحسنت!':lang==='om'?'Himawwan hundi barreeffaman! Hojii gaarii!':lang==='ps'?'ټولې جملې لیکل شوې! آفرین!':lang==='zh'?'所有句子已抄写！做得好！':'All sentences copied! Well done!')+'</div>';
    c.appendChild(done);
    const rb=document.createElement('button'); rb.className='btn-reset'; rb.style='margin-top:10px;'; rb.textContent=t('resetBtn'); rb.onclick=initCopyDrill; c.appendChild(rb);
    return;
  }
  const phrase=copyPhrases[copyIdx];

  // ── VISUAL EXAMPLE BOX ──────────────────────────────────────────
  const demo=document.createElement('div'); demo.className='copy-demo';
  const demoTitle=lang==='en'?'⚠️ ATTENTION — Do NOT answer! Copy the sentence EXACTLY!':lang==='tr'?'⚠️ DİKKAT — Cevap verme! Cümleyi AYNEN kopyala!':lang==='ar'?'⚠️ انتباه — لا تجب! انسخ الجملة بالضبط!':lang==='om'?'⚠️ XIYYEEFFANNOO — Hin deebisiin! Hima SIRRIITTI barreessi!':lang==='ps'?'⚠️ پام — ځواب مه ورکوه! جمله دقیقه کاپي کړه!':lang==='zh'?'⚠️ 注意 — 不要回答！请准确抄写句子！':'⚠️ LET OP — Geef geen antwoord! Kopieer de zin PRECIES!';
  const goodLbl=lang==='en'?'✅ CORRECT — exact copy:':lang==='tr'?'✅ DOĞRU — tam kopya:':lang==='ar'?'✅ صحيح — نسخة مطابقة:':lang==='om'?'✅ SIRRII — kopii sirrii:':lang==='ps'?'✅ سم — دقیقه کاپي:':lang==='zh'?'✅ 正确 — 准确复制：':'✅ GOED — exacte kopie:';
  const badLbl=lang==='en'?'❌ WRONG — this is an answer, not a copy!':lang==='tr'?'❌ YANLIŞ — bu bir cevap, kopya değil!':lang==='ar'?'❌ خطأ — هذا جواب وليس نسخة!':lang==='om'?'❌ DOGOGGORA — kun deebii, kopii miti!':lang==='ps'?'❌ غلط — دا ځواب دی، کاپي نه دی!':lang==='zh'?'❌ 错误 — 这是答案，不是复制！':'❌ FOUT — dit is een antwoord, geen kopie!';
  demo.innerHTML=`<div class="copy-demo-title">${demoTitle}</div>`
    +`<div class="copy-demo-row good"><div class="copy-demo-icon">✅</div><div class="copy-demo-content"><div class="copy-demo-label">${goodLbl}</div><div class="copy-demo-sentence">"Ik ga naar Spanje."</div><div class="copy-demo-input">⌨️ → <strong>Ik ga naar Spanje.</strong></div></div></div>`
    +`<div class="copy-demo-row bad"><div class="copy-demo-icon">❌</div><div class="copy-demo-content"><div class="copy-demo-label">${badLbl}</div><div class="copy-demo-sentence">"Ik ga naar Spanje."</div><div class="copy-demo-input">⌨️ → <s style="color:#C62828;">Ik ga naar Turkije.</s></div></div></div>`;
  c.appendChild(demo);

  const pb=document.createElement('div'); pb.className='drill-progress-bar';
  const pf=document.createElement('div'); pf.className='drill-progress-fill'; pf.style.width=((copyIdx/copyPhrases.length)*100)+'%'; pb.appendChild(pf); c.appendChild(pb);
  const score=document.createElement('div'); score.className='drill-score'; score.textContent=(copyIdx+1)+' / '+copyPhrases.length; c.appendChild(score);
  const card=document.createElement('div'); card.className='drill-card';
  const copyLabel = lang==='en'?'📋 COPY this sentence — write the SAME words:':lang==='tr'?'📋 Bu cümleyi KOPYALA — AYNI kelimeleri yaz:':lang==='ar'?'📋 انسخ هذه الجملة — اكتب نفس الكلمات:':lang==='om'?'📋 Hima kana KOPPII — jecha WALFAKKAATAA barreessi:':lang==='ps'?'📋 دا جمله کاپي کړه — ورته کلمې ولیکه:':lang==='zh'?'📋 抄写这个句子 — 写相同的词：':'📋 KOPIEER deze zin — schrijf DEZELFDE woorden:';
  card.innerHTML='<div style="font-size:0.95rem;font-weight:900;color:#E65100;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;background:#FFF3E0;padding:10px 12px;border-radius:10px;border-left:4px solid #E65100;">'+copyLabel+'</div>'
    +'<div style="font-size:1.4rem;font-weight:900;margin-bottom:6px;color:var(--blue);background:#E3F2FD;padding:12px 14px;border-radius:10px;border:2px dashed var(--blue);">📖 '+phrase+'</div>'
    +audioBtn(phrase)+'<div style="height:8px;"></div>'
    +'<div style="font-size:0.78rem;font-weight:800;color:#E65100;margin-bottom:6px;">⬇️ '+(lang==='en'?'Now type the SAME sentence below:':lang==='tr'?'Şimdi AYNI cümleyi aşağıya yaz:':lang==='ar'?'الآن اكتب نفس الجملة أدناه:':lang==='om'?'Amma hima WALFAKKAATAA barreessi:':lang==='ps'?'اوس ورته جمله لاندې ولیکه:':lang==='zh'?'现在在下方输入相同的句子：':'Typ nu DEZELFDE zin hieronder:')+'</div>';
  const inp=document.createElement('input'); inp.className='drill-write-input'; inp.type='text'; inp.id='copy-inp';
  inp.style='font-size:1.35rem;font-weight:900;padding:20px;text-align:center;border:3px solid var(--blue);border-radius:14px;color:var(--text);margin-top:8px;box-shadow:0 4px 15px rgba(0,0,0,0.06);';
  inp.placeholder='...';
  card.appendChild(inp);
  const checkBtn=document.createElement('button'); checkBtn.className='btn-check'; checkBtn.textContent=t('checkBtn');
  checkBtn.onclick=()=>{
    const val=inp.value.trim(); const ok=val===phrase;
    const fb=document.getElementById('copy-fb'); fb.className='feedback-box show'+(ok?'':' wrong-fb');
    if(ok){
      fb.textContent=t('drillCorrectMsg'); speak(phrase); inp.disabled=true; checkBtn.style.display='none';
      const nxt=document.createElement('button'); nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;';
      nxt.textContent=t('nextSentence')+' →'; nxt.onclick=()=>{copyIdx++;renderCopyDrill();}; card.appendChild(nxt);
    } else {
      let msg='';
      if(val.toLowerCase()===phrase.toLowerCase()&&val!==phrase) msg=(lang==='en'?'❌ Almost! Check capital letters and punctuation.':lang==='tr'?'❌ Neredeyse! Büyük harfleri ve noktalamayı kontrol et.':lang==='ar'?'❌ تقريباً! تحقق من الأحرف الكبيرة وعلامات الترقيم.':lang==='om'?'❌ Xiqqoo hafteera! Qubee guddaa fi mallattoo sirreessi.':lang==='ps'?'❌ نږدې! لوی توری او نښې وګوره.':lang==='zh'?'❌ 差一点！检查大小写和标点符号。':'❌ Bijna! Let op hoofdletters en leestekens.');
      else msg=(lang==='en'?'❌ Not the same. Try again: ':lang==='tr'?'❌ Aynı değil. Tekrar dene: ':lang==='ar'?'❌ ليست نفسها. حاول مرة أخرى: ':lang==='om'?'❌ Wal hin fakkaatu. Irra deebi\'ii yaali: ':lang==='ps'?'❌ ورته نه دی. بیا هڅه وکړه: ':lang==='zh'?'❌ 不一样。再试一次： ':'❌ Niet hetzelfde. Probeer opnieuw: ')+phrase;
      fb.textContent=msg; inp.focus(); inp.select();
    }
  };
  card.appendChild(checkBtn);
  const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='copy-fb'; card.appendChild(fb); c.appendChild(card);
  const rb=document.createElement('button'); rb.className='btn-reset'; rb.textContent=t('resetBtn'); rb.onclick=initCopyDrill; c.appendChild(rb);
  inp.addEventListener('keydown',e=>{if(e.key==='Enter')checkBtn.click();}); setTimeout(()=>inp.focus(),100);
}

// ── S4: DRILL ───────────────────────────────────────────────────────
function getTranslation(w){
  if(lang==='en') return w.en;
  if(lang==='tr') return w.tr;
  if(lang==='ar') return w.ar;
  if(lang==='om') return w.om;
  if(lang==='ps') return w.ps;
  if(lang==='zh') return w.zh;
  return w.desc_nl;
}

function initDrill(){ drillQueue=shuffle(wordsData.map((w,i)=>i)); drillCurrent=0; drillCorrect=0; renderDrill(); }
function renderDrill(){
  const s = document.querySelectorAll('.screen')[currentIndex]; const c=s.querySelector('.drill-container-wrap'); if(!c) return; c.innerHTML='';
  const isNL = lang==='nl';
  // mode tabs
  const modes = isNL ? [
    {key:'mc_meaning',  label:'Wat betekent dit?'},
    {key:'mc_reverse',  label:'Welk woord past?'},
    {key:'write',       label:'Schrijf het woord ✏️'},
  ] : [
    {key:'mc_meaning',  label:lang==='tr'?'Bu ne demek?':lang==='ar'?'ماذا يعني هذا؟':lang==='om'?'Maal jechuudha?':lang==='ps'?'دا څه معنی لري؟':lang==='zh'?'这是什么意思？':'What does it mean?'},
    {key:'mc_reverse',  label:lang==='tr'?'Hollandaca nasıl?':lang==='ar'?'كيف بالهولندية؟':lang==='om'?'Afaan Holandiin akkamiin?':lang==='ps'?'په هالنډي څنګه؟':lang==='zh'?'荷兰语怎么说？':'How in Dutch?'},
    {key:'write',       label:lang==='tr'?'Hollandaca yaz ✏️':lang==='ar'?'اكتب بالهولندية ✏️':lang==='om'?'Afaan Holandiin barreessi ✏️':lang==='ps'?'په هالنډي ولیکه ✏️':lang==='zh'?'用荷兰语写 ✏️':'Write in Dutch ✏️'},
  ];
  const tabs=document.createElement('div'); tabs.className='drill-mode-tabs';
  modes.forEach(m=>{
    const b=document.createElement('button'); b.className='drill-mode-tab'+(drillMode===m.key?' active-tab':'');
    b.textContent=m.label; b.onclick=()=>{drillMode=m.key;initDrill();}; tabs.appendChild(b);
  });
  c.appendChild(tabs);

  if(drillCurrent>=drillQueue.length){
    const done=document.createElement('div'); done.className='drill-card';
    done.innerHTML=`<div style="font-size:3rem;margin-bottom:10px;">🎉</div><div style="font-size:1.2rem;font-weight:900;color:var(--green);">${t('drillDoneMsg')}</div>`;
    c.appendChild(done);
    const rb=document.createElement('button'); rb.className='btn-reset'; rb.style='margin-top:10px;'; rb.textContent=t('drillReset'); rb.onclick=initDrill; c.appendChild(rb);
    return;
  }
  const pb=document.createElement('div'); pb.className='drill-progress-bar';
  const pf=document.createElement('div'); pf.className='drill-progress-fill'; pf.style.width=((drillCurrent/wordsData.length)*100)+'%'; pb.appendChild(pf); c.appendChild(pb);
  const score=document.createElement('div'); score.className='drill-score'; score.textContent=`${t('drillScore')} ${drillCorrect} / ${wordsData.length}`; c.appendChild(score);

  const wordIdx=drillQueue[drillCurrent]; const word=wordsData[wordIdx];
  const card=document.createElement('div'); card.className='drill-card';

  if(drillMode==='mc_meaning'){
    // Show NL word, pick the right meaning
    const question=word.nl;
    const correctAnswer=getTranslation(word);
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>getTranslation(w));
    const opts=shuffle([correctAnswer,...distractors]);
    const sub=isNL?'Wat betekent dit woord?':lang==='tr'?'Bu kelime ne demek?':lang==='ar'?'ماذا تعني هذه الكلمة؟':lang==='om'?'Jechni kun maal jechuudha?':lang==='ps'?'دا کلمه څه معنی لري؟':lang==='zh'?'这个词是什么意思？':'What does this word mean?';
    card.innerHTML=`<div style="font-size:2rem;margin-bottom:8px;">${word.emoji}</div><div class="drill-question">${question}</div><div class="drill-question-sub">${sub}</div>${audioBtn(word.nl)}<div style="margin-top:14px;"></div>`;
    const optsDiv=document.createElement('div'); optsDiv.className='drill-options';
    opts.forEach(opt=>{
      const btn=document.createElement('button'); btn.className='drill-opt'; btn.textContent=opt;
      btn.onclick=()=>answerDrill(btn,opt===correctAnswer,word.nl); optsDiv.appendChild(btn);
    });
    card.appendChild(optsDiv);
  } else if(drillMode==='mc_reverse'){
    // Show meaning, pick the right NL word
    const question=getTranslation(word);
    const correctAnswer=word.nl;
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>w.nl);
    const opts=shuffle([correctAnswer,...distractors]);
    const sub=isNL?'Welk Nederlands woord past hierbij?':lang==='tr'?'Hangi Hollandaca kelime uyuyor?':lang==='ar'?'أي كلمة هولندية تناسب؟':lang==='om'?'Jecha Afaan Holandii kami ta\'a?':lang==='ps'?'کومه هالنډي کلمه ورته ده؟':lang==='zh'?'哪个荷兰语词匹配？':'Which Dutch word matches?';
    card.innerHTML=`<div style="font-size:2rem;margin-bottom:8px;">${word.emoji}</div><div class="drill-question">${question}</div><div class="drill-question-sub">${sub}</div><div style="margin-top:14px;"></div>`;
    const optsDiv=document.createElement('div'); optsDiv.className='drill-options';
    opts.forEach(opt=>{
      const btn=document.createElement('button'); btn.className='drill-opt'; btn.textContent=opt;
      btn.onclick=()=>answerDrill(btn,opt===correctAnswer,word.nl); optsDiv.appendChild(btn);
    });
    card.appendChild(optsDiv);
  } else {
    // write mode
    const question=getTranslation(word);
    const correctAnswer=word.nl.toLowerCase().trim();
    const sub=isNL?'Schrijf dit woord in het Nederlands:':lang==='tr'?'Bu kelimeyi Hollandaca yaz:':lang==='ar'?'اكتب هذه الكلمة بالهولندية:':lang==='om'?'Jecha kana Afaan Holandiin barreessi:':lang==='ps'?'دا کلمه په هالنډي ولیکه:':lang==='zh'?'用荷兰语写这个词：':'Write this word in Dutch:';
    card.innerHTML=`<div style="font-size:2rem;margin-bottom:8px;">${word.emoji}</div><div class="drill-question">${question}</div><div class="drill-question-sub">${sub}</div><div style="margin-top:14px;"></div>`;
    const inp=document.createElement('input'); inp.className='drill-write-input'; inp.type='text'; inp.id='drill-write-inp';
    inp.placeholder=isNL?'Schrijf hier...':lang==='tr'?'Buraya yaz...':lang==='ar'?'اكتب هنا...':lang==='om'?'Asitti barreessi...':lang==='ps'?'دلته ولیکه...':lang==='zh'?'在这里写...':'Write here...';
    card.appendChild(inp);
    const submitBtn=document.createElement('button'); submitBtn.className='btn-check'; submitBtn.textContent=t('checkBtn');
    submitBtn.onclick=()=>{ const val=inp.value.toLowerCase().trim(); const ok=val===correctAnswer||val===correctAnswer.replace(/^de |^het /,''); answerDrill(submitBtn,ok,word.nl,val,word.nl); };
    card.appendChild(submitBtn);
    inp.addEventListener('keydown',e=>{if(e.key==='Enter')submitBtn.click();});
  }
  const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='drill-fb'; card.appendChild(fb); c.appendChild(card);
  const rb=document.createElement('button'); rb.className='btn-reset'; rb.textContent=t('drillReset'); rb.onclick=initDrill; c.appendChild(rb);
}

function answerDrill(el,correct,speakText,written,correctWritten){
  const fb=document.getElementById('drill-fb'); const card=fb.parentElement;
  if(correct){
    drillCorrect++; drillCurrent++; fb.className='feedback-box show'; fb.textContent=t('drillCorrectMsg'); speak(speakText);
    if(el.classList.contains('drill-opt')) { el.classList.add('correct'); }
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    if(el.classList.contains('btn-check')) el.style.display='none';
    const nxt=document.createElement('button'); nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;';
    nxt.textContent=t('nextSentence')+' →'; nxt.onclick=renderDrill; card.appendChild(nxt);
  } else {
    fb.className='feedback-box show wrong-fb';
    fb.textContent=t('drillWrongMsg')+(correctWritten?` ✔ ${correctWritten}`:'');
    if(el.classList.contains('drill-opt')) el.classList.add('wrong');
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    if(el.classList.contains('btn-check')) el.style.display='none';
    const nxt=document.createElement('button'); nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;';
    nxt.textContent=t('resetBtn');
    nxt.onclick=()=>{drillQueue=shuffle(wordsData.map((_,i)=>i));drillCurrent=0;drillCorrect=0;renderDrill();};
    card.appendChild(nxt);
  }
}

// ── S5: SORT ────────────────────────────────────────────────────────
function initSort(){ sortExercises=sortExercisesBase.map(e=>({...e})); sortIdx=0; buildSort(); }
function buildSort(){
  sortSlots=[]; sortChipBtns=[];
  const ex=sortExercises[sortIdx]; const shuffledWords=shuffle(ex.words);
  const c=document.getElementById('sort-container'); c.innerHTML='';
  const lbl=lang==='nl'?'Zin':lang==='tr'?'Cümle':lang==='ar'?'جملة':lang==='om'?'Hima':lang==='ps'?'جمله':lang==='zh'?'句子':'Sentence';
  const instr=lang==='nl'?'Maak een goede zin:':lang==='tr'?'Doğru bir cümle kur:':lang==='ar'?'كوّن جملة صحيحة:':lang==='om'?'Hima sirrii ijaari:':lang==='ps'?'سمه جمله جوړه کړه:':lang==='zh'?'造一个正确的句子：':'Make a correct sentence:';
  const hdr=document.createElement('div'); hdr.className='sort-header';
  hdr.innerHTML=`<div class="sort-header-meta">${lbl} ${sortIdx+1} / ${sortExercises.length}</div><div style="font-size:0.88rem;color:#555;font-weight:700;">${instr}</div>`;
  c.appendChild(hdr);
  const speakRow=document.createElement('div'); speakRow.style='display:flex;align-items:center;gap:8px;margin-bottom:10px;';
  const hearLbl=lang==='nl'?'Hoor de zin:':lang==='tr'?'Cümleyi dinle:':lang==='ar'?'استمع للجملة:':lang==='om'?'Hima dhaggeeffadhu:':lang==='ps'?'جمله واوره:':lang==='zh'?'听句子：':'Hear it:';
  speakRow.innerHTML=`<span style="font-size:0.78rem;font-weight:700;color:var(--muted);">${hearLbl}</span>${audioBtn(ex.answer.replace(/\s\./g,'.').replace(/\s\?/g,'?').replace(/\s!/g,'!'))}`;
  c.appendChild(speakRow);
  const chipsDiv=document.createElement('div'); chipsDiv.className='word-chips';
  shuffledWords.forEach(w=>{
    const btn=document.createElement('button'); btn.className='chip'; btn.textContent=w;
    btn.onclick=()=>tapSortChip(btn,w); chipsDiv.appendChild(btn); sortChipBtns.push(btn);
  });
  c.appendChild(chipsDiv);
  const slotsDiv=document.createElement('div'); slotsDiv.className='answer-slots';
  ex.words.forEach((_,i)=>{
    const slot=document.createElement('div'); slot.className='slot';
    slot.innerHTML=`<span class="slot-num">${i+1}</span><span class="slot-text"></span>`;
    slot.onclick=()=>removeSortSlot(slot); slotsDiv.appendChild(slot); sortSlots.push(slot);
  });
  c.appendChild(slotsDiv);
  const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='sort-fb'; c.appendChild(fb);
  const snav=document.createElement('div'); snav.className='sort-nav';
  snav.innerHTML=`<button class="sort-nav-btn" onclick="prevSort()" ${sortIdx===0?'disabled':''}>← ${t('prevSentence')}</button><button class="sort-nav-btn primary" onclick="nextSort()" ${sortIdx===sortExercises.length-1?'disabled':''}>${t('nextSentence')} →</button>`;
  c.appendChild(snav);
  const rb=document.createElement('button'); rb.className='btn-reset'; rb.textContent=t('resetBtn'); rb.onclick=initSort; c.appendChild(rb);
}
function tapSortChip(btn,w){ if(btn.classList.contains('used'))return; const empty=sortSlots.find(s=>!s.classList.contains('filled')); if(!empty)return; empty.querySelector('.slot-text').textContent=w; empty.classList.add('filled'); btn.classList.add('used'); if(!sortSlots.find(s=>!s.classList.contains('filled'))) checkSort(); }
function removeSortSlot(slot){ if(!slot.classList.contains('filled'))return; const w=slot.querySelector('.slot-text').textContent; slot.querySelector('.slot-text').textContent=''; slot.classList.remove('filled','correct-slot','wrong-slot'); const chip=sortChipBtns.find(b=>b.textContent===w&&b.classList.contains('used')); if(chip)chip.classList.remove('used'); const fb=document.getElementById('sort-fb'); if(fb)fb.className='feedback-box'; }
function checkSort(){ const ex=sortExercises[sortIdx]; const expected=ex.answer.split(' '); let ok=true; sortSlots.forEach((s,i)=>{s.classList.remove('correct-slot','wrong-slot');if(s.classList.contains('filled')){const w=s.querySelector('.slot-text').textContent;if(w===expected[i])s.classList.add('correct-slot');else{s.classList.add('wrong-slot');ok=false;}}else ok=false;}); const fb=document.getElementById('sort-fb'); fb.className='feedback-box show'+(ok?'':' wrong-fb'); fb.textContent=ok?t('drillCorrectMsg'):`${t('drillWrongMsg')} → ${ex.answer.replace(/\s\./g,'.').replace(/\s\?/g,'?').replace(/\s!/g,'!')}`; if(ok){ speak(ex.answer.replace(/\s\./g,'.').replace(/\s\?/g,'?').replace(/\s!/g,'!')); sortSlots.forEach(s=>s.onclick=null); sortChipBtns.forEach(b=>b.onclick=null); const snav=document.querySelector('#sort-container .sort-nav'); if(snav){ const c=document.createElement('button'); c.textContent=t('nextSentence')+' →'; c.className='btn-main'; c.style='margin-bottom:12px;width:100%;'; c.onclick=nextSort; snav.parentNode.insertBefore(c,snav); } } }
function nextSort(){ if(sortIdx<sortExercises.length-1){sortIdx++;buildSort();} }
function prevSort(){ if(sortIdx>0){sortIdx--;buildSort();} }

// ── S6: CONV ORDER ──────────────────────────────────────────────────
function initConv(){ convSets=shuffle(convSetsBase.map(s=>({...s,lines:[...s.lines]}))); convIdx=0; buildConv(); }
function buildConv(){
  convSelected=null; const set=convSets[convIdx]; const shuffledLines=shuffle(set.lines);
  const c=document.getElementById('conv-order-container'); c.innerHTML='';
  const lbl=document.createElement('div'); lbl.className='conv-set-label'; lbl.textContent=set.label; c.appendChild(lbl);
  const info=document.createElement('div'); info.className='info-box';
  info.textContent=lang==='nl'?'👆 Tik een zin aan. Tik dan op de juiste plek hieronder.':lang==='tr'?'👆 Bir cümleye dokun. Sonra aşağıda doğru yere yerleştir.':lang==='ar'?'👆 اضغط على جملة. ثم اضغط على المكان الصحيح أدناه.':lang==='om'?'👆 Hima cuqaasi. Achi booda iddoo sirrii armaan gadii cuqaasi.':lang==='ps'?'👆 یوه جمله کېکاږه. بیا لاندې سم ځای کېکاږه.':lang==='zh'?'👆 点击一个句子。然后点击下方正确的位置。':'👆 Tap a sentence. Then tap the correct spot below.';
  c.appendChild(info);
  const src=document.createElement('div'); src.className='conv-source'; src.id='conv-src';
  shuffledLines.forEach(line=>{
    const btn=document.createElement('button'); btn.className='conv-chip'; btn.dataset.text=line.text; btn.dataset.speaker=line.speaker;
    const spA=set.lines[0].speaker;
    const isSpeakerB=line.speaker!==spA;
    btn.innerHTML=`<span class="conv-speaker${isSpeakerB?' sp-b':''}">${line.speaker}</span><bdi dir="ltr">${line.text}</bdi>`;
    btn.onclick=()=>selectConvChip(btn); src.appendChild(btn);
  });
  c.appendChild(src);
  const oa=document.createElement('div'); oa.className='order-area';
  const oaT=document.createElement('div'); oaT.className='order-area-title'; oaT.textContent=t('convOrderTitle'); oa.appendChild(oaT);
  const sw=document.createElement('div'); sw.id='conv-slots';
  set.lines.forEach((line,i)=>{
    const slot=document.createElement('div'); slot.className='order-slot'; slot.dataset.pos=i;
    const label=i===0?t('beginLabel'):i===set.lines.length-1?t('endLabel'):(i+1)+'';
    slot.innerHTML=`<span class="order-slot-num">${label}</span><span class="order-slot-content" style="flex:1;"></span>`;
    slot.onclick=()=>placeConvLine(slot,i,set.lines[i]); sw.appendChild(slot);
  });
  oa.appendChild(sw); c.appendChild(oa);
  const chk=document.createElement('button'); chk.className='btn-check'; chk.textContent=t('checkBtn'); chk.onclick=checkConv; c.appendChild(chk); const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='conv-fb'; c.appendChild(fb);
  const pLbl=lang==='nl'?'Vorig gesprek':lang==='tr'?'Önceki konuşma':lang==='ar'?'المحادثة السابقة':lang==='om'?'Haasawa dura':lang==='ps'?'مخکینی خبرې':lang==='zh'?'上一个对话':'Prev';
  const nLbl=lang==='nl'?'Volgend gesprek':lang==='tr'?'Sonraki konuşma':lang==='ar'?'المحادثة التالية':lang==='om'?'Haasawa itti aanu':lang==='ps'?'بلې خبرې':lang==='zh'?'下一个对话':'Next';
  const cnav=document.createElement('div'); cnav.className='conv-set-nav';
  cnav.innerHTML=`<button class="conv-set-btn" onclick="prevConv()" ${convIdx===0?'disabled':''}>← ${pLbl}</button><button class="conv-set-btn primary" onclick="nextConv()" ${convIdx===convSets.length-1?'disabled':''}>${nLbl} →</button>`;
  c.appendChild(cnav);
  const rb=document.createElement('button'); rb.className='btn-reset'; rb.textContent=t('resetBtn'); rb.onclick=buildConv; c.appendChild(rb);
}
function selectConvChip(btn){ if(btn.classList.contains('placed'))return; document.querySelectorAll('#conv-src .conv-chip.selected').forEach(b=>b.classList.remove('selected')); if(convSelected===btn){convSelected=null;return;} btn.classList.add('selected'); convSelected=btn; }
function placeConvLine(slot){ if(!convSelected)return; if(slot.dataset.placedSpeaker){ document.querySelectorAll('#conv-src .conv-chip').forEach(b=>{if(b.dataset.speaker===slot.dataset.placedSpeaker&&b.dataset.text===slot.dataset.placedText&&b.classList.contains('placed'))b.classList.remove('placed');}); }
  const speaker=convSelected.dataset.speaker; const text=convSelected.dataset.text;
  const spA=convSets[convIdx].lines[0].speaker; const isSpeakerB=speaker!==spA;
  slot.querySelector('.order-slot-content').innerHTML=`<span class="conv-speaker${isSpeakerB?' sp-b':''}" style="font-size:0.68rem;font-weight:900;text-transform:uppercase;margin-right:6px;">${speaker}</span><bdi dir="ltr">${text}</bdi>`;
  slot.classList.add('has-content'); slot.classList.remove('correct-conv','wrong-slot'); slot.dataset.placedSpeaker=speaker; slot.dataset.placedText=text;
  convSelected.classList.remove('selected'); convSelected.classList.add('placed'); convSelected=null;
  const fb=document.getElementById('conv-fb'); if(fb)fb.className='feedback-box';
  
}
function checkConv(){ const set=convSets[convIdx]; const slots=document.querySelectorAll('#conv-slots .order-slot'); let correct=0; slots.forEach((slot,i)=>{slot.classList.remove('correct-conv','wrong-slot');if(slot.dataset.placedSpeaker===set.lines[i].speaker&&slot.dataset.placedText===set.lines[i].text){slot.classList.add('correct-conv');correct++;}else{slot.classList.add('wrong-slot');}}); const fb=document.getElementById('conv-fb'); fb.className='feedback-box show'+(correct===set.lines.length?'':' wrong-fb'); fb.textContent=correct===set.lines.length?t('drillCorrectMsg'):`${correct} / ${set.lines.length}`; if(correct===set.lines.length){ const snav=document.querySelector('#conv-order-container .conv-set-nav'); if(snav){ const cnavBtn=document.getElementById('conv-nxt-auto'); if(!cnavBtn){ const b=document.createElement('button'); b.id='conv-nxt-auto'; b.textContent=t('nextSentence')+' →'; b.className='btn-main'; b.style='margin-bottom:12px;width:100%;'; b.onclick=nextConv; snav.parentNode.insertBefore(b,snav); } } slots.forEach(s=>s.onclick=null); } }
function nextConv(){ if(convIdx<convSets.length-1){convIdx++;buildConv();} }
function prevConv(){ if(convIdx>0){convIdx--;buildConv();} }

// ── S7: Q5A ─────────────────────────────────────────────────────────
function initQ5a(){ q5a=deepShuffle(q5aBase); q5aIdx=0; renderQ5a(); }
function renderQ5a(){
  const q=q5a[q5aIdx]; const c=document.getElementById('q5a-container');
  const pLbl=lang==='nl'?'← Vorige':lang==='tr'?'← Önceki':lang==='ar'?'← السابق':lang==='om'?'← Dura':lang==='ps'?'← مخکینی':lang==='zh'?'← 上一个':'← Prev';
  const nLbl=lang==='nl'?'Volgende →':lang==='tr'?'Sonraki →':lang==='ar'?'التالي →':lang==='om'?'Itti aanee →':lang==='ps'?'بل →':lang==='zh'?'下一个 →':'Next →';
  c.innerHTML=`<div class="question-card"><div class="question-label">${t('questionLabel')}</div><div class="question-text">${q.prompt}</div></div>
    <div class="options" id="q5a-opts">${q.options.map((o,oi)=>`<button class="option-btn" data-correct="${o.correct}" data-idx="${oi}" onclick="answerQ5a(this)">${o.text}</button>`).join('')}</div>
    <div class="feedback-box" id="q5a-fb"></div>
    <div class="q-nav"><button class="q-nav-btn" onclick="prevQ5a()" ${q5aIdx===0?'disabled':''}>${pLbl}</button><button class="q-nav-btn primary" onclick="nextQ5a()" ${q5aIdx===q5a.length-1?'disabled':''}>${nLbl}</button></div>
    <div class="q-counter">${q5aIdx+1} / ${q5a.length}</div>
    <button class="btn-reset" onclick="initQ5a()">${t('resetBtn')}</button>`;
}
function answerQ5a(btn){ if(document.querySelector('#q5a-opts .option-btn.correct, #q5a-opts .option-btn.wrong'))return; const correct=btn.dataset.correct==='true'; document.querySelectorAll('#q5a-opts .option-btn').forEach(b=>{b.onclick=null;b.style.cursor='default';}); btn.classList.add(correct?'correct':'wrong'); if(!correct){document.querySelectorAll('#q5a-opts .option-btn').forEach(b=>{if(b.dataset.correct==='true')b.classList.add('correct');});} const fb=document.getElementById('q5a-fb'); fb.className='feedback-box show'+(correct?'':' wrong-fb'); fb.textContent=correct?t('drillCorrectMsg'):t('drillWrongMsg'); }
function nextQ5a(){ if(q5aIdx<q5a.length-1){q5aIdx++;renderQ5a();} }
function prevQ5a(){ if(q5aIdx>0){q5aIdx--;renderQ5a();} }

// ── S8: Q5B ─────────────────────────────────────────────────────────
function initQ5b(){ q5b=deepShuffle(q5bBase); q5bIdx=0; renderQ5b(); }
function renderQ5b(){
  const q=q5b[q5bIdx]; const c=document.getElementById('q5b-container');
  const pLbl=lang==='nl'?'← Vorige':lang==='tr'?'← Önceki':lang==='ar'?'← السابق':lang==='om'?'← Dura':lang==='ps'?'← مخکینی':lang==='zh'?'← 上一个':'← Prev';
  const nLbl=lang==='nl'?'Volgende →':lang==='tr'?'Sonraki →':lang==='ar'?'التالي →':lang==='om'?'Itti aanee →':lang==='ps'?'بل →':lang==='zh'?'下一个 →':'Next →';
  c.innerHTML=`<div class="question-card"><div class="question-label">${t('questionLabel')}</div><div class="question-text">${q.prompt}</div></div>
    <div class="options" id="q5b-opts">${q.options.map((o,oi)=>`<button class="option-btn" data-correct="${o.correct}" data-idx="${oi}" onclick="answerQ5b(this)">${o.text}</button>`).join('')}</div>
    <div class="feedback-box" id="q5b-fb"></div>
    <div class="q-nav"><button class="q-nav-btn" onclick="prevQ5b()" ${q5bIdx===0?'disabled':''}>${pLbl}</button><button class="q-nav-btn primary" onclick="nextQ5b()" ${q5bIdx===q5b.length-1?'disabled':''}>${nLbl}</button></div>
    <div class="q-counter">${q5bIdx+1} / ${q5b.length}</div>
    <button class="btn-reset" onclick="initQ5b()">${t('resetBtn')}</button>`;
}
function answerQ5b(btn){ if(document.querySelector('#q5b-opts .option-btn.correct, #q5b-opts .option-btn.wrong'))return; const correct=btn.dataset.correct==='true'; document.querySelectorAll('#q5b-opts .option-btn').forEach(b=>{b.onclick=null;b.style.cursor='default';}); btn.classList.add(correct?'correct':'wrong'); document.querySelectorAll('#q5b-opts .option-btn').forEach(b=>{if(b.dataset.correct==='true')b.classList.add('correct');}); const fb=document.getElementById('q5b-fb'); fb.className='feedback-box show'+(correct?'':' wrong-fb'); fb.textContent=(correct?t('drillCorrectMsg'):t('drillWrongMsg'))+' — '+q5b[q5bIdx].feedback; }
function nextQ5b(){ if(q5bIdx<q5b.length-1){q5bIdx++;renderQ5b();} }
function prevQ5b(){ if(q5bIdx>0){q5bIdx--;renderQ5b();} }

// ── S9: WRITE QUESTIONS ─────────────────────────────────────────────
function buildWriteQuestions(){
  const ql=document.getElementById('write-questions'); if(!ql) return;
  const questions = t('writeQuestions');
  ql.innerHTML='';
  questions.forEach(q=>{ const li=document.createElement('li'); li.textContent=q; ql.appendChild(li); });
}

// ── WHATSAPP ────────────────────────────────────────────────────────
function sendFreeTextWA(){
  const ft=document.getElementById('free-text').value||'...';
  const msg=t('waFreeMsg')+ft;
  window.open(`https://wa.me/${TEACHER_WA}?text=${encodeURIComponent(msg)}`,'_blank');
}
function sendConvFillWA(){
  const set=convFillSets[convFillIdx]; let lines=[];
  set.lines.forEach((line,li)=>{
    if(line.input){ const val=document.getElementById(`cf-${convFillIdx}-${li}`)?.value||'...'; lines.push(`Jij: ${val}`); }
    else lines.push(`${line.speaker}: ${line.fixed}`);
  });
  let msg = '';
  if (lang === 'nl') msg = 'Hallo docent! Dit is mijn gesprek (thema 8.1, '+set.label+'):\n';
  else if (lang === 'tr') msg = 'Merhaba öğretmenim! Bu benim konuşmam (tema 8.1, '+set.label+'):\n';
  else if (lang === 'ar') msg = 'مرحباً أستاذ! هذه محادثتي (موضوع 8.1, '+set.label+'):\n';
  else if (lang === 'om') msg = 'Akkam barsiisaa! Kun haasawa kooti (mata duree 8.1, '+set.label+'):\n';
  else if (lang === 'ps') msg = 'سلام ښوونکی! دا زما خبرې دي (موضوع 8.1, '+set.label+'):\n';
  else if (lang === 'zh') msg = '老师您好！这是我的对话（主题8.1，'+set.label+'）：\n';
  else msg = 'Hello teacher! My conversation (theme 8.1, '+set.label+'):\n';
  msg += lines.join('\n');
  window.open(`https://wa.me/${TEACHER_WA}?text=${encodeURIComponent(msg)}`,'_blank');
}

// ── S10: CONV FILL ──────────────────────────────────────────────────
function buildConvFill(){ convFillIdx=0; renderConvFill(); }
function renderConvFill(){
  const set=convFillSets[convFillIdx]; const c=document.getElementById('conv-fill-container'); c.innerHTML='';
  const wrap=document.createElement('div'); wrap.className='conv-fill-wrap';
  const title=document.createElement('div'); title.className='conv-fill-title'; title.textContent=`${t('convFillTitle')} — ${set.label}`; wrap.appendChild(title);
  set.lines.forEach((line,li)=>{
    const isJij=line.speaker==='Jij';
    const lineDiv=document.createElement('div'); lineDiv.className='conv-line';
    const sp=document.createElement('div'); sp.className=`conv-line-speaker ${isJij?'sp-a':'sp-b'}`; sp.textContent=line.speaker; lineDiv.appendChild(sp);
    const contentDiv=document.createElement('div'); contentDiv.style='flex:1;';
    if(line.input){
      const hint=lang==='ar'?line.hint_ar:lang==='tr'?line.hint_tr:lang==='en'?line.hint_en:lang==='om'?line.hint_om:lang==='ps'?line.hint_ps:lang==='zh'?line.hint_zh:line.hint_nl;
      const inp=document.createElement('input'); inp.className='conv-fill-input'; inp.type='text'; inp.id=`cf-${convFillIdx}-${li}`; inp.placeholder='...'; contentDiv.appendChild(inp);
      const hintDiv=document.createElement('div'); hintDiv.className='conv-hint'; hintDiv.textContent='💡 '+hint; contentDiv.appendChild(hintDiv);
      const toggleBtn=document.createElement('button');
      toggleBtn.style='background:none;border:none;font-size:0.78rem;font-weight:800;color:var(--blue);cursor:pointer;padding:4px 0;font-family:Nunito,sans-serif;';
      const showLbl=lang==='en'?'💡 Show example':lang==='tr'?'💡 Örnek göster':lang==='ar'?'💡 إظهار مثال':lang==='om'?'💡 Fakkeenya agarsiisi':lang==='ps'?'💡 بېلګه وښییه':lang==='zh'?'💡 显示示例':'💡 Toon voorbeeld';
      const hideLbl=lang==='en'?'🙈 Hide':lang==='tr'?'🙈 Gizle':lang==='ar'?'🙈 إخفاء':lang==='om'?'🙈 Dhoksi':lang==='ps'?'🙈 پټ کړه':lang==='zh'?'🙈 隐藏':'🙈 Verberg';
      toggleBtn.textContent=showLbl;
      const exDiv=document.createElement('div'); exDiv.style='color:var(--green);font-size:0.82rem;font-weight:800;margin-top:3px;display:none;'; exDiv.textContent='✏️ '+line.example;
      toggleBtn.onclick=()=>{exDiv.style.display=exDiv.style.display==='none'?'block':'none';toggleBtn.textContent=exDiv.style.display==='none'?showLbl:hideLbl;};
      contentDiv.appendChild(toggleBtn); contentDiv.appendChild(exDiv);
    } else {
      const fixedRow=document.createElement('div'); fixedRow.className='conv-line-fixed-row';
      fixedRow.innerHTML=`<div class="conv-line-fixed">${line.fixed}</div>${audioBtn(line.fixed)}`; contentDiv.appendChild(fixedRow);
    }
    lineDiv.appendChild(contentDiv); wrap.appendChild(lineDiv);
  });
  c.appendChild(wrap);
  const nav=document.createElement('div'); nav.className='conv-fill-nav';
  const pLbl=lang==='nl'?'← Vorig gesprek':lang==='tr'?'← Önceki':lang==='ar'?'← السابق':lang==='om'?'← Dura':lang==='ps'?'← مخکینی':lang==='zh'?'← 上一个':'← Prev';
  const nLbl=lang==='nl'?'Volgend gesprek →':lang==='tr'?'Sonraki →':lang==='ar'?'التالي →':lang==='om'?'Itti aanee →':lang==='ps'?'بل →':lang==='zh'?'下一个 →':'Next →';
  const prevBtn=document.createElement('button'); prevBtn.className='conv-fill-nav-btn'; prevBtn.disabled=convFillIdx===0; prevBtn.textContent=pLbl;
  prevBtn.onclick=()=>{if(convFillIdx>0){convFillIdx--;renderConvFill();}}; nav.appendChild(prevBtn);
  const counter=document.createElement('div'); counter.className='conv-set-counter'; counter.style='padding-top:10px;min-width:60px;text-align:center;'; counter.textContent=`${convFillIdx+1} / ${convFillSets.length}`; nav.appendChild(counter);
  const nextBtn=document.createElement('button'); nextBtn.className='conv-fill-nav-btn primary'; nextBtn.disabled=convFillIdx===convFillSets.length-1; nextBtn.textContent=nLbl;
  nextBtn.onclick=()=>{if(convFillIdx<convFillSets.length-1){convFillIdx++;renderConvFill();}}; nav.appendChild(nextBtn);
  c.appendChild(nav);
}

// ── S11: PAIR WORK ──────────────────────────────────────────────────
function buildPairWork(){
  const c=document.getElementById('pair-work-container'); c.innerHTML='';
  const isNL=lang==='nl'; const isEN=lang==='en'; const isTR=lang==='tr'; const isOM=lang==='om'; const isPS=lang==='ps'; const isZH=lang==='zh';
  const steps=[
    {icon:'👫', title_nl:'Stap 1 — Ga naast een klasgenoot zitten', title_en:'Step 1 — Sit next to a classmate', title_tr:'Adım 1 — Sınıf arkadaşının yanına otur', title_ar:'الخطوة 1 — اجلس بجانب زميل', title_om:'Tarkaanfii 1 — Hiriyyaa kee cinaa taa\'i', title_ps:'ګام 1 — د ملګري تر څنګ کېنه',
     desc_nl:'Zoek een klasgenoot. Ga naast diegene zitten. Jullie gaan samen een reisgesprek oefenen.', desc_en:'Find a classmate. Sit next to that person. Together you will practise a travel conversation.', desc_tr:'Bir sınıf arkadaşı bul. Yanına otur. Birlikte seyahat konuşması yapacaksınız.', desc_ar:'ابحث عن زميل. اجلس بجانبه. ستتدربان على محادثة سفر معاً.', desc_om:'Hiriyyaa kee barbaadi. Cinaa isaa taa\'i. Haasawa imala waliin shaakaltania.', desc_ps:'ملګری ولتول. د هغه تر څنګ کېنه. تاسو به یوځای د سفر خبرې تمرین کوئ.', desc_zh:'找一个同学。坐在他旁边。你们将一起练习旅行对话。'},
    {icon:'🃏', title_nl:'Stap 2 — Kies: ben jij persoon A of persoon B?', title_en:'Step 2 — Choose: are you person A or B?', title_tr:'Adım 2 — A mı B mi olacaksın?', title_ar:'الخطوة 2 — اختر: هل أنت الشخص أ أم ب؟', title_om:'Tarkaanfii 2 — Fili: nama A moo B?', title_ps:'ګام 2 — وټاکه: ته کس A یې کې B؟',
     desc_nl:'Besluit wie persoon A is en wie persoon B. Persoon A begint het gesprek.', desc_en:'Decide who is A and who is B. Person A starts.', desc_tr:'Kim A kim B olacağını belirle. A başlar.', desc_ar:'قرروا من سيكون أ ومن سيكون ب. الشخص أ يبدأ.', desc_om:'Eenyu A fi eenyu B akka ta\'e murteessi. Namni A jalqaba.', desc_ps:'پرېکړه چا A دی او چا B. کس A پیل کوي.', desc_zh:'决定谁是A谁是B。A先开始。'},
  ];
  steps.forEach((s,i)=>{
    const box=document.createElement('div'); box.className='pair-step';
    const title=lang==='ar'?s.title_ar:isTR?s.title_tr:isEN?s.title_en:isOM?s.title_om:isPS?s.title_ps:isZH?s.title_zh:s.title_nl;
    const desc=lang==='ar'?s.desc_ar:isTR?s.desc_tr:isEN?s.desc_en:isOM?s.desc_om:isPS?s.desc_ps:isZH?s.desc_zh:s.desc_nl;
    box.innerHTML=`<div class="pair-step-icon">${s.icon}</div><div class="pair-step-title">${title}</div><div class="pair-step-desc">${desc}</div>`;
    c.appendChild(box);
  });
  const roleRow=document.createElement('div'); roleRow.className='pair-role-row';
  const roleA=document.createElement('div'); roleA.className='pair-role-card role-a';
  const aTasks=['1️⃣ Begroet: "Hallo!"','2️⃣ Vraag: "Waar ga jij naartoe?"','3️⃣ Reageer: "Wat leuk!"','4️⃣ Afscheid: "Fijne vakantie!"'];
  roleA.innerHTML=`<div class="pair-role-label">${isNL?'Persoon A':isEN?'Person A':isTR?'Kişi A':isPS?'کس A':isZH?'角色A':lang==='om'?'Nama A':'الشخص أ'}</div><div class="pair-role-icon">🙋</div>${aTasks.map(t=>`<div class="pair-task">${t}</div>`).join('')}`;
  const roleB=document.createElement('div'); roleB.className='pair-role-card role-b';
  const bTasks=['1️⃣ Begroet terug: "Hallo!"','2️⃣ Vertel: "Ik ga naar …"','3️⃣ Zeg hoe: "Met het vliegtuig."','4️⃣ Afscheid: "Dankjewel, doei!"'];
  roleB.innerHTML=`<div class="pair-role-label">${isNL?'Persoon B':isEN?'Person B':isTR?'Kişi B':isPS?'کس B':isZH?'角色B':lang==='om'?'Nama B':'الشخص ب'}</div><div class="pair-role-icon">🙋‍♂️</div>${bTasks.map(t=>`<div class="pair-task">${t}</div>`).join('')}`;
  roleRow.appendChild(roleA); roleRow.appendChild(roleB); c.appendChild(roleRow);
  const switchBox=document.createElement('div'); switchBox.className='info-box';
  switchBox.innerHTML=isNL?'🔄 <strong>Daarna wisselen!</strong> A wordt B, B wordt A. Doe het gesprek nog een keer!':isEN?'🔄 <strong>Then switch!</strong> A becomes B, B becomes A. Do it again!':isTR?'🔄 <strong>Sonra değiştir!</strong> A B olur, B A olur. Tekrar yap!':isPS?'🔄 <strong>بیا بدل کړئ!</strong> A B کېږي، B A کېږي. بیا یې وکړئ!':isZH?'🔄 <strong>然后交换！</strong> A变成B，B变成A。再做一次！':lang==='om'?'🔄 <strong>Achi booda jijjiiraa!</strong> A B ta\'a, B A ta\'a. Irra deebi\'ii godhi!':'🔄 <strong>ثم بدّلا!</strong> أ يصبح ب، ب يصبح أ. أعيدا المحادثة!';
  c.appendChild(switchBox);
}

// ── S12: VOICE MEMO ─────────────────────────────────────────────────
function buildVoiceMemo(){
  const c=document.getElementById('voice-memo-container'); c.innerHTML='';
  const isNL=lang==='nl'; const isEN=lang==='en'; const isTR=lang==='tr'; const isZH=lang==='zh';
  const stepsData=[
    {emoji:'🗣️', title_nl:'Oefen het gesprek eerst samen', title_en:'Practise together first', title_tr:'Önce birlikte alıştırma yap', title_ar:'تدربا معاً أولاً', title_ps:'لومړی یوځای تمرین وکړئ', title_zh:'先一起练习',
     desc_nl:'Spreek het reisgesprek samen door. Probeer zo natuurlijk mogelijk te klinken!', desc_en:'Speak the travel conversation together. Try to sound as natural as possible!', desc_tr:'Seyahat konuşmasını birlikte yapın. Doğal olmaya çalışın!', desc_ar:'تحدثا محادثة السفر معاً. حاولا أن تبدوا طبيعيين!', desc_ps:'د سفر خبرې یوځای وکړئ. هڅه وکړئ چې تبيعي ښکاري!', desc_zh:'一起练习旅行对话。尽量说得自然！'},
    {emoji:'🤳', title_nl:'Open WhatsApp', title_en:'Open WhatsApp', title_tr:'WhatsApp\'ı aç', title_ar:'افتح واتساب', title_ps:'واټس اپ پرانیزه', title_om:'WhatsApp banii', title_zh:'打开WhatsApp',
     desc_nl:'Open WhatsApp op jouw telefoon. Ga naar het gesprek met de docent.', desc_en:'Open WhatsApp on your phone. Go to the conversation with the teacher.', desc_tr:'Telefonunda WhatsApp\'ı aç. Öğretmenle olan konuşmaya git.', desc_ar:'افتح واتساب على هاتفك. اذهب إلى المحادثة مع المعلم.', desc_ps:'په موبایل کې واټس اپ پرانیزه. ښوونکي سره خبرو ته لاړ شه.', desc_om:'Bilbila kee irratti WhatsApp banii. Haasawa barsiisaa waliin qabduutti darbi.', desc_zh:'在手机上打开WhatsApp。转到与老师的聊天界面。'},
    {emoji:'🎙️', title_nl:'Houd de microfoon knop ingedrukt', title_en:'Hold down the microphone button', title_tr:'Mikrofon düğmesini basılı tut', title_ar:'اضغط مع الاستمرار على زر الميكروفون', title_ps:'د مایکروفون تګمه کېکاږه ونیسه', title_zh:'按住麦克风按钮',
     desc_nl:'In WhatsApp: houd de 🎙️ knop ingedrukt. Voer het gesprek samen. Laat los als je klaar bent.', desc_en:'In WhatsApp: hold down the 🎙️ button. Do the conversation together. Release when finished.', desc_tr:'WhatsApp\'ta: 🎙️ düğmesini basılı tut. Konuşmayı birlikte yapın. Bitince bırakın.', desc_ar:'في واتساب: اضغط مع الاستمرار على زر 🎙️. أجرِ المحادثة معاً. أفلت عند الانتهاء.', desc_zh:'在WhatsApp中：按住🎙️按钮。一起进行对话。完成后松开。', desc_ps:'په WhatsApp کې: د 🎙️ تګمه کېکاږه ونیسه. یوځای خبرې وکړئ. کله چې تیار شوې پرېږده.'},
    {emoji:'📤', title_nl:'Stuur de opname', title_en:'Send the recording', title_tr:'Kaydı gönder', title_ar:'أرسل التسجيل', title_ps:'ضبط شوی ولېږه', title_zh:'发送录音',
     desc_nl:'Laat de knop los en druk op "Stuur".', desc_en:'Release the button and press "Send".', desc_tr:'Düğmeyi bırak ve "Gönder"e bas.', desc_ar:'أفلت الزر واضغط على "إرسال".', desc_ps:'تګمه پرېږده او "لېږل" کېکاږه.', desc_zh:'松开按钮并按“发送”。'},
  ];
  const wrap=document.createElement('div'); wrap.className='voice-steps';
  stepsData.forEach((s,i)=>{
    const box=document.createElement('div'); box.className='voice-step';
    const title=lang==='ar'?s.title_ar:lang==='ps'?s.title_ps:lang==='om'?(s.title_om||s.title_en):isTR?s.title_tr:isEN?s.title_en:isZH?(s.title_zh||s.title_en):s.title_nl;
    const desc=lang==='ar'?s.desc_ar:lang==='ps'?s.desc_ps:lang==='om'?(s.desc_om||s.desc_en):isTR?s.desc_tr:isEN?s.desc_en:isZH?(s.desc_zh||s.desc_en):s.desc_nl;
    box.innerHTML=`<div class="voice-step-emoji">${s.emoji}</div><div class="voice-step-content"><div class="voice-step-title">${i+1}. ${title}</div><div class="voice-step-desc">${desc}</div></div>`;
    wrap.appendChild(box);
  });
  c.appendChild(wrap);
  const waBtn=document.createElement('button'); waBtn.className='wa-btn';
  waBtn.innerHTML=`📲 ${isNL?'Open WhatsApp — stuur voice memo naar docent':isEN?'Open WhatsApp — send voice memo to teacher':isTR?'WhatsApp\'ı aç — sesli mesaj gönder':lang==='ps'?'واټس اپ پرانيزه — ښوونکي ته غږیز پیغام ولېږه':lang==='om'?'WhatsApp banii — ergaa sagalee barsiisaatti ergi':lang==='zh'?'打开WhatsApp — 发送语音给老师':'افتح واتساب — أرسل رسالة صوتية'}`;
  waBtn.onclick=()=>{
    const msg=isNL?'Hallo docent! Ik stuur nu mijn voice memo van thema 8.1 ⭐⭐ 🎤':isEN?'Hello teacher! Sending my voice memo for theme 8.1 ⭐⭐ 🎤':isTR?'Merhaba öğretmenim! Tema 8.1 sesli mesajımı gönderiyorum 🎤':lang==='ps'?'سلام ښوونکی! د موضوع 8.1 غږیز پیغام لېږم 🎤':lang==='om'?'Akkam barsiisaa! Ergaa sagalee mata duree 8.1 ⭐⭐ ergaa jira 🎤':lang==='zh'?'老师您好！发给您主题8.1的语音消息 ⭐⭐ 🎤':'مرحباً أستاذ! سأرسل تسجيلي الصوتي للموضوع 8.1 ⭐⭐ 🎤';
    window.open(`https://wa.me/${TEACHER_WA}?text=${encodeURIComponent(msg)}`,'_blank');
  };
  c.appendChild(waBtn);
}

// ── LEARNED WORDS ───────────────────────────────────────────────────
function buildLearnedWords(){
  const c=document.getElementById('learned-words-list');
  c.innerHTML=wordsData.map(w=>{
    let trans='';
    if(lang==='en') trans=w.en;
    else if(lang==='tr') trans=w.tr;
    else if(lang==='ar') trans=w.ar;
    else if(lang==='om') trans=w.om;
    else if(lang==='ps') trans=w.ps;
    else if(lang==='zh') trans=w.zh;
    return `<div class="learned-word"><span>${w.emoji} ${w.nl}</span>${trans?`<span class="learned-word-en">${trans}</span>`:''}</div>`;
  }).join('');
}

// ── TEXTS ───────────────────────────────────────────────────────────
const textMap={
  's1-num':'s1num','s1-title':'s1title','s1-desc':'s1desc',
  's2-num':'s2num','s2-title':'s2title','s2-desc':'s2desc','s2-info':'s2info',
  's3b-num':'s3b_num','s3b-title':'s3b_title','s3b-desc':'s3b_desc',
  's3-num':'s3num','s3-title':'s3title','s3-desc':'s3desc',
  's4-num':'s4num','s4-title':'s4title','s4-desc':'s4desc',
  's5-num':'s5num','s5-title':'s5title','s5-desc':'s5desc',
  's6-num':'s6num','s6-title':'s6title','s6-desc':'s6desc',
  's7-num':'s7num','s7-title':'s7title','s7-desc':'s7desc',
  's8-num':'s8num','s8-title':'s8title','s8-desc':'s8desc',
  's9-num':'s9num','s9-title':'s9title','s9-desc':'s9desc',
  's10-num':'s10num','s10-title':'s10title','s10-desc':'s10desc',
  's11-num':'s11num','s11-title':'s11title','s11-desc':'s11desc',
  's12-num':'s12num','s12-title':'s12title','s12-desc':'s12desc',
  'sg-title':'sgTitle','sg1':'sg1','sg2':'sg2','sg3':'sg3','sg4':'sg4','sg5':'sg5',
  'congrats-title':'congratsTitle','congrats-sub':'congratsSub','learned-title':'learnedTitle',
  'btn-restart':'restart','ftlabel':'ftlabel','fthint':'fthint',
  'wa-free-text':'waFree','wa-conv-text':'waConv',
  'progress-label-text':'progress',
};

const nextLabels={
  's1-next':'Volgende stap →','s3b-next':'Volgende stap →','s2-next':'Volgende →','s3-next':'Volgende stap →',
  's4-next':'Volgende stap →','s5-next':'Volgende stap →','s6-next':'Volgende stap →',
  's7-next':'Volgende stap →','s8-next':'Volgende stap →','s9-next':'Volgende stap →',
  's10-next':'Volgende stap →','s11-next':'Volgende stap →',
};
const nextLabelsOther={
  's1-next':'→','s3b-next':'→','s2-next':'→','s3-next':'→',
  's4-next':'→','s5-next':'→','s6-next':'→',
  's7-next':'→','s8-next':'→','s9-next':'→',
  's10-next':'→','s11-next':'→',
};


function updateTexts(){
  if (!window.T_adjusted) {
    Object.keys(T).forEach(l => {
      Object.keys(T[l]).forEach(k => {
        if(k.match(/num$/)) {
          let str = T[l][k].replace(/13/g, '15');
          str = str.replace(/\d+/, m => {
             let n = parseInt(m);
             return (n >= 5 && n <= 13) ? (n + 2) : n;
          });
          T[l][k] = str;
        }
      });
      T[l]['s4anum'] = T[l]['s3num'].replace(/\d+/, '4'); 
      T[l]['s4bnum'] = T[l]['s3num'].replace(/\d+/, '5');
      T[l]['s4cnum'] = T[l]['s3num'].replace(/\d+/, '6');
    });
    window.T_adjusted = true;
  }

  for(const [id,key] of Object.entries(textMap)){
    const el=document.getElementById(id); if(!el) continue;
    const val=T[lang]?.[key]||'';
    if(val) el.innerHTML=val;
  }
  const labels=lang==='nl'?nextLabels:nextLabelsOther;
  for(const id of Object.keys(labels)){
    const el=document.getElementById(id); if(!el) continue;
    if(lang==='nl'){ el.textContent=labels[id]; continue; }
    const nxt=lang==='en'?'Next step →':lang==='tr'?'Sonraki adım →':lang==='ps'?'بل ګام →':lang==='om'?'Tarkaanfii itti aanu →':lang==='zh'?'下一步 →':'الخطوة التالية →';
    el.textContent=nxt;
  }
}

// ── NAV SEPARATORS ──────────────────────────────────────────────────
function addNavSeparators(){
  document.querySelectorAll('.nav-separator').forEach(el=>el.remove());
  const sepText=lang==='nl'?'── ✅ Klaar met deze oefening? Ga dan naar de volgende stap ──':lang==='en'?'── ✅ Done with this exercise? Go to the next step ──':lang==='tr'?'── ✅ Bu alıştırmayı bitirdin mi? Sonraki adıma geç ──':lang==='ar'?'── ✅ انتهيت من هذا التمرين؟ انتقل للخطوة التالية ──':lang==='om'?'── ✅ Shaakala kana xumurte? Tarkaanfii itti aanutti darbi ──':lang==='ps'?'── ✅ دا تمرین پای ته رسې؟ بل ګام ته لاړ شه ──':lang==='zh'?'── ✅ 完成这个练习了吗？进入下一步 ──':'── ✅ Done? Next step ──';
  document.querySelectorAll('.nav-area').forEach(nav=>{
    const sep=document.createElement('div'); sep.className='nav-separator';
    sep.textContent=sepText;
    nav.parentElement.insertBefore(sep,nav);
  });
}

// ── REBUILD ─────────────────────────────────────────────────────────
function rebuildAll(){
  buildWordGrid(); buildRepeatGrid(); renderDrill();
  buildSort(); buildConv(); renderQ5a(); renderQ5b();
  buildWriteQuestions(); buildConvFill(); buildPairWork(); buildVoiceMemo();
  buildLearnedWords(); updateTexts(); updateProgress(); addNavSeparators();
}

// ── RESTART ─────────────────────────────────────────────────────────
function restartAll(){
  initCopyDrill(); initDrill(); initSort(); initConv(); initQ5a(); initQ5b();
  buildConvFill(); buildPairWork(); buildVoiceMemo();
  buildWordGrid(); buildRepeatGrid(); buildWriteQuestions();
  buildLearnedWords(); updateTexts(); addNavSeparators(); goTo(1);
}

// ── INIT ────────────────────────────────────────────────────────────
initCopyDrill(); initDrill(); initSort(); initConv(); initQ5a(); initQ5b();
buildWordGrid(); buildRepeatGrid(); buildWriteQuestions();
buildConvFill(); buildPairWork(); buildVoiceMemo();
buildLearnedWords(); updateTexts(); buildDots(); addNavSeparators();
