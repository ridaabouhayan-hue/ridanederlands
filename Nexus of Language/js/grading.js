/* Nexus of Language — answer grading with Levenshtein tiers.

   evaluate(correct, given) -> { status, distance, best, diffHtml }
     status: 'correct'  (edit distance 0-1)  -> green, accepted
             'close'     (edit distance 2)    -> orange, "bijna goed"
             'wrong'     (edit distance 3+)   -> red
   `correct` may be a single string OR an array of accepted answers; the
   smallest distance across all accepted answers wins, so alternatives like
   ["Ik heet Youssef", "Mijn naam is Youssef"] both pass.
   diffHtml highlights the characters in the learner's answer that differ,
   so the app can show WHERE the mistake was. */

const Grading = (() => {
  function cleanString(str) {
    return String(str || '')
      .toLowerCase()
      .trim()
      .replace(/[.,?!;:()'"]/g, '')
      .replace(/\s+/g, ' ');
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
  }

  function levenshtein(a, b) {
    const m = a.length, n = b.length;
    if (m === 0) return n;
    if (n === 0) return m;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
      }
    }
    return dp[m][n];
  }

  /* Highlight, in the learner's `given` string, the characters that don't
     line up with the best accepted answer (case-insensitive backtrace). */
  function diffHighlight(best, given) {
    const a = best, b = given;
    const al = a.toLowerCase(), bl = b.toLowerCase();
    const m = a.length, n = b.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        const cost = al[i - 1] === bl[j - 1] ? 0 : 1;
        dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
      }
    }
    const marks = new Array(n).fill(false); // true => this char of `given` is wrong/extra
    let i = m, j = n;
    while (i > 0 && j > 0) {
      const cost = al[i - 1] === bl[j - 1] ? 0 : 1;
      if (dp[i][j] === dp[i - 1][j - 1] + cost) { if (cost === 1) marks[j - 1] = true; i--; j--; }
      else if (dp[i][j] === dp[i][j - 1] + 1) { marks[j - 1] = true; j--; }
      else { i--; }
    }
    while (j > 0) { marks[j - 1] = true; j--; }
    let html = '';
    for (let k = 0; k < n; k++) {
      const ch = escapeHtml(b[k]);
      html += marks[k] ? `<span class="diff-wrong">${ch}</span>` : ch;
    }
    return html || escapeHtml(given);
  }

  /* Highlight, on the CORRECT answer, the characters the learner got wrong or
     left out — so a missing letter (a deletion) is visible, which the
     given-string highlighter can't show. */
  function diffHighlightCorrect(best, given) {
    const a = best, b = given;
    const al = a.toLowerCase(), bl = b.toLowerCase();
    const m = a.length, n = b.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        const cost = al[i - 1] === bl[j - 1] ? 0 : 1;
        dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
      }
    }
    const marks = new Array(m).fill(false); // true => this char of `best` is missing/wrong in given
    let i = m, j = n;
    while (i > 0 && j > 0) {
      const cost = al[i - 1] === bl[j - 1] ? 0 : 1;
      if (dp[i][j] === dp[i - 1][j - 1] + cost) { if (cost === 1) marks[i - 1] = true; i--; j--; }
      else if (dp[i][j] === dp[i - 1][j] + 1) { marks[i - 1] = true; i--; } // deletion: best char missing in given
      else { j--; } // insertion in given
    }
    while (i > 0) { marks[i - 1] = true; i--; }
    let html = '';
    for (let k = 0; k < m; k++) {
      const ch = escapeHtml(a[k]);
      html += marks[k] ? `<span class="diff-wrong">${ch}</span>` : ch;
    }
    return html || escapeHtml(best);
  }

  function evaluate(correct, given) {
    const answers = Array.isArray(correct) ? correct : [correct];
    const g = cleanString(given);
    let best = answers[0], bestDist = Infinity;
    for (const ans of answers) {
      const d = levenshtein(cleanString(ans), g);
      if (d < bestDist) { bestDist = d; best = ans; }
    }
    const status = bestDist <= 1 ? 'correct' : bestDist === 2 ? 'close' : 'wrong';
    return {
      status, distance: bestDist, best,
      diffHtml: diffHighlight(best, given),
      diffCorrectHtml: diffHighlightCorrect(best, given)
    };
  }

  return { cleanString, escapeHtml, levenshtein, diffHighlight, evaluate };
})();
