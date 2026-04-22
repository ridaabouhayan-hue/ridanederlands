import sys
import re

files = [
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-3ster.html"
]

def patch_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # --- 1. Fix answerDrill auto-advance ---
    old_answer_drill = """function answerDrill(el,correct,speakText,written,correctWritten){
  const fb=document.getElementById('drill-fb');
  if(correct){
    drillCorrect++;
    drillCurrent++;
    fb.className='feedback-box show';
    fb.textContent=t('drillCorrectMsg');
    speak(speakText);
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    setTimeout(renderDrill,900);
  } else {
    fb.className='feedback-box show wrong-fb';
    fb.textContent=t('drillWrongMsg')+(correctWritten?` ✔ ${correctWritten}`:'');
    if(el.classList.contains('drill-opt')) el.classList.add('wrong');
    document.querySelectorAll('.drill-opt').forEach(b=>{
      if(b.textContent===(correctWritten||'___')) b.classList.add('correct');
    });
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    // reset queue from scratch
    setTimeout(()=>{ drillQueue=shuffle(wordsData.map((_,i)=>i)); drillCurrent=0; drillCorrect=0; renderDrill(); },1400);
  }
}"""
    
    new_answer_drill = """function answerDrill(el,correct,speakText,written,correctWritten){
  const fb=document.getElementById('drill-fb');
  const card=fb.parentElement;
  if(correct){
    drillCorrect++;
    drillCurrent++;
    fb.className='feedback-box show';
    fb.textContent=t('drillCorrectMsg');
    speak(speakText);
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    if(el.classList.contains('btn-check')) el.style.display='none';
    const nxt=document.createElement('button');
    nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;';
    nxt.textContent=typeof t('nextSentence')==='string'?t('nextSentence').replace('→','').trim()+' →':'Volgende →';
    nxt.onclick=renderDrill;
    card.appendChild(nxt);
  } else {
    fb.className='feedback-box show wrong-fb';
    fb.textContent=t('drillWrongMsg')+(correctWritten?` ✔ ${correctWritten}`:'');
    if(el.classList.contains('drill-opt')) el.classList.add('wrong');
    document.querySelectorAll('.drill-opt').forEach(b=>{
      if(b.textContent===(correctWritten||'___')) b.classList.add('correct');
    });
    document.querySelectorAll('.drill-opt,.btn-check').forEach(b=>b.onclick=null);
    if(el.classList.contains('btn-check')) el.style.display='none';
    const nxt=document.createElement('button');
    nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;background-color:var(--red);color:white;';
    nxt.textContent=t('resetBtn');
    nxt.onclick=()=>{ drillQueue=shuffle(wordsData.map((_,i)=>i)); drillCurrent=0; drillCorrect=0; renderDrill(); };
    card.appendChild(nxt);
  }
}"""

    html = html.replace(old_answer_drill, new_answer_drill)


    # --- 2. Fix renderCopyDrill auto-advance ---
    old_copy_drill_success = """    if(ok){
      fb.textContent = t('drillCorrectMsg');
      speak(phrase);
      inp.disabled = true;
      checkBtn.disabled = true;
      setTimeout(() => { copyIdx++; renderCopyDrill(); }, 900);
    } else {"""

    new_copy_drill_success = """    if(ok){
      fb.textContent = t('drillCorrectMsg');
      speak(phrase);
      inp.disabled = true;
      checkBtn.style.display = 'none';
      const nxt=document.createElement('button');
      nxt.className='btn-main'; nxt.style='margin-top:10px;width:100%;';
      nxt.textContent=typeof t('nextSentence')==='string'?t('nextSentence').replace('→','').trim()+' →':'Volgende →';
      nxt.onclick=()=>{ copyIdx++; renderCopyDrill(); };
      card.appendChild(nxt);
    } else {"""
    
    html = html.replace(old_copy_drill_success, new_copy_drill_success)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

for fpath in files:
    patch_file(fpath)
    print("Patched auto-advance logic in", fpath)
