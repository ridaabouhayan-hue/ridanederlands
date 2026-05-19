import re
import os

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

def update_zinsbouw(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    already_injected = 'function levenshtein(' in content
    
    # if(val.toLowerCase()===ans.toLowerCase()){fb.className='dd-feedback ok';fb.textContent='✓ '+(lang==='nl'?'Goed!':'Dobrze!');input.style.borderColor='var(--success)'}
    # else{fb.className='dd-feedback no';fb.textContent='✗ '+(lang==='nl'?'Fout!':'Błąd!');input.style.borderColor='var(--error)'}
    
    # We will search for this exact block.
    pattern = re.compile(
        r"if\s*\(\s*val\.toLowerCase\(\)\s*===\s*ans\.toLowerCase\(\)\s*\)\s*\{([^}]+)\}\s*else\s*\{([^}]+)\}"
    )

    def repl(match):
        success_block = match.group(1)
        fail_block = match.group(2)
        return f"""
        let d = levenshtein(val.toLowerCase(), ans.toLowerCase());
        if (d === 0) {{
            {success_block.strip()}
        }} else if (d <= 2) {{
            fb.className = 'dd-feedback ok';
            fb.textContent = '✓ Goed! Let op de spelling: ' + ans;
            fb.style.color = '#ca8a04';
            input.style.borderColor = '#ca8a04';
        }} else {{
            {fail_block.strip()}
            fb.style.color = '';
        }}
        """.strip()

    new_content, count = pattern.subn(repl, content)
    if count > 0:
        if not already_injected:
            new_content = re.sub(r'<script>', f'<script>\n{LEVENSHTEIN_JS}', new_content, count=1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} ({count} replacements)")
    else:
        print(f"No replacements in {filepath}")

update_zinsbouw(r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\zinsbouw_v2.html")
