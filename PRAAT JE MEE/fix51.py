import re
import os

base_file = r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html"

with open(base_file, 'r', encoding='utf-8') as f:
    base_html = f.read()

def apply_common_fixes(html):
    # Fix 4: Add AR button next to EN
    html = html.replace(
        '<button class="lang-btn" id="btn-en" onclick="setLang(\'en\')">🇬🇧 EN</button>',
        '<button class="lang-btn" id="btn-en" onclick="setLang(\'en\')">🇬🇧 EN</button>\n    <button class="lang-btn" id="btn-ar" onclick="setLang(\'ar\')">🇸🇦 AR</button>'
    )
    
    # Fix 4: setLang function
    setlang_old = """function setLang(l){
  lang=l;
  document.getElementById('btn-nl').classList.toggle('active-lang',l==='nl');
  document.getElementById('btn-en').classList.toggle('active-lang',l==='en');
  rebuildAll();
}"""
    setlang_new = """function setLang(l){
  lang = l;
  document.getElementById('btn-nl').classList.toggle('active-lang', l==='nl');
  document.getElementById('btn-en').classList.toggle('active-lang', l==='en');
  document.getElementById('btn-ar').classList.toggle('active-lang', l==='ar');
  document.body.setAttribute('dir', l==='ar' ? 'rtl' : 'ltr');
  rebuildAll();
}"""
    html = html.replace(setlang_old, setlang_new)
    # in case my old script had slightly different spacing:
    html = re.sub(
        r"function setLang\(l\)\{.*?rebuildAll\(\);\s*\}",
        setlang_new,
        html,
        flags=re.DOTALL
    )

    # Fix 4: buildWordGrid updates
    wordgrid_old = """    card.innerHTML=`<div class="word-main-row"><div class="word-emoji">${w.emoji}</div><div><div class="word-nl">${w.nl}</div>${lang==='en'?`<div class="word-en">${w.en}</div>`:''}</div></div>${audioBtn(w.nl)}`;"""
    wordgrid_new = """    card.innerHTML=`
      <div class="word-main-row">
        <div class="word-emoji">${w.emoji}</div>
        <div>
          <div class="word-nl">${w.nl}</div>
          ${lang==='en'?`<div class="word-en">${w.en}</div>`:''}
          ${lang==='ar'?`<div class="word-en" style="font-family:Arial;direction:rtl;text-align:right;">${w.ar||''}</div>`:''}
        </div>
      </div>
      ${audioBtn(w.nl)}`;"""
    html = html.replace(wordgrid_old, wordgrid_new)

    # Fix 4: Add Arabic T translations
    t_ar = """
  ar:{
    progress:'التقدم',
    s1num:'الخطوة 1 من 13 · تعلم الكلمات',s1title:'انظر واقرأ الكلمات',s1desc:'اضغط على 🔊 لسماع الكلمة. ثم قلها بنفسك!',
    s2num:'الخطوة 2 من 13 · التكرار',s2title:'كرر بصوت عالٍ! 🗣️',s2desc:'اضغط على 🔊 وقل الجملة بصوت عالٍ. بقدر ما تريد!',
    s2info:'💡 كرر كل جملة 3 مرات على الأقل. كلما كان أكثر، كان أفضل!',
    s3b_num:'الخطوة 3 من 13 · انسخ الجمل',s3b_title:'انسخ الجملة ✏️',s3b_desc:'اكتب كل جملة بالضبط. انتبه إلى الأحرف الكبيرة والنقطة أو علامة الاستفهام!',
    s3num:'الخطوة 4 من 13 · تدريب الكلمات',s3title:'هل تعرف الكلمات؟ 🧠',s3desc:'تدرب على الكلمات. لا أخطاء! إذا أخطأت، ابدأ من جديد.',
    s4num:'الخطوة 5 من 13 · بناء الجمل',s4title:'ابنِ الجملة! 🧩',s4desc:'اضغط على الكلمات بالترتيب الصحيح.',
    s5num:'الخطوة 6 من 13 · ترتيب المحادثة',s5title:'ضع المحادثة في الترتيب الصحيح 💬',s5desc:'اضغط على جملة → ثم اضغط على المكان الصحيح.',
    s6num:'الخطوة 7 من 13 · اختر الجملة الصحيحة',s6title:'أي جملة صحيحة؟ ✅',s6desc:'اختر الجملة ذات ترتيب الكلمات الصحيح.',
    s7num:'الخطوة 8 من 13 · اختر الإجابة الصحيحة',s7title:'ما هي الإجابة الصحيحة؟ 🤔',s7desc:'شخص يسأل سؤالاً. اختر الإجابة الصحيحة.',
    s8num:'الخطوة 9 من 13 · اكتب عن نفسك',s8title:'اكتب عن نفسك ✍️',s8desc:'أكمل الجمل بمعلوماتك الخاصة.',
    fill1label:'اسمك:',fill2label:'بلدك:',fill3label:'التحية + الاسم:',
    fill1hint:'💡 أنا أحمد.',fill2hint:'💡 أنا من المغرب.',fill3hint:'💡 ابدأ بـ: مرحباً أو صباح الخير',
    ftlabel:'أخبر عن نفسك',
    fthint:'📝 اكتب: من أنت، من أين أنت؟ واسأل الشخص الآخر أيضاً: من أنت ومن أين أنت؟',
    waFill:'📲 أرسل جملي إلى المعلم',
    waFree:'🎤 أرسل نص + رسالة صوتية',
    waConv:'📲 أرسل هذه المحادثة إلى المعلم',
    s9num:'الخطوة 10 من 13 · املأ المحادثة',s9title:'أكمل المحادثة 📝',s9desc:'املأ ما تقوله. استخدم التلميح إذا احتجت إلى مساعدة.',
    s10num:'الخطوة 11 من 13 · تدرب مع زميل',s10title:'تدربا معاً! 👥',s10desc:'اجلس بجانب زميل. ستتدربان على محادثة معاً.',
    s11num:'الخطوة 12 من 13 · سجل وأرسل',s11title:'سجل المحادثة! 🎤',s11desc:'افعل هذا مع زميلك. أرسل التسجيل إلى المعلم.',
    s12num:'الخطوة 13 من 13 · محادثة حرة',s12title:'تحدث أمام الفصل! 🌟',s12desc:'الآن افعلها بنفسك، بدون مساعدة. أنت تستطيع فعلها!',
    sgTitle:'خطوة بخطوة',
    sg1:'حيّ الشخص',sg2:'قل من أنت',sg3:'قل من أين أنت',sg4:'اسأل من هو الشخص الآخر',sg5:'أنهِ المحادثة',
    congratsTitle:'أحسنت!',congratsSub:'لقد أكملت جميع الخطوات!',
    learnedTitle:'📚 الكلمات التي تعلمتها',restart:'↺ تدرب مرة أخرى',
    convOrderTitle:'ضع في الترتيب الصحيح',beginLabel:'ابدأ 🟢',endLabel:'نهاية 🔴',
    questionLabel:'سؤال:',
    convFillTitle:'املأ ما تقوله',
    waMsg:'مرحباً أستاذ! هذه جملي:\\n',
    waFreeMsg:'مرحباً أستاذ! هذا نصي:\\n',
    waVoiceTip:'\\n\\n🎤 سأرسل أيضاً رسالة صوتية!',
    drillCorrectMsg:'✅ صحيح! أحسنت!',drillWrongMsg:'❌ خطأ! ابدأ من جديد.',
    drillDoneMsg:'🎉 جميع الكلمات صحيحة! جرب وضعاً آخر.',
    drillScore:'صحيح:',drillReset:'↺ حاول مرة أخرى (ترتيب جديد)',
    checkBtn:'✓ تحقق',resetBtn:'↺ ابدأ من جديد',
    prevSentence:'السابق',nextSentence:'التالي',
  }"""
    html = re.sub(r"const T = \{", f"const T = {{{t_ar},", html)

    # fallback t() function
    html = html.replace("function t(k){ return T[lang][k]||k; }", "function t(k){ return T[lang][k] || T['en'][k] || k; }")

    # Fix 2: ✏️ button toggle in renderConvFill
    old_ex = """      const ex=document.createElement('div');
      ex.className='conv-hint';
      ex.style='color:var(--green);margin-top:2px;';
      ex.textContent='✏️ '+line.example;
      contentDiv.appendChild(ex);"""
    
    new_ex = """      const toggleBtn = document.createElement('button');
      toggleBtn.style = 'background:none;border:none;font-size:0.78rem;font-weight:800;color:var(--blue);cursor:pointer;padding:4px 0;font-family:Nunito,sans-serif;';
      toggleBtn.textContent = lang === 'en' ? '💡 Show example answer' : (lang === 'ar' ? '💡 إظهار مثال الإجابة' : '💡 Toon voorbeeldantwoord');
      const exDiv = document.createElement('div');
      exDiv.style = 'color:var(--green);font-size:0.82rem;font-weight:800;margin-top:3px;display:none;';
      exDiv.textContent = '✏️ ' + line.example;
      toggleBtn.onclick = () => {
        exDiv.style.display = exDiv.style.display === 'none' ? 'block' : 'none';
        let lblShow = lang === 'en' ? '💡 Show example answer' : (lang === 'ar' ? '💡 إظهار مثال الإجابة' : '💡 Toon voorbeeldantwoord');
        let lblHide = lang === 'en' ? '🙈 Hide' : (lang === 'ar' ? '🙈 إخفاء' : '🙈 Verberg');
        toggleBtn.textContent = exDiv.style.display === 'none' ? lblShow : lblHide;
      };
      contentDiv.appendChild(toggleBtn);
      contentDiv.appendChild(exDiv);"""
    
    html = re.sub(r"const ex=document\.createElement\('div'\);(.*?)contentDiv\.appendChild\(ex\);", new_ex, html, flags=re.DOTALL)

    # Also update hint logic for renderConvFill
    html = html.replace("const hint=lang==='en'?line.hint_en:line.hint_nl;", "const hint = lang==='ar' ? line.hint_ar : lang==='en' ? line.hint_en : line.hint_nl;")
    html = html.replace("hintDiv.textContent='💡 '+(lang==='en'?line.hint_en:line.hint_nl);", "hintDiv.textContent='💡 '+(lang==='ar' ? line.hint_ar : lang==='en'?line.hint_en:line.hint_nl);")
    
    return html

def create_1ster():
    html = apply_common_fixes(base_html)
    
    # 1. Update pairwork tasks
    # Replaces the generated pair work tasks in JS
    a_tasks_nl = ['1️⃣ Begroet de medewerker: "Goedemiddag!"', '2️⃣ Zeg dat je kijkt: "Nee, dank u. Ik kijk even."', '3️⃣ Vraag naar kleding: "Heeft u een trui voor mij?"', '4️⃣ Sluit af: "Bedankt. Tot ziens."']
    a_tasks_en = ['1️⃣ Greet the employee: "Goedemiddag!"', '2️⃣ Say you are looking: "Nee, dank u. Ik kijk even."', '3️⃣ Ask for clothing: "Heeft u een trui voor mij?"', '4️⃣ Close: "Bedankt. Tot ziens."']
    b_tasks_nl = ['1️⃣ Begroet de klant: "Goedemiddag. Kan ik u helpen?"', '2️⃣ Reageer: "Ja hoor." of "Sorry, die heb ik niet."', '3️⃣ Vraag door: "Welke kleur wilt u?"', '4️⃣ Sluit af: "Graag gedaan. Tot ziens."']
    b_tasks_en = ['1️⃣ Greet the customer: "Goedemiddag. Kan ik u helpen?"', '2️⃣ Respond: "Ja hoor." or "Sorry, die heb ik niet."', '3️⃣ Ask: "Welke kleur wilt u?"', '4️⃣ Close: "Graag gedaan. Tot ziens."']
    html = re.sub(r"const aTasks=isEN \? \[.*?\] : \[.*?\];", f"const aTasks=isEN ? {a_tasks_en} : {a_tasks_nl};", html)
    html = re.sub(r"const bTasks=isEN \? \[.*?\] : \[.*?\];", f"const bTasks=isEN ? {b_tasks_en} : {b_tasks_nl};", html)
    
    # wordsData with Arabic 1-ster
    words_data_new = """const wordsData = [
{nl:'Kan ik u helpen?', en:'Can I help you?', ar:'هل أستطيع مساعدتك؟', emoji:'🛍️'},
{nl:'de trui', en:'the sweater', ar:'السترة', emoji:'👕'},
{nl:'de broek', en:'the trousers', ar:'البنطلون', emoji:'👖'},
{nl:'de jas', en:'the coat/jacket', ar:'المعطف', emoji:'🧥'},
{nl:'klein', en:'small', ar:'صغير', emoji:'🔽'},
{nl:'groot', en:'big / large', ar:'كبير', emoji:'🔼'},
{nl:'Ik kijk even.', en:'I\\'m just looking.', ar:'أنا أتصفح فقط.', emoji:'👀'},
{nl:'Heeft u … ?', en:'Do you have … ?', ar:'هل لديك … ؟', emoji:'🤝'},
{nl:'Nee, dank u.', en:'No, thank you.', ar:'لا، شكراً.', emoji:'🙏'},
{nl:'Jammer.', en:'What a pity.', ar:'للأسف.', emoji:'😔'},
{nl:'Bedankt.', en:'Thank you.', ar:'شكراً.', emoji:'🙏'},
{nl:'Tot ziens.', en:'Goodbye.', ar:'مع السلامة.', emoji:'👋'},
];"""
    html = re.sub(r"const wordsData = \[\s*.*?\s*\];", words_data_new, html, flags=re.DOTALL)
    
    # Add hint_ar to convFillSets manually:
    html = html.replace("hint_nl:'Zeg dat je even rondkijkt', hint_en:'Say you are taking a look around'", "hint_nl:'Zeg dat je even rondkijkt', hint_en:'Say you are taking a look around', hint_ar:'قل أنك تتصفح'")
    html = html.replace("hint_nl:'Vraag naar een kledingstuk', hint_en:'Ask for a piece of clothing'", "hint_nl:'Vraag naar een kledingstuk', hint_en:'Ask for a piece of clothing', hint_ar:'اسأل عن قطعة ملابس'")
    html = html.replace("hint_nl:'Reageer en vraag iets anders', hint_en:'Respond and ask for something else'", "hint_nl:'Reageer en vraag iets anders', hint_en:'Respond and ask for something else', hint_ar:'تفعل واسأل عن شيء آخر'")
    html = html.replace("hint_nl:'Sluit het gesprek af', hint_en:'Close the conversation'", "hint_nl:'Sluit het gesprek af', hint_en:'Close the conversation', hint_ar:'أنهِ المحادثة'")
    
    html = html.replace("hint_nl:'Zeg wat je zoekt', hint_en:'Say what you are looking for'", "hint_nl:'Zeg wat je zoekt', hint_en:'Say what you are looking for', hint_ar:'قل ما تبحث عنه'")
    html = html.replace("hint_nl:'Noem een kleur', hint_en:'Name a colour'", "hint_nl:'Noem een kleur', hint_en:'Name a colour', hint_ar:'سمِّ لوناً'")
    html = html.replace("hint_nl:'Sluit af beleefd', hint_en:'Close politely'", "hint_nl:'Sluit af beleefd', hint_en:'Close politely', hint_ar:'أنهِ المحادثة بأدب'")
    
    html = html.replace("hint_nl:'Vraag toestemming', hint_en:'Ask for permission to speak'", "hint_nl:'Vraag toestemming', hint_en:'Ask for permission to speak', hint_ar:'اطلب الإذن'")
    html = html.replace("hint_nl:'Vraag naar de maat', hint_en:'Ask for the size'", "hint_nl:'Vraag naar de maat', hint_en:'Ask for the size', hint_ar:'اسأل عن المقاس'")
    html = html.replace("hint_nl:'Vraag of ze het kunnen bestellen', hint_en:'Ask if they can order it'", "hint_nl:'Vraag of ze het kunnen bestellen', hint_en:'Ask if they can order it', hint_ar:'اسأل إن كان بإمكانهم طلبه'")
    html = html.replace("hint_nl:'Reageer blij en sluit af', hint_en:'React happily and close'", "hint_nl:'Reageer blij en sluit af', hint_en:'React happily and close', hint_ar:'تفاعل بسعادة وأنهِ المحادثة'")
    
    with open(r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html", 'w', encoding='utf-8') as f:
         f.write(html)


def apply_stars_replacements(html, stars_str, title, wordsData, repeatPhrases, copyPhrases, sortBase, convSets, q5aBase, q5bBase, convFillSets, aTasks_nl, aTasks_en, bTasks_nl, bTasks_en, stappenplan_nl, stappenplan_en):
    # Change Title and topbar
    html = html.replace("Thema 5.1 ⭐ — Kleding", title)
    html = html.replace("Thema 5.1 ⭐", f"Thema 5.1 {stars_str}")
    html = html.replace("thema 5.1", f"thema 5.1") # keep lowercase

    # Data arrays
    html = re.sub(r"const wordsData = \[\s*.*?\s*\];", f"const wordsData = [{wordsData}];", html, flags=re.DOTALL)
    html = re.sub(r"const repeatPhrases = \[\s*.*?\s*\];", f"const repeatPhrases = [{repeatPhrases}];", html, flags=re.DOTALL)
    html = re.sub(r"const copyPhrases = \[\s*.*?\s*\];", f"const copyPhrases = [{copyPhrases}];", html, flags=re.DOTALL)
    html = re.sub(r"const sortExercisesBase = \[\s*.*?\s*\];", f"const sortExercisesBase = [{sortBase}];", html, flags=re.DOTALL)
    html = re.sub(r"const convSetsBase = \[\s*.*?\s*\];", f"const convSetsBase = [{convSets}];", html, flags=re.DOTALL)
    html = re.sub(r"const q5aBase = \[\s*.*?\s*\];", f"const q5aBase = [{q5aBase}];", html, flags=re.DOTALL)
    html = re.sub(r"const q5bBase = \[\s*.*?\s*\];", f"const q5bBase = [{q5bBase}];", html, flags=re.DOTALL)
    html = re.sub(r"const convFillSets = \[\s*.*?\s*\];", f"const convFillSets = [{convFillSets}];", html, flags=re.DOTALL)
    
    # Pair work tasks
    html = re.sub(r"const aTasks=isEN \? \[.*?\] : \[.*?\];", f"const aTasks=isEN ? {aTasks_en} : {aTasks_nl};", html)
    html = re.sub(r"const bTasks=isEN \? \[.*?\] : \[.*?\];", f"const bTasks=isEN ? {bTasks_en} : {bTasks_nl};", html)

    # Stappenplan replacement (vrij gesprek)
    # Rebuilding the HTML block for steps instead of regex string replace.
    speech_guide = f"""<div class="speech-guide">
    <div class="speech-guide-title" id="sg-title">Stappenplan</div>
    <div class="speech-step"><div class="speech-step-icon">1️⃣</div><div><div class="speech-step-text" id="sg1">{stappenplan_nl[0]}</div><div class="speech-step-example"></div></div></div>
    <div class="speech-step"><div class="speech-step-icon">2️⃣</div><div><div class="speech-step-text" id="sg2">{stappenplan_nl[1]}</div><div class="speech-step-example"></div></div></div>
    <div class="speech-step"><div class="speech-step-icon">3️⃣</div><div><div class="speech-step-text" id="sg3">{stappenplan_nl[2]}</div><div class="speech-step-example"></div></div></div>
    <div class="speech-step"><div class="speech-step-icon">4️⃣</div><div><div class="speech-step-text" id="sg4">{stappenplan_nl[3]}</div><div class="speech-step-example"></div></div></div>
    <div class="speech-step"><div class="speech-step-icon">5️⃣</div><div><div class="speech-step-text" id="sg5">{stappenplan_nl[4]}</div><div class="speech-step-example"></div></div></div>
  </div>"""

    html = re.sub(r'<div class="speech-guide">.*?</div>\s*<div class="congrats-wrap">', speech_guide + '\n  <div class="congrats-wrap">', html, flags=re.DOTALL)
    return html

def create_2ster():
    html = apply_common_fixes(base_html)

    wordsData = """
{nl:'de kleur', en:'the colour', ar:'اللون', emoji:'🎨'},
{nl:'de bril', en:'the glasses', ar:'النظارات', emoji:'👓'},
{nl:'oud', en:'old', ar:'قديم', emoji:'⏳'},
{nl:'nieuw', en:'new', ar:'جديد', emoji:'✨'},
{nl:'rood', en:'red', ar:'أحمر', emoji:'🔴'},
{nl:'paars', en:'purple', ar:'أرجواني', emoji:'🟣'},
{nl:'geel', en:'yellow', ar:'أصفر', emoji:'🟡'},
{nl:'blauw', en:'blue', ar:'أزرق', emoji:'🔵'},
{nl:'oranje', en:'orange', ar:'برتقالي', emoji:'🟠'},
{nl:'groen', en:'green', ar:'أخضر', emoji:'🟢'},
{nl:'roze', en:'pink', ar:'وردي', emoji:'🌸'},
{nl:'Ik wil graag …', en:'I would like …', ar:'أريد أن …', emoji:'😊'},
{nl:'Welke kleur wilt u?', en:'What colour would you like?', ar:'ما اللون الذي تريده؟', emoji:'🎨'},
{nl:'Wat vindt u hiervan?', en:'What do you think of this?', ar:'ما رأيك في هذا؟', emoji:'🤔'}
"""
    repeatPhrases = """
{nl:'Mijn bril is oud. Ik wil graag een nieuwe bril.', emoji:'👓'},
{nl:'Welke kleur wilt u?', emoji:'🎨'},
{nl:'Ik vind rood niet mooi.', emoji:'🔴'},
{nl:'Paars is mooi.', emoji:'🟣'},
{nl:'Heeft u een gele bril?', emoji:'🟡'},
{nl:'Ik heb wel een blauwe bril.', emoji:'🔵'},
{nl:'Dat is een mooie bril.', emoji:'😊'}
"""
    copyPhrases = """
'Mijn bril is oud. Ik wil graag een nieuwe bril.',
'Welke kleur wilt u?',
'Ik vind rood niet mooi.',
'Paars is mooi.',
'Heeft u een gele bril?',
'Ik heb wel een blauwe bril.',
'Dat is een mooie bril.'
"""
    sortBase = """
{words:['bril','een','wil','Ik','graag','nieuwe','.'], answer:'Ik wil graag een nieuwe bril .'},
{words:['kleur','Welke','u','wilt','?'], answer:'Welke kleur wilt u ?'},
{words:['niet','rood','vind','Ik','mooi','.'], answer:'Ik vind rood niet mooi .'},
{words:['gele','Heeft','bril','u','een','?'], answer:'Heeft u een gele bril ?'},
{words:['blauwe','heb','bril','Ik','een','wel','.'], answer:'Ik heb wel een blauwe bril .'}
"""
    convSets = """
  {label:'Gesprek 1', lines:[
    {speaker:'Medewerker', text:'Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Mijn bril is oud. Ik wil graag een nieuwe bril.'},
    {speaker:'Medewerker', text:'Dat kan. Welke kleur wilt u?'},
    {speaker:'Klant', text:'Paars. Paars is mooi.'},
    {speaker:'Medewerker', text:'Alstublieft. Wat vindt u hiervan?'},
    {speaker:'Klant', text:'Nee, ik vind paars niet mooi.'},
    {speaker:'Medewerker', text:'Ik heb wel een blauwe bril.'},
    {speaker:'Klant', text:'Ja, dat is een mooie bril!'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Ik zoek een rode trui.'},
    {speaker:'Medewerker', text:'Een rode trui. Welke maat?'},
    {speaker:'Klant', text:'Klein.'},
    {speaker:'Medewerker', text:'Alstublieft.'},
    {speaker:'Klant', text:'Hmm, ik vind rood niet mooi.'},
    {speaker:'Medewerker', text:'Ik heb ook een groene trui.'},
    {speaker:'Klant', text:'Groen is mooi! Dank u.'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Medewerker', text:'Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Ik zoek een blauwe jas.'},
    {speaker:'Medewerker', text:'Klein of groot?'},
    {speaker:'Klant', text:'Klein.'},
    {speaker:'Medewerker', text:'Sorry, ik heb geen kleine blauwe jas.'},
    {speaker:'Klant', text:'Heeft u een groene jas?'},
    {speaker:'Medewerker', text:'Ja hoor. Alstublieft.'},
    {speaker:'Klant', text:'Mooi! Dank u.'},
  ]},
  {label:'Gesprek 4', lines:[
    {speaker:'Klant', text:'Ik wil graag een nieuwe bril.'},
    {speaker:'Medewerker', text:'Welke kleur wilt u?'},
    {speaker:'Klant', text:'Geel.'},
    {speaker:'Medewerker', text:'Geel? Nee, ik heb geen gele bril.'},
    {speaker:'Klant', text:'En oranje?'},
    {speaker:'Medewerker', text:'Oranje ook niet.'},
    {speaker:'Klant', text:'En roze?'},
    {speaker:'Medewerker', text:'Ja, een roze bril. Alstublieft.'},
  ]},
  {label:'Gesprek 5', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Ja. Mijn broek is oud. Ik wil een nieuwe broek.'},
    {speaker:'Medewerker', text:'Welke kleur?'},
    {speaker:'Klant', text:'Blauw.'},
    {speaker:'Medewerker', text:'Een blauwe broek. Klein of groot?'},
    {speaker:'Klant', text:'Groot.'},
    {speaker:'Medewerker', text:'Alstublieft.'},
    {speaker:'Klant', text:'Mooi. Dank u.'},
  ]}
"""
    q5aBase = """
{prompt:'Mijn bril is oud. Ik wil graag …', options:[
  {text:'een nieuwe bril.', correct:true},
  {text:'bril nieuwe een.', correct:false},
  {text:'nieuwe een bril.', correct:false},
]},
{prompt:'Welke kleur wilt u?', options:[
  {text:'Ik wil blauw.', correct:false},
  {text:'Blauw wil ik.', correct:false},
  {text:'Paars. Paars is mooi.', correct:true},
]},
{prompt:'Ik vind rood …', options:[
  {text:'niet mooi.', correct:true},
  {text:'mooi niet.', correct:false},
  {text:'mooi is niet.', correct:false},
]},
{prompt:'Welke zin klopt?', options:[
  {text:'Ik heb wel een blauwe bril.', correct:true},
  {text:'Een blauwe heb ik wel bril.', correct:false},
  {text:'Bril ik heb een blauwe.', correct:false},
]}
"""
    q5bBase = """
{prompt:'Welke kleur wilt u?', options:[
  {text:'Ik woon in Utrecht.', correct:false},
  {text:'Paars. Paars is mooi.', correct:true},
  {text:'Ik ben moe.', correct:false},
], feedback:'Bij "Welke kleur?" zeg je de kleur die je wilt.'},
{prompt:'Wat vindt u hiervan?', options:[
  {text:'Tot ziens!', correct:false},
  {text:'Nee, ik vind rood niet mooi.', correct:true},
  {text:'Kan ik u helpen?', correct:false},
], feedback:'Bij "Wat vindt u hiervan?" zeg je of je het mooi vindt of niet.'},
{prompt:'Mijn bril is oud.', options:[
  {text:'Jammer.', correct:false},
  {text:'Ik wil graag een nieuwe bril.', correct:true},
  {text:'Bedankt. Tot ziens.', correct:false},
], feedback:'Als iets oud is, zeg je: "Ik wil graag een nieuw(e) …"'},
{prompt:'Ik heb geen gele bril.', options:[
  {text:'Bedankt.', correct:false},
  {text:'Goed.', correct:false},
  {text:'En heeft u een blauwe bril?', correct:true},
], feedback:'Als ze het niet hebben, vraag je naar een andere kleur.'},
{prompt:'Alstublieft. Een paarse bril.', options:[
  {text:'Nee, ik vind paars niet mooi.', correct:true},
  {text:'Tot ziens.', correct:false},
  {text:'Ik kijk even.', correct:false},
], feedback:'Na het krijgen van iets zeg je wat je ervan vindt.'}
"""
    convFillSets = """
  {label:'Gesprek 1', lines:[
    {speaker:'Medewerker', fixed:'Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg dat je een nieuwe bril wil', hint_en:'Say you want a new pair of glasses', hint_ar:'قل أنك تريد نظارة جديدة', example:'Ja. Ik wil graag een nieuwe bril.'},
    {speaker:'Medewerker', fixed:'Welke kleur wilt u?'},
    {speaker:'Jij', input:true, hint_nl:'Noem een kleur', hint_en:'Name a colour', hint_ar:'سمِّ لوناً', example:'Paars. Paars is mooi.'},
    {speaker:'Medewerker', fixed:'Alstublieft. Wat vindt u hiervan?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg of je het mooi vindt', hint_en:'Say if you like it', hint_ar:'قل ما إذا كان يعجبك', example:'Nee, ik vind paars niet mooi.'},
    {speaker:'Medewerker', fixed:'Ik heb wel een blauwe bril.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer positief', hint_en:'Respond positively', hint_ar:'تفاعل بإيجابية', example:'Ja, dat is een mooie bril!'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Medewerker', fixed:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg wat je zoekt', hint_en:'Say what you are looking for', hint_ar:'قل ما تبحث عنه', example:'Ja. Ik zoek een rode trui.'},
    {speaker:'Medewerker', fixed:'Welke maat?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg de maat', hint_en:'Say the size', hint_ar:'قل المقاس', example:'Klein.'},
    {speaker:'Medewerker', fixed:'Alstublieft.'},
    {speaker:'Jij', input:true, hint_nl:'Zeg wat je van de kleur vindt', hint_en:'Say what you think of the colour', hint_ar:'قل رأيك في اللون', example:'Hmm, ik vind rood niet mooi.'},
    {speaker:'Medewerker', fixed:'Ik heb ook een groene trui.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer en sluit af', hint_en:'Respond and close', hint_ar:'تفاعل وأنهِ المحادثة', example:'Groen is mooi! Dank u.'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Medewerker', fixed:'Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg welke kleur jas je zoekt', hint_en:'Say which colour jacket you want', hint_ar:'قل لون المعطف الذي تبحث عنه', example:'Ja. Ik zoek een blauwe jas.'},
    {speaker:'Medewerker', fixed:'Sorry, ik heb geen kleine blauwe jas.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag naar een andere kleur', hint_en:'Ask for a different colour', hint_ar:'اسأل عن لون آخر', example:'Heeft u een groene jas?'},
    {speaker:'Medewerker', fixed:'Ja hoor. Alstublieft.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer blij', hint_en:'Respond happily', hint_ar:'تفاعل بسعادة', example:'Mooi! Dank u.'},
  ]}
"""
    aTasks_nl = ['1️⃣ Zeg wat je zoekt: "Ik wil graag een nieuwe bril."', '2️⃣ Noem een kleur: "Paars."', '3️⃣ Reageer: "Nee, ik vind paars niet mooi."', '4️⃣ Sluit af: "Ja, dat is mooi! Dank u."']
    aTasks_en = ['1️⃣ Say what you are looking for: "Ik wil graag een nieuwe bril."', '2️⃣ Name a color: "Paars."', '3️⃣ React: "Nee, ik vind paars niet mooi."', '4️⃣ Close: "Ja, dat is mooi! Dank u."']
    bTasks_nl = ['1️⃣ Begroet: "Kan ik u helpen?"', '2️⃣ Vraag naar kleur: "Welke kleur wilt u?"', '3️⃣ Laat zien: "Alstublieft. Wat vindt u hiervan?"', '4️⃣ Geef alternatief: "Ik heb ook een blauwe bril."']
    bTasks_en = ['1️⃣ Greet: "Kan ik u helpen?"', '2️⃣ Ask for color: "Welke kleur wilt u?"', '3️⃣ Show item: "Alstublieft. Wat vindt u hiervan?"', '4️⃣ Give alternative: "Ik heb ook een blauwe bril."']

    st_nl = ['Vertel wat oud is: "Mijn … is oud."', 'Zeg wat je wil: "Ik wil graag een nieuwe …"', 'Kies een kleur als de medewerker vraagt', 'Reageer op het aanbod', 'Sluit af: "Dank u. Tot ziens."']
    st_en = ['Tell what is old: "Mijn … is oud."', 'Say what you want: "Ik wil graag een nieuwe …"', 'Choose a color when the employee asks', 'React to the offer', 'Close: "Dank u. Tot ziens."']

    html = apply_stars_replacements(html, '⭐⭐', 'Thema 5.1 ⭐⭐ — Kleding', wordsData, repeatPhrases, copyPhrases, sortBase, convSets, q5aBase, q5bBase, convFillSets, aTasks_nl, aTasks_en, bTasks_nl, bTasks_en, st_nl, st_en)
    
    with open(r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html", 'w', encoding='utf-8') as f:
         f.write(html)

def create_3ster():
    html = apply_common_fixes(base_html)

    wordsData = """
{nl:'Eén moment.', en:'One moment.', ar:'لحظة واحدة.', emoji:'⏱️'},
{nl:'dezelfde', en:'the same', ar:'نفس', emoji:'🔄'},
{nl:'de schoen, de schoenen', en:'the shoe(s)', ar:'الحذاء، الأحذية', emoji:'👟'},
{nl:'de riem', en:'the belt', ar:'الحزام', emoji:'👔'},
{nl:'de maat', en:'the size', ar:'المقاس', emoji:'📏'},
{nl:'lichtblauw', en:'light blue', ar:'أزرق فاتح', emoji:'💙'},
{nl:'donkerbruin', en:'dark brown', ar:'بني داكن', emoji:'🟤'},
{nl:'Mag ik iets vragen?', en:'May I ask something?', ar:'هل يمكنني أن أسأل شيئاً؟', emoji:'🙋'},
{nl:'Kunt u ze bestellen?', en:'Can you order them?', ar:'هل يمكنك طلبها؟', emoji:'📦'},
{nl:'Graag gedaan.', en:'You\\'re welcome.', ar:'على الرحب والسعة.', emoji:'😊'},
{nl:'Zegt u het maar.', en:'Go ahead / Tell me.', ar:'تفضل.', emoji:'🗣️'},
{nl:'Kunt u het vinden?', en:'Can you find what you need?', ar:'هل يمكنك العثور عليه؟', emoji:'🔍'},
{nl:'een andere kleur', en:'a different colour', ar:'لون آخر', emoji:'🎨'},
{nl:'op zaterdag', en:'on Saturday', ar:'يوم السبت', emoji:'📅'}
"""
    repeatPhrases = """
{nl:'Mag ik iets vragen?', emoji:'🙋'},
{nl:'Zegt u het maar.', emoji:'🗣️'},
{nl:'Heeft u deze schoen ook in maat 38?', emoji:'👟'},
{nl:'Eén moment.', emoji:'⏱️'},
{nl:'Het is dezelfde schoen, maar een andere kleur.', emoji:'🔄'},
{nl:'Kunt u ze bestellen?', emoji:'📦'},
{nl:'Graag gedaan. Tot zaterdag.', emoji:'😊'}
"""
    copyPhrases = """
'Mag ik iets vragen?',
'Zegt u het maar.',
'Heeft u deze schoen ook in maat 38?',
'Eén moment.',
'Het is dezelfde schoen, maar een andere kleur.',
'Kunt u ze bestellen?',
'Graag gedaan. Tot zaterdag.'
"""
    sortBase = """
{words:['vragen','iets','Mag','ik','?'], answer:'Mag ik iets vragen ?'},
{words:['schoen','deze','ook','Heeft','38','u','maat','in','?'], answer:'Heeft u deze schoen ook in maat 38 ?'},
{words:['moment','Eén','.'], answer:'Eén moment .'},
{words:['ze','Kunt','bestellen','u','?'], answer:'Kunt u ze bestellen ?'},
{words:['kleur','schoen','dezelfde','het','maar','een','andere','is','.'], answer:'Het is dezelfde schoen maar een andere kleur .'}
"""
    convSets = """
  {label:'Gesprek 1', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Mag ik iets vragen?'},
    {speaker:'Medewerker', text:'Natuurlijk. Zegt u het maar.'},
    {speaker:'Klant', text:'Heeft u deze schoen in maat 38?'},
    {speaker:'Medewerker', text:'Eén moment.'},
    {speaker:'Medewerker', text:'Ik heb de donkerbruine niet in maat 38.'},
    {speaker:'Klant', text:'Kunt u ze bestellen?'},
    {speaker:'Medewerker', text:'Ja hoor, op zaterdag.'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kunt u het vinden?'},
    {speaker:'Klant', text:'Nee, ik zoek een lichtblauwe riem.'},
    {speaker:'Medewerker', text:'Sorry, die hebben we niet.'},
    {speaker:'Klant', text:'En een donkerbruine riem?'},
    {speaker:'Medewerker', text:'Eén moment.'},
    {speaker:'Medewerker', text:'Ja, de donkerbruine riem heb ik wel.'},
    {speaker:'Klant', text:'Heel fijn. Dank u wel.'},
    {speaker:'Medewerker', text:'Graag gedaan. Tot ziens.'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Medewerker', text:'Kan ik u helpen?'},
    {speaker:'Klant', text:'Mag ik iets vragen?'},
    {speaker:'Medewerker', text:'Natuurlijk. Zegt u het maar.'},
    {speaker:'Klant', text:'Heeft u deze jas ook in maat 40?'},
    {speaker:'Medewerker', text:'Eén moment.'},
    {speaker:'Medewerker', text:'Nee, maat 40 heb ik niet. Ik heb dezelfde jas in een andere kleur.'},
    {speaker:'Klant', text:'Kunt u ze bestellen?'},
    {speaker:'Medewerker', text:'Ja hoor.'},
  ]},
  {label:'Gesprek 4', lines:[
    {speaker:'Medewerker', text:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Klant', text:'Nee hoor, ik kijk even.'},
    {speaker:'Medewerker', text:'Prima.'},
    {speaker:'Klant', text:'Mag ik iets vragen?'},
    {speaker:'Medewerker', text:'Zegt u het maar.'},
    {speaker:'Klant', text:'Heeft u deze broek ook in blauw?'},
    {speaker:'Medewerker', text:'Nee, alleen in zwart.'},
    {speaker:'Klant', text:'Jammer. Tot ziens.'},
  ]},
  {label:'Gesprek 5', lines:[
    {speaker:'Medewerker', text:'Goedemiddag meneer. Daar zijn de schoenen.'},
    {speaker:'Klant', text:'Heel fijn dat ik ze op zaterdag heb.'},
    {speaker:'Medewerker', text:'Heeft u verder nog vragen?'},
    {speaker:'Klant', text:'Nee, dat was het. Heel fijn. Dank u wel.'},
    {speaker:'Medewerker', text:'Graag gedaan. Tot ziens.'},
    {speaker:'Klant', text:'Tot ziens. Dag mevrouw.'},
    {speaker:'Medewerker', text:'Dag meneer. Een prettige dag!'},
    {speaker:'Klant', text:'Afscheid.'},
  ]}
"""
    q5aBase = """
{prompt:'Heeft u deze schoen ook in maat 38?', options:[
  {text:'Maat 38 heeft u ook deze schoen?', correct:false},
  {text:'Heeft u deze schoen ook in maat 38?', correct:true},
  {text:'Ook maat 38 schoen heeft u?', correct:false},
]},
{prompt:'Hoe vraag je toestemming om iets te vragen?', options:[
  {text:'Mag ik iets vragen?', correct:true},
  {text:'Iets vragen mag ik?', correct:false},
  {text:'Ik mag vragen iets?', correct:false},
]},
{prompt:'Welke zin klopt?', options:[
  {text:'Het dezelfde is schoen maar kleur andere een.', correct:false},
  {text:'Het is dezelfde schoen, maar een andere kleur.', correct:true},
  {text:'Dezelfde schoen het maar is andere kleur een.', correct:false},
]},
{prompt:'Hoe vraag je of ze iets kunnen bestellen?', options:[
  {text:'Ze kunt u bestellen?', correct:false},
  {text:'Bestellen kunt ze u?', correct:false},
  {text:'Kunt u ze bestellen?', correct:true},
]}
"""
    q5bBase = """
{prompt:'Kunt u het vinden?', options:[
  {text:'Ik ben moe.', correct:false},
  {text:'Nee, ik zoek een lichtblauwe riem.', correct:true},
  {text:'Tot ziens.', correct:false},
], feedback:'Als een medewerker vraagt "Kunt u het vinden?" zeg je wat je zoekt.'},
{prompt:'Mag ik iets vragen?', options:[
  {text:'Bedankt.', correct:false},
  {text:'Tot ziens!', correct:false},
  {text:'Natuurlijk. Zegt u het maar.', correct:true},
], feedback:'Op "Mag ik iets vragen?" antwoord je: "Natuurlijk. Zegt u het maar."'},
{prompt:'Ik heb de donkerbruine schoenen niet in maat 38.', options:[
  {text:'Dank u wel.', correct:false},
  {text:'Kunt u ze bestellen?', correct:true},
  {text:'Nee, ik kijk even.', correct:false},
], feedback:'Als ze de maat niet hebben, vraag je of ze het kunnen bestellen.'},
{prompt:'Ja hoor, ik heb de schoenen dan op zaterdag.', options:[
  {text:'Jammer.', correct:false},
  {text:'Graag gedaan.', correct:false},
  {text:'Heel fijn. Dank u wel.', correct:true},
], feedback:'Als het goed nieuws is, zeg je: "Heel fijn. Dank u wel."'},
{prompt:'Ik heb wel dezelfde schoen, maar in een andere kleur.', options:[
  {text:'Eén moment.', correct:false},
  {text:'Nee, ik wil graag de donkerbruine.', correct:true},
  {text:'Kan ik u helpen?', correct:false},
], feedback:'Als je liever de originele kleur wil, zeg je welke je wilt.'}
"""
    convFillSets = """
  {label:'Gesprek 1', lines:[
    {speaker:'Medewerker', fixed:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Vraag toestemming', hint_en:'Ask permission to ask something', hint_ar:'اطلب الإذن لسؤال', example:'Mag ik iets vragen?'},
    {speaker:'Medewerker', fixed:'Natuurlijk. Zegt u het maar.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag naar de maat', hint_en:'Ask about the size', hint_ar:'اسأل عن المقاس', example:'Heeft u deze schoen in maat 38?'},
    {speaker:'Medewerker', fixed:'Eén moment. Ik heb de donkerbruine niet in maat 38.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag of ze het kunnen bestellen', hint_en:'Ask if they can order it', hint_ar:'اسأل إن كان بإمكانهم طلبه', example:'Kunt u ze bestellen?'},
    {speaker:'Medewerker', fixed:'Ja hoor, op zaterdag.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer blij en sluit af', hint_en:'Respond happily and close', hint_ar:'تفاعل بسعادة وأنهِ', example:'Heel fijn. Dank u wel.'},
  ]},
  {label:'Gesprek 2', lines:[
    {speaker:'Medewerker', fixed:'Kunt u het vinden?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg wat je zoekt', hint_en:'Say what you are looking for', hint_ar:'قل ما تبحث عنه', example:'Nee, ik zoek een lichtblauwe riem.'},
    {speaker:'Medewerker', fixed:'Sorry, die hebben we niet.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer en vraag iets anders', hint_en:'Respond and ask for something else', hint_ar:'تفاعل واسأل عن شيء آخر', example:'En een donkerbruine riem?'},
    {speaker:'Medewerker', fixed:'Ja, de donkerbruine riem heb ik wel.'},
    {speaker:'Jij', input:true, hint_nl:'Reageer blij', hint_en:'Respond happily', hint_ar:'تفاعل بسعادة', example:'Heel fijn. Dank u wel.'},
    {speaker:'Medewerker', fixed:'Graag gedaan. Tot ziens.'},
    {speaker:'Jij', input:true, hint_nl:'Sluit af', hint_en:'Close the conversation', hint_ar:'أنهِ المحادثة', example:'Tot ziens.'},
  ]},
  {label:'Gesprek 3', lines:[
    {speaker:'Medewerker', fixed:'Goedemiddag. Kan ik u helpen?'},
    {speaker:'Jij', input:true, hint_nl:'Zeg dat je kijkt', hint_en:'Say you are just looking', hint_ar:'قل أنك تتصفح فقط', example:'Nee hoor, ik kijk even.'},
    {speaker:'Medewerker', fixed:'Prima.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag toestemming', hint_en:'Ask permission', hint_ar:'اطلب الإذن', example:'Mag ik iets vragen?'},
    {speaker:'Medewerker', fixed:'Zegt u het maar.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag naar de maat', hint_en:'Ask about the size', hint_ar:'اسأل عن المقاس', example:'Heeft u deze jas ook in maat 40?'},
    {speaker:'Medewerker', fixed:'Nee, maat 40 heb ik niet.'},
    {speaker:'Jij', input:true, hint_nl:'Vraag of ze het kunnen bestellen', hint_en:'Ask if they can order it', hint_ar:'اسأل إن كان بإمكانهم طلبه', example:'Kunt u ze bestellen?'},
  ]}
"""
    aTasks_nl = ['1️⃣ Zeg dat je iets wil vragen: "Mag ik iets vragen?"', '2️⃣ Vraag naar maat of kleur: "Heeft u … in maat …?"', '3️⃣ Als ze het niet hebben: "Kunt u ze bestellen?"', '4️⃣ Sluit af: "Heel fijn. Dank u wel. Tot ziens."']
    aTasks_en = ['1️⃣ Say you want to ask something: "Mag ik iets vragen?"', '2️⃣ Ask about size or color: "Heeft u … in maat …?"', '3️⃣ If they don\'t have it: "Kunt u ze bestellen?"', '4️⃣ Close: "Heel fijn. Dank u wel. Tot ziens."']
    bTasks_nl = ['1️⃣ Begroet: "Goedemiddag. Kan ik u helpen?"', '2️⃣ Reageer: "Eén moment." of "Sorry, die heb ik niet."', '3️⃣ Bied alternatief: "Het is dezelfde … maar een andere kleur."', '4️⃣ Sluit af: "Graag gedaan. Tot zaterdag."']
    bTasks_en = ['1️⃣ Greet: "Goedemiddag. Kan ik u helpen?"', '2️⃣ React: "Eén moment." or "Sorry, die heb ik niet."', '3️⃣ Offer alternative: "Het is dezelfde … maar een andere kleur."', '4️⃣ Close: "Graag gedaan. Tot zaterdag."']

    st_nl = ['Vraag toestemming: "Mag ik iets vragen?"', 'Vraag naar maat of kleur', 'Reageer op het antwoord van de medewerker', 'Bestel als nodig: "Kunt u ze bestellen?"', 'Sluit af: "Heel fijn. Dank u wel. Tot ziens."']
    st_en = ['Ask permission: "Mag ik iets vragen?"', 'Ask about size or color', 'React to the answer of the employee', 'Order if necessary: "Kunt u ze bestellen?"', 'Close: "Heel fijn. Dank u wel. Tot ziens."']

    html = apply_stars_replacements(html, '⭐⭐⭐', 'Thema 5.1 ⭐⭐⭐ — Kleding', wordsData, repeatPhrases, copyPhrases, sortBase, convSets, q5aBase, q5bBase, convFillSets, aTasks_nl, aTasks_en, bTasks_nl, bTasks_en, st_nl, st_en)
    
    with open(r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-3ster.html", 'w', encoding='utf-8') as f:
         f.write(html)


create_1ster()
create_2ster()
create_3ster()
print("All files updated created successfully.")
