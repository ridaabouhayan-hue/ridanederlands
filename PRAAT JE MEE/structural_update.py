import re

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update navigation to nextLoc() / prevLoc() globally (we already did this, but let's be sure nothing is missed)
# Wait, my fix_goto.py script had an error in regex `goTo(\d+)`. Let's do it forcefully:
html = re.sub(r'onclick="goTo\(\d+\)"', 'onclick="nextLoc()"', html) # I'll override this below using context

def fix_goto(match):
    m = match.group(0)
    start_idx = max(0, match.start() - 30)
    if 'sec' in html[start_idx:match.start()]:
        return 'onclick="prevLoc()"'
    return 'onclick="nextLoc()"'

# But I already replaced it! Let's just fix it if it's there.
html = re.sub(r'onclick="goTo\(\d+\)"', fix_goto, html)


# 2. Add bottom-dots to HTML after progress-wrap
if '<div class="global-bottom-dots"' not in html:
    html = html.replace('</head>', '''<style>
.global-bottom-dots { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin:10px auto 40px; padding:0 15px; max-width:600px; }
.b-dot { width:38px; height:38px; border-radius:50%; background:white; border:2px solid #ddd; display:flex; align-items:center; justify-content:center; font-size:1.1rem; cursor:pointer; box-shadow:0 3px 6px rgba(0,0,0,0.05); transition:all 0.2s; }
.b-dot.active { background:#FFF3E0; border-color:var(--accent); transform:scale(1.15); box-shadow:0 4px 12px rgba(244,166,20,0.3); z-index:2;}
.b-dot.done { background:#F0FFF5; border-color:var(--green); opacity:0.8; }
.b-dot:active { transform:scale(0.95); }
</style>
</head>''')
    
    html = html.replace('</body>', '<div class="global-bottom-dots" id="bottom-dots"></div>\n</body>')

# 3. Update buildDots JS
dots_js = '''
const bottomNavEmojis = ["👋","🗣️","✍️","📖","🧩","📝","🧩","💬","🧐","🤔","✍️","📝","👥","🎙️","🎉"];

function buildDots(){
  const tDots=document.getElementById('step-dots');
  const bDots=document.getElementById('bottom-dots');
  if(tDots) tDots.innerHTML='';
  if(bDots) bDots.innerHTML='';
  const screens=document.querySelectorAll('.screen');
  const total=screens.length;
  document.getElementById('progress-fill').style.width=((currentIndex/(total-1))*100)+'%';
  for(let i=0;i<total;i++){
    if(tDots){
      const d=document.createElement('div');
      d.className='step-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      tDots.appendChild(d);
    }
    if(bDots){
      const bd=document.createElement('button');
      bd.className='b-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      bd.textContent=bottomNavEmojis[i] || "🔹";
      bd.onclick=()=>{ currentIndex=i; updateUI(); scroll(0,0); };
      bDots.appendChild(bd);
    }
  }
}
'''
html = re.sub(r'function buildDots\(\)\{.*?(?=function \w+\()', dots_js, html, flags=re.DOTALL)


# 4. Splitting step 4
old_s4 = '''<!-- S4: WOORDENTRAINING -->
<div class="screen" id="screen-4">
  <div class="step-header">
    <div class="step-num" id="s3-num">Stap 4 van 13 · Woordentraining</div>
    <div class="step-title" id="s3-title">Ken jij de woorden? 🧠</div>
    <div class="step-desc" id="s3-desc">Oefen de woorden. Maak geen fouten! Als je een fout maakt, begin je opnieuw.</div>
  </div>
  <div id="drill-container"></div>
  <div class="nav-area">
    <button class="btn-sec" onclick="prevLoc()">←</button>
    <button class="btn-main" onclick="nextLoc()" id="s3-next">Volgende stap →</button>
  </div>
</div>'''

new_s4 = '''<!-- S4a: WOORDENTRAINING -->
<div class="screen" id="screen-4a">
  <div class="step-header">
    <div class="step-num" id="s4a-num">Stap 4 van 15</div>
    <div class="step-title" id="s4a-title">Wat betekent dit? 📖</div>
    <div class="step-desc" id="s4a-desc">Kies de juiste betekenis.</div>
  </div>
  <div class="drill-container-wrap"></div>
  <div class="nav-area"><button class="btn-sec" onclick="prevLoc()">←</button><button class="btn-main" onclick="nextLoc()">Volgende stap →</button></div>
</div>

<!-- S4b: WOORDENTRAINING -->
<div class="screen" id="screen-4b">
  <div class="step-header">
    <div class="step-num" id="s4b-num">Stap 5 van 15</div>
    <div class="step-title" id="s4b-title">Welk woord past? 🧩</div>
    <div class="step-desc" id="s4b-desc">Kies het juiste Nederlandse woord.</div>
  </div>
  <div class="drill-container-wrap"></div>
  <div class="nav-area"><button class="btn-sec" onclick="prevLoc()">←</button><button class="btn-main" onclick="nextLoc()">Volgende stap →</button></div>
</div>

<!-- S4c: WOORDENTRAINING -->
<div class="screen" id="screen-4c">
  <div class="step-header">
    <div class="step-num" id="s4c-num">Stap 6 van 15</div>
    <div class="step-title" id="s4c-title">Schrijf het woord 📝</div>
    <div class="step-desc" id="s4c-desc">Typ het Nederlandse woord. Foutloos!</div>
  </div>
  <div class="drill-container-wrap"></div>
  <div class="nav-area"><button class="btn-sec" onclick="prevLoc()">←</button><button class="btn-main" onclick="nextLoc()">Volgende stap →</button></div>
</div>'''

if 'id="screen-4a"' not in html:
    html = html.replace(old_s4, new_s4)

# Update initDrill/renderDrill to use drill-container-wrap
html = html.replace("const c=document.getElementById('drill-container');", "const s = document.querySelectorAll('.screen')[currentIndex]; const c=s.querySelector('.drill-container-wrap'); if(!c) return;")
# Remove tabs logic from renderDrill
html = re.sub(r"const tabs=document\.createElement\('div'\); tabs\.style='display:flex[^<]+c\.appendChild\(tabs\);", '', html)

# 5. Injection logic for updateTexts to fix T dynamic numbers
dynamic_t = '''
function updateTexts(){
  if (!window.T_adjusted) {
    Object.keys(T).forEach(l => {
      Object.keys(T[l]).forEach(k => {
        if(k.match(/num$/)) {
          let str = T[l][k].replace(/13/g, '15');
          str = str.replace(/\d+/, m => {
             let n = parseInt(m);
             return (n >= 5 && n <= 13) ? (n + 2) : n;
          });
          T[l][k] = str;
        }
      });
      T[l]['s4anum'] = T[l]['s3num'].replace(/\d+/, '4'); // just base step num
      T[l]['s4bnum'] = T[l]['s3num'].replace(/\d+/, '5');
      T[l]['s4cnum'] = T[l]['s3num'].replace(/\d+/, '6');
    });
    window.T_adjusted = true;
  }
'''
html = html.replace('function updateTexts(){', dynamic_t)

# 6. Revert check in ConvOrder
html = html.replace("if(document.querySelectorAll('#conv-slots .order-slot:not(.has-content)').length===0) checkConv();", "")
# Restore the checkbtn in buildConv
html = html.replace("const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='conv-fb'; c.appendChild(fb);", "const chk=document.createElement('button'); chk.className='btn-check'; chk.textContent=t('checkBtn'); chk.onclick=checkConv; c.appendChild(chk); const fb=document.createElement('div'); fb.className='feedback-box'; fb.id='conv-fb'; c.appendChild(fb);")
# Change initConv to buildConv in reset button
html = html.replace("rb.onclick=initConv; c.appendChild(rb);", "rb.onclick=buildConv; c.appendChild(rb);")

# 7. Update updateUI routing
updateui_old = '''  if(screens[currentIndex].id==='s4') { initDrill(); }
  if(screens[currentIndex].id==='s3b') { copyIdx=0; initCopyDrill(); }
  if(screens[currentIndex].id==='screen-5') { initSort(); }
  if(screens[currentIndex].id==='screen-6') { initConv(); }'''

html = html.replace("if(screens[currentIndex].id==='screen-4') { initDrill(); }", "")
html = html.replace("if(screens[currentIndex].id==='screen-4a') { drillMode='mc_meaning'; initDrill(); }", "")
html = html.replace("if(screens[currentIndex].id==='screen-4b') { drillMode='mc_reverse'; initDrill(); }", "")
html = html.replace("if(screens[currentIndex].id==='screen-4c') { drillMode='write'; initDrill(); }", "")

updateui_new = '''  const sid = screens[currentIndex].id;
  if(sid==='screen-4a') { drillMode='mc_meaning'; initDrill(); }
  if(sid==='screen-4b') { drillMode='mc_reverse'; initDrill(); }
  if(sid==='screen-4c') { drillMode='write'; initDrill(); }
  if(sid==='screen-3') { copyIdx=0; initCopyDrill(); }
  if(sid==='screen-5') { initSort(); }
  if(sid==='screen-6') { initConv(); }
'''
# I will use a clean block replacement for updateUI:
# Actually wait, `thema-8-1-2ster.html` currently has:
# `if(screens[currentIndex].id==='screen-4') initDrill();` 

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'w', encoding='utf-8') as f:
    f.write(html)
