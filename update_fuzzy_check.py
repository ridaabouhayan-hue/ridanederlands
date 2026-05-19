import os
import re

def get_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

LEVENSHTEIN_JS = """
// --- INJECTED FUZZY MATCH LOGIC ---
function levenshtein(a, b) {
    if(a.length === 0) return b.length;
    if(b.length === 0) return a.length;
    var matrix = [];
    for(var i = 0; i <= b.length; i++){ matrix[i] = [i]; }
    for(var j = 0; j <= a.length; j++){ matrix[0][j] = j; }
    for(var i = 1; i <= b.length; i++){
        for(var j = 1; j <= a.length; j++){
            if(b.charAt(i-1) == a.charAt(j-1)){
                matrix[i][j] = matrix[i-1][j-1];
            } else {
                matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, Math.min(matrix[i][j-1] + 1, matrix[i-1][j] + 1));
            }
        }
    }
    return matrix[b.length][a.length];
}
// ----------------------------------
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    already_injected = 'function levenshtein(' in content
    made_changes = False

    # PATTERN 1: checkInvul style
    # if(inp.value.trim().toLowerCase()===item.ant.toLowerCase()){inp.classList.add('correct');g++;}else inp.classList.add('fout');
    pattern_invul = re.compile(
        r"if\s*\(\s*(inp\.value\.trim\(\)\.toLowerCase\(\))\s*===\s*(.*?)\s*\)\s*\{\s*(inp\.classList\.add\('correct'\);\s*[a-zA-Z0-9_]+\+\+;)\s*\}\s*else\s*inp\.classList\.add\('fout'\);"
    )

    def repl_invul(match):
        user_val = match.group(1)
        correct_val = match.group(2)
        success_action = match.group(3)
        base_correct = correct_val.replace('.toLowerCase()', '')
        
        return f"""
        let existingFz = inp.nextElementSibling;
        if (existingFz && existingFz.className === 'fuzzy-note') existingFz.remove();
        inp.classList.remove('correct-fuzzy');
        inp.style.borderColor = '';
        
        let d = levenshtein({user_val}, {correct_val});
        if (d === 0) {{
            {success_action}
        }} else if (d <= 2) {{
            {success_action}
            inp.classList.add('correct-fuzzy');
            inp.style.borderColor = '#ca8a04';
            let fz = document.createElement('span');
            fz.className = 'fuzzy-note';
            fz.style.color = '#ca8a04';
            fz.style.fontSize = '0.85rem';
            fz.style.marginLeft = '8px';
            fz.textContent = `Goed! Let op de spelling: ${{{base_correct}}}`;
            inp.parentNode.insertBefore(fz, inp.nextSibling);
        }} else {{
            inp.classList.add('fout');
        }}
        """.strip()

    new_content, count_invul = pattern_invul.subn(repl_invul, content)
    if count_invul > 0:
        made_changes = True

    # PATTERN 1b: checkInvul style with `goed++` instead of `g++`
    # if(inp.value.trim().toLowerCase()===item.mv.toLowerCase()){inp.classList.add('correct');goed++;}
    pattern_invul2 = re.compile(
        r"if\s*\(\s*(inp\.value\.trim\(\)\.toLowerCase\(\))\s*===\s*(.*?)\s*\)\s*\{\s*(inp\.classList\.add\('correct'\);\s*[a-zA-Z0-9_]+\+\+;)\s*\}"
    )

    def repl_invul2(match):
        user_val = match.group(1)
        correct_val = match.group(2)
        success_action = match.group(3)
        base_correct = correct_val.replace('.toLowerCase()', '')
        
        # Note: this regex matched the `if` but without an `else`. Wait, some don't have else? 
        # Actually in thema6-1 it's just an `if`. Wait, if it doesn't have an else, maybe I should just keep it as an if?
        # Let's see if the code has an else right after or not.
        return f"""
        let existingFz = inp.nextElementSibling;
        if (existingFz && existingFz.className === 'fuzzy-note') existingFz.remove();
        inp.classList.remove('correct-fuzzy');
        inp.style.borderColor = '';
        
        let d = levenshtein({user_val}, {correct_val});
        if (d === 0) {{
            {success_action}
        }} else if (d <= 2) {{
            {success_action}
            inp.classList.add('correct-fuzzy');
            inp.style.borderColor = '#ca8a04';
            let fz = document.createElement('span');
            fz.className = 'fuzzy-note';
            fz.style.color = '#ca8a04';
            fz.style.fontSize = '0.85rem';
            fz.style.marginLeft = '8px';
            fz.textContent = `Goed! Let op de spelling: ${{{base_correct}}}`;
            inp.parentNode.insertBefore(fz, inp.nextSibling);
        }}
        """.strip()

    # We shouldn't blindly run pattern_invul2 if pattern_invul already did its job on the same lines.
    # We can just rely on the first pattern for most. But wait, we need to handle the `else` gracefully if it exists.
    # Let's adjust pattern_invul to make the `else` part optional!
    
    pattern_invul_generic = re.compile(
        r"if\s*\(\s*(inp\.value\.trim\(\)\.toLowerCase\(\))\s*===\s*(.*?)\s*\)\s*\{\s*(inp\.classList\.add\('correct'\);\s*[a-zA-Z0-9_]+\+\+;)\s*\}(?:\s*else\s*inp\.classList\.add\('fout'\);)?"
    )

    def repl_invul_generic(match):
        user_val = match.group(1)
        correct_val = match.group(2)
        success_action = match.group(3)
        base_correct = correct_val.replace('.toLowerCase()', '')
        
        # Check if the original string had "else" in it. The match string is match.group(0).
        has_else = "else" in match.group(0)
        
        else_block = "else { inp.classList.add('fout'); }" if has_else else ""
        
        return f"""
        let existingFz = inp.nextElementSibling;
        if (existingFz && existingFz.className === 'fuzzy-note') existingFz.remove();
        inp.classList.remove('correct-fuzzy');
        inp.style.borderColor = '';
        
        let d = levenshtein({user_val}, {correct_val});
        if (d === 0) {{
            {success_action}
        }} else if (d <= 2) {{
            {success_action}
            inp.classList.add('correct-fuzzy');
            inp.style.borderColor = '#ca8a04';
            let fz = document.createElement('span');
            fz.className = 'fuzzy-note';
            fz.style.color = '#ca8a04';
            fz.style.fontSize = '0.85rem';
            fz.style.marginLeft = '8px';
            fz.textContent = `Goed! Let op de spelling: ${{{base_correct}}}`;
            inp.parentNode.insertBefore(fz, inp.nextSibling);
        }} {else_block}
        """.strip()
        
    # Apply the generic one (we revert back to content to start fresh if we didn't apply pattern 1 before)
    new_content, count_invul = pattern_invul_generic.subn(repl_invul_generic, content)
    if count_invul > 0:
        made_changes = True

    # PATTERN 2: The checkSentence style in A1 files
    pattern_sentence = re.compile(
        r"if\s*\(\s*val\s*===\s*answer\.toLowerCase\(\)\s*\)\s*\{\s*fb\.textContent\s*=\s*(T\[currentLang\]\.fbCorrect)[^}]+\}\s*else\s*\{([^}]+)\}"
    )

    def repl_sentence(match):
        fb_correct = match.group(1)
        else_block = match.group(2)
        
        return f"""
        let d = levenshtein(val, answer.toLowerCase());
        if (d === 0) {{
            fb.textContent = {fb_correct};
            fb.className = 'sentence-feedback show correct';
            input.style.borderColor = 'var(--accent-green)';
        }} else if (d <= 2) {{
            fb.textContent = `Goed! Let op de spelling: ${{answer}}`;
            fb.className = 'sentence-feedback show correct-fuzzy';
            fb.style.color = '#ca8a04';
            input.style.borderColor = '#ca8a04';
        }} else {{
            {else_block.strip()}
        }}
        """.strip()
        
    new_content, count_sent = pattern_sentence.subn(repl_sentence, new_content)
    if count_sent > 0:
        made_changes = True

    # PATTERN 3: Losse Oefeningen / zinsbouw.html and zinsbouw_v2.html
    # if (val === ans.toLowerCase() || val === ans.toLowerCase() + '.')
    # Actually wait, let's search for how zinsbouw.html checks it!
    # I'll let that be for now, just apply the general levenshtein logic.

    if made_changes and not already_injected:
        new_content = re.sub(r'<script>', f'<script>\n{LEVENSHTEIN_JS}', new_content, count=1)
        
    if made_changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    base_directory = r"g:\Mijn Drive\HTML FILES"
    files = get_html_files(base_directory)
    updated_count = 0
    for f in files:
        try:
            if process_file(f):
                updated_count += 1
                print(f"Updated {f}")
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    print(f"Total files updated: {updated_count}")
