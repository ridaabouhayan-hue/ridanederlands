/* Nexus of Language — typing / fill-in / production answer.
   Uses Grading.evaluate for Levenshtein tiers (green/orange/red) and
   accepts multiple correct answers. If exercise.audioText is present a
   speaker button is shown so the app can "ask" a question the learner
   answers (production practice). */

const TypingExercise = (() => {
  function render(container, exercise, opts) {
    if (exercise.prompt && exercise.prompt.en) {
      const prompt = document.createElement('div');
      prompt.className = 'exercise-prompt';
      prompt.textContent = exercise.prompt.en;
      container.appendChild(prompt);
    }

    if (exercise.audioText) {
      const playBtn = document.createElement('button');
      playBtn.type = 'button';
      playBtn.className = 'speak-btn';
      playBtn.textContent = '🔊';
      playBtn.setAttribute('aria-label', 'Speel de vraag af');
      const play = () => Audio_.playAudio({ id: exercise.audioId, text: exercise.audioText, lang: exercise.lang || 'nl', gender: exercise.voice });
      playBtn.addEventListener('click', play);
      container.appendChild(playBtn);
      setTimeout(play, 300);
    }

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'type-input';
    input.placeholder = 'Typ je antwoord in het Nederlands...';
    input.autocomplete = 'off';
    input.autocapitalize = 'off';
    input.spellcheck = false;
    container.appendChild(input);
    setTimeout(() => input.focus(), 50);

    input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && input.value.trim() && opts && opts.onCommit) opts.onCommit();
    });

    return {
      autoCommit: false,
      hasAnswer: () => input.value.trim().length > 0,
      check() {
        if (!input.value.trim()) return null;
        const res = Grading.evaluate(exercise.correct, input.value);
        input.disabled = true;
        input.classList.add(res.status === 'correct' ? 'correct' : res.status === 'close' ? 'close' : 'incorrect');
        const correctText = res.best || (Array.isArray(exercise.correct) ? exercise.correct[0] : exercise.correct);
        return { status: res.status, correctText, diffHtml: res.diffHtml, diffCorrectHtml: res.diffCorrectHtml, distance: res.distance };
      }
    };
  }

  return { render };
})();
