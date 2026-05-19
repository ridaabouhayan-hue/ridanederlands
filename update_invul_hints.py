import os
import re

def get_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def update_invul_feedback(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The previous injection in checkInvul for fuzzy matching looks like:
    # } else {
    #    inp.classList.add('fout');
    # }
    
    # We want to replace it with:
    # } else {
    #    inp.classList.add('fout');
    #    let existingWr = inp.nextElementSibling;
    #    if (existingWr && existingWr.className === 'wrong-note') existingWr.remove();
    #    let ansSpan = document.createElement('span');
    #    ansSpan.className = 'wrong-note';
    #    ansSpan.style.color = '#e63946';
    #    ansSpan.style.fontSize = '0.85rem';
    #    ansSpan.style.marginLeft = '8px';
    #    ansSpan.innerHTML = `(Antwoord: ${item.ant || item.a || item.ans || item.mv}` + (item.hint ? ' — Tip: ' + item.hint : '') + ')';
    #    inp.parentNode.insertBefore(ansSpan, inp.nextSibling);
    # }
    
    # Wait, the variable for the correct answer was captured in item.ant etc.
    # In my previous python script I did:
    # let d = levenshtein(..., item.ant);
    # Let's search for the else block.
    # We will search for:
    # \} else \{\s*inp\.classList\.add\('fout'\);\s*\}
    # And we'll replace it with the new logic. BUT we need the correct answer variable.
    # The correct answer variable is usually `item.ant`, `item.a`, `item.mv`, `item.ans`.
    # I can just use `(item.ant || item.a || item.ans || item.mv)`.
    
    pattern = re.compile(
        r"\} else \{\s*inp\.classList\.add\('fout'\);\s*\}"
    )

    replacement = r"""} else {
            inp.classList.add('fout');
            let existingWr = inp.nextElementSibling;
            if (existingWr && existingWr.className === 'wrong-note') existingWr.remove();
            let ansSpan = document.createElement('span');
            ansSpan.className = 'wrong-note';
            ansSpan.style.color = '#e63946';
            ansSpan.style.fontSize = '0.85rem';
            ansSpan.style.marginLeft = '8px';
            let correctAns = item.ant || item.a || item.ans || item.mv || '...';
            if(typeof correctAns === 'string') correctAns = correctAns.replace(/\.toLowerCase\(\)/g, '');
            ansSpan.innerHTML = `(Antwoord: ${correctAns}` + (item.hint ? ' — Tip: ' + item.hint : '') + ')';
            inp.parentNode.insertBefore(ansSpan, inp.nextSibling);
        }"""

    new_content, count = pattern.subn(replacement, content)
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
        if update_invul_feedback(f):
            updated_count += 1
            print(f"Updated {f}")
            
    print(f"Total files updated: {updated_count}")
