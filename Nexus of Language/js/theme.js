/* Nexus of Language — light/dark theme.
   The actual data-theme is set by a tiny inline <head> script (to avoid a
   flash of the wrong theme); this module just wires the toggle button and
   persists the choice. Any element with [data-theme-toggle] becomes a
   toggle. */

const Theme = (() => {
  function current() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }
  function set(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem('nol_theme', t); } catch (e) {}
    render();
  }
  function toggle() { set(current() === 'dark' ? 'light' : 'dark'); }
  function render() {
    document.querySelectorAll('[data-theme-toggle]').forEach(b => {
      b.textContent = current() === 'dark' ? '☀️' : '🌙';
      b.setAttribute('aria-label', current() === 'dark' ? 'Licht thema' : 'Donker thema');
    });
  }
  function init() {
    document.querySelectorAll('[data-theme-toggle]').forEach(b => b.addEventListener('click', toggle));
    render();
  }
  return { init, toggle, current, set };
})();

document.addEventListener('DOMContentLoaded', Theme.init);
