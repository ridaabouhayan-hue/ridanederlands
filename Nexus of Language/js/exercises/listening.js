/* Nexus of Language — listening exercise.
   Plays exercise.audioText (pre-generated mp3 -> TTS fallback) then defers
   to the MC or typing renderer for the answer, forwarding the { onCommit }
   options so listening-MC still auto-commits. */

const ListeningExercise = (() => {
  function render(container, exercise, opts) {
    const prompt = document.createElement('div');
    prompt.className = 'exercise-prompt';
    prompt.innerHTML = `${Grading.escapeHtml(exercise.prompt.en)}<span class="prompt-sub">🎧 Luisteroefening</span>`;
    container.appendChild(prompt);

    const playBtn = document.createElement('button');
    playBtn.type = 'button';
    playBtn.className = 'speak-btn-lg';
    playBtn.textContent = '🔊';
    playBtn.setAttribute('aria-label', 'Speel audio af');
    const play = () => Audio_.playAudio({ id: exercise.audioId, text: exercise.audioText, lang: exercise.lang || 'nl', gender: exercise.voice });
    playBtn.addEventListener('click', play);
    container.appendChild(playBtn);
    setTimeout(play, 300);

    const answerBox = document.createElement('div');
    container.appendChild(answerBox);

    const inner = exercise.mode === 'typing'
      ? TypingExercise.render(answerBox, Object.assign({}, exercise, { audioText: null, prompt: null }), opts)
      : MultipleChoiceExercise.render(answerBox, Object.assign({}, exercise, { prompt: null }), opts);

    return {
      autoCommit: inner.autoCommit,
      hasAnswer: inner.hasAnswer,
      check: inner.check
    };
  }

  return { render };
})();
