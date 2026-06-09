# Google Apps Script Setup voor ONA Dashboard Synchronisatie

Dit document bevat de code en stapsgewijze instructies om je ONA Dashboard te koppelen aan je eigen Google Drive. Hierdoor wordt alle voortgang van je cursisten veilig opgeslagen in een bestand genaamd `ona_dashboard_data.json` in jouw Google Drive en synchroniseert het automatisch tussen al je apparaten (telefoon, laptop, computer).

---

## Deel 1: De Google Apps Script Code

Kopieer de onderstaande code volledig:

```javascript
function doGet(e) {
  // CORS header toevoegen zodat de browser de response mag lezen
  return ContentService.createTextOutput(JSON.stringify(getData()))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    saveData(data);
    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getData() {
  var fileName = "ona_dashboard_data.json";
  var files = DriveApp.getFilesByName(fileName);
  if (files.hasNext()) {
    var file = files.next();
    var content = file.getAs("application/json").getDataAsString();
    return JSON.parse(content);
  }
  return { onaData: null };
}

function saveData(data) {
  var fileName = "ona_dashboard_data.json";
  var files = DriveApp.getFilesByName(fileName);
  var file;
  if (files.hasNext()) {
    file = files.next();
    file.setContent(JSON.stringify(data));
  } else {
    file = DriveApp.createFile(fileName, JSON.stringify(data), "application/json");
  }
}
```

---

## Deel 2: Stappenplan om te Deployen (Eenmalig)

Volg deze eenvoudige stappen om het script te publiceren in je Google-account:

1. **Open Google Apps Script:**
   Ga naar [script.google.com](https://script.google.com/) en log in met je Google-account.

2. **Nieuw project:**
   Klik linksboven op de blauwe knop **Nieuw project** (New Project).

3. **Plak de code:**
   - Wis alle eventuele code die al in de editor staat (`function myFunction() { ... }`).
   - Plak de gekopieerde code hierboven in de editor.

4. **Sla het project op:**
   Klik op het **schijf-icoontje** (Opslaan / Save) bovenaan. Geef het project een naam, bijvoorbeeld: *ONA Dashboard Sync*.

5. **Deploy als Web App (Cruciaal voor toegang vanaf apparaten):**
   - Klik rechtsboven op de blauwe knop **Implementeren** (Deploy) en kies **Nieuwe implementatie** (New deployment).
   - Klik naast "Type selecteren" op het tandwiel-icoontje en kies **Web-app** (Web app).
   - Vul de volgende velden in:
     - **Beschrijving (Description):** *ONA Sync Service*
     - **Uitvoeren als (Execute as):** **Ikzelf / Me** (jouw eigen Gmail-adres)
     - **Wie heeft toegang (Who has access):** **Iedereen / Anyone** (dit is essentieel zodat je dashboard vanaf elk apparaat verbinding kan maken).
   - Klik op de blauwe knop **Implementeren** (Deploy).

6. **Toegang verlenen:**
   Google vraagt om toestemming om bestanden te beheren in Google Drive (om het JSON-bestand te kunnen opslaan).
   - Klik op **Toegang verlenen** (Authorize access).
   - Kies je Google-account.
   - Krijg je een waarschuwing dat de app niet geverifieerd is? Geen zorgen, dit is je eigen script! Klik onderin op **Geavanceerd** (Advanced) en daarna op **Ga naar ONA Dashboard Sync (onveilig)**.
   - Klik op **Toestaan** (Allow).

7. **Kopieer de Web-app URL:**
   - Kopieer de gegenereerde **Web-app-URL** (begint met `https://script.google.com/macros/s/.../exec`).

---

## Deel 3: De link in het ONA Dashboard zetten

1. Open je **ONA Dashboard** in de browser.
2. Klik bovenaan in de header op de nieuwe knop **⚙️ Cloud Sync**.
3. Plak de Web-app URL in het invoerveld en klik op **Opslaan**.
4. Je dashboard synchroniseert nu direct! Doe dit op al je apparaten (met dezelfde URL) om overal dezelfde cursisten en voortgang te zien.
