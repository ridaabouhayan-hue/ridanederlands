/* Nexus of Language — SM-2 style spaced repetition engine (Anki-derived).
   Deliberately exposes only two functions so the algorithm can later be
   swapped for something like Half-Life Regression without touching callers. */

const SRS = (() => {
  const DAY_MS = 86400000;
  const MIN_EASE = 1.3;

  function freshState() {
    return { interval: 0, ease: 2.5, reps: 0, dueAt: 0 };
  }

  function nextState(prev, wasCorrect) {
    const s = Object.assign({}, prev);
    if (wasCorrect) {
      s.reps += 1;
      if (s.reps === 1) s.interval = 1;
      else if (s.reps === 2) s.interval = 6;
      else s.interval = Math.round(s.interval * s.ease);
      s.ease = Math.min(3.0, s.ease + 0.1);
    } else {
      s.reps = 0;
      s.interval = 1;
      s.ease = Math.max(MIN_EASE, s.ease - 0.2);
    }
    s.dueAt = Date.now() + s.interval * DAY_MS;
    return s;
  }

  return {
    /* itemIds whose stored SRS state is due (or overdue), oldest-due first.
       Items never seen before have no state and are not "due" for review —
       they're introduced as new content instead. */
    getDueItems(itemIds, maxN) {
      const now = Date.now();
      const due = itemIds
        .map(id => ({ id, state: DataStore.getItemState(id) }))
        .filter(x => x.state && x.state.dueAt <= now)
        .sort((a, b) => a.state.dueAt - b.state.dueAt)
        .map(x => x.id);
      return typeof maxN === 'number' ? due.slice(0, maxN) : due;
    },

    recordResponse(itemId, wasCorrect) {
      const prev = DataStore.getItemState(itemId) || freshState();
      const updated = nextState(prev, wasCorrect);
      DataStore.setItemState(itemId, updated);
      return updated;
    },

    /* True if this item has been answered correctly on its last N reviews
       in a row — used by the XP-cap gamification guardrail. */
    isOverlearned(itemId, n) {
      const s = DataStore.getItemState(itemId);
      return !!(s && s.reps >= n);
    }
  };
})();
