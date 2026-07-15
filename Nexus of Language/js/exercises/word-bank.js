/* Nexus of Language — word-bank sentence building.
   Strict: the assembled sentence must match (after punctuation/case
   normalization) exactly, so it's correct (distance 0) or wrong. */

const WordBankExercise = (() => {
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function render(container, exercise, opts) {
    if (exercise.prompt && exercise.prompt.en) {
      const prompt = document.createElement('div');
      prompt.className = 'exercise-prompt';
      prompt.textContent = exercise.prompt.en;
      container.appendChild(prompt);
    }

    const target = document.createElement('div');
    target.className = 'sentence-target';
    container.appendChild(target);

    const pool = document.createElement('div');
    pool.className = 'word-bank-pool';
    container.appendChild(pool);

    const chosen = [];

    function makeChip(word, inPool) {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'word-chip';
      chip.textContent = word;
      chip.addEventListener('click', () => {
        if (chip.disabled) return;
        if (inPool) {
          chip.classList.add('used');
          chip.disabled = true;
          const targetChip = makeChip(word, false);
          target.appendChild(targetChip);
          chosen.push({ word, poolChip: chip, targetChip });
        } else {
          const entry = chosen.find(c => c.targetChip === chip);
          if (entry) {
            entry.poolChip.classList.remove('used');
            entry.poolChip.disabled = false;
            chosen.splice(chosen.indexOf(entry), 1);
          }
          chip.remove();
        }
      });
      return chip;
    }

    shuffle(exercise.words).forEach(w => pool.appendChild(makeChip(w, true)));

    return {
      autoCommit: false,
      hasAnswer: () => chosen.length > 0,
      check() {
        if (chosen.length === 0) return null;
        const built = chosen.map(c => c.word).join(' ');
        const res = Grading.evaluate(exercise.correct, built);
        const correct = res.distance === 0;
        target.classList.add(correct ? 'target-correct' : 'target-wrong');
        [...pool.children, ...target.children].forEach(c => c.disabled = true);
        return {
          status: correct ? 'correct' : 'wrong',
          correctText: exercise.correct,
          distance: res.distance
        };
      }
    };
  }

  return { render };
})();
