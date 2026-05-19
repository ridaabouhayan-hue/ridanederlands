import re
filepath = r'g:\Mijn Drive\HTML FILES\Losse Oefeningen\zinsbouw_v2.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

drag_replacements = [
    ('answer:"Ik werk elke dag in de fabriek"', 'answer:"Ik werk elke dag in de fabriek", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
    ('answer:"Zij spreekt drie talen op het werk"', 'answer:"Zij spreekt drie talen op het werk", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
    ('answer:"Wij hebben pauze om 12 uur"', 'answer:"Wij hebben pauze om 12 uur", hint:{nl:"Tijd (om 12 uur) komt na het object.", pl:"Czas po obiekcie."}'),
    ('answer:"Hij wil supervisor worden"', 'answer:"Hij wil supervisor worden", hint:{nl:"Tweede werkwoord (worden) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
    ('answer:"Ik moet morgen vroeg werken"', 'answer:"Ik moet morgen vroeg werken", hint:{nl:"Tweede werkwoord (werken) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
    ('answer:"De levering komt vandaag niet"', 'answer:"De levering komt vandaag niet", hint:{nl:"Niet staat achteraan in de zin.", pl:"Niet stoi na końcu."}'),
    ('answer:"Zij kan goed Nederlands spreken"', 'answer:"Zij kan goed Nederlands spreken", hint:{nl:"Tweede werkwoord (spreken) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
    ('answer:"De voorman controleert de machine"', 'answer:"De voorman controleert de machine", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
    ('answer:"Wij kunnen de bestelling versturen"', 'answer:"Wij kunnen de bestelling versturen", hint:{nl:"Tweede werkwoord (versturen) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
    ('answer:"Hij gaat volgend jaar de supervisor opvolgen"', 'answer:"Hij gaat volgend jaar de supervisor opvolgen", hint:{nl:"Tweede werkwoord (opvolgen) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
    ('answer:"Waar werk jij vandaag"', 'answer:"Waar werk jij vandaag", hint:{nl:"Vraagwoord (waar) + werkwoord + onderwerp.", pl:"Słowo pytające + czasownik + podmiot."}'),
    ('answer:"Heb je pauze om 12 uur"', 'answer:"Heb je pauze om 12 uur", hint:{nl:"Ja/nee vraag begint met het werkwoord.", pl:"Pytanie tak/nie zaczyna się od czasownika."}'),
    ('answer:"Ik heb geen tijd vandaag"', 'answer:"Ik heb geen tijd vandaag", hint:{nl:"Gebruik geen voor het zelfstandig naamwoord.", pl:"Użyj geen przed rzeczownikiem."}'),
    ('answer:"Hij werkt niet op de expeditie"', 'answer:"Hij werkt niet op de expeditie", hint:{nl:"Niet staat voor de plaats.", pl:"Niet stoi przed miejscem."}')
]

for old, new in drag_replacements:
    content = content.replace(old, new)

schrijf_replacements = [
  ('answer:"Hij werkt in het magazijn"', 'answer:"Hij werkt in het magazijn", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
  ('answer:"Ik heb twee kinderen"', 'answer:"Ik heb twee kinderen", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
  ('answer:"Zij wil Nederlands leren"', 'answer:"Zij wil Nederlands leren", hint:{nl:"Tweede werkwoord (leren) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
  ('answer:"De machine is vandaag kapot"', 'answer:"De machine is vandaag kapot", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
  ('answer:"Hij moet de collega\'s aansturen"', 'answer:"Hij moet de collega\'s aansturen", hint:{nl:"Tweede werkwoord (aansturen) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
  ('answer:"Zij heeft een nieuwe bestelling"', 'answer:"Zij heeft een nieuwe bestelling", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
  ('answer:"Wij kunnen morgen beginnen"', 'answer:"Wij kunnen morgen beginnen", hint:{nl:"Tweede werkwoord (beginnen) staat achteraan.", pl:"Drugi czasownik na końcu."}'),
  ('answer:"Ik stuur het pakket naar de klant"', 'answer:"Ik stuur het pakket naar de klant", hint:{nl:"Werkwoord op positie 2.", pl:"Czasownik na pozycji 2."}'),
  ('answer:"Waarom is de vrachtwagen laat"', 'answer:"Waarom is de vrachtwagen laat", hint:{nl:"Vraagwoord + werkwoord + onderwerp.", pl:"Słowo pytające + czasownik + podmiot."}'),
  ('answer:"Ik werk vandaag niet in de productie"', 'answer:"Ik werk vandaag niet in de productie", hint:{nl:"Niet staat voor de plaats.", pl:"Niet stoi przed miejscem."}')
]
for old, new in schrijf_replacements:
    content = content.replace(old, new)

# Update drag logic
content = re.sub(
    r"fb\.textContent='✗ '\+\(lang==='nl'\?'Antwoord: ':'Odpowiedź: '\)\+item\.answer",
    "fb.innerHTML='✗ '+(lang==='nl'?'Antwoord: ':'Odpowiedź: ')+item.answer + (item.hint ? '<br><span style=\"color:var(--accent2);font-size:0.85rem\">💡 Tip: ' + item.hint[lang] + '</span>' : '')",
    content
)

# Update schrijf logic
# Wait, for schrijf, the checking is inside checkSchrijf(val, ans, fb, input). BUT in zinsbouw_v2 it's inline in buildSchrijfExercises.
# } else { fb.className = 'dd-feedback no'; fb.textContent = '✗ ' + (lang === 'nl' ? 'Fout!' : 'Błąd!'); input.style.borderColor = 'var(--error)' }
content = re.sub(
    r"\} else \{\s*fb\.className = 'dd-feedback no';\s*fb\.textContent = '✗ ' \+ \(lang === 'nl' \? 'Fout!' : 'Błąd!'\);\s*fb\.style\.color = '';",
    "} else { fb.className = 'dd-feedback no'; fb.innerHTML = '✗ ' + (lang === 'nl' ? 'Fout! Antwoord: ' : 'Błąd! Odpowiedź: ') + ans + (item.hint ? '<br><span style=\"color:var(--accent2);font-size:0.85rem\">💡 Tip: ' + item.hint[lang] + '</span>' : ''); fb.style.color = '';",
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated datasets in zinsbouw_v2.html")
