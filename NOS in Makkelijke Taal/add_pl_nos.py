import re
import os

file_path = r"g:\Mijn Drive\HTML FILES\NOS in Makkelijke Taal\transcript_nos_11mei.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Polish button if it doesn't exist
if '<button class="lang-btn" data-lang="pl">🇵🇱 PL</button>' not in content:
    button_html = '        <button class="lang-btn" data-lang="pl">🇵🇱 PL</button>\n    </div>'
    content = content.replace('    </div>\n\n    <!-- HEADER & VIDEO -->', button_html + '\n\n    <!-- HEADER & VIDEO -->')
    
    # Wait, the closing div has a specific format. Let's do a more robust replace:
    content = re.sub(
        r'(<button class="lang-btn" data-lang="vi">🇻🇳 VN</button>\s*)</div>',
        r'\1<button class="lang-btn" data-lang="pl">🇵🇱 PL</button>\n    </div>',
        content
    )

pl_dict = {
    "situations": "sytuacje",
    "railway track": "tory kolejowe",
    "island": "wyspa",
    "harbor / port": "port",
    "to repair": "naprawiać",
    "climate change": "zmiana klimatu",
    "to cross": "przechodzić / przekraczać",
    "life-threatening": "zagrażający życiu",
    "organization": "organizacja",
    "safety": "bezpieczeństwo",
    "campaign / action": "kampania / akcja",
    "short videos / clips": "krótkie filmy",
    "to warn": "ostrzegać",
    "hurry / rush": "pośpiech",
    "to blink / flash": "migać",
    "dangerous": "niebezpieczny",
    "footage / images": "nagrania / obrazy",
    "train driver": "maszynista",
    "more careful": "bardziej ostrożny",
    "to get scared / be startled": "przestraszyć się",
    "railway crossing": "przejazd kolejowy",
    "student": "uczeń",
    "sensible / smart": "rozsądny",
    "government": "rząd",
    "maintenance": "konserwacja",
    "collapsed / sunken": "zapadnięty / zawalony",
    "municipality": "gmina",
    "overloaded": "przeciążony",
    "closed off / blocked": "zamknięty / zablokowany",
    "accessible": "dostępny",
    "repair": "naprawa",
    "residents": "mieszkańcy",
    "tropical": "tropikalny",
    "coral reefs": "rafy koralowe",
    "extreme": "ekstremalny",
    "floods": "powodzie",
    "judge": "sędzia",
    "to protect": "chronić",
    "colorful": "kolorowy",
    "to disappear": "znikać",
    "tourists": "turyści",
    "diving schools": "szkoły nurkowania",
    "administrators / governors": "administratorzy / zarządcy",
    "obvious / goes without saying": "oczywisty",
    "to act / intervene": "działać / interweniować",
    "cloudy": "pochmurnie",
    "rain": "deszcz"
}

def replace_vocab(match):
    full_match = match.group(0)
    en_val = match.group(1)
    if 'data-pl=' in full_match:
        return full_match
    
    pl_val = pl_dict.get(en_val, en_val)
    # Insert data-pl before the closing >
    # The match is the entire opening tag <span class="vocab" ...>
    # Find the last > and insert there
    idx = full_match.rfind('>')
    if idx != -1:
        return full_match[:idx] + f' data-pl="{pl_val}">' + full_match[idx+1:]
    return full_match

# Regex to match the span and capture the data-en value
pattern = re.compile(r'<span class="vocab"[^>]*data-en="([^"]+)"[^>]*>')
new_content = pattern.sub(replace_vocab, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Polish translations added!")
