/* Nexus of Language — home screen: HUD, profile, section paths, and the
   unit-detail modal (which lists a unit's lessons with per-lesson locking,
   so entering a unit is no longer a confusing straight jump into a lesson). */

(function () {
  const esc = Grading.escapeHtml;
  const hudBar = document.getElementById('hud-bar');
  const statsLine = document.getElementById('stats-line');
  const sectionsEl = document.getElementById('sections');
  const profileChip = document.getElementById('profile-chip');
  if (!sectionsEl) return;

  /* ---------------- HUD + profile ---------------- */
  function renderHud() {
    const state = DataStore.getState();
    hudBar.innerHTML = `
      <div class="hud-chip streak"><span class="icon">🔥</span>${state.streak.count}</div>
      <div class="hud-chip xp"><span class="icon">⭐</span>${state.xp.total}</div>`;
    statsLine.textContent = `${state.stats.wordsReviewed} woorden geoefend · ${DataStore.getAccuracy()}% nauwkeurigheid`;
    profileChip.innerHTML = `<span class="icon">👤</span>${esc(DataStore.getProfile())}`;
  }

  /* ---------------- generic modal helper ---------------- */
  function openModal(buildContent) {
    closeModal();
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'nol-modal';
    const card = document.createElement('div');
    card.className = 'modal-card';
    const close = document.createElement('button');
    close.className = 'modal-close';
    close.innerHTML = '&times;';
    close.setAttribute('aria-label', 'Sluiten');
    close.addEventListener('click', closeModal);
    card.appendChild(close);
    buildContent(card);
    overlay.appendChild(card);
    overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
    document.body.appendChild(overlay);
  }
  function closeModal() {
    const m = document.getElementById('nol-modal');
    if (m) m.remove();
  }

  /* ---------------- unit detail ---------------- */
  function openUnit(unit) {
    openModal(card => {
      const head = document.createElement('div');
      head.className = 'modal-head';
      head.innerHTML = `<div class="modal-icon">${unit.icon}</div>
        <h2>${esc(unit.title)}</h2><p>${esc(unit.subtitle)}</p>`;
      card.appendChild(head);

      const list = document.createElement('div');
      list.className = 'lesson-list';
      unit.lessons.forEach((lesson, i) => {
        const done = DataStore.isLessonComplete(unit.id, lesson.id);
        const unlocked = DataStore.isLessonUnlocked(unit, i);
        const row = document.createElement('button');
        row.type = 'button';
        row.className = 'lesson-row' + (done ? ' done' : '') + (!unlocked ? ' locked' : '');
        row.disabled = !unlocked;
        const icon = done ? '✓' : unlocked ? '▶' : '🔒';
        row.innerHTML = `<span class="lesson-row-icon">${icon}</span>
          <span class="lesson-row-text"><strong>${esc(lesson.label)}</strong><span>${esc(lesson.title)}</span></span>`;
        row.addEventListener('click', () => {
          if (!unlocked) return;
          window.location.href = `lesson.html?u=${unit.id}&l=${lesson.id}`;
        });
        list.appendChild(row);
      });
      card.appendChild(list);
    });
  }

  /* ---------------- profile modal ---------------- */
  function openProfile() {
    openModal(card => {
      const head = document.createElement('div');
      head.className = 'modal-head';
      head.innerHTML = `<div class="modal-icon">👤</div><h2>Profiel</h2>
        <p>Je voortgang wordt in deze browser bewaard, per naam.</p>`;
      card.appendChild(head);

      const nameWrap = document.createElement('div');
      nameWrap.className = 'profile-field';
      nameWrap.innerHTML = `<label>Naam</label>`;
      const nameInput = document.createElement('input');
      nameInput.type = 'text';
      nameInput.className = 'type-input';
      nameInput.value = DataStore.getProfile();
      nameWrap.appendChild(nameInput);
      const saveBtn = document.createElement('button');
      saveBtn.className = 'btn btn-primary';
      saveBtn.textContent = 'Opslaan / wisselen';
      saveBtn.addEventListener('click', () => {
        DataStore.setProfile(nameInput.value);
        closeModal();
        renderHud();
        renderSections();
      });
      nameWrap.appendChild(saveBtn);
      card.appendChild(nameWrap);

      const others = DataStore.listProfiles().filter(n => n !== DataStore.getProfile());
      if (others.length) {
        const sw = document.createElement('div');
        sw.className = 'profile-field';
        sw.innerHTML = `<label>Bestaande profielen</label>`;
        others.forEach(n => {
          const b = document.createElement('button');
          b.className = 'btn btn-secondary profile-switch';
          b.textContent = '👤 ' + n;
          b.addEventListener('click', () => { DataStore.setProfile(n); closeModal(); renderHud(); renderSections(); });
          sw.appendChild(b);
        });
        card.appendChild(sw);
      }

      const codeWrap = document.createElement('div');
      codeWrap.className = 'profile-field';
      codeWrap.innerHTML = `<label>Voortgang meenemen naar een ander apparaat</label>`;
      const code = document.createElement('textarea');
      code.className = 'code-box';
      code.readOnly = true;
      code.value = DataStore.exportCode();
      codeWrap.appendChild(code);
      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn btn-secondary';
      copyBtn.textContent = 'Kopieer code';
      copyBtn.addEventListener('click', () => { code.select(); try { document.execCommand('copy'); } catch (e) {} copyBtn.textContent = 'Gekopieerd ✓'; });
      codeWrap.appendChild(copyBtn);
      card.appendChild(codeWrap);

      const impWrap = document.createElement('div');
      impWrap.className = 'profile-field';
      impWrap.innerHTML = `<label>Code importeren</label>`;
      const imp = document.createElement('textarea');
      imp.className = 'code-box';
      imp.placeholder = 'Plak hier je voortgangscode...';
      impWrap.appendChild(imp);
      const impBtn = document.createElement('button');
      impBtn.className = 'btn btn-primary';
      impBtn.textContent = 'Importeer';
      impBtn.addEventListener('click', () => {
        if (DataStore.importCode(imp.value)) { closeModal(); renderHud(); renderSections(); }
        else { impBtn.textContent = 'Ongeldige code'; }
      });
      impWrap.appendChild(impBtn);
      card.appendChild(impWrap);
    });
  }

  /* ---------------- first-visit name prompt ---------------- */
  function ensureProfile() {
    if (DataStore.hasProfileSet()) return;
    openModal(card => {
      card.querySelector('.modal-close').style.display = 'none';
      const head = document.createElement('div');
      head.className = 'modal-head';
      head.innerHTML = `<div class="modal-icon">🧭</div><h2>Welkom!</h2><p>Hoe heet je? Zo bewaren we jouw voortgang.</p>`;
      card.appendChild(head);
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'type-input';
      input.placeholder = 'Je naam';
      card.appendChild(input);
      const btn = document.createElement('button');
      btn.className = 'btn btn-primary';
      btn.style.marginTop = '14px';
      btn.textContent = 'Beginnen';
      const go = () => { DataStore.setProfile(input.value || 'Gast'); closeModal(); renderHud(); renderSections(); };
      btn.addEventListener('click', go);
      input.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
      card.appendChild(btn);
      setTimeout(() => input.focus(), 50);
    });
  }

  /* ---------------- section paths ---------------- */
  function firstOpenLesson(unit) {
    const incomplete = unit.lessons.find(l => !DataStore.isLessonComplete(unit.id, l.id));
    return incomplete || unit.lessons[0];
  }

  function renderSections() {
    sectionsEl.innerHTML = '';
    COURSE.sections.forEach(section => {
      const wrap = document.createElement('div');
      wrap.className = 'course-section';
      wrap.innerHTML = `<div class="section-title"><h1>${esc(section.title)}</h1></div>`;
      const path = document.createElement('div');
      path.className = 'path-map';

      section.units.forEach((unit, index) => {
        const coming = !!unit.comingSoon || !unit.lessons || !unit.lessons.length;
        const unlocked = !coming && DataStore.isUnitUnlocked(section.units, index);
        const complete = !coming && DataStore.isUnitComplete(unit);

        const nodeWrap = document.createElement('div');
        nodeWrap.className = 'unit-node-wrap';
        const node = document.createElement('button');
        node.type = 'button';
        node.className = 'unit-node' + (coming ? ' coming' : !unlocked ? ' locked' : '') + (complete ? ' complete' : '');
        node.textContent = unit.icon;
        node.disabled = coming || !unlocked;
        if (complete) node.insertAdjacentHTML('beforeend', '<span class="node-check">✓</span>');
        node.addEventListener('click', () => { if (unlocked) openUnit(unit); });

        const label = document.createElement('div');
        label.className = 'unit-label';
        const sub = coming ? 'Binnenkort' : unit.subtitle;
        label.innerHTML = `${esc(unit.title)}<span class="unit-sub">${esc(sub)}</span>`;

        nodeWrap.appendChild(node);
        nodeWrap.appendChild(label);
        path.appendChild(nodeWrap);
      });
      wrap.appendChild(path);
      sectionsEl.appendChild(wrap);
    });
  }

  profileChip.addEventListener('click', openProfile);

  renderHud();
  renderSections();
  ensureProfile();
})();
