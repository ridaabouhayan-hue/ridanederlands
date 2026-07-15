/* Nexus of Language — multiple choice.
   Contract: render(container, exercise, { onCommit }) -> controller
     controller = { autoCommit, hasAnswer(), check() -> {status, correctText, distance} }
   MC is autoCommit: selecting an option immediately calls onCommit() (no
   separate "Controleren" click). */

const MultipleChoiceExercise = (() => {
  function render(container, exercise, opts) {
    let selected = null;
    let decided = false;
    const optionEls = [];

    if (exercise.prompt && exercise.prompt.en) {
      const prompt = document.createElement('div');
      prompt.className = 'exercise-prompt';
      prompt.textContent = exercise.prompt.en;
      container.appendChild(prompt);
    }

    const grid = document.createElement('div');
    grid.className = 'mc-grid';
    exercise.options.forEach((opt, i) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mc-option';
      btn.textContent = opt;
      btn.addEventListener('click', () => {
        if (decided) return;
        selected = i;
        decided = true;
        optionEls.forEach(e => e.classList.remove('selected'));
        btn.classList.add('selected');
        if (opts && opts.onCommit) opts.onCommit();
      });
      grid.appendChild(btn);
      optionEls.push(btn);
    });
    container.appendChild(grid);

    return {
      autoCommit: true,
      hasAnswer: () => selected !== null,
      check() {
        if (selected === null) return null;
        const correct = selected === exercise.correct;
        optionEls.forEach((e, i) => {
          e.disabled = true;
          if (i === exercise.correct) e.classList.add('correct');
          else if (i === selected) e.classList.add('incorrect');
        });
        return {
          status: correct ? 'correct' : 'wrong',
          correctText: exercise.options[exercise.correct],
          distance: correct ? 0 : 9
        };
      }
    };
  }

  return { render };
})();
