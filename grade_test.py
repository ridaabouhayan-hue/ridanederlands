import re
import sys
import json
import os
import argparse

# =====================================================================
# 1. UTILITY FUNCTIONS & LOGIC
# =====================================================================
def normalize(s):
    if not s:
        return ""
    # Remove punctuation
    s = re.sub(r'[\.\?\!\,\;]', '', s)
    s = s.lower()
    # Normalize multiple whitespace characters to a single space
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
    
    # Exact match after normalization
    if any(normalize(ans) == student_norm for ans in correct_list):
        return "correct", 1.0
        
    # Fuzzy match with Levenshtein
    if student_norm:
        min_dist = min(levenshtein_distance(student_norm, normalize(ans)) for ans in correct_list)
        
        if is_sentence:
            threshold = 5  # Margin for full sentences (e.g. dictation)
        else:
            primary_len = len(normalize(correct_list[0]))
            if primary_len <= 4:
                threshold = 1  # For very short words
            else:
                threshold = 2  # Standard word spelling margin
                
        if min_dist <= threshold:
            return "half", 0.5
            
    return "incorrect", 0.0

def clean_answer_status(ans):
    if not ans:
        return ""
    # Strip emojis
    ans = ans.replace("✅", "")
    # Strip everything after ❌ or 🟠
    ans = re.sub(r'[❌🟠].*$', '', ans)
    # Strip parentheses containing feedback comments
    ans = re.sub(r'\s*\([^)]*(?:moet zijn|spelling|yajib|خطأ).*?\)', '', ans, flags=re.IGNORECASE)
    return ans.strip()

def format_score(score):
    if isinstance(score, float) and score.is_integer():
        return str(int(score))
    return str(score).replace('.', ',')

# =====================================================================
# 2. PASTE PARSER
# =====================================================================
def parse_pasted_text(text, test_config):
    lines = text.strip().split('\n')
    sections = {sec_name: [] for sec_name in test_config["sections"].keys()}
    current_section = None
    student_name = None
    
    # Map section names (nl and ar) to their internal keys
    section_mapping = {}
    for sec_key, sec_data in test_config["sections"].items():
        section_mapping[sec_key.lower()] = sec_key
        if "title_nl" in sec_data:
            section_mapping[sec_data["title_nl"].lower()] = sec_key
        if "title_ar" in sec_data:
            section_mapping[sec_data["title_ar"].lower()] = sec_key
            
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match student name
        name_match = re.search(r'(?:Naam|Name|الاسم)\s*:\s*\**([^*]+)\**', line, re.IGNORECASE)
        if name_match:
            student_name = name_match.group(1).strip()
            continue
            
        # Match section header (e.g., "*1. Woordenschat*" or "*Woordenschat*")
        clean_header = line.replace("*", "").strip().lower()
        clean_header = re.sub(r'^\d+[\.\s]+', '', clean_header).strip()
        
        matched_sec = None
        for name_key, sec_key in section_mapping.items():
            if name_key in clean_header:
                matched_sec = sec_key
                break
                
        if matched_sec:
            current_section = matched_sec
            continue
            
        # Skip other metadata and layout templates
        if any(x in line.lower() for x in ["resultaat", "totaalscore", "feedbackbrief", "beste", "je hebt de oefentoets", "score:", "wat gaat al goed", "wat kun je nog", "met vriendelijke groet", "de docent"]):
            continue
            
        # Extract question value
        match = re.search(r'^(?:-|•)?\s*(?:Vraag|Zin|Zinnen|Vragen)\s*\d+\s*=\s*(.*)$', line, re.IGNORECASE)
        ans_val = None
        if match:
            ans_val = match.group(1).strip()
        else:
            match = re.search(r'^\d+[\.\)\s]+\s*(.*)$', line)
            if match:
                ans_val = match.group(1).strip()
            elif line.startswith('-') or line.startswith('•'):
                ans_val = line[1:].strip()
            else:
                if not line.startswith('*') and not line.startswith('---'):
                    ans_val = line
                    
        if ans_val is not None:
            clean_ans = clean_answer_status(ans_val)
            if current_section:
                max_len = len(test_config["sections"][current_section]["keys"])
                if len(sections[current_section]) < max_len:
                    sections[current_section].append(clean_ans)
            else:
                # Add to first section that isn't full yet
                for sec_key in test_config["sections"].keys():
                    max_len = len(test_config["sections"][sec_key]["keys"])
                    if len(sections[sec_key]) < max_len:
                        sections[sec_key].append(clean_ans)
                        break
                        
    # Pad incomplete sections with empty strings
    for sec_key, sec_data in test_config["sections"].items():
        max_len = len(sec_data["keys"])
        while len(sections[sec_key]) < max_len:
            sections[sec_key].append("")
            
    return student_name, sections

# =====================================================================
# 3. GRADING ENGINE & OUTPUT GENERATOR
# =====================================================================
DUTCH_TEMPLATE = """*--- FEEDBACKBRIEF VOOR DE CURSIST ---*

Beste {name},

Je hebt de {test_title} gemaakt. Goed gedaan! Hier is jouw resultaat:

*Jouw resultaat:*
- *Score:* {score} van de {max_score} punten goed.
- *Resultaat:* {status}

*Wat gaat al goed:*
{strengths}

*Wat kun je nog oefenen:*
{improvements}

Met vriendelijke groet,
De docent"""

ARABIC_TEMPLATE = """*--- FEEDBACKBRIEF VOOR DE CURSIST ---*

عزيزي {name}،

لقد قمت بحل {test_title}. أحسنت صنعاً! إليك تفاصيل نتيجتك وملاحظات المعلم:

*نتيجتك:*
- *الدرجة:* {score} من أصل {max_score} نقطة صحيحة.
- *النتيجة النهائية:* {status}

*ما تجيده بالفعل (نقاط قوتك):*
{strengths}

*ما يمكنك التدرب عليه أكثر (نصائح للتعلم):*
{improvements}

مع أطيب التحيات،
المعلم"""

def run_grading(student_name, answers, test_config, lang="nl"):
    total_score = 0.0
    test_title = test_config["title_ar"] if lang == "ar" else test_config["title_nl"]
    
    report = f"*RESULTAAT {test_title.upper()}*\n"
    report += f"*Naam:* {student_name}\n\n"
    
    sections_scores = {}
    sections_detailed = {}
    sections_reports = {}
    
    for sec_key, sec_data in test_config["sections"].items():
        sec_score = 0.0
        sec_title = sec_data["title_ar"] if lang == "ar" else sec_data["title_nl"]
        
        prefix = "Zin" if sec_data["is_sentence"] else "Vraag"
        if lang == "ar":
            prefix = "الجملة" if sec_data["is_sentence"] else "السؤال"
            
        moet_zijn_str = "يجب أن تكون:" if lang == "ar" else "moet zijn:"
        spelling_str = "خطأ إملائي،" if lang == "ar" else "spelling,"
        
        sec_report = f"*{sec_title}* (Score: {{SCORE_{sec_key}}}/{len(sec_data['keys'])})\n"
        sections_detailed[sec_key] = []
        
        for i, keys in enumerate(sec_data["keys"]):
            ans = answers[sec_key][i]
            status_type, score_val = grade_answer(ans, keys, is_sentence=sec_data["is_sentence"])
            sec_score += score_val
            
            sections_detailed[sec_key].append({
                "ans": ans,
                "status": status_type,
                "score": score_val
            })
            
            if status_type == "correct":
                sec_report += f"- {prefix} {i+1} = {ans or '...'} ✅\n"
            elif status_type == "half":
                sec_report += f"- {prefix} {i+1} = {ans or '...'} 🟠 ({spelling_str} {moet_zijn_str} {keys[0]})\n"
            else:
                sec_report += f"- {prefix} {i+1} = {ans or '...'} ❌ ({moet_zijn_str} {keys[0]})\n"
                
        sec_report = sec_report.replace(f"{{SCORE_{sec_key}}}", format_score(sec_score))
        sections_scores[sec_key] = sec_score
        sections_reports[sec_key] = sec_report
        total_score += sec_score
        
    formatted_total_score = format_score(total_score)
    max_score = test_config["max_score"]
    
    report += f"*TOTAALSCORE:* {formatted_total_score}/{max_score}\n\n"
    for sec_key in test_config["sections"].keys():
        report += sections_reports[sec_key] + "\n"
        
    # Generate feedback brief
    goed_punten = []
    oefen_punten = []
    
    passed = total_score >= test_config["passing_score"]
    
    for sec_key, sec_data in test_config["sections"].items():
        sec_score = sections_scores[sec_key]
        max_sec_score = len(sec_data["keys"])
        formatted_sec_score = format_score(sec_score)
        
        title = sec_data["title_ar"] if lang == "ar" else sec_data["title_nl"]
        
        if sec_score >= sec_data["threshold"]:
            success_text = sec_data["success_ar"] if lang == "ar" else sec_data["success_nl"]
            goed_punten.append(f"*- {title} ({formatted_sec_score}/{max_sec_score}):* {success_text}")
        else:
            fail_prefix = sec_data["fail_prefix_ar"] if lang == "ar" else sec_data["fail_prefix_nl"]
            imp_block = f"*- {title} ({formatted_sec_score}/{max_sec_score}):* {fail_prefix}"
            
            # Check tips
            triggered_tips = []
            for tip in sec_data.get("tips", []):
                # Check if any question index triggers this tip
                if any(sections_detailed[sec_key][idx]["score"] < 1.0 for idx in tip["if_incorrect"]):
                    tip_text = tip["text_ar"] if lang == "ar" else tip["text_nl"]
                    triggered_tips.append(tip_text)
                    
            if triggered_tips:
                prefix_char = "  "
                imp_block += "\n" + "\n".join(f"{prefix_char}- {t}" for t in triggered_tips)
                
            rule_text = sec_data.get("rule_ar" if lang == "ar" else "rule_nl")
            if rule_text:
                indented_rule = "\n".join("  " + l for l in rule_text.strip().split("\n"))
                imp_block += "\n\n" + indented_rule
                
            oefen_punten.append(imp_block)
            
    if lang == "ar":
        status_str = "درجة *مقبول (ناجح)*! تهانينا! 🎉" if passed else "درجة *غير كافٍ*. لا تستسلم وتدرب مرة أخرى! 💪"
        strengths_str = "\n".join(goed_punten) if goed_punten else "- واصل التدريب، أنت على الطريق الصحيح!"
        improvements_str = "\n".join(oefen_punten) if oefen_punten else "- لا توجد ملاحظات، لقد أتقنت كل شيء! ممتاز!"
        
        feedback_brief = ARABIC_TEMPLATE.format(
            name=student_name,
            test_title=test_config["title_ar"],
            score=formatted_total_score,
            max_score=max_score,
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
            test_title=test_config["title_nl"],
            score=formatted_total_score,
            max_score=max_score,
            status=status_str,
            strengths=strengths_str,
            improvements=improvements_str
        )
        
    return report + "\n\n" + feedback_brief

# =====================================================================
# 4. CLI FLOW
# =====================================================================
def get_paste_input():
    print("\nPlak hieronder de tekst met antwoorden (bijvoorbeeld uit WhatsApp).")
    print("Druk op Ctrl+D (Linux/Mac) of Ctrl+Z en Enter (Windows) wanneer je klaar bent:")
    print("-" * 50)
    lines = []
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            lines.append(line)
    except KeyboardInterrupt:
        pass
    print("-" * 50)
    return "".join(lines)

def run_interactive(test_config, lang):
    print(f"\n=== INTERACTIEF NAKIJKEN: {test_config['title_nl'].upper()} ===")
    
    student_name = input("Naam cursist: ").strip()
    while not student_name:
        student_name = input("Naam cursist (verplicht): ").strip()
        
    answers = {}
    
    for sec_key, sec_data in test_config["sections"].items():
        print(f"\n--- {sec_data['title_nl']} ---")
        answers[sec_key] = []
        
        prefix = "Zin" if sec_data["is_sentence"] else "Vraag"
        for i in range(len(sec_data["keys"])):
            ans = input(f"  {prefix} {i+1}: ").strip()
            answers[sec_key].append(ans)
            
    return student_name, answers

def main():
    # Find config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "toets_keys.json")
    
    if not os.path.exists(config_path):
        print(f"Error: Config bestand 'toets_keys.json' niet gevonden op {config_path}")
        sys.exit(1)
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            all_configs = json.load(f)
    except Exception as e:
        print(f"Error bij laden van 'toets_keys.json': {e}")
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="Standaard Toets Nakijken Tool (ridanederlands)")
    parser.add_argument("--test", type=str, default="thema7", choices=list(all_configs.keys()), help="De ID van de toets in de config.")
    parser.add_argument("--interactive", action="store_true", help="Start handmatige vraag-voor-vraag invoer.")
    parser.add_argument("--paste", action="store_true", help="Start de plak-modus om een tekstblok te scannen.")
    parser.add_argument("--name", type=str, default=None, help="Naam van de cursist (indien niet interactief).")
    parser.add_argument("--lang", type=str, default="nl", choices=["nl", "ar"], help="Taal van de feedbackbrief (nl of ar). Standaard: nl.")
    
    args = parser.parse_args()
    
    test_config = all_configs[args.test]
    
    # Determine mode: default to paste mode if no args are set (very convenient for teachers)
    mode_paste = args.paste
    mode_interactive = args.interactive
    
    if not mode_paste and not mode_interactive:
        # Prompt user to choose mode
        print("=== STANDAARD TOETS NAKIJKEN ===")
        print("1) Plak-modus (WhatsApp bericht kopiëren en plakken - Snelst!)")
        print("2) Handmatige invoer (Vraag voor vraag beantwoorden)")
        choice = input("Maak een keuze (1 of 2, standaard 1): ").strip()
        if choice == "2":
            mode_interactive = True
        else:
            mode_paste = True
            
    if mode_paste:
        # Paste Mode
        pasted_text = get_paste_input()
        student_name, answers = parse_pasted_text(pasted_text, test_config)
        
        # If student name wasn't detected, prompt for it
        if not student_name:
            if args.name:
                student_name = args.name
            else:
                student_name = input("Naam cursist: ").strip()
                while not student_name:
                    student_name = input("Naam cursist (verplicht): ").strip()
    else:
        # Interactive Mode
        student_name, answers = run_interactive(test_config, args.lang)
        
    # Generate report
    result_text = run_grading(student_name, answers, test_config, args.lang)
    
    print("\n" + "=" * 60)
    print("GEFORMATTEERD NAKIJKBLAD & FEEDBACKBRIEF:")
    print("=" * 60)
    print(result_text)
    print("=" * 60)

if __name__ == "__main__":
    main()
