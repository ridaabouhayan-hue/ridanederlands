# Google Apps Script Setup voor E-mail Back-up (Generiek & Herbruikbaar)

Dit document bevat de code en stapsgewijze instructies om de A2-oefenomgeving te verbinden met jouw e-mailinbox. 

> [!TIP]
> De code is zo ontworpen dat deze **universeel en herberuikbaar** is. Je hoeft dit script maar één keer op te zetten in Google Apps Script. Daarna kun je **dezelfde URL** gebruiken voor al je toekomstige toetsen en HTML-pagina's zonder dat je de Google Script-code hoeft aan te passen!

---

## Deel 1: De Google Apps Script Code (Universeel)

Kopieer de onderstaande JavaScript-code volledig:

```javascript
function doPost(e) {
  try {
    // Ontvang de gegevens van de website
    var data = JSON.parse(e.postData.contents);
    
    // ===== HIER JOUW STANDAARD E-MAILADRES INVULLEN =====
    var defaultRecipient = "ridaabouhayan@gmail.com"; 
    // ==========================================
    
    // Ontvanger bepalen (gebruik meegestuurde 'toEmail', of val terug op standaard)
    var recipientEmail = data.toEmail || defaultRecipient;
    
    // Onderwerp en body bepalen
    var subject = "";
    var body = "";
    
    if (data.subject && data.body) {
      // 1. GENERIEKE ROUTE (Voor nieuwe toetsen en herbruikbaarheid!)
      subject = data.subject;
      body = data.body;
    } else {
      // 2. LEGACY ROUTE (Automatische compatibiliteit met de A2-oefenomgeving)
      body = data.reportText || "Geen inhoud meegegeven.";
      if (data.examType === "schrijven" && data.opgaveIndex) {
        subject = "📝 A2 Schrijven - " + data.opgaveTitle + " - " + data.kandidaat;
      } else if (data.examType === "schrijven") {
        subject = "📝 A2 Schrijven Examen " + data.examId + " (Compleet) - " + data.kandidaat;
      } else if (data.examType === "lezen") {
        subject = "📖 A2 Lezen Examen " + data.examId + " - " + data.kandidaat;
      } else {
        subject = "🇳🇱 A2 Examen Resultaat - " + (data.kandidaat || "Onbekend");
      }
    }
    
    // Verstuur de e-mail
    MailApp.sendEmail({
      to: recipientEmail,
      subject: subject,
      body: body
    });
    
    // Return succes status
    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return foutmelding als er iets misgaat
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

---

## Deel 2: Stappenplan om te Deployen (Eenmalig)

Volg deze stappen om het script te publiceren:

1. **Open Google Apps Script:**
   Ga naar [script.google.com](https://script.google.com/) en log in met je Google-account.

2. **Nieuw project:**
   Klik linksboven op de blauwe knop **Nieuw project** (New Project).

3. **Plak de code:**
   - Wis alle eventuele code die al in de editor staat (`function myFunction() { ... }`).
   - Plak de gekopieerde code hierboven in de editor.

4. **Pas je e-mailadres aan:**
   Pas op regel 6 `ridaabouhayan@gmail.com` aan naar het e-mailadres waarop je de resultaten standaard wilt ontvangen.

5. **Sla het project op:**
   Klik op het **schijf-icoontje** (Opslaan / Save) bovenaan. Geef het project een naam, bijvoorbeeld: *Universele Mail Koppeling*.

6. **Deploy als Web App:**
   - Klik rechtsboven op de blauwe knop **Implementeren** (Deploy) en kies **Nieuwe implementatie** (New deployment).
   - Klik naast "Type selecteren" op het tandwiel-icoontje en kies **Web-app** (Web app).
   - Vul de volgende velden in:
     - **Beschrijving (Description):** *Examen Mailer*
     - **Uitvoeren als (Execute as):** **Ikzelf / Me** (jouw eigen Gmail-adres)
     - **Wie heeft toegang (Who has access):** **Iedereen / Anyone** (essentieel zodat websites verbinding kunnen maken!).
   - Klik op de blauwe knop **Implementeren** (Deploy).

7. **Toegang verlenen:**
   Google vraagt om toestemming om e-mails te sturen namens jou.
   - Klik op **Toegang verlenen** (Authorize access).
   - Kies je Google-account.
   - Krijg je een waarschuwing dat de app niet geverifieerd is? Klik onderin op **Geavanceerd** (Advanced) en daarna op **Ga naar Universele Mail Koppeling (onveilig)**.
   - Klik op **Toestaan** (Allow).

8. **Kopieer de Web-app URL:**
   - Kopieer de gegenereerde **Web-app-URL** (begint met `https://script.google.com/macros/s/...`).

---

## Deel 3: De link in de A2 website zetten

1. Open het bestand [index.html](file:///g:/Mijn%20Drive/HTML%20FILES/A2%20examen/index.html).
2. Zoek helemaal bovenaan in het `<script>` gedeelte (ongeveer regel 1338) naar deze regel:
   ```javascript
   const GOOGLE_APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx_YOUR-SCRIPT-ID-HERE/exec";
   ```
3. Vervang de dummy URL tussen de aanhalingstekens door de Web-app-URL die je bij stap 8 hebt gekregen.
4. Sla het bestand op.

---

## Deel 4: Hoe gebruik je dit bij NIEUWE toetsen of oefeningen?

Als je in de toekomst een nieuwe toets maakt (bijvoorbeeld `lezen_3.html` of `spreken_oefening.html`), hoef je **geen nieuw Google Script aan te maken**. Je gebruikt gewoon dezelfde URL!

Plak de onderstaande Javascript-functie in je nieuwe HTML-bestand:

```javascript
// Pas deze URL aan naar jouw Universele Web App URL!
const GOOGLE_MAIL_URL = "HIER_JOUW_GEKOPIEERDE_WEB_APP_URL"; 

function verstuurNaarEmail(onderwerp, inhoud, naarEmail = "ridaabouhayan@gmail.com") {
    // Bouw de generieke data op
    const data = {
        toEmail: naarEmail,
        subject: onderwerp,
        body: inhoud
    };

    // Stuur naar Google Script
    fetch(GOOGLE_MAIL_URL, {
        method: "POST",
        mode: "no-cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(() => console.log("Resultaten succesvol naar e-mail verzonden op de achtergrond!"))
    .catch(err => console.error("Fout bij achtergrond e-mail:", err));
}
```

### Voorbeeld van gebruik in een nieuwe toets:
Wanneer een student op "Toets afronden" of "Verstuur" klikt in je nieuwe bestand, roep je de functie simpelweg zo aan:

```javascript
// Voorbeeld:
const onderwerp = "🏆 Resultaat: Lezen Examen 2 - Ali Yilmaz";
const resultatenText = "Vraag 1: A (Goed)\nVraag 2: C (Fout)\nTotaalscore: 18/20 goed.";

verstuurNaarEmail(onderwerp, resultatenText);
```

Het script regelt de rest en stuurt de e-mail direct naar jouw inbox. Dit maakt het super makkelijk om snel nieuwe onderdelen toe te voegen!
