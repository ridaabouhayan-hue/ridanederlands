import re
import sys
import argparse

# =====================================================================
# 1. ANTWOORDSLEUTELS & STRUCTUUR
# =====================================================================
ANSWER_KEYS = {
    "woordenschat": [
        ["auto", "de auto"],
        ["trein", "de trein"],
        ["fiets", "de fiets"],
        ["vliegtuig", "het vliegtuig"],
        ["bus", "de bus"],
        ["boot", "de boot", "schip", "het schip"],
        ["station", "het station"]
    ],
    "grammatica": [
        ["mag"],
        ["kunnen"],
        ["mag"],
        ["kunnen"],
        ["kan"],
        ["mogen"],
        ["kan"]
    ],
    "voorzetsels": [
        ["om"],
        ["in"],
        ["op"],
        ["voor"],
        ["achter"],
        ["naast"],
        ["onder"]
    ],
    "dictee": [
        ["Waar is het station?", "Waar is het station"],
        ["Ik ga met de bus naar school.", "Ik ga met de bus naar school"],
        ["Hoe laat vertrekt de trein?", "Hoe laat vertrekt de trein"],
        ["Mag ik een ticket naar Amsterdam?", "Mag ik een ticket naar Amsterdam", "Mag ik een ticket naar amsterdam", "Mag ik een ticket naar amsterdam?"],
        ["De reis duurt dertig minuten.", "De reis duurt dertig minuten"],
        ["Wij gaan op vakantie naar Spanje.", "Wij gaan op vakantie naar Spanje", "Wij gaan op vakantie naar spanje", "Wij gaan op vakantie naar spanje."],
        ["Ik heb mijn koffer gepakt.", "Ik heb mijn koffer gepakt"]
    ],
    "vraagwoorden": [
        ["Waar"],
        ["Hoe"],
        ["Wie"],
        ["Wanneer", "Hoe laat"],
        ["Hoeveel"],
        ["Waarom"],
        ["Wat"]
    ]
}

# =====================================================================
# 2. MATCHING & GRADEN LOGICA
# =====================================================================
def normalize(s):
    if not s:
        return ""
    s = re.sub(r'[\.\?\!\,\;]', '', s)
    s = s.lower()
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def grade_answer(student_ans, correct_list, is_sentence=False):
    student_norm = normalize(student_ans)
    
    # Exacte match
    if any(normalize(ans) == student_norm for ans in correct_list):
        return "correct", 1.0
        
    # Half correct (spellingfout) via Levenshtein
    if student_norm:
        min_dist = min(levenshtein_distance(student_norm, normalize(ans)) for ans in correct_list)
        
        threshold = 2
        if is_sentence:
            threshold = 5
        else:
            primary_len = len(normalize(correct_list[0]))
            if primary_len <= 4:
                threshold = 1
                
        if min_dist <= threshold:
            return "half", 0.5
            
    return "incorrect", 0.0

# =====================================================================
# 3. FEEDBACKBRIEF TEMPLATES
# =====================================================================
DUTCH_TEMPLATE = """*--- FEEDBACKBRIEF VOOR DE CURSIST ---*

Beste {name},

Je hebt de oefentoets voor Thema 7 (Reizen & Vervoer) gemaakt. Goed gedaan! Hier is jouw resultaat:

*Jouw resultaat:*
- *Score:* {score} van de 35 punten goed.
- *Resultaat:* {status}

*Wat gaat al goed:*
{strengths}

*Wat kun je nog oefenen:*
{improvements}

Met vriendelijke groet,
De docent"""

ARABIC_TEMPLATE = """*--- FEEDBACKBRIEF VOOR DE CURSIST ---*

عزيزي {name}،

لقد قمت بحل الاختبار التجريبي للموضوع 7 (السفر ووسائل النقل). أحسنت صنعاً! إليك تفاصيل نتيجتك وملاحظات المعلم:

*نتيجتك:*
- *الدرجة:* {score} من أصل 35 نقطة صحيحة.
- *النتيجة النهائية:* {status}

*ما تجيده بالفعل (نقاط قوتك):*
{strengths}

*ما يمكنك التدرب عليه أكثر (نصائح للتعلم):*
{improvements}

مع أطيب التحيات،
المعلم"""

# =====================================================================
# 4. RAPPORTEREN & NAKIJKEN
# =====================================================================
def run_grading(student_name, answers, lang="nl"):
    total_score = 0.0
    report = f"*RESULTAAT OEFENTOETS THEMA 7 (A1)*\n"
    report += f"*Naam:* {student_name}\n\n"
    
    sections_scores = {}
    sections_reports = {}
    
    sections_keys = ["woordenschat", "grammatica", "voorzetsels", "dictee", "vraagwoorden"]
    sections_names_nl = {
        "woordenschat": "Woordenschat",
        "grammatica": "Grammatica",
        "voorzetsels": "Voorzetsels",
        "dictee": "Dictee",
        "vraagwoorden": "Vraagwoorden"
    }
    
    sections_names_ar = {
        "woordenschat": "المفردات",
        "grammatica": "القواعد",
        "voorzetsels": "حروف الجر",
        "dictee": "الإملاء",
        "vraagwoorden": "أدوات الاستفهام"
    }
    
    sec_name = sections_names_ar if lang == "ar" else sections_names_nl
    moet_zijn_str = "يجب أن تكون:" if lang == "ar" else "moet zijn:"
    spelling_str = "خطأ إملائي،" if lang == "ar" else "spelling,"
    
    for sec in sections_keys:
        sec_score = 0.0
        sec_report = f"*{sec_name[sec]}* (Score: {{SCORE_{sec}}}/7)\n"
        
        for i in range(7):
            ans = answers[sec][i]
            keys = ANSWER_KEYS[sec][i]
            status_type, score_val = grade_answer(ans, keys, is_sentence=(sec == "dictee"))
            sec_score += score_val
            
            prefix = "Zin" if sec == "dictee" else "Vraag"
            if lang == "ar":
                prefix = "الجملة" if sec == "dictee" else "السؤال"
                
            if status_type == "correct":
                sec_report += f"- {prefix} {i+1} = {ans or '...'} ✅\n"
            elif status_type == "half":
                sec_report += f"- {prefix} {i+1} = {ans or '...'} 🟠 ({spelling_str} {moet_zijn_str} {keys[0]})\n"
            else:
                sec_report += f"- {prefix} {i+1} = {ans or '...'} ❌ ({moet_zijn_str} {keys[0]})\n"
                
        sec_report = sec_report.replace(f"{{SCORE_{sec}}}", str(sec_score).replace('.', ','))
        sections_scores[sec] = sec_score
        sections_reports[sec] = sec_report
        total_score += sec_score
        
    formatted_total_score = str(total_score).replace('.', ',')
    
    # Voeg score toe aan rapportkop
    report += f"*TOTAALSCORE:* {formatted_total_score}/35\n\n"
    for sec in sections_keys:
        report += sections_reports[sec] + "\n"
        
    # Genereer de feedbackbrief
    goed_punten = []
    oefen_punten = []
    
    passed = total_score >= 20
    
    # 1. Woordenschat
    if lang == "ar":
        if sections_scores["woordenschat"] >= 5:
            goed_punten.append(f"*- المفردات والكلمات ({str(sections_scores['woordenschat']).replace('.', ',')}/7):* أنت تعرف مفردات السفر ووسائل النقل بشكل ممتاز! لقد قمت بكتابة الكلمات بالهولندية بشكل صحيح.")
        else:
            oefen_punten.append(f"*- المفردات والكلمات ({str(sections_scores['woordenschat']).replace('.', ',')}/7):* تدرب على الكلمات الهولندية لوسائل النقل (مثل سيارة، قطار، حافلة، دراجة، طائرة).")
    else:
        if sections_scores["woordenschat"] >= 5:
            goed_punten.append(f"*- Woordenschat ({str(sections_scores['woordenschat']).replace('.', ',')}/7):* Je kent de reissymbolen en woorden over reizen en vervoer heel goed!")
        else:
            oefen_punten.append(f"*- Woordenschat ({str(sections_scores['woordenschat']).replace('.', ',')}/7):* Oefen de Nederlandse woorden voor voertuigen (auto, trein, bus, etc.).")
            
    # Helper checking for specific questions
    def get_ans(sec, idx):
        return answers[sec][idx]
    def is_correct(sec, idx):
        return grade_answer(get_ans(sec, idx), ANSWER_KEYS[sec][idx])[0] == "correct"

    # 2. Grammatica
    if lang == "ar":
        if sections_scores["grammatica"] >= 7:
            goed_punten.append(f"*- القواعد ({str(sections_scores['grammatica']).replace('.', ',')}/7):* أنت تعرف الفرق بين mogen (الإذن/القواعد) و kunnen (القدرة) بشكل ممتاز.")
        else:
            tips = []
            if not is_correct("grammatica", 1) or not is_correct("grammatica", 3):
                tips.append("Kunnen (القدرة/المهارة): Wij *kunnen* heel snel fietsen (نحن نستطيع ركوب الدراجة).")
            if not is_correct("grammatica", 0) or not is_correct("grammatica", 5):
                tips.append("Mogen (الإذن/القواعد): Hier *mag* je niet parkeren (لا يسمح لك بالوقوف هنا).")
            if not is_correct("grammatica", 2) or not is_correct("grammatica", 4) or not is_correct("grammatica", 6):
                tips.append("الأسئلة والطلب: *Mag* ik hier zitten? (هل يسمح لي بالجلوس؟). *Kan* jij mij helpen? (هل تستطيع مساعدتي؟).")
            
            rule = "\n  _قاعدة للتذكر:_\n  - *Kunnen* = للقدرة على فعل شيء أو مهارة تعلمتها (مثال: أستطيع السباحة).\n  - *Mogen* = للمسموح به أو القواعد العامة (مثال: يُسمح لك بالدخول)."
            oefen_punten.append(f"*- القواعد ({str(sections_scores['grammatica']).replace('.', ',')}/7):* انتبه للفرق بين Mogen و Kunnen:\n  " + "\n  ".join(tips) + rule)
    else:
        if sections_scores["grammatica"] >= 7:
            goed_punten.append(f"*- Grammatica ({str(sections_scores['grammatica']).replace('.', ',')}/7):* Je weet goed wanneer je mogen of kunnen moet gebruiken.")
        else:
            tips = []
            if not is_correct("grammatica", 1) or not is_correct("grammatica", 3):
                tips.append("*Kunnen* (vaardigheid/mogelijkheid): Wij *kunnen* heel snel fietsen. Zij *kunnen* goed Nederlands spreken.")
            if not is_correct("grammatica", 0) or not is_correct("grammatica", 5):
                tips.append("*Mogen* (toestemming/regels): Hier *mag* je niet parkeren. De kinderen *mogen* buiten spelen van de docent.")
            if not is_correct("grammatica", 2) or not is_correct("grammatica", 4) or not is_correct("grammatica", 6):
                tips.append("*Vragen & Hulp:* *Mag* ik hier zitten? (toestemming). *Kan* jij mij helpen? (hulp).")
            
            rule = "\n  _Grammaticaregel:_\n  - *Kunnen* = wat je kunt (vaardigheid) of wat mogelijk is. (Ik *kan* zwemmen).\n  - *Mogen* = wat is toegestaan of regel is. (Je *mag* hier niet parkeren)."
            oefen_punten.append(f"*- Grammatica ({str(sections_scores['grammatica']).replace('.', ',')}/7):* Let op het verschil tussen mogen en kunnen:\n  - " + "\n  - ".join(tips) + rule)

    # 3. Voorzetsels
    if lang == "ar":
        if sections_scores["voorzetsels"] >= 7:
            goed_punten.append(f"*- حروف الجر ({str(sections_scores['voorzetsels']).replace('.', ',')}/7):* أنت تفهم حروف جر المكان والزمان بشكل ممتاز.")
        else:
            tips = []
            if not is_correct("voorzetsels", 0): tips.append("Om: مع الوقت والساعة (*om* kwart over drie).")
            if not is_correct("voorzetsels", 1): tips.append("In: للداخل، الماء في الكوب (*in* het glas).")
            if not is_correct("voorzetsels", 2): tips.append("Op: فوق السطح، الأطباق على الطاولة (*op* de eettafel).")
            if not is_correct("voorzetsels", 3): tips.append("Voor: للوقوف أمام شخص في الطابور (*voor* mij).")
            if not is_correct("voorzetsels", 4): tips.append("Achter: للجهة الخلفية، الحديقة خلف المنزل (*achter* het huis).")
            if not is_correct("voorzetsels", 5): tips.append("Naast: للجلوس بجانب النافذة (*naast* het raam).")
            if not is_correct("voorzetsels", 6): tips.append("Onder: عندما يسقط القلم تحت الطاولة (*onder* de tafel).")
            
            rule = "\n  _قاعدة للتذكر:_\n  - استخدم **Om** للأوقات بالساعة.\n  - استخدم حروف جر المكان (**in, op, naast, voor, achter, onder**) لوصف موقع الأشياء بدقة."
            oefen_punten.append(f"*- حروف الجر ({str(sections_scores['voorzetsels']).replace('.', ',')}/7):* تدرب على حروف الجر الخاصة بالمكان والوقت:\n  " + "\n  ".join(tips) + rule)
    else:
        if sections_scores["voorzetsels"] >= 7:
            goed_punten.append(f"*- Voorzetsels ({str(sections_scores['voorzetsels']).replace('.', ',')}/7):* Je snapt de voorzetsels voor plaats en tijd al heel goed.")
        else:
            tips = []
            if not is_correct("voorzetsels", 0): tips.append("*Tijd (om):* De trein vertrekt *om* kwart over drie.")
            if not is_correct("voorzetsels", 1): tips.append("*In:* Water zit *in* het glas.")
            if not is_correct("voorzetsels", 2): tips.append("*Op:* Borden staan *op* de eettafel.")
            if not is_correct("voorzetsels", 3): tips.append("*Voor:* Mo staat *voor* mij in de rij.")
            if not is_correct("voorzetsels", 4): tips.append("*Achter:* De tuin ligt *achter* het huis.")
            if not is_correct("voorzetsels", 5): tips.append("*Naast:* Zitten *naast* het raam.")
            if not is_correct("voorzetsels", 6): tips.append("*Onder:* De pen ligt *onder* de tafel.")
            
            rule = "\n  _Grammaticaregel:_\n  - Gebruik *om* voor specifieke kloktijden.\n  - Gebruik *in, op, naast, voor, achter, onder* voor de juiste posities."
            oefen_punten.append(f"*- Voorzetsels ({str(sections_scores['voorzetsels']).replace('.', ',')}/7):* Oefen de voorzetsels van plaats en tijd:\n  - " + "\n  - ".join(tips) + rule)

    # 4. Dictee
    if lang == "ar":
        if sections_scores["dictee"] >= 5:
            goed_punten.append(f"*- الإملاء ({str(sections_scores['dictee']).replace('.', ',')}/7):* مهارات الاستماع والكتابة لديك ممتازة! تهجئة الجمل دقيقة للغاية.")
        else:
            oefen_punten.append(f"*- الإملاء ({str(sections_scores['dictee']).replace('.', ',')}/7):* انتبه للأخطاء الإملائية والكلمات المتشابهة: اكتب **een** وليس *en*، واكتب **ticket** وليس *tiket*، واكتب **minuten** وليس *muneten*، واكتب **koffer** وليس *koofer*، واكتب **gepakt** وليس *gebakt*، وتذكر كتابة أسماء الدول بحرف كبير (**Spanje**).")
    else:
        if sections_scores["dictee"] >= 5:
            goed_punten.append(f"*- Dictee ({str(sections_scores['dictee']).replace('.', ',')}/7):* Je luister- en schrijfvaardigheid is uitstekend! Je spelt de zinnen heel nauwkeurig.")
        else:
            oefen_punten.append(f"*- Dictee ({str(sections_scores['dictee']).replace('.', ',')}/7):* Let goed op de klanken en spelling. Let op woorden zoals: *een* (niet 'en'), *ticket* (niet 'tiket'), *minuten*, *koffer*, *gepakt* en schrijf landen met een hoofdletter (*Spanje*).")

    # 5. Vraagwoorden
    if lang == "ar":
        if sections_scores["vraagwoorden"] >= 7:
            goed_punten.append(f"*- أدوات الاستفهام ({str(sections_scores['vraagwoorden']).replace('.', ',')}/7):* أنت تعرف جيداً كيفية طرح الأسئلة بالهولندية.")
        else:
            tips = []
            if not is_correct("vraagwoorden", 0): tips.append("*Waar* woon jij? (locatie -> in Amsterdam)")
            if not is_correct("vraagwoorden", 1): tips.append("*Hoe* ga jij? (vervoer/manier -> met de trein)")
            if not is_correct("vraagwoorden", 2): tips.append("*Wie* is dat? (persoon -> mijn broer)")
            if not is_correct("vraagwoorden", 3): tips.append("*Wanneer* begint de les? (tijd -> om 9 uur)")
            if not is_correct("vraagwoorden", 4): tips.append("*Hoeveel* kost dat? (aantal/prijs -> vijf euro)")
            if not is_correct("vraagwoorden", 5): tips.append("*Waarom* leer je Nederlands? (reden -> omdat ik hier woon)")
            if not is_correct("vraagwoorden", 6): tips.append("*Wat* doe jij? (activiteit/ding -> een cursus)")
            
            rule = "\n  _ملخص أدوات الاستفهام:_\n  - *Waar* (للمكان)، *Hoe* (للمواصلات/الطريقة)، *Wie* (للشخص)، *Wanneer* (للوقت)، *Hoeveel* (للعدد/السعر)، *Waarom* (للسبب)، *Wat* (للشيء/النشاط)."
            oefen_punten.append(f"*- أدوات الاستفهام ({str(sections_scores['vraagwoorden']).replace('.', ',')}/7):* تدرب على ربط أداة الاستفهام بالإجابة المناسبة:\n  " + "\n  ".join(tips) + rule)
    else:
        if sections_scores["vraagwoorden"] >= 7:
            goed_punten.append(f"*- Vraagwoorden ({str(sections_scores['vraagwoorden']).replace('.', ',')}/7):* Je weet heel goed hoe je vragen stelt met Hoe, Wat, Waar, Wie, Wanneer, Hoeveel en Waarom.")
        else:
            tips = []
            if not is_correct("vraagwoorden", 0): tips.append("*Waar* woon jij? (locatie -> in Amsterdam)")
            if not is_correct("vraagwoorden", 1): tips.append("*Hoe* ga jij? (vervoer/manier -> met de trein)")
            if not is_correct("vraagwoorden", 2): tips.append("*Wie* is dat? (persoon -> mijn broer)")
            if not is_correct("vraagwoorden", 3): tips.append("*Wanneer* begint de les? (tijd -> om 9 uur)")
            if not is_correct("vraagwoorden", 4): tips.append("*Hoeveel* kost dat? (aantal/prijs -> vijf euro)")
            if not is_correct("vraagwoorden", 5): tips.append("*Waarom* leer je Nederlands? (reden -> omdat ik hier woon)")
            if not is_correct("vraagwoorden", 6): tips.append("*Wat* doe jij? (activiteit/ding -> een cursus)")
            
            rule = "\n  _Vraagwoorden overzicht:_\n  - *Waar* (locatie), *Hoe* (vervoer), *Wie* (persoon), *Wanneer* (tijd), *Hoeveel* (prijs), *Waarom* (reden), *Wat* (ding/actie)."
            oefen_punten.append(f"*- Vraagwoorden ({str(sections_scores['vraagwoorden']).replace('.', ',')}/7):* Oefen welke vraagwoorden bij de antwoorden horen:\n  - " + "\n  - ".join(tips) + rule)

    # Compileer brief
    if lang == "ar":
        status_str = "درجة *مقبول (ناجح)*! تهانينا! 🎉" if passed else "درجة *غير كافٍ*. لا تستسلم وتدرب مرة أخرى! 💪"
        strengths_str = "\n".join(goed_punten) if goed_punten else "- واصل التدريب، أنت على الطريق الصحيح!"
        improvements_str = "\n".join(oefen_punten) if oefen_punten else "- لا توجد ملاحظات، لقد أتقنت كل شيء! ممتاز!"
        
        feedback_brief = ARABIC_TEMPLATE.format(
            name=student_name,
            score=formatted_total_score,
            status=status_str,
            strengths=strengths_str,
            improvements=improvements_str
        )
    else:
        status_str = "Dit is een *voldoende*! Gefeliciteerd! 🎉" if passed else "Dit is helaas nog *onvoldoende*. Geef niet op, oefen nog een keer! 💪"
        strengths_str = "\n".join(goed_punten) if goed_punten else "- Blijf oefenen, je bent op de goede weg!"
        improvements_str = "\n".join(oefen_punten) if oefen_punten else "- Geen leertips, je hebt alles onder de knie! Super!"
        
        feedback_brief = DUTCH_TEMPLATE.format(
            name=student_name,
            score=formatted_total_score,
            status=status_str,
            strengths=strengths_str,
            improvements=improvements_str
        )
        
    return report + "\n\n" + feedback_brief

# =====================================================================
# 5. CLI INTERACTIEVE LOGICA
# =====================================================================
def prompt_interactive(lang):
    print("=== NT2 OEFENTOETS THEMA 7 NAKIJKEN ===")
    name = input("Naam cursist: ").strip()
    while not name:
        name = input("Naam cursist (verplicht): ").strip()
        
    answers = {}
    
    # 1. Woordenschat
    print("\n--- 1. Woordenschat ---")
    cues = ["Car", "Train", "Bicycle", "Airplane", "Bus", "Boat", "Station"]
    answers["woordenschat"] = []
    for i, cue in enumerate(cues):
        ans = input(f"  Vraag {i+1} ({cue}): ").strip()
        answers["woordenschat"].append(ans)
        
    # 2. Grammatica
    print("\n--- 2. Grammatica ---")
    answers["grammatica"] = []
    for i in range(7):
        ans = input(f"  Vraag {i+1} (mag/mogen/kan/kunnen): ").strip()
        answers["grammatica"].append(ans)
        
    # 3. Voorzetsels
    print("\n--- 3. Voorzetsels ---")
    answers["voorzetsels"] = []
    for i in range(7):
        ans = input(f"  Vraag {i+1}: ").strip()
        answers["voorzetsels"].append(ans)
        
    # 4. Dictee
    print("\n--- 4. Dictee ---")
    answers["dictee"] = []
    for i in range(7):
        ans = input(f"  Zin {i+1}: ").strip()
        answers["dictee"].append(ans)
        
    # 5. Vraagwoorden
    print("\n--- 5. Vraagwoorden ---")
    answers["vraagwoorden"] = []
    for i in range(7):
        ans = input(f"  Vraag {i+1}: ").strip()
        answers["vraagwoorden"].append(ans)
        
    result_text = run_grading(name, answers, lang)
    print("\n" + "="*50)
    print("GEFORMATTEERD WHATSAPP-BERICHT:")
    print("="*50)
    print(result_text)
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatisch nakijken en feedback opstellen voor Thema 7 A1 Oefentoets.")
    parser.add_argument("--interactive", action="store_true", help="Start de interactieve invoer in de terminal.")
    parser.add_argument("--name", type=str, default="Cursist", help="Naam van de cursist.")
    parser.add_argument("--lang", type=str, default="nl", choices=["nl", "ar"], help="Taal van de feedbackbrief (nl of ar).")
    
    args = parser.parse_args()
    
    if args.interactive or len(sys.argv) == 1:
        # Als er geen arguments zijn of --interactive is gezet, doe interactieve CLI
        prompt_interactive(args.lang)
    else:
        # Als er arguments zijn maar niet interactief, doe mock check van Boudjema
        mock_answers = {
            "woordenschat": ["Auto", "Trein", "Fiets", "Vliegtuig", "bus", "boot", "Station"],
            "grammatica": ["mag", "mogen", "kan", "kunnen", "kan", "kunnen", "kan"],
            "voorzetsels": ["om", "in", "op", "Naast", "Voor", "Onder", "Op"],
            "dictee": [
                "Waar is het station?",
                "Ik ga met de bus naar school.",
                "Hoe laat vertrekt de trein.",
                "Mag ik en tiket naar Amesterdam.",
                "De reis is dertig muneten.",
                "Wij gaan om vakantie naar espanya.",
                "Ik heb mijn koofer gebakt."
            ],
            "vraagwoorden": ["Waar", "Wat", "Wie", "Wanneer", "Hoeveel", "Waarom", "Wat"]
        }
        result = run_grading(args.name if args.name != "Cursist" else "Boudjema", mock_answers, args.lang)
        print(result)
