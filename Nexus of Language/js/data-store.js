/* Nexus of Language — localStorage-backed progress store.
   Progress is keyed per PROFILE name, so several students sharing one
   device each keep their own streak/XP/SRS state without a login. A
   profile's progress can also be exported/imported as a short code to move
   between devices (the zero-backend stand-in for accounts). */

const DataStore = (() => {
  const PROFILE_KEY = 'nol_active_profile';
  const KEY_PREFIX = 'nol_progress_v1__';

  function activeProfile() {
    try { return localStorage.getItem(PROFILE_KEY) || 'Gast'; } catch (e) { return 'Gast'; }
  }
  function storageKey() { return KEY_PREFIX + activeProfile(); }

  function defaultState() {
    return {
      xp: { total: 0 },
      streak: { count: 0, lastActiveDate: null },
      stats: { wordsReviewed: 0, reviewsCorrect: 0 },
      unitsProgress: {},   // { [unitId]: { lessonsDone: [lessonId, ...] } }
      srs: {}               // { [itemId]: { interval, ease, reps, dueAt } }
    };
  }

  function load() {
    try {
      const raw = localStorage.getItem(storageKey());
      if (!raw) return defaultState();
      const parsed = JSON.parse(raw);
      const d = defaultState();
      return {
        xp: Object.assign(d.xp, parsed.xp),
        streak: Object.assign(d.streak, parsed.streak),
        stats: Object.assign(d.stats, parsed.stats),
        unitsProgress: parsed.unitsProgress || {},
        srs: parsed.srs || {}
      };
    } catch (e) {
      return defaultState();
    }
  }

  let state = load();

  function persist() {
    try { localStorage.setItem(storageKey(), JSON.stringify(state)); } catch (e) {}
  }

  function todayStr() { return new Date().toISOString().slice(0, 10); }
  function daysBetween(a, b) {
    return Math.round((new Date(b + 'T00:00:00') - new Date(a + 'T00:00:00')) / 86400000);
  }

  return {
    getState() { return state; },
    getProfile() { return activeProfile(); },

    setProfile(name) {
      const clean = String(name || '').trim().slice(0, 24) || 'Gast';
      try { localStorage.setItem(PROFILE_KEY, clean); } catch (e) {}
      state = load();
      return clean;
    },

    hasProfileSet() {
      try { return !!localStorage.getItem(PROFILE_KEY); } catch (e) { return false; }
    },

    listProfiles() {
      const names = [];
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          if (k && k.startsWith(KEY_PREFIX)) names.push(k.slice(KEY_PREFIX.length));
        }
      } catch (e) {}
      return names;
    },

    // --- progress code (export/import for cross-device) ---
    exportCode() {
      try { return btoa(unescape(encodeURIComponent(JSON.stringify(state)))); } catch (e) { return ''; }
    },
    importCode(code) {
      try {
        const parsed = JSON.parse(decodeURIComponent(escape(atob(code.trim()))));
        if (!parsed || typeof parsed !== 'object') return false;
        const d = defaultState();
        state = {
          xp: Object.assign(d.xp, parsed.xp),
          streak: Object.assign(d.streak, parsed.streak),
          stats: Object.assign(d.stats, parsed.stats),
          unitsProgress: parsed.unitsProgress || {},
          srs: parsed.srs || {}
        };
        persist();
        return true;
      } catch (e) { return false; }
    },

    addXP(amount) { state.xp.total += amount; persist(); return state.xp.total; },

    touchStreak() {
      const today = todayStr();
      const last = state.streak.lastActiveDate;
      if (last === today) { /* already counted */ }
      else if (last && daysBetween(last, today) === 1) { state.streak.count += 1; state.streak.lastActiveDate = today; }
      else { state.streak.count = 1; state.streak.lastActiveDate = today; }
      persist();
      return state.streak.count;
    },

    recordPracticeStat(wasCorrect) {
      state.stats.wordsReviewed += 1;
      if (wasCorrect) state.stats.reviewsCorrect += 1;
      persist();
    },

    getAccuracy() {
      const { wordsReviewed, reviewsCorrect } = state.stats;
      if (!wordsReviewed) return 100;
      return Math.round((reviewsCorrect / wordsReviewed) * 100);
    },

    isLessonComplete(unitId, lessonId) {
      const u = state.unitsProgress[unitId];
      return !!(u && u.lessonsDone.includes(lessonId));
    },

    completeLesson(unitId, lessonId) {
      if (!state.unitsProgress[unitId]) state.unitsProgress[unitId] = { lessonsDone: [] };
      const u = state.unitsProgress[unitId];
      if (!u.lessonsDone.includes(lessonId)) u.lessonsDone.push(lessonId);
      persist();
    },

    isUnitComplete(unit) {
      if (!unit.lessons || !unit.lessons.length) return false;
      const u = state.unitsProgress[unit.id];
      if (!u) return false;
      return unit.lessons.every(l => u.lessonsDone.includes(l.id));
    },

    isUnitUnlocked(units, index) {
      if (index === 0) return true;
      const prev = units[index - 1];
      if (!prev.lessons || !prev.lessons.length) return false;
      return this.isUnitComplete(prev);
    },

    // A lesson within a unit unlocks when the previous lesson is done.
    isLessonUnlocked(unit, lessonIndex) {
      if (lessonIndex === 0) return true;
      return this.isLessonComplete(unit.id, unit.lessons[lessonIndex - 1].id);
    },

    getItemState(itemId) { return state.srs[itemId] || null; },
    setItemState(itemId, itemState) { state.srs[itemId] = itemState; persist(); }
  };
})();
