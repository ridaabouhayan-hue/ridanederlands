/* Nexus of Language — lesson player.
   Builds the step queue (dialogue intro, new-word cards, authored exercises,
   SRS-due review items) and drives hearts / XP / timer / streak / feedback
   tiers / summary around it. */

(function () {
  const params = new URLSearchParams(window.location.search);
  const unitId = params.get('u');
  const lessonId = params.get('l');

  function findUnitLesson() {
    for (const section of COURSE.sections) {
      for (const unit of section.units) {
        if (unit.id !== unitId) continue;
        const lesson = (unit.lessons || []).find(l => l.id === lessonId);
        if (lesson) return { section, unit, lesson };
      }
    }
    return null;
  }

  const found = findUnitLesson();
  const root = document.getElementById('lesson-root');
  const captionEl = document.getElementById('lesson-caption');
  if (!found) {
    root.innerHTML = '<p style="padding:24px">Les niet gevonden. <a href="index.html">Terug</a></p>';
    return;
  }
  const { section, unit, lesson } = found;
  if (captionEl) {
    captionEl.innerHTML = `${Grading.escapeHtml(section.title)} &middot; <strong>${Grading.escapeHtml(unit.title)}</strong> &middot; ${Grading.escapeHtml(lesson.label)}: ${Grading.escapeHtml(lesson.title)}`;
  }

  const esc = Grading.escapeHtml;

  /* ---- auto-generated review exercises for SRS-due items ---- */
  function distractorsFor(itemId, n) {
    const pool = Object.keys(VOCAB).filter(id => id !== itemId);
    const picked = [];
    while (picked.length < n && pool.length) {
      picked.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
    }
    return picked.map(id => VOCAB[id].en);
  }

  function buildReviewExercise(itemId, i) {
    const item = VOCAB[itemId];
    if (!item) return null;
    if (i % 2 === 0) {
      return { id: `rev_${itemId}`, type: 'typing', itemId, prompt: { en: `Translate: "${item.en}"` }, correct: item.nl.replace('...', '').trim() || item.nl };
    }
    const options = [item.en, ...distractorsFor(itemId, 3)];
    for (let j = options.length - 1; j > 0; j--) { const k = Math.floor(Math.random() * (j + 1)); [options[j], options[k]] = [options[k], options[j]]; }
    return { id: `rev_${itemId}`, type: 'mcq', itemId, prompt: { en: `What does "${item.nl}" mean?` }, options, correct: options.indexOf(item.en) };
  }

  /* ---- build the step queue ---- */
  const queue = [];
  if (lesson.id === 'l1' && unit.dialogue) queue.push({ kind: 'dialogue' });
  (lesson.newWords || []).forEach(w => queue.push({ kind: 'newword', word: w }));
  (lesson.exercises || []).forEach(ex => queue.push({ kind: 'exercise', exercise: ex }));
  if (lesson.id === 'l3') {
    const authoredItems = (lesson.exercises || []).map(e => e.itemId).filter(Boolean);
    SRS.getDueItems(Object.keys(VOCAB), 4)
      .filter(id => !authoredItems.includes(id))
      .forEach((id, i) => { const ex = buildReviewExercise(id, i); if (ex) queue.push({ kind: 'exercise', exercise: ex }); });
  }

  // Any completed lesson with real graded exercises keeps the streak — that's
  // genuine daily practice. The anti-grinding guard lives on XP (overlearned
  // items earn less), not here.
  const didPractice = queue.some(s => s.kind === 'exercise');
  const firstExerciseIndex = queue.findIndex(s => s.kind === 'exercise');

  let stepIndex = 0;
  let hearts = 5;
  let xpEarned = 0;
  const startedAt = Date.now();
  let timerHandle = null;
  let controller = null;

  const progressFill = document.getElementById('progress-fill');
  const heartsEl = document.getElementById('lesson-hearts');
  const timerEl = document.getElementById('lesson-timer');
  document.getElementById('lesson-close').addEventListener('click', () => { window.location.href = 'index.html'; });

  function renderHearts() {
    heartsEl.textContent = '❤️'.repeat(Math.max(hearts, 0)) + '🖤'.repeat(5 - Math.max(hearts, 0));
  }
  function startTimer() {
    timerHandle = setInterval(() => {
      const secs = Math.floor((Date.now() - startedAt) / 1000);
      timerEl.textContent = `⏱ ${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`;
    }, 1000);
  }
  function updateProgress() {
    progressFill.style.width = `${Math.min(100, (stepIndex / queue.length) * 100)}%`;
  }

  function confettiBurst() {
    const emojis = ['🎉', '✨', '🎊', '⭐'];
    for (let i = 0; i < 14; i++) {
      const el = document.createElement('div');
      el.className = 'confetti-emoji';
      el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
      el.style.left = `${Math.random() * 100}vw`;
      el.style.fontSize = `${16 + Math.random() * 18}px`;
      el.style.animationDelay = `${Math.random() * 0.4}s`;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 3200);
    }
  }

  function clearFooter() {
    const f = document.querySelector('.exercise-footer');
    if (f) f.remove();
  }

  function renderStep() {
    updateProgress();
    clearFooter();
    root.innerHTML = '';
    controller = null;
    const step = queue[stepIndex];
    if (!step) return renderSummary();
    if (step.kind === 'dialogue') return renderDialogue();
    if (step.kind === 'newword') return renderNewWord(step.word);
    if (step.kind === 'exercise') return renderExercise(step.exercise);
  }

  function renderDialogue() {
    const scene = document.createElement('div');
    scene.className = 'dialogue-scene';
    scene.innerHTML = `<h2>${esc(unit.title)}</h2><p class="dialogue-hint">Tik op een zin om te luisteren.</p>`;
    unit.dialogue.forEach(line => {
      const row = document.createElement('div');
      row.className = 'dialogue-line';
      row.innerHTML = `<div class="speaker">${line.speaker}</div>
        <div class="bubble"><div class="nl">${esc(line.nl)}</div><div class="en">${esc(line.en)}</div></div>`;
      const bubble = row.querySelector('.bubble');
      bubble.style.cursor = 'pointer';
      bubble.addEventListener('click', () => Audio_.playAudio({ text: line.nl, lang: 'nl', gender: line.voice }));
      scene.appendChild(row);
    });
    root.appendChild(scene);
    const btn = document.createElement('button');
    btn.className = 'btn btn-primary dialogue-continue';
    btn.textContent = 'Doorgaan';
    btn.addEventListener('click', () => { stepIndex++; renderStep(); });
    root.appendChild(btn);
  }

  function renderNewWord(word) {
    const card = document.createElement('div');
    card.className = 'newword-card';
    card.innerHTML = `<div class="nw-badge">Nieuw woord</div>
      <div class="nw-word">${esc(word.nl)}</div>
      <div class="nw-en">${esc(word.en)}</div>
      <button class="speak-btn-lg" type="button" aria-label="Speel audio af">🔊</button>`;
    root.appendChild(card);
    const play = () => Audio_.playAudio({ text: word.nl.split('/')[0].trim(), lang: 'nl' });
    card.querySelector('.speak-btn-lg').addEventListener('click', play);
    setTimeout(play, 300);
    const btn = document.createElement('button');
    btn.className = 'btn btn-primary dialogue-continue';
    btn.textContent = 'Doorgaan';
    btn.addEventListener('click', () => { stepIndex++; renderStep(); });
    root.appendChild(btn);
  }

  function renderExercise(exercise) {
    const wrap = document.createElement('div');
    wrap.className = 'exercise-card';
    root.appendChild(wrap);

    if (lesson.grammarNote && stepIndex === firstExerciseIndex) {
      const noteBtn = document.createElement('button');
      noteBtn.type = 'button';
      noteBtn.className = 'grammar-note-btn';
      noteBtn.textContent = '💡 Grammatica-tip';
      const panel = document.createElement('div');
      panel.className = 'grammar-note-panel';
      panel.innerHTML = `<div class="nl">${esc(lesson.grammarNote.nl)}</div><div class="en">${esc(lesson.grammarNote.en)}</div>`;
      noteBtn.addEventListener('click', () => panel.classList.toggle('open'));
      wrap.appendChild(noteBtn);
      wrap.appendChild(panel);
    }

    const renderers = { mcq: MultipleChoiceExercise, wordbank: WordBankExercise, typing: TypingExercise, listening: ListeningExercise };
    controller = renderers[exercise.type].render(wrap, exercise, { onCommit: () => triggerCheck(exercise) });
    renderFooter(exercise);
  }

  function renderFooter(exercise) {
    clearFooter();
    const footer = document.createElement('div');
    footer.className = 'exercise-footer';
    if (controller.autoCommit) {
      footer.innerHTML = `<div class="footer-hint">Kies een antwoord</div>`;
    } else {
      footer.innerHTML = `<div></div><button class="btn btn-primary" id="check-btn">Controleren</button>`;
      footer.querySelector('#check-btn').addEventListener('click', () => triggerCheck(exercise));
    }
    document.body.appendChild(footer);
  }

  function triggerCheck(exercise) {
    if (!controller) return;
    const result = controller.check();
    if (!result) return;
    handleResult(exercise, result);
  }

  function handleResult(exercise, result) {
    const { status, correctText, diffCorrectHtml, distance } = result;
    const passed = status === 'correct';

    if (exercise.itemId) {
      SRS.recordResponse(exercise.itemId, passed);
      DataStore.recordPracticeStat(passed);
    }
    if (passed) {
      const overlearned = exercise.itemId && SRS.isOverlearned(exercise.itemId, 3);
      xpEarned += overlearned ? 2 : 10;
    } else if (status === 'wrong') {
      hearts--;
      renderHearts();
    }
    // 'close' (orange): counts as not-passed for XP/SRS but costs no heart.

    const footer = document.querySelector('.exercise-footer');
    footer.className = `exercise-footer ${status}`;

    let headline, detail = '';
    if (passed && distance === 1) {
      headline = 'Goed gedaan! 🎉';
      detail = `<div class="feedback-answer">Bijna perfect — let op: ${diffCorrectHtml || esc(correctText)}</div>`;
    } else if (passed) {
      headline = 'Perfect! 🎉';
    } else if (status === 'close') {
      headline = 'Bijna goed!';
      detail = `<div class="feedback-answer">Correct: ${diffCorrectHtml || '<b>' + esc(correctText) + '</b>'}</div>`;
    } else {
      headline = 'Niet goed.';
      detail = `<div class="feedback-answer">Juiste antwoord: <b>${esc(correctText)}</b></div>`;
    }

    footer.innerHTML = `<div><div class="feedback-text ${status}">${headline}</div>${detail}</div>
      <button class="btn ${status === 'correct' ? 'btn-primary' : status === 'close' ? 'btn-close' : 'btn-wrong'}" id="continue-btn">Doorgaan</button>`;
    document.getElementById('continue-btn').addEventListener('click', () => {
      clearFooter();
      if (hearts <= 0) return renderFail();
      stepIndex++;
      renderStep();
    });
  }

  function renderFail() {
    clearInterval(timerHandle);
    clearFooter();
    document.querySelector('.lesson-topbar').style.display = 'none';
    if (captionEl) captionEl.style.display = 'none';
    root.innerHTML = `<div class="fail-screen">
      <div class="fail-emoji">💔</div>
      <h1>Geen hartjes meer</h1>
      <p>Geen zorgen, je voortgang van eerdere lessen blijft bewaard. Probeer deze les opnieuw!</p><br>
      <button class="btn btn-primary" id="retry-btn">Opnieuw proberen</button>
      <br><br><a href="index.html" class="text-link">Terug naar het overzicht</a></div>`;
    document.getElementById('retry-btn').addEventListener('click', () => window.location.reload());
  }

  function renderSummary() {
    clearInterval(timerHandle);
    clearFooter();
    const elapsedSec = Math.floor((Date.now() - startedAt) / 1000);
    if (elapsedSec < queue.length * 12) xpEarned += 10;

    DataStore.completeLesson(unit.id, lesson.id);
    if (didPractice) DataStore.touchStreak();
    DataStore.addXP(xpEarned);

    document.querySelector('.lesson-topbar').style.display = 'none';
    if (captionEl) captionEl.style.display = 'none';
    const state = DataStore.getState();
    root.innerHTML = `<div class="summary-screen">
      <div class="summary-emoji">🏆</div>
      <h1>${esc(lesson.label)} voltooid!</h1>
      <div class="summary-stats">
        <div class="summary-stat xp"><div class="value">+${xpEarned}</div><div class="label">XP</div></div>
        <div class="summary-stat streak"><div class="value">🔥 ${state.streak.count}</div><div class="label">Streak</div></div>
        <div class="summary-stat accuracy"><div class="value">${DataStore.getAccuracy()}%</div><div class="label">Nauwkeurigheid</div></div>
      </div>
      <button class="btn btn-primary" id="back-btn">Verder</button></div>`;
    document.getElementById('back-btn').addEventListener('click', () => { window.location.href = 'index.html'; });
    confettiBurst();
  }

  renderHearts();
  startTimer();
  renderStep();
})();
