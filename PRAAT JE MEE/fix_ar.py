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
    
    # Update dict values in T using regex
    def replace_t_key(lang_key, dict_key, new_val):
        nonlocal html
        pattern = rf"({lang_key}:{{.*?){dict_key}:'.*?',(.*?}})"
        # Some are separated by commas or at the end
        # A safer approach is to regex sub specifically for those keys.
        pass

    # Actually, a simpler way to change T is just doing direct replace of the exact lines since I know exactly what they look like in the files!
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
    # First, let's prepare the sg strings for the right star level
    if starlvl == 1:
        sg_nl = "sg1:'Begroet de medewerker',sg2:'Zeg wat je zoekt',sg3:'Kies een kleur',sg4:'Reageer op het kledingstuk',sg5:'Sluit het gesprek af',"
        sg_en = "sg1:'Greet the employee',sg2:'Say what you are looking for',sg3:'Choose a colour',sg4:'React to the clothing item',sg5:'Close the conversation',"
        sg_ar = "sg1:'حيّ الموظف',sg2:'قل ما تبحث عنه',sg3:'اختر لوناً',sg4:'تفاعل مع قطعة الملابس',sg5:'أنهِ المحادثة',"
    elif starlvl == 2:
        sg_nl = r"""sg1:'Vertel wat oud is: \"Mijn … is oud.\"',sg2:'Zeg wat je wil: \"Ik wil graag een nieuwe …\"',sg3:'Kies een kleur als de medewerker vraagt',sg4:'Reageer op het aanbod',sg5:'Sluit af: \"Dank u. Tot ziens.\"',"""
        sg_en = r"""sg1:'Tell what is old: \"Mijn … is oud.\"',sg2:'Say what you want: \"Ik wil graag een nieuwe …\"',sg3:'Choose a colour when asked',sg4:'React to the offer',sg5:'Close: \"Dank u. Tot ziens.\"',"""
        sg_ar = r"""sg1:'أخبر ما هو القديم: \"Mijn … is oud.\"',sg2:'قل ما تريده: \"Ik wil graag een nieuwe …\"',sg3:'اختر لوناً عندما يُطلب منك',sg4:'تفاعل مع العرض',sg5:'أنهِ المحادثة: \"Dank u. Tot ziens.\"',"""
    else: # 3
        sg_nl = r"""sg1:'Vraag toestemming: \"Mag ik iets vragen?\"',sg2:'Vraag naar maat of kleur',sg3:'Reageer op het antwoord van de medewerker',sg4:'Bestel als nodig: \"Kunt u ze bestellen?\"',sg5:'Sluit af: \"Heel fijn. Dank u wel. Tot ziens.\"',"""
        sg_en = r"""sg1:'Ask permission: \"Mag ik iets vragen?\"',sg2:'Ask about size or colour',sg3:'React to the employee\\'s answer',sg4:'Order if necessary: \"Kunt u ze bestellen?\"',sg5:'Close: \"Heel fijn. Dank u wel. Tot ziens.\"',"""
        sg_ar = r"""sg1:'اطلب الإذن: \"Mag ik iets vragen?\"',sg2:'اسأل عن المقاس أو اللون',sg3:'تفاعل مع إجابة الموظف',sg4:'اطلب إذا لزم الأمر: \"Kunt u ze bestellen?\"',sg5:'أنهِ المحادثة: \"Heel fijn. Dank u wel. Tot ziens.\"',"""

    # We replace the existing sg1..sg5 lines:
    html = re.sub(r"sg1:'حيّ الشخص',sg2:'قل من أنت',sg3:'قل من أين أنت',sg4:'اسأل من هو الشخص الآخر',sg5:'أنهِ المحادثة',", sg_ar, html)
    html = re.sub(r"sg1:'Begroet de winkelmedewerker',sg2:'Zeg wat je zoekt',sg3:'Vraag naar kleur of maat',sg4:'Reageer op het antwoord',sg5:'Sluit het gesprek beleefd af',", sg_nl, html)
    html = re.sub(r"sg1:'Greet the store employee',sg2:'Say what you are looking for',sg3:'Ask about color or size',sg4:'React to the answer',sg5:'Close the conversation politely',", sg_en, html)
    # Also for 1ster it was old thema-1-1 values for en and nl:
    html = re.sub(r"sg1:'Begroet de persoon',sg2:'Zeg wie jij bent',sg3:'Zeg waar jij vandaan komt',sg4:'Vraag wie de ander is',sg5:'Sluit het gesprek af',", sg_nl, html)
    html = re.sub(r"sg1:'Greet the person',sg2:'Say who you are',sg3:'Say where you are from',sg4:'Ask who the other person is',sg5:'Close the conversation',", sg_en, html)
    

    # --- 3. Fix renderDrill AR fallback logic ---

    # modes
    old_modes = """  const modes=[
    {key:'mc_nl2en',   label:lang==='nl'?'Wat betekent dit?':'What does it mean?'},
    {key:'mc_en2nl',   label:lang==='nl'?'Hoe zeg je dit in NL?':'How to say in Dutch?'},
    {key:'write_en2nl',label:lang==='nl'?'Schrijf in het NL ✏️':'Write in Dutch ✏️'},
  ];"""
    new_modes = """  const modes=[
    {key:'mc_nl2en',   label:lang==='nl'?'Wat betekent dit?':lang==='ar'?'ماذا يعني هذا؟':'What does it mean?'},
    {key:'mc_en2nl',   label:lang==='nl'?'Hoe zeg je dit in NL?':lang==='ar'?'كيف تقول هذا بالهولندية؟':'How to say in Dutch?'},
    {key:'write_en2nl',label:lang==='nl'?'Schrijf in het NL ✏️':lang==='ar'?'اكتب بالهولندية ✏️':'Write in Dutch ✏️'},
  ];"""
    html = html.replace(old_modes, new_modes)

    # mode text variables
    old_mc_txt = """    const subNL2EN=lang==='nl'?'Wat betekent dit?':'What does this mean?';
    const subEN2NL=lang==='nl'?'Hoe zeg je dit in het Nederlands?':'How do you say this in Dutch?';"""
    new_mc_txt = """    const subNL2EN=lang==='nl'?'Wat betekent dit?':lang==='ar'?'ماذا يعني هذا؟':'What does this mean?';
    const subEN2NL=lang==='nl'?'Hoe zeg je dit in het Nederlands?':lang==='ar'?'كيف تقول هذا بالهولندية؟':'How do you say this in Dutch?';"""
    html = html.replace(old_mc_txt, new_mc_txt)

    old_wr_txt = """    const subLabel=lang==='nl'?'Schrijf dit in het Nederlands:':'Write this in Dutch:';"""
    new_wr_txt = """    const subLabel=lang==='nl'?'Schrijf dit in het Nederlands:':lang==='ar'?'اكتب هذا بالهولندية:':'Write this in Dutch:';"""
    html = html.replace(old_wr_txt, new_wr_txt)

    # question and answer dynamic keys
    old_qa = """    const isNL2EN=drillMode==='mc_nl2en';
    const question=isNL2EN?word.nl:word.en;
    const correctAnswer=isNL2EN?word.en:word.nl;
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>isNL2EN?w.en:w.nl);"""
    
    new_qa = """    const isNL2EN=drillMode==='mc_nl2en';
    const question=isNL2EN?word.nl:(lang==='ar'?word.ar:word.en);
    const correctAnswer=isNL2EN?(lang==='ar'?word.ar:word.en):word.nl;
    const distractors=shuffle(wordsData.filter((_,i)=>i!==wordIdx)).slice(0,2).map(w=>isNL2EN?(lang==='ar'?w.ar:w.en):w.nl);"""
    html = html.replace(old_qa, new_qa)

    # write mode dynamic key
    old_wr_qa = """    const question=word.en;
    const correctAnswer=word.nl.toLowerCase().trim();"""
    new_wr_qa = """    const question=lang==='ar'?word.ar:word.en;
    const correctAnswer=word.nl.toLowerCase().trim();"""
    html = html.replace(old_wr_qa, new_wr_qa)

    old_write_inp = """    inp.placeholder=lang==='nl'?'Schrijf hier in het Nederlands...':'Write in Dutch here...';"""
    new_write_inp = """    inp.placeholder=lang==='nl'?'Schrijf hier in het Nederlands...':lang==='ar'?'اكتب بالهولندية هنا...':'Write in Dutch here...';"""
    html = html.replace(old_write_inp, new_write_inp)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

for fpath, starlvl in files:
    patch_file(fpath, starlvl)
    print("Patched", fpath)

