import re

file_path = r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded topbar
content = content.replace('van 13</div>', 'van 17</div>')

# Replace in script translations (Dutch)
content = re.sub(r"Stap (\d+) van 13", r"Stap \1 van 17", content)

# Replace in script translations (English)
content = re.sub(r"Step (\d+) of 13", r"Step \1 of 17", content)

# Replace in script translations (Turkish)
content = re.sub(r"Adım (\d+) / 13", r"Adım \1 / 17", content)

# Replace in script translations (Arabic)
content = re.sub(r"الخطوة (\d+) من 13", r"الخطوة \1 من 17", content)

# Replace in script translations (Oromo)
content = re.sub(r"Tarkaanfii (\d+) / 13", r"Tarkaanfii \1 / 17", content)

# Replace in script translations (Pashto)
content = re.sub(r"ګام (\d+) له 13", r"ګام \1 له 17", content)

# Replace in script translations (Chinese)
content = re.sub(r"第(\d+)步/共13步", r"第\1步/共17步", content)

# Replace TOTAL constant again just in case (though it was already 17)
content = re.sub(r"const TOTAL = 13;", r"const TOTAL = 17;", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")
