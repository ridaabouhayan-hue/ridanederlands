import os
import re

def process_file(filepath):
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if it's zinsbouw.html (checkQuizAnswer) or zinsbouw_v2.html (checkQuiz)
    func_name = 'checkQuiz' if 'checkQuiz(' in content else 'checkQuizAnswer'
    
    if func_name == 'checkQuiz':
        # Replace checkQuiz logic
        # Original:
        # function checkQuiz(qi,chosen,div){
        #   if(div.dataset.done)return;div.dataset.done='1';quizAnswered++;
        #   const labels=div.querySelectorAll('label'),fb=div.querySelector('.feedback'),correct=quizData[qi].correct;
        #   labels.forEach((l,j)=>{if(j===correct)l.classList.add('correct');if(j===chosen&&j!==correct)l.classList.add('wrong')});
        #   fb.style.display='block';
        #   if(chosen===correct){quizScore++;fb.style.background='#d4edda';fb.style.color='var(--success)';fb.textContent='✓ '+(lang==='nl'?'Goed! ':'Dobrze! ')+quizData[qi].explain[lang]}
        #   else{fb.style.background='#fde8e8';fb.style.color='var(--error)';fb.textContent='✗ '+(lang==='nl'?'Fout. ':'Źle. ')+quizData[qi].explain[lang]}
        #   document.getElementById('quizProgress').style.width=(quizAnswered/10*100)+'%';
        #   if(quizAnswered===10){document.getElementById('scoreBar').style.display='block';document.getElementById('scoreNum').textContent=quizScore+'/10'}
        # }
        
        replacement = """
function checkQuiz(qi,chosen,div){
  if(div.dataset.done === '1') return;
  let attempts = parseInt(div.dataset.attempts || '0');
  attempts++;
  div.dataset.attempts = attempts;

  const labels=div.querySelectorAll('label'),fb=div.querySelector('.feedback'),correct=quizData[qi].correct;
  labels.forEach(l => l.classList.remove('wrong'));

  if(chosen===correct){
    div.dataset.done='1';
    quizAnswered++;
    quizScore += (attempts === 1 ? 1 : 0.5);
    labels.forEach((l,j)=>{if(j===correct)l.classList.add('correct');});
    fb.style.display='block';
    fb.style.background='#d4edda';fb.style.color='var(--success)';
    fb.innerHTML='✓ '+(lang==='nl'?'Goed! ':'Dobrze! ')+quizData[qi].explain[lang];
  } else {
    labels.forEach((l,j)=>{if(j===chosen)l.classList.add('wrong');});
    fb.style.display='block';
    fb.style.background='#fde8e8';fb.style.color='var(--error)';
    
    if (attempts === 1) {
        fb.innerHTML='✗ '+(lang==='nl'?'Fout. ':'Źle. ') + '<button class="retry-btn" style="margin-left:10px;padding:4px 8px;border-radius:4px;border:none;background:var(--accent);color:white;cursor:pointer;">' + (lang==='nl'?'Probeer opnieuw':'Spróbuj ponownie') + '</button>';
        fb.querySelector('.retry-btn').onclick = function(e) {
            e.stopPropagation();
            labels.forEach(l => l.classList.remove('wrong'));
            fb.style.display = 'none';
        };
    } else {
        div.dataset.done='1';
        quizAnswered++;
        labels.forEach((l,j)=>{if(j===correct)l.classList.add('correct');});
        fb.innerHTML='✗ '+(lang==='nl'?'Fout. ':'Źle. ')+quizData[qi].explain[lang];
    }
  }

  document.getElementById('quizProgress').style.width=(quizAnswered/10*100)+'%';
  if(quizAnswered===10){document.getElementById('scoreBar').style.display='block';document.getElementById('scoreNum').textContent=quizScore+'/10'}
}
        """.strip()
        
        # We need to replace the entire function checkQuiz(...){ ... }
        # Let's use a regex that captures the function body
        pattern = re.compile(r"function checkQuiz\(qi,chosen,div\)\{.*?(?=\n// ============================|\nconst dragSentences|\nfunction buildDragExercises)", re.DOTALL)
        
        new_content, count = pattern.subn(replacement + "\n", content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

    elif func_name == 'checkQuizAnswer':
        replacement = """
function checkQuizAnswer(qi,chosen,div){
    if(div.dataset.done === '1') return;
    let attempts = parseInt(div.dataset.attempts || '0');
    attempts++;
    div.dataset.attempts = attempts;

    const labels=div.querySelectorAll('label'),fb=div.querySelector('.feedback'),correct=quizData[qi].correct;
    labels.forEach(l => l.classList.remove('wrong'));

    if(chosen===correct){
        div.dataset.done='1';
        quizAnswered++;
        quizScore += (attempts === 1 ? 1 : 0.5);
        labels.forEach((l,j)=>{if(j===correct)l.classList.add('correct');});
        fb.style.display='block';
        fb.style.background='#d4edda';fb.style.color='var(--success)';
        fb.innerHTML='✓ '+(lang==='nl'?'Goed!':'Dobrze!')+' '+quizData[qi].explain[lang];
    } else {
        labels.forEach((l,j)=>{if(j===chosen)l.classList.add('wrong');});
        fb.style.display='block';
        fb.style.background='#fde8e8';fb.style.color='var(--error)';
        
        if (attempts === 1) {
            fb.innerHTML='✗ '+(lang==='nl'?'Fout. ':'Źle. ') + '<button class="retry-btn" style="margin-left:10px;padding:4px 8px;border-radius:4px;border:none;background:var(--accent);color:white;cursor:pointer;">' + (lang==='nl'?'Probeer opnieuw':'Spróbuj ponownie') + '</button>';
            fb.querySelector('.retry-btn').onclick = function(e) {
                e.stopPropagation();
                labels.forEach(l => l.classList.remove('wrong'));
                fb.style.display = 'none';
            };
        } else {
            div.dataset.done='1';
            quizAnswered++;
            labels.forEach((l,j)=>{if(j===correct)l.classList.add('correct');});
            fb.innerHTML='✗ '+(lang==='nl'?'Fout. ':'Źle. ')+' '+quizData[qi].explain[lang];
        }
    }

    document.getElementById('quizProgress').style.width=(quizAnswered/10*100)+'%';
    if(quizAnswered===10){document.getElementById('scoreBar').style.display='block';document.getElementById('scoreNum').textContent=quizScore+'/10'}
}
        """.strip()
        
        pattern = re.compile(r"function checkQuizAnswer\(qi,chosen,div\)\{.*?(?=\n// ============================|\nconst dragSentences|\nfunction resetQuiz)", re.DOTALL)
        new_content, count = pattern.subn(replacement + "\n", content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

    return False

print(process_file(r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\zinsbouw_v2.html"))
print(process_file(r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\zinsbouw.html"))
