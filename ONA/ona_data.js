// Data structuur en logica voor het gedetailleerde ONA Dashboard

const CLOUD_API_URL = "https://api.restful-api.dev/objects/ff8081819d82fab6019e802499c624b8";

const onaItems = [
    { id: 'c1', label: 'K1: Oriëntatie', type: 'card' },
    { id: 'c2', label: 'K2: Beroepsbeeld', type: 'card' },
    { id: 'c3', label: 'K3: Kwaliteiten', type: 'card' },
    { id: 'c4', label: 'K4: Kansen', type: 'card' },
    { id: 'd_vac1', label: '📄 Vacature 1', type: 'doc' },
    { id: 'd_vac2', label: '📄 Vacature 2', type: 'doc' },
    { id: 'c5', label: 'K5: Competenties', type: 'card' },
    { id: 'c6', label: 'K6: Netwerk', type: 'card' },
    { id: 'c7', label: 'K7: Werk vinden', type: 'card' },
    { id: 'd_cv', label: '📄 CV', type: 'doc' },
    { id: 'd_brief', label: '📄 Motivatiebrief', type: 'doc' },
    { id: 'd_form1', label: '📄 Formulier 1', type: 'doc' },
    { id: 'd_form2', label: '📄 Formulier 2', type: 'doc' },
    { id: 'c8', label: 'K8: Werkcultuur', type: 'card' }
];

function createEmptyItems() {
    const items = {};
    onaItems.forEach(item => {
        items[item.id] = 'open'; 
    });
    return items;
}

const defaultData = {
    "ona-35": [],
    "ona-36": [],
    "ona-37": [],
    "ona-38": [],
    "ona-39": [],
    "ona-40": [],
    "ona-41": [],
    "ona-42": [],
    "ona-43": [
        { id: "43-1", name: "Andrea", driveLink: "https://drive.google.com/", items: createEmptyItems(), submitted: false },
        { id: "43-2", name: "Neeraj", driveLink: "https://drive.google.com/", items: createEmptyItems(), submitted: false },
        { id: "43-3", name: "Zohreh", driveLink: "https://drive.google.com/", items: createEmptyItems(), submitted: false },
        { id: "43-4", name: "Hiba", driveLink: "https://drive.google.com/", items: createEmptyItems(), submitted: false },
        { id: "43-5", name: "Seetha", driveLink: "https://drive.google.com/", items: createEmptyItems(), submitted: false }
    ]
};

let activeGroup = "ona-43";
let onaData = defaultData; // Start met default, wordt overschreven door cloud
let isLoaded = false;

// Cloud logica
async function loadFromCloud() {
    try {
        const response = await fetch(CLOUD_API_URL);
        const json = await response.json();
        
        if (json && json.data && json.data.onaData) {
            onaData = json.data.onaData;
            // Migreer of reset als de oude groepsstructuur er nog is of als we nieuwe groepen missen
            if (onaData["groep-42"] || !onaData["ona-43"]) {
                onaData = defaultData;
                saveToCloud();
            }
        } else {
            // Eerste keer? Gebruik defaultData en sla direct op
            onaData = defaultData;
            saveToCloud();
        }
        isLoaded = true;
        renderDashboard();
    } catch (e) {
        console.error("Fout bij laden uit cloud:", e);
        alert("Kon data niet laden uit de cloud. Controleer je internetverbinding.");
    }
}

async function saveToCloud() {
    try {
        await fetch(CLOUD_API_URL, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: "ona_rabou_db",
                data: { onaData: onaData }
            })
        });
    } catch (e) {
        console.error("Fout bij opslaan naar cloud:", e);
        alert("Fout bij opslaan! Controleer je internetverbinding.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Dark mode instellen op basis van localstorage
    if (localStorage.getItem('onaDarkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }

    // Voeg dynamisch event listeners toe aan alle groepsselectie knoppen
    document.querySelectorAll('.group-tabs .tab-btn').forEach(btn => {
        const groupId = btn.id.replace('btn-', '');
        btn.addEventListener('click', () => switchGroup(groupId));
    });
    
    // Haal data op uit de cloud!
    loadFromCloud();
});

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('onaDarkMode', isDark ? 'true' : 'false');
}

function switchGroup(groupId) {
    activeGroup = groupId;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${groupId}`).classList.add('active');
    renderDashboard();
}

function toggleItemStatus(studentId, itemId) {
    if (!isLoaded) return;
    
    const students = onaData[activeGroup];
    const student = students.find(s => s.id === studentId);
    
    // Altijd aanpasbaar, ook als submitted!
    if (student) {
        const current = student.items[itemId];
        let next = 'open';
        if (current === 'open') next = 'feedback';
        else if (current === 'feedback') next = 'goed';
        else if (current === 'goed') next = 'open';
        
        student.items[itemId] = next;
        
        // Zodra niet alles meer 'goed' is, gaat de 'ingediend' badge weg
        let allGood = true;
        onaItems.forEach(item => {
            if (student.items[item.id] !== 'goed') allGood = false;
        });
        
        if (!allGood) {
            student.submitted = false;
        }
        
        // Asynchroon opslaan en direct renderen voor snelle UI
        saveToCloud();
        renderDashboard();
    }
}

function submitPortfolio(studentId) {
    if (confirm("Weet je zeker dat het portfolio online is ingediend?")) {
        const students = onaData[activeGroup];
        const student = students.find(s => s.id === studentId);
        
        if (student) {
            student.submitted = true;
            saveToCloud();
            renderDashboard();
            
            if (window.confetti) {
                confetti({
                    particleCount: 150,
                    spread: 80,
                    origin: { y: 0.6 },
                    colors: ['#fce043', '#fb7ba2', '#4361ee', '#2ec4b6']
                });
            }
        }
    }
}

function addNewStudent() {
    const name = prompt("Naam van de cursist:");
    if (!name) return;
    
    const driveLink = prompt("Link naar Google Drive map (optioneel):", "https://drive.google.com/");
    
    const newStudent = {
        id: Date.now().toString(),
        name: name,
        driveLink: driveLink || "#",
        items: createEmptyItems(),
        submitted: false
    };
    
    onaData[activeGroup].push(newStudent);
    saveToCloud();
    renderDashboard();
}

function renderDashboard() {
    const grid = document.getElementById('dashboard-grid');
    grid.innerHTML = ''; 
    
    if (!isLoaded) {
        grid.innerHTML = '<div style="text-align:center; padding:50px; font-size:1.5em; grid-column: 1 / -1;">☁️ Data ophalen uit de cloud... Momentje!</div>';
        return;
    }
    
    const students = onaData[activeGroup];
    
    students.forEach(student => {
        const card = document.createElement('div');
        card.className = 'student-card detail-card'; 
        
        let itemsHtml = '<div class="items-grid">';
        let allGood = true;
        
        onaItems.forEach(item => {
            const status = student.items[item.id]; 
            if (status !== 'goed') allGood = false;
            
            const isDoc = item.type === 'doc';
            const indentClass = isDoc ? 'item-doc' : 'item-card';
            
            let icon = '⚪';
            if (status === 'feedback') icon = '🟠';
            if (status === 'goed') icon = '✅';
            
            itemsHtml += `
                <div class="tracker-item status-badge-${status} ${indentClass}" onclick="toggleItemStatus('${student.id}', '${item.id}')">
                    <span class="item-icon">${icon}</span>
                    <span class="item-label">${item.label}</span>
                </div>
            `;
        });
        itemsHtml += '</div>';
        
        let submitHtml = '';
        if (student.submitted) {
            submitHtml = `<div class="submitted-badge">🎉 Portfolio online ingediend!</div>`;
        } else if (allGood) {
            submitHtml = `<button class="confetti-btn" onclick="submitPortfolio('${student.id}')">✨ Portfolio online ingediend?</button>`;
        }
        
        card.innerHTML = `
            <div class="student-header">
                <div class="student-name">
                    👤 ${student.name}
                </div>
                <a href="${student.driveLink}" target="_blank" class="drive-link" title="Open Google Drive">📁</a>
            </div>
            
            <div class="items-section">
                ${itemsHtml}
            </div>
            
            ${submitHtml}
        `;
        
        grid.appendChild(card);
    });
    
    const addCard = document.createElement('button');
    addCard.className = 'add-student-btn';
    addCard.innerHTML = '➕ Nieuwe cursist';
    addCard.onclick = addNewStudent;
    grid.appendChild(addCard);
}
