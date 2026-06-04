import os
import sys
import json
import subprocess
from google import genai

# ================================================
# 1. API KEY INSTELLEN
root_dir = os.path.dirname(os.path.abspath(__file__))
api_key_path = os.path.join(root_dir, "API.txt")

GEMINI_API_KEY = None
if os.path.exists(api_key_path):
    with open(api_key_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip()
                break

if not GEMINI_API_KEY:
    print("❌ Kan GEMINI_API_KEY niet vinden in API.txt in de hoofdmap.")
    sys.exit(1)

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# ================================================
# 2. HUISWERK INLEZEN
homework_file = os.path.join(root_dir, "huiswerk.txt")
if not os.path.exists(homework_file):
    print("❌ Kan huiswerk.txt niet vinden. Open de batch-file om te starten.")
    sys.exit(1)

with open(homework_file, "r", encoding="utf-8") as f:
    homework_content = f.read().strip()

if not homework_content:
    print("❌ Het bestand huiswerk.txt is leeg! Plak er eerst huiswerk in.")
    sys.exit(1)

# ================================================
# 3. GEMINI AANROEPEN
print("⏳ Bezig met nakijken via Gemini...")

prompt = f"""Je bent een deskundige NT2 docent (Nederlands als Tweede Taal). Een cursist heeft huiswerk ingeleverd (dit kan een woordenlijst zijn met definities en voorbeeldzinnen, of een geschreven tekst).
  
Kijk het huiswerk grondig na op:
1. Betekenis en vertaling (is de vertaling naar de moedertaal correct? Zo nee, geef de juiste vertaling).
2. Grammatica en woordvolgorde in de voorbeeldzinnen/tekst.
3. Spelling, woordvorm en leestekens.

Schrijf een opbouwende, vriendelijke en motiverende feedbackbrief in het Nederlands gericht aan de cursist, geschikt om via WhatsApp te sturen.
BELANGRIJK:
- Formatteer voor WhatsApp: gebruik een ENKELE asterisk (*) voor vetgedrukte woorden (zoals *Zin 1:* of *Correctie:*). Gebruik absoluut GEEN dubbele asterisks (**).
- Geef duidelijke uitleg bij eventuele fouten. Als de cursist een vertaling of woord verkeerd heeft begrepen, of een grammaticafout maakt, leg dan kort in de moedertaal van de cursist uit wat het verschil is (bijvoorbeeld in het Pools, Arabisch, Chinees, etc., afhankelijk van welke taal de cursist gebruikt in het huiswerk).
- Als een zin of woord helemaal goed is, geef dan een compliment (bijv. "Helemaal goed!").

Hier is het huiswerk van de cursist:
---
{homework_content}
---
"""

try:
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={'temperature': 0.2}
    )
    feedback = response.text
except Exception as e:
    print(f"❌ Fout bij het aanroepen van Gemini: {e}")
    sys.exit(1)

# Print feedback naar de console
print("\n===================================================")
print("📝 GEGENEREERDE FEEDBACK:")
print("===================================================\n")
print(feedback)
print("\n===================================================")

# ================================================
# 4. KOPIËREN NAAR KLEMBORD
def copy_to_clipboard(text):
    # Probeer eerst via tkinter (het meest betrouwbaar met unicode op Windows)
    try:
        import tkinter as tk
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()
        return True
    except Exception:
        # Fallback naar Windows native clip command
        try:
            subprocess.run("clip", input=text, text=True, check=True, shell=True)
            return True
        except Exception:
            return False

if copy_to_clipboard(feedback):
    print("✅ Succes! De feedback is automatisch gekopieerd naar je klembord.")
    print("   Je kunt het direct in WhatsApp plakken met Ctrl + V.")
else:
    print("⚠️ Waarschuwing: Kon de feedback niet automatisch kopiëren naar je klembord.")
    print("   Kopieer de bovenstaande tekst handmatig uit dit venster.")
