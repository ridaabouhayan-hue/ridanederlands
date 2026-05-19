import os
import re

def get_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def update_drag_feedback(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We look for checkDragItem
    # In A1 files:
    # else{res.textContent=count+'/'+cw.length+' woorden goed. Probeer verder!';res.className='drag-result partial';}
    
    # We want to change this so it shows the correct answer and the hint.
    # We can do this with regex.
    pattern = re.compile(
        r"else\s*\{\s*res\.textContent\s*=\s*count\s*\+\s*'/'\s*\+\s*cw\.length\s*\+\s*' woorden goed\. Probeer verder!';\s*res\.className\s*=\s*'drag-result partial';\s*\}"
    )

    def repl(match):
        return """else{
            res.innerHTML = '✗ Fout. Antwoord: <strong>' + s.words.join(' ').replace(/ \./g, '.') + '</strong>' + (s.hint ? '<br><span style="color:var(--accent-red);font-size:0.85rem">💡 Tip: ' + s.hint + '</span>' : '');
            res.className='drag-result wrong';
        }"""

    new_content, count = pattern.subn(repl, content)
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    base_directory = r"g:\Mijn Drive\HTML FILES"
    files = get_html_files(base_directory)
    updated_count = 0
    for f in files:
        if update_drag_feedback(f):
            updated_count += 1
            print(f"Updated {f}")
            
    print(f"Total files updated: {updated_count}")
