import os
import re

def get_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

inj = "try{localStorage.setItem('completed_' + location.pathname.split('/').pop(), 'true');}catch(e){}"

def inject_progress(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it's the index.html, we just add the reading script
    if filepath.endswith("index.html") or filepath.endswith("index_test.html"):
        if '<!-- PROGRESS INJECTION -->' in content:
            return False
            
        script = """
<!-- PROGRESS INJECTION -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a').forEach(a => {
        try {
            let href = a.getAttribute('href');
            if (href && !href.startsWith('http')) {
                let filename = href.split('/').pop();
                if (localStorage.getItem('completed_' + filename) === 'true') {
                    a.innerHTML += ' <span style="font-size:0.95rem;margin-left:6px;" title="Voltooid">✅</span>';
                }
            }
        } catch(e){}
    });
});
</script>
<!-- /PROGRESS INJECTION -->
"""
        new_content = content.replace('</body>', script + '\n</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    # For other files, we inject `inj` in success branches
    original = content

    # 1. checkDragItem
    # if(ok){res.textContent='🎉 Goed! '
    content = re.sub(
        r"if\s*\(\s*ok\s*\)\s*\{\s*res\.textContent\s*=\s*'🎉 Goed!",
        f"if(ok){{{inj}res.textContent='🎉 Goed!",
        content
    )

    # 2. checkInvul
    # (g===invulData.length?'score-goed':g>=7?'score-midden':'score-slecht')
    # Actually, let's just replace:
    # const sc=document.getElementById('invul-score');
    # with:
    # if(g===invulData.length) { inj } const sc=...
    content = re.sub(
        r"const\s+sc\s*=\s*document\.getElementById\('invul-score'\);",
        f"if(g===invulData.length){{{inj}}} const sc=document.getElementById('invul-score');",
        content
    )

    # 3. checkMCq
    # _mc_state[key].done++;
    # const total = total;
    # if(_mc_state[key].done===total){ sc.style.display='inline-block' ... }
    # Let's replace:
    # if(_mc_state[key].done===total) {
    content = re.sub(
        r"if\s*\(\s*_mc_state\[key\]\.done\s*===\s*total\s*\)\s*\{",
        f"if(_mc_state[key].done===total){{{inj}",
        content
    )

    # 4. checkSentence
    # if (d === 0) { ... } else if (d <= 2) { ... }
    content = re.sub(
        r"if\s*\(\s*d\s*===\s*0\s*\)\s*\{",
        f"if(d===0){{{inj}",
        content
    )
    content = re.sub(
        r"\} else if \(\s*d\s*<=\s*2\s*\)\s*\{",
        f"}} else if (d <= 2) {{{inj}",
        content
    )
    
    # 5. checkQuiz in zinsbouw_v2 and zinsbouw
    # if(quizAnswered===10)
    content = re.sub(
        r"if\s*\(\s*quizAnswered\s*===\s*10\s*\)\s*\{",
        f"if(quizAnswered===10){{{inj}",
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    base_directory = r"g:\Mijn Drive\HTML FILES"
    files = get_html_files(base_directory)
    updated_count = 0
    for f in files:
        if inject_progress(f):
            updated_count += 1
            print(f"Updated {f}")
            
    print(f"Total files updated: {updated_count}")
