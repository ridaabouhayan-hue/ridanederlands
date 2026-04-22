import re

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'r', encoding='utf-8') as f:
    html = f.read()

def repl(m):
    # Find preceding text to determine if it's the back or next button
    start_search = max(0, m.start() - 40)
    preceding = html[start_search:m.start()]
    if 'btn-sec' in preceding or '←' in preceding or 'Vorig' in preceding:
        return 'onclick="prevLoc()"'
    else:
        return 'onclick="nextLoc()"'

new_html = re.sub(r'onclick="goTo\(\d+\)"', repl, html)

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Done replacing goTo with prevLoc/nextLoc!")
