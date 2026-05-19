import os
import re

def get_html_files(base_dir):
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

speech_script = """
<!-- SPEECH SYNTHESIS INJECTION -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    function speakNative(text) {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'nl-NL';
        u.rate = 0.9;
        window.speechSynthesis.speak(u);
    }
    
    function createSpeakBtn(text) {
        let btn = document.createElement('button');
        btn.innerHTML = '🔊';
        btn.className = 'native-speak-btn';
        btn.style.cssText = 'background:none;border:none;cursor:pointer;font-size:1.05rem;margin-left:6px;padding:0;transition:transform 0.2s;vertical-align:middle;outline:none;box-shadow:none;';
        btn.onclick = (e) => { e.preventDefault(); e.stopPropagation(); speakNative(text); };
        btn.onmouseover = () => btn.style.transform = 'scale(1.2)';
        btn.onmouseout = () => btn.style.transform = 'scale(1)';
        return btn;
    }

    // 1. .vocab spans
    document.querySelectorAll('.vocab').forEach(el => {
        if (!el.nextElementSibling || !el.nextElementSibling.classList.contains('native-speak-btn')) {
            el.parentNode.insertBefore(createSpeakBtn(el.textContent.trim()), el.nextSibling);
        }
    });

    // 2. Conjugation tables (.conj-table, .ww-tabel)
    document.querySelectorAll('.conj-table tbody tr, .ww-tabel tbody tr').forEach(row => {
        if (row.cells.length >= 2) {
            let targetCell = row.cells[1];
            // If the target cell already has a button, skip
            if (!targetCell.querySelector('.native-speak-btn') && !targetCell.querySelector('button')) {
                targetCell.appendChild(createSpeakBtn(targetCell.textContent.trim()));
            }
        }
    });

    // 3. Example sentences (.example)
    document.querySelectorAll('.example').forEach(el => {
        if (!el.querySelector('.native-speak-btn') && !el.querySelector('button')) {
            let clone = el.cloneNode(true);
            let transl = clone.querySelector('.transl');
            if (transl) transl.remove();
            let text = clone.textContent.replace(/\\([^)]+\\)/g, '').trim();
            el.appendChild(createSpeakBtn(text));
        }
    });
});
</script>
<!-- /SPEECH SYNTHESIS INJECTION -->
"""

def inject_speech(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<!-- SPEECH SYNTHESIS INJECTION -->' in content:
        return False
        
    # Replace the Google TTS with native speech if we see function speak(text, isSlow = false)
    # Actually, we don't need to replace it if they only asked to ADD buttons to .vocab, conjugation tables, etc.
    # The new buttons will use speakNative.

    # Inject before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', speech_script + '\n</body>')
    else:
        new_content = content + speech_script

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

if __name__ == "__main__":
    base_directory = r"g:\Mijn Drive\HTML FILES"
    files = get_html_files(base_directory)
    updated_count = 0
    for f in files:
        if inject_speech(f):
            updated_count += 1
            
    print(f"Total files updated: {updated_count}")
