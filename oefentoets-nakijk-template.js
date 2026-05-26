/**
 * TEMPLATE: AUTOMATISCH NAKIJKEN & RAPPORTEREN OEFENTOETSEN
 * 
 * Dit bestand dient als standaard template voor het nakijken en formatteren van 
 * oefentoetsen binnen het ridanederlands-project. Kopieer en pas deze logica aan 
 * voor andere thema's of niveaus (A1, A2, etc.).
 */

// ==========================================
// 1. DEFINEER DE ANTWOORDSLEUTELS
// ==========================================
const answerKeys = {
    // Definieer per sectie een array met geldige antwoorden (inclusief synoniemen/lidwoorden)
    woordenschat: [
        ["antwoord1", "alternatief1"],
        ["antwoord2", "alternatief2"]
    ],
    grammatica: [
        ["antwoord1"],
        ["antwoord2"]
    ],
    voorzetsels: [
        ["antwoord1"],
        ["antwoord2"]
    ],
    dictee: [
        ["Hele zin 1.", "Hele zin 1 zonder punt"],
        ["Hele zin 2.", "Hele zin 2 zonder punt"]
    ],
    vraagwoorden: [
        ["antwoord1"],
        ["antwoord2"]
    ]
};

// ==========================================
// 2. NORMALISATIE & GRADING LOGICA
// ==========================================

/**
 * Normaliseert invoer door leestekens te verwijderen, lowercase te maken en spaties te trimmen.
 */
function normalize(str) {
    if (!str) return "";
    return str.toLowerCase()
        .replace(/[\.\?\!\,\;]/g, '') // Verwijder punten, vraagtekens, komma's, etc.
        .replace(/\s+/g, ' ')         // Vervang meerdere spaties door 1 spatie
        .trim();
}

/**
 * Berekent de Levenshtein-afstand tussen twee strings (aantal aanpassingen).
 */
function getLevenshteinDistance(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    const matrix = [];
    for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1, // vervanging
                    Math.min(
                        matrix[i][j - 1] + 1, // invoeging
                        matrix[i - 1][j] + 1  // verwijdering
                    )
                );
            }
        }
    }
    return matrix[b.length][a.length];
}

/**
 * Beoordeelt het antwoord van de student tegen de lijst van correcte antwoorden.
 * @param {string} studentAns Het antwoord van de cursist.
 * @param {string[]} correctList De lijst van geldige antwoorden.
 * @param {boolean} isSentence Indien true, betreft het een zin (zoals dictee) met een ruimere spelfoutmarge.
 * @returns {object} { status: "correct"|"half"|"incorrect", score: 0|0.5|1 }
 */
function gradeAnswer(studentAns, correctList, isSentence = false) {
    const studentNorm = normalize(studentAns);
    
    // 1. Exacte match (na normalisatie) -> Goed (1 punt)
    if (correctList.some(ans => normalize(ans) === studentNorm)) {
        return { status: "correct", score: 1.0 };
    }
    
    // 2. Levenshtein-controle voor spelfouten -> Half goed (0.5 punt)
    if (studentNorm.length > 0) {
        let minDistance = Infinity;
        for (let ans of correctList) {
            const ansNorm = normalize(ans);
            const dist = getLevenshteinDistance(studentNorm, ansNorm);
            if (dist < minDistance) {
                minDistance = dist;
            }
        }
        
        let threshold = 2; // Standaard marge voor losse woorden
        if (isSentence) {
            threshold = 5; // Marge voor hele zinnen (dictee)
        } else {
            const primaryLen = normalize(correctList[0]).length;
            if (primaryLen <= 4) {
                threshold = 1; // Heel korte woorden (marge van max 1 letter)
            }
        }
        
        if (minDistance <= threshold) {
            return { status: "half", score: 0.5 };
        }
    }
    
    // 3. Foutief -> Fout (0 punten)
    return { status: "incorrect", score: 0.0 };
}

// ==========================================
// 3. WHATSAPP RAPPORTAGE & FEEDBACK GENERATOR
// ==========================================
function sendToWhatsApp() {
    // Haal de naam van de student op
    const nameInput = document.getElementById('student-name');
    const studentName = nameInput ? nameInput.value.trim() : "";
    if (!studentName) {
        alert("Vul alstublieft eerst je naam in.");
        if (nameInput) nameInput.focus();
        return;
    }

    // Helpers om de ingevulde waardes op te halen
    const val = (id) => (document.getElementById(id).value || "").trim();
    const dropVal = (id) => document.getElementById(id).getAttribute('data-answer') || "";

    let totalScore = 0;
    let report = `*RESULTAAT OEFENTOETS THEMA [NUMMER] ([NIVEAU])*\n`;
    report += `*Naam:* ${studentName}\n\n`;

    // ------------------------------------------
    // SECTIE 1: VERWERK ONDERDEEL 1
    // ------------------------------------------
    let score1 = 0;
    let report1 = `*1. [Sectienaam]* (Score: {SCORE1}/[AantalVragen])\n`;
    
    for (let i = 1; i <= 2; i++) { // pas de range aan naar aantal vragen
        const ans = val('q1_' + i); // of dropVal(...)
        const correctList = answerKeys.woordenschat[i - 1];
        const res = gradeAnswer(ans, correctList);
        score1 += res.score;
        
        if (res.status === "correct") {
            report1 += `- Vraag ${i} = ${ans || "..."} ✅\n`;
        } else if (res.status === "half") {
            report1 += `- Vraag ${i} = ${ans || "..."} 🟠 (spelling, moet zijn: ${correctList[0]})\n`;
        } else {
            report1 += `- Vraag ${i} = ${ans || "..."} ❌ (moet zijn: ${correctList[0]})\n`;
        }
    }
    report1 = report1.replace("{SCORE1}", String(score1).replace('.', ','));
    totalScore += score1;
    report1 += `\n`;

    // Herhaal bovenstaande structuur voor report2, report3, report4, etc.

    // Totaalscore afronden met komma's
    let formattedTotalScore = String(totalScore).replace('.', ',');
    report += `*TOTAALSCORE:* ${formattedTotalScore}/[TotaalAantalVragen]\n\n`;
    report += report1; // + report2 + report3 + etc.

    // ------------------------------------------
    // SECTIE 2: GENEREER FEEDBACKBRIEF
    // ------------------------------------------
    let feedback = `*--- FEEDBACKBRIEF VOOR DE CURSIST ---*\n\n`;
    feedback += `Beste ${studentName},\n\n`;
    feedback += `Je hebt de oefentoets voor Thema [NUMMER] gemaakt. Goed gedaan! Hier is jouw resultaat:\n\n`;
    feedback += `*Jouw resultaat:*\n`;
    feedback += `- *Score:* ${formattedTotalScore} van de [TotaalAantalVragen] punten goed.\n`;
    const passed = totalScore >= 20; // Pas de voldoende-grens aan
    feedback += `- *Resultaat:* ${passed ? "Dit is een *voldoende*! Gefeliciteerd! 🎉" : "Dit is helaas nog *onvoldoende*. Geef niet op, oefen nog een keer! 💪"}\n\n`;

    let goedPunten = [];
    let oefenPunten = [];

    // Evalueer prestaties per onderdeel en voeg gerichte grammatica/spellingstips toe
    // Voorbeeld:
    if (score1 >= 5) {
        goedPunten.push(`*Onderdeel 1 (${String(score1).replace('.', ',')}/7):* Omschrijving van wat al goed gaat.`);
    } else {
        oefenPunten.push(`*Onderdeel 1 (${String(score1).replace('.', ',')}/7):* Uitleg en tips voor wat beter kan.`);
    }

    feedback += `*Wat gaat al goed:*\n`;
    feedback += goedPunten.length > 0 ? `- ` + goedPunten.join('\n- ') + `\n\n` : `- Blijf oefenen, je bent op de goede weg!\n\n`;

    feedback += `*Wat kun je nog oefenen:*\n`;
    feedback += oefenPunten.length > 0 ? `- ` + oefenPunten.join('\n- ') + `\n\n` : `- Geen leertips, je hebt alles onder de knie! Super!\n\n`;

    feedback += `Met vriendelijke groet,\nDe docent`;

    const finalMessage = report + `\n\n` + feedback;

    // Open WhatsApp
    const phone = "31626211106";
    const url = `https://wa.me/${phone}?text=${encodeURIComponent(finalMessage)}`;
    window.open(url, '_blank');
}
