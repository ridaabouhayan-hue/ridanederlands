/* ==========================================================
   EVC NT2 CORE JAVASCRIPT (kern.js)
   Bevat:
   - StorageAdapter & Firebase-skelet
   - Autorisatie & logout logic
   - Dynamische navigatiebalk-generator
   - Voortgangsberekening en statistieken
   ========================================================== */

// 1. StorageAdapter
var geheugen = {};
var opslagOk = false;
try {
  localStorage.setItem('__evc_test', '1');
  localStorage.removeItem('__evc_test');
  opslagOk = true;
} catch (e) {
  opslagOk = false;
}

var StorageAdapter = {
  naam: 'localStorage',
  set: function(sleutel, waarde) {
    if (opslagOk) {
      try {
        localStorage.setItem(sleutel, waarde);
        return;
      } catch (e) {}
    }
    geheugen[sleutel] = waarde;
  },
  get: function(sleutel) {
    if (opslagOk) {
      try {
        return localStorage.getItem(sleutel);
      } catch (e) {}
    }
    return geheugen[sleutel] || null;
  },
  remove: function(sleutel) {
    if (opslagOk) {
      try {
        localStorage.removeItem(sleutel);
      } catch (e) {}
    }
    delete geheugen[sleutel];
  }
};

/* Voorbeeld-skelet voor Firestore integratie (later te activeren):
var FirebaseAdapter = {
  naam: 'firebase',
  set: function(sleutel, waarde){
    // setDoc(doc(db,'evc',sleutel),{v:waarde})
  },
  get: function(sleutel){
    // return getDoc(...).data().v
  },
  remove: function(sleutel){
    // deleteDoc(doc(db,'evc',sleutel))
  }
};
StorageAdapter = FirebaseAdapter; // Deactiveer localStorage door dit aan te zetten
*/

function opslaan(sleutel, waarde) {
  StorageAdapter.set(sleutel, waarde);
}
function ophalen(sleutel) {
  return StorageAdapter.get(sleutel);
}
function verwijderen(sleutel) {
  StorageAdapter.remove(sleutel);
}

// 2. Autorisatie Controle
if (sessionStorage.getItem('evc_auth') !== '1') {
  let path = '../index.html';
  if (window.location.pathname.includes('/starrs/')) {
    path = '../../index.html';
  }
  window.location.href = path;
}

window.evcLogout = function() {
  sessionStorage.removeItem('evc_auth');
  let path = '../index.html';
  if (window.location.pathname.includes('/starrs/')) {
    path = '../../index.html';
  }
  window.location.href = path;
};

// 3. Navigatiebalk Generator
const CHECKBOX_IDS = [
  'v1-1', 'v1-2', 'v1-3',
  'v2-1', 'v2-2',
  'v3-1', 'v3-2',
  'v4-1', 'v4-2',
  'v5-1', 'v5-2',
  'v6-1',
  'v7-1', 'v7-2',
  's1-1', 's1-2', 's1-3',
  's2-1', 's2-2',
  's3-1', 's3-2', 's3-3',
  's4-1'
];

const STATUS_IDS = [
  'a2_zelf', 'a2_bew1', 'a2_bew2',
  'a3_zelf', 'a3_bew1', 'a3_bew2',
  'a4_zelf', 'a4_bew1', 'a4_bew2', 'a4_obs', 'a4_ref',
  'a5_zelf', 'a5_bew1', 'a5_bew2',
  'b1_zelf', 'b1_bew1', 'b1_bew2',
  'b2_zelf', 'b2_bew1', 'b2_bew2',
  'b3_zelf', 'b3_bew1', 'b3_bew2',
  'b4_lit', 'b4_refl', 'b4_pop', 'b4_fdbk_verst', 'b4_fdbk_verwerkt',
  'c3_zelf', 'c3_bew1', 'c3_bew2',
  'c2_besluit',
  'd1_cv', 'd1_schema', 'd1_lid', 'd1_aanmeld', 'd1_werk_verkl', 'd1_diploma'
];

function genereerNav() {
  const nav = document.querySelector('nav');
  if (!nav) return;
  
  let prefix = '';
  if (window.location.pathname.includes('/starrs/')) {
    prefix = '../';
  }
  
  const currentPath = window.location.pathname;
  const inStarrs = currentPath.includes('/starrs/');
  
  // Eenvoudige extractie van bestandsnaam
  const parts = currentPath.split('/');
  const currentFile = parts[parts.length - 1] || 'index.html';
  
  const links = [
    { label: 'Start', url: prefix + 'index.html', active: currentFile === 'index.html' && !inStarrs },
    { label: 'Dashboard', url: prefix + 'dashboard.html', active: currentFile === 'dashboard.html' },
    { label: 'Status', url: prefix + 'status.html', active: currentFile === 'status.html' },
    { label: 'Opdrachten', url: prefix + 'opdrachten.html', active: currentFile === 'opdrachten.html' },
    { label: 'STARR\'s', url: prefix + 'starrs/index.html', active: inStarrs },
    { label: 'Profiel', url: prefix + 'profiel.html', active: currentFile === 'profiel.html' },
    { label: 'Documenten', url: prefix + 'documenten.html', active: currentFile === 'documenten.html' }
  ];
  
  let html = '<div class="nav-binnen">';
  html += `<a class="nav-logo" href="${prefix}index.html">EVC NT2</a>`;
  links.forEach(l => {
    html += `<a href="${l.url}" class="${l.active ? 'active' : ''}">${l.label}</a>`;
  });
  html += '<a href="javascript:void(0)" onclick="evcLogout()" style="margin-left:auto; color:var(--rood);">🔒 Uitloggen</a>';
  html += '</div>';
  
  nav.innerHTML = html;
  nav.setAttribute('aria-label', 'Hoofdnavigatie');
}

// 4. Voortgangsberekening
function getEVCProgress() {
  let checkedCount = 0;
  CHECKBOX_IDS.forEach(id => {
    if (ophalen('evc_' + id) === '1') {
      checkedCount++;
    }
  });

  let definitiefCount = 0;
  STATUS_IDS.forEach(id => {
    if (ophalen('evc_status_' + id) === 'Definitief') {
      definitiefCount++;
    }
  });

  const totalTasks = CHECKBOX_IDS.length + STATUS_IDS.length;
  const completedTasks = checkedCount + definitiefCount;
  const percentage = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return {
    completed: completedTasks,
    total: totalTasks,
    percentage: percentage,
    checkedCount: checkedCount,
    definitiefCount: definitiefCount
  };
}

// DomContentLoaded init
document.addEventListener('DOMContentLoaded', () => {
  genereerNav();
  
  // Als er een opslag-status element is op de geopende pagina, configureer dit
  const opslagStatusEl = document.getElementById('opslag-status');
  if (opslagStatusEl) {
    if (!opslagOk) {
      opslagStatusEl.textContent = 'Let op: opslag niet beschikbaar. Open de site via een webserver (zoals Netlify) om voortgang op te slaan.';
      opslagStatusEl.classList.add('geheugen');
    } else {
      opslagStatusEl.textContent = 'Voortgang wordt automatisch lokaal opgeslagen';
      opslagStatusEl.classList.remove('geheugen');
    }
  }

  // Zet datum neer op pagina's waar id="datum-nu" aanwezig is
  const datumNuEl = document.getElementById('datum-nu');
  if (datumNuEl) {
    datumNuEl.textContent = new Date().toLocaleDateString('nl-NL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  }
});
