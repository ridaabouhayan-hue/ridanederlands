import sys
import re

files = [
    (r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html", 1),
    (r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html", 2),
    (r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-3ster.html", 3)
]

def patch_file(fpath, starlvl):
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # --- 1. Fix Fill in sentences (Schrijf over jezelf) HTML ---
    html = html.replace('<div class="fill-sentence">Ik ben ___________.</div>', '<div class="fill-sentence">Ik zoek ___________.</div>')
    html = html.replace('<div class="fill-sentence">Ik kom uit ___________.</div>', '<div class="fill-sentence">Ik wil graag ___________.</div>')
    html = html.replace('<div class="fill-sentence">___________, ik ben ___________.</div>', '<div class="fill-sentence">Ik heb maat ___________.</div>')
    
    # For AR:
    html = html.replace("fill1label:'اسمك:',fill2label:'بلدك:',fill3label:'التحية + الاسم:',", "fill1label:'قطعة الملابس:',fill2label:'لونك المفضل:',fill3label:'مقاسك:',")
    html = html.replace("fill1hint:'💡 أنا أحمد.',fill2hint:'💡 أنا من المغرب.',fill3hint:'💡 ابدأ بـ: مرحباً أو صباح الخير',", "fill1hint:'💡 Ik zoek een trui.',fill2hint:'💡 Ik wil graag rood.',fill3hint:'💡 Ik heb maat 40.',")
    html = html.replace("ftlabel:'أخبر عن نفسك',", "ftlabel:'تحدث عن شراء الملابس',")
    html = html.replace("fthint:'📝 اكتب: من أنت، من أين أنت؟ واسأل الشخص الآخر أيضاً: من أنت ومن أين أنت؟',", "fthint:'📝 اكتب: ما الذي تبحث عنه، وما هو اللون والمقاس؟ واسأل الشخص الآخر: ما الذي تبحث عنه؟',")

    # For NL:
    html = html.replace("fill1label:'Jouw naam:',fill2label:'Jouw land:',fill3label:'Begroeting + naam:',", "fill1label:'Kledingstuk:',fill2label:'Jouw kleur:',fill3label:'Jouw maat:',")
    html = html.replace("fill1hint:'💡 Ik ben Ahmed.',fill2hint:'💡 Ik kom uit Marokko.',fill3hint:'💡 Begin met: Hallo of Goedemorgen',", "fill1hint:'💡 Ik zoek een trui.',fill2hint:'💡 Ik wil graag rood.',fill3hint:'💡 Ik heb maat 40.',")
    html = html.replace("ftlabel:'Vertel over jezelf',", "ftlabel:'Vertel over kleding kopen',")
    html = html.replace("fthint:'📝 Schrijf: wie ben jij, waar kom jij vandaan? Vraag ook aan de ander: wie ben jij en waar kom jij vandaan?',", "fthint:'📝 Schrijf: wat zoek je, welke kleur en welke maat? En vraag aan de ander: wat zoek jij?',")

    # For EN:
    html = html.replace("fill1label:'Your name:',fill2label:'Your country:',fill3label:'Greeting + name:',", "fill1label:'Clothing item:',fill2label:'Your colour:',fill3label:'Your size:',")
    html = html.replace("fill1hint:'💡 Ik ben Ahmed.',fill2hint:'💡 Ik kom uit Morocco.',fill3hint:'💡 Start with: Hallo or Goedemorgen',", "fill1hint:'💡 Ik zoek een trui.',fill2hint:'💡 Ik wil graag rood.',fill3hint:'💡 Ik heb maat 40.',")
    html = html.replace("ftlabel:'Tell about yourself',", "ftlabel:'Tell about buying clothes',")
    html = html.replace("fthint:'📝 Write: who are you, where do you come from? Also ask the other person: who are you and where do you come from?',", "fthint:'📝 Write: what are you looking for, what colour and what size? And ask the other person: what are you looking for?',")

    # --- 2. Fix Stappenplan (Step 12/sg keys) ---
    if starlvl == 1:
        sg_nl = "sg1:'Begroet de winkelmedewerker',sg2:'Zeg wat je zoekt',sg3:'Vraag naar kleur of maat',sg4:'Reageer op het antwoord',sg5:'Sluit het gesprek beleefd af',"
        sg_en = "sg1:'Greet the store employee',sg2:'Say what you are looking for',sg3:'Ask about color or size',sg4:'React to the answer',sg5:'Close the conversation politely',"
        sg_ar = "sg1:'حيّ الموظف',sg2:'قل ما تبحث عنه',sg3:'اسأل عن اللون أو الحجم',sg4:'تفاعل مع الإجابة',sg5:'أنهِ المحادثة بأدب',"
    elif starlvl == 2:
        sg_nl = r"""sg1:'Vertel wat oud is: \"Mijn … is oud.\"',sg2:'Zeg wat je wil: \"Ik wil graag een nieuwe …\"',sg3:'Kies een kleur als de medewerker vraagt',sg4:'Reageer op het aanbod',sg5:'Sluit af: \"Dank u. Tot ziens.\"',"""
        sg_en = r"""sg1:'Tell what is old: \"Mijn … is oud.\"',sg2:'Say what you want: \"Ik wil graag een nieuwe …\"',sg3:'Choose a colour when asked',sg4:'React to the offer',sg5:'Close: \"Dank u. Tot ziens.\"',"""
        sg_ar = r"""sg1:'أخبر ما هو القديم: \"Mijn … is oud.\"',sg2:'قل ما تريده: \"Ik wil graag een nieuwe …\"',sg3:'اختر لوناً عندما يُطلب منك',sg4:'تفاعل مع العرض',sg5:'أنهِ المحادثة: \"Dank u. Tot ziens.\"',"""
    else: # 3
        sg_nl = r"""sg1:'Vraag toestemming: \"Mag ik iets vragen?\"',sg2:'Vraag naar maat of kleur',sg3:'Reageer op het antwoord van de medewerker',sg4:'Bestel als nodig: \"Kunt u ze bestellen?\"',sg5:'Sluit af: \"Heel fijn. Dank u wel. Tot ziens.\"',"""
        sg_en = r"""sg1:'Ask permission: \"Mag ik iets vragen?\"',sg2:'Ask about size or colour',sg3:'React to the employee\\'s answer',sg4:'Order if necessary: \"Kunt u ze bestellen?\"',sg5:'Close: \"Heel fijn. Dank u wel. Tot ziens.\"',"""
        sg_ar = r"""sg1:'اطلب الإذن: \"Mag ik iets vragen?\"',sg2:'اسأل عن المقاس أو اللون',sg3:'تفاعل مع إجابة الموظف',sg4:'اطلب إذا لزم الأمر: \"Kunt u ze bestellen?\"',sg5:'أنهِ المحادثة: \"Heel fijn. Dank u wel. Tot ziens.\"',"""

    html = re.sub(r"sg1:'حيّ الشخص',sg2:'قل من أنت',sg3:'قل من أين أنت',sg4:'اسأل من هو الشخص الآخر',sg5:'أنهِ المحادثة',", sg_ar, html)
    html = re.sub(r"sg1:'Begroet de winkelmedewerker',sg2:'Zeg wat je zoekt',sg3:'Vraag naar kleur of maat',sg4:'Reageer op het antwoord',sg5:'Sluit het gesprek beleefd af',", sg_nl, html)
    html = re.sub(r"sg1:'Greet the store employee',sg2:'Say what you are looking for',sg3:'Ask about color or size',sg4:'React to the answer',sg5:'Close the conversation politely',", sg_en, html)
    # 1-ster had old values
    html = re.sub(r"sg1:'Begroet de persoon',sg2:'Zeg wie jij bent',sg3:'Zeg waar jij vandaan komt',sg4:'Vraag wie de ander is',sg5:'Sluit het gesprek af',", sg_nl, html)
    html = re.sub(r"sg1:'Greet the person',sg2:'Say who you are',sg3:'Say where you are from',sg4:'Ask who the other person is',sg5:'Close the conversation',", sg_en, html)
    
    # --- 3. Fix renderDrill AR fallback logic ---
    html = html.replace("""  const modes=[
    {key:'mc_nl2en',   label:lang==='nl'?'Wat betekent dit?':'What does it mean?'},
    {key:'mc_en2nl',   label:lang==='nl'?'Hoe zeg je dit in NL?':'How to say in Dutch?'},
    {key:'write_en2nl',label:lang==='nl'?'Schrijf in het NL ✏️':'Write in Dutch ✏️'},
  ];""", """  const modes=[
    {key:'mc_nl2en',   label:lang==='nl'?'Wat betekent dit?':lang==='ar'?'ماذا يعني هذا؟':'What does it mean?'},
    {key:'mc_en2nl',   label:lang==='nl'?'Hoe zeg je dit in NL?':lang==='ar'?'كيف تقول هذا بالهولندية؟':'How to say in Dutch?'},
    {key:'write_en2nl',label:lang==='nl'?'Schrijf in het NL ✏️':lang==='ar'?'اكتب بالهولندية ✏️':'Write in Dutch ✏️'},
  ];""")

    html = html.replace("""    const subNL2EN=lang==='nl'?'Wat betekent dit?':'What does this mean?';
    const subEN2NL=lang==='nl'?'Hoe zeg je dit in het Nederlands?':'How do you say this in Dutch?';""", """    const subNL2EN=lang==='nl'?'Wat betekent dit?':lang==='ar'?'ماذا يعني هذا؟':'What does this mean?';
    const subEN2NL=lang==='nl'?'Hoe zeg je dit in het Nederlands?':lang==='ar'?'كيف تقول هذا بالهولندية؟':'How do you say this in Dutch?';""")

    html = html.replace("""    const subLabel=lang==='nl'?'Schrijf dit in het Nederlands:':'Write this in Dutch:';""", """    const subLabel=lang==='nl'?'Schrijf dit in het Nederlands:':lang==='ar'?'اكتب هذا بالهولندية:':'Write this in Dutch:';""")

    html = html.replace("""    const isNL2EN=drillMode==='mc_nl2en';
    const question=isNL2EN?word.nl:word.en;
    const correctAnswer=isNL2EN?word.en:word.nl;
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>isNL2EN?w.en:w.nl);""", """    const isNL2EN=drillMode==='mc_nl2en';
    const question=isNL2EN?word.nl:(lang==='ar'?word.ar:word.en);
    const correctAnswer=isNL2EN?(lang==='ar'?word.ar:word.en):word.nl;
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>isNL2EN?(lang==='ar'?w.ar:w.en):w.nl);""")

    html = html.replace("""    const question=word.en;
    const correctAnswer=word.nl.toLowerCase().trim();""", """    const question=lang==='ar'?word.ar:word.en;
    const correctAnswer=word.nl.toLowerCase().trim();""")

    html = html.replace("""    inp.placeholder=lang==='nl'?'Schrijf hier in het Nederlands...':'Write in Dutch here...';""", """    inp.placeholder=lang==='nl'?'Schrijf hier in het Nederlands...':lang==='ar'?'اكتب بالهولندية هنا...':'Write in Dutch here...';""")

    # --- 4. Fix renderCopyDrill ---
    html = html.replace("""+(isEN?'Copy this sentence exactly:':'Schrijf deze zin precies over:')+""", """+(lang==='en'?'Copy this sentence exactly:':(lang==='ar'?'انسخ هذه الجملة بالضبط:':'Schrijf deze zin precies over:'))+""")
    html = html.replace("""inp.placeholder = isEN ? 'Type exactly what you see above...' : 'Schrijf exact hetzelfde over...';""", """inp.placeholder = lang==='en' ? 'Type exactly what you see above...' : (lang==='ar'?'اكتب بالضبط ما تراه أعلاه...':'Schrijf exact hetzelfde over...');""")
    html = html.replace("""hint.textContent = isEN ? '💡 Capital letter at start. End with . or ?' : '💡 Begin met een hoofdletter. Eindig met . of ?';""", """hint.textContent = lang==='en' ? '💡 Capital letter at start. End with . or ?' : (lang==='ar'?'💡 ابدأ بحرف كبير. وانهِ بـ . أو ؟':'💡 Begin met een hoofdletter. Eindig met . of ?');""")
    html = html.replace("""msg = isEN ? '❌ Almost! Check capital letters and punctuation.' : '❌ Bijna! Let op hoofdletters en leestekens.';""", """msg = lang==='en' ? '❌ Almost! Check capital letters and punctuation.' : (lang==='ar'?'❌ تقريباً! تحقق من الأحرف الكبيرة وعلامات الترقيم.':'❌ Bijna! Let op hoofdletters en leestekens.');""")
    html = html.replace("""msg = (isEN ? '❌ Not the same. Try again: ' : '❌ Niet hetzelfde. Probeer opnieuw: ') + phrase;""", """msg = (lang==='en' ? '❌ Not the same. Try again: ' : (lang==='ar'?'❌ ليست نفسها. حاول مرة أخرى: ':'❌ Niet hetzelfde. Probeer opnieuw: ')) + phrase;""")

    # --- 5. Fix buildVoiceMemo steps ---
    voice_memo_old = """    {
      emoji:'🗣️',
      title_nl:'Oefen het gesprek eerst samen',
      title_en:'Practise the conversation together first',
      desc_nl:'Spreek het gesprek samen door. Probeer zo natuurlijk mogelijk te klinken — niet voorlezen, maar echt praten! Oefen 1 of 2 keer voordat je opneemt.',
      desc_en:'Speak the conversation together. Try to sound as natural as possible — don\\'t read it, really talk! Practise 1 or 2 times before recording.',
      example_nl:'💡 A zegt: "Hallo!" → B: "Hallo! Welkom!" → A: "Ik ben [naam]..." enzovoort.',
      example_en:'💡 A says: "Hallo!" → B: "Hallo! Welkom!" → A: "Ik ben [naam]..." and so on.',
    },
    {
      emoji:'🤳',
      title_nl:'Open WhatsApp',
      title_en:'Open WhatsApp',
      desc_nl:'Open WhatsApp op jouw telefoon. Ga naar het gesprek met de docent.',
      desc_en:'Open WhatsApp on your phone. Go to the conversation with the teacher.',
      example: null,
    },
    {
      emoji:'🎙️',
      title_nl:'Houd de microfoon knop ingedrukt',
      title_en:'Hold down the microphone button',
      desc_nl:'In WhatsApp: houd de 🎙️ knop ingedrukt. Voer het gesprek samen. Laat los als je klaar bent.',
      desc_en:'In WhatsApp: hold down the 🎙️ button. Do the conversation together. Release when finished.',
      example_nl:'Jij zegt: "Hallo, ik ben [naam]. Ik kom uit [land]." — Je partner vraagt en antwoordt ook.',
      example_en:'You say: "Hallo, ik ben [naam]. Ik kom uit [land]." — Your partner also asks and answers.',
    },
    {
      emoji:'📤',
      title_nl:'Stuur de opname',
      title_en:'Send the recording',
      desc_nl:'Laat de knop los en druk op "Stuur". De docent ontvangt de opname.',
      desc_en:'Release the button and press "Send". The teacher will receive the recording.',
      example: null,
    },"""

    voice_memo_new = """    {
      emoji:'🗣️',
      title_nl:'Oefen het gesprek eerst samen',
      title_en:'Practise the conversation together first',
      title_ar:'تدربا على المحادثة معاً أولاً',
      desc_nl:'Spreek het gesprek samen door. Probeer zo natuurlijk mogelijk te klinken — niet voorlezen, maar echt praten! Oefen 1 of 2 keer voordat je opneemt.',
      desc_en:'Speak the conversation together. Try to sound as natural as possible — don\\'t read it, really talk! Practise 1 or 2 times before recording.',
      desc_ar:'تحدثا المحادثة معاً. حاول أن تبدو طبيعياً قدر الإمكان — لا تقرأ، بل تحدث حقاً! تدرب مرة أو مرتين قبل التسجيل.',
      example_nl:'💡 A zegt: "Hallo!" → B: "Hallo! Welkom!" → A: "Ik ben [naam]..." enzovoort.',
      example_en:'💡 A says: "Hallo!" → B: "Hallo! Welkom!" → A: "Ik ben [naam]..." and so on.',
      example_ar:'💡 أ يقول: "Hallo!" → ب: "Hallo! Welkom!" → أ: "Ik ben [naam]..." وهكذا.',
    },
    {
      emoji:'🤳',
      title_nl:'Open WhatsApp',
      title_en:'Open WhatsApp',
      title_ar:'افتح واتساب',
      desc_nl:'Open WhatsApp op jouw telefoon. Ga naar het gesprek met de docent.',
      desc_en:'Open WhatsApp on your phone. Go to the conversation with the teacher.',
      desc_ar:'افتح واتساب على هاتفك. اذهب إلى المحادثة مع المعلم.',
      example: null,
    },
    {
      emoji:'🎙️',
      title_nl:'Houd de microfoon knop ingedrukt',
      title_en:'Hold down the microphone button',
      title_ar:'اضغط مع الاستمرار على زر الميكروفون',
      desc_nl:'In WhatsApp: houd de 🎙️ knop ingedrukt. Voer het gesprek samen. Laat los als je klaar bent.',
      desc_en:'In WhatsApp: hold down the 🎙️ button. Do the conversation together. Release when finished.',
      desc_ar:'في واتساب: اضغط مع الاستمرار على زر 🎙️. أجرِ المحادثة معاً. أفلت الزر عند الانتهاء.',
      example_nl:'Jij zegt: "Ik zoek een trui." — Je partner reageert als winkelmedewerker.',
      example_en:'You say: "Ik zoek een trui." — Your partner responds as store employee.',
      example_ar:'أنت تقول: "Ik zoek een trui." — ويرد شريكك كموظف متجر.',
    },
    {
      emoji:'📤',
      title_nl:'Stuur de opname',
      title_en:'Send the recording',
      title_ar:'أرسل التسجيل',
      desc_nl:'Laat de knop los en druk op "Stuur". De docent ontvangt de opname.',
      desc_en:'Release the button and press "Send". The teacher will receive the recording.',
      desc_ar:'أفلت الزر واضغط على "إرسال". سيتلقى المعلم التسجيل.',
      example: null,
    },"""

    html = html.replace(voice_memo_old, voice_memo_new)
    
    # And update HTML constructor for voice steps
    html = html.replace("""const example=isEN?(s.example_en||s.example):(s.example_nl||s.example);""", """const example=lang==='ar'?(s.example_ar||s.example):lang==='en'?(s.example_en||s.example):(s.example_nl||s.example);""")
    html = html.replace("""<div class="voice-step-title">${i+1}. ${isEN?s.title_en:s.title_nl}</div>""", """<div class="voice-step-title">${i+1}. ${lang==='ar'?s.title_ar:lang==='en'?s.title_en:s.title_nl}</div>""")
    html = html.replace("""<div class="voice-step-desc">${isEN?s.desc_en:s.desc_nl}</div>""", """<div class="voice-step-desc">${lang==='ar'?s.desc_ar:lang==='en'?s.desc_en:s.desc_nl}</div>""")

    # --- 6. waBtn in buildVoiceMemo ---
    html = html.replace("""waBtn.innerHTML=`📲 ${isEN?'Open WhatsApp — send voice memo to teacher':'Open WhatsApp — stuur voice memo naar docent'}`;""", """waBtn.innerHTML=`📲 ${lang==='ar'?'افتح واتساب — أرسل تسجيلاً صوتياً للمعلم':lang==='en'?'Open WhatsApp — send voice memo to teacher':'Open WhatsApp — stuur voice memo naar docent'}`;""")
    html = html.replace("""const msg=isEN?'Hello teacher! I will now send my voice memo for theme 1.1 ⭐ 🎤':'Hallo docent! Ik stuur nu mijn voice memo van thema 5.1 ⭐ 🎤';""", f"const msg=lang==='ar'?'مرحباً أستاذ! سأرسل تسجيلي الصوتي للموضوع 5.1 {starlvl*'*'} 🎤':lang==='en'?'Hello teacher! I will now send my voice memo for theme 5.1 {starlvl*'*'} 🎤':'Hallo docent! Ik stuur nu mijn voice memo van thema 5.1 {starlvl*'*'} 🎤';")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

for fpath, starlvl in files:
    patch_file(fpath, starlvl)
    print("Patched", fpath)

