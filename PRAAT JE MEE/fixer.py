import re

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update emojis to numbers
html = html.replace('bd.textContent=bottomNavEmojis[i] || "🔹";', 'bd.textContent=(i+1);')
html = html.replace('font-size:1.1rem;', 'font-size:1.0rem; font-weight:900;')

# 2. Fix the next buttons
# Both btn-main and btn-sec shouldn't all be prevLoc. btn-main should be nextLoc!
html = html.replace('<button class="btn-main" onclick="prevLoc()"', '<button class="btn-main" onclick="nextLoc()"')

# 3. Fix Step 4 missing content
# initDrill returns early if `c` is missing.
# Wait! In updateUI():
# if(sid==='screen-4a') { drillMode='mc_meaning'; initDrill(); }
# BUT the IDs in the divs might be <div class="screen" id="screen-4a">
# Let's verify what `c` is selected:
# const s = document.querySelectorAll('.screen')[currentIndex]; const c=s.querySelector('.drill-container-wrap');

# Wait! Does step 4a have a .drill-container-wrap?
# In my new_s4 HTML:
# <div class="screen" id="screen-4a"> ... <div class="drill-container-wrap"></div> ... 
# Yes, it has it!
# WHY would it fail?
# Because `updateUI` did NOT correctly map `sid==='screen-4a'`.
# Let's check updateUI in the file currently!

with open('fixer_debug.txt', 'w', encoding='utf-8') as d:
    m = re.search(r'function updateUI\(\).*?\}', html, re.DOTALL)
    d.write(m.group(0))

# 4. In my previous script I mistakenly deleted the whole updateUI routing!
# updateui_old = "..."
# html = html.replace("if(screens[currentIndex].id==='screen-4a')...", "")
# It MUST BE:
updateui_routing_fix = '''  const act = screens[currentIndex];
  if(act.id==='screen-4a') { drillMode='mc_meaning'; initDrill(); }
  else if(act.id==='screen-4b') { drillMode='mc_reverse'; initDrill(); }
  else if(act.id==='screen-4c') { drillMode='write'; initDrill(); }
  else if(act.id==='screen-3') { copyIdx=0; initCopyDrill(); }
  else if(act.id==='screen-5') { initSort(); }
  else if(act.id==='screen-6') { initConv(); }
  else if(act.id==='screen-7') { initQ5a(); }
  else if(act.id==='screen-8') { initQ5b(); }
  else if(act.id==='screen-10') { initConvFill(); }'''

html = re.sub(r'const act = screens\[currentIndex\];.*?(?=window\.scrollTo)', updateui_routing_fix + '\n  ', html, flags=re.DOTALL)

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done via fixer.py")
