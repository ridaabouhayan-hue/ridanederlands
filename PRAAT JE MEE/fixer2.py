import re

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix NEXT BUTTONS ALWAYS
html = html.replace('<button class="btn-main" onclick="prevLoc()"', '<button class="btn-main" onclick="nextLoc()"')

# Insert CSS for bottom-dots if missing
if 'global-bottom-dots' not in html:
    html = html.replace('</head>', '''<style>
.global-bottom-dots { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin:10px auto 40px; padding:0 15px; max-width:600px; }
.b-dot { width:38px; height:38px; border-radius:50%; background:white; border:2px solid #ddd; display:flex; align-items:center; justify-content:center; font-size:1.0rem; font-weight:900; cursor:pointer; box-shadow:0 3px 6px rgba(0,0,0,0.05); transition:all 0.2s; }
.b-dot.active { background:#FFF3E0; border-color:var(--accent); transform:scale(1.15); box-shadow:0 4px 12px rgba(244,166,20,0.3); z-index:2;}
.b-dot.done { background:#F0FFF5; border-color:var(--green); opacity:0.8; }
.b-dot:active { transform:scale(0.95); }
</style>
</head>''')
    html = html.replace('</body>', '<div class="global-bottom-dots" id="bottom-dots"></div>\n</body>')

# Replace buildDots to include bottom dots logic
dots_js = '''function buildDots(){
  const tDots=document.getElementById('step-dots');
  const bDots=document.getElementById('bottom-dots');
  if(tDots) tDots.innerHTML='';
  if(bDots) bDots.innerHTML='';
  const screens=document.querySelectorAll('.screen');
  const total=screens.length;
  for(let i=0;i<total;i++){
    if(tDots){
      const d=document.createElement('div');
      d.className='step-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      tDots.appendChild(d);
    }
    if(bDots){
      const bd=document.createElement('button');
      bd.className='b-dot'+(i===currentIndex?' active':i<currentIndex?' done':'');
      bd.textContent=(i+1);
      bd.onclick=()=>{ currentIndex=i; updateUI(); scroll(0,0); };
      bDots.appendChild(bd);
    }
  }
}
function speak'''

html = re.sub(r'function buildDots\(\).*?function speak', dots_js, html, flags=re.DOTALL)

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done fixer2")
