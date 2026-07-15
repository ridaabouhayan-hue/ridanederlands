"""Nexus of Language — pre-generate ElevenLabs mp3s.

Adapted from ../../genereer_toets_audio.py. Male dialogue speakers get a male
voice; everyone else a female voice. Tuned for slow, clear NT2 pronunciation
(lower speed, higher stability). TTS text is cleaned (drop "...", turn "a / b"
into a natural pause) while the FILENAME slug is derived from the original
display text so it still matches Audio_.slugify() in js/audio.js.

Usage:  python generate_audio.py           (skips files that already exist)
        python generate_audio.py --force    (regenerate everything)
"""

import os
import re
import sys
import json
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
API_FILE = os.path.join(REPO_ROOT, 'API_ELEVENLABS.txt')
VOICES_FILE = os.path.join(REPO_ROOT, 'stemmen.json')
AUDIO_DIR = os.path.join(os.path.dirname(__file__), '..', 'audio')

FORCE = '--force' in sys.argv


def slugify(text):
    """Must match Audio_.slugify() in js/audio.js."""
    t = text.lower()
    t = re.sub(r"[.,?!;:()'\"/\\:*<>|]", '', t)
    t = t.strip()
    t = re.sub(r'\s+', '_', t)
    return t


def clean_for_tts(text):
    """Make the spoken form clearer without changing the slug."""
    t = text.replace('...', '')
    t = t.replace('/', ', ')          # "groot / klein" -> natural pause
    t = re.sub(r'\s+', ' ', t).strip()
    if ' ' not in t and not t.endswith(('.', '?', '!')):
        t = t[:1].upper() + t[1:] + '.'   # isolated words: clearer with a period
    return t


def load_api_key():
    if not os.path.exists(API_FILE):
        print(f"Fout: '{API_FILE}' niet gevonden!"); return None
    with open(API_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()


def load_voices():
    if not os.path.exists(VOICES_FILE):
        print(f"Fout: '{VOICES_FILE}' niet gevonden!"); return None
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_speech(text, voice_id, api_key, output_path):
    if os.path.exists(output_path) and not FORCE:
        print(f"Overslaan (bestaat al): {os.path.basename(output_path)}"); return 'skip'
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": api_key}
    data = {
        "text": clean_for_tts(text),
        "model_id": "eleven_multilingual_v2",
        # Slow + clear + steady for NT2 learners.
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.0,
            "use_speaker_boost": True,
            "speed": 0.82
        }
    }
    print(f"Genereren: '{text}' -> {os.path.basename(output_path)}")
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(r.content)
        return 'ok'
    print(f"❌ Fout ({r.status_code}): {r.text}")
    return 'err'


# Every Dutch text spoken anywhere in data/course.js.
ALL_TEXTS = [
    # Unit 1
    "Hallo! Ik heet Fatima. Hoe heet jij?", "Hoi Fatima, ik ben Youssef.",
    "Waar kom je vandaan?", "Ik kom uit Marokko. En jij?",
    "Ik kom uit Syrië. Ik woon nu in Utrecht.", "Leuk je te ontmoeten!",
    "hallo", "ik heet...", "ik kom uit...", "ik woon in...", "hoe heet jij?",
    "waar kom je vandaan?", "leuk je te ontmoeten", "tot ziens",
    "Hallo, ik heet Fatima.", "Tot ziens!",
    # Unit 2
    "Heb jij een grote familie?", "Ja, ik heb een broer en twee zussen.",
    "Ben je getrouwd?", "Nee, ik ben niet getrouwd. En jij?",
    "Ik ben getrouwd. Ik heb een dochter.",
    "de vader", "de moeder", "de broer", "de zus", "ik heb...",
    "het kind / de kinderen", "getrouwd", "mijn",
    "Dit is mijn moeder.", "Ik ben niet getrouwd.", "Ik heb een broer en twee zussen.",
    # Unit 3
    "Waar woon je, Fatima?", "Ik woon in een kleine flat in Utrecht.",
    "Hoeveel kamers heeft de flat?", "Er is een woonkamer, een keuken en een slaapkamer.",
    "Klinkt gezellig!", "Waar woon je?",
    "de keuken", "de slaapkamer", "de badkamer", "de woonkamer", "groot / klein",
    "het huis / de flat", "er is / er zijn", "hoeveel kamers?",
    "Waar is de badkamer?", "De keuken is klein, maar gezellig.",
    # Unit 4
    "Wat wil je drinken?", "Mag ik een koffie, alstublieft?",
    "En wil je ook iets eten?", "Ja, een broodje kaas graag. Dat is lekker!",
    "De rekening, alstublieft!",
    "de koffie", "het water", "het brood", "mag ik...?", "alstublieft",
    "lekker", "de rekening", "de menukaart",
    "Dat is heel lekker!", "Mag ik de menukaart, alstublieft?",
    # Unit 5
    "Hoeveel kosten deze appels?", "Twee euro per kilo.",
    "Oké, en de melk? Is die duur?", "Nee, de melk is goedkoop. Één euro.",
    "Fijn, ik ga naar de kassa.",
    "de winkel", "het geld", "hoeveel kost dit?", "de melk", "de appels",
    "goedkoop / duur", "de kassa", "ik ga naar...",
    "Hoeveel kost dit?", "De melk is goedkoop, maar de koffie is duur.",
    "Twee euro per kilo appels.",
    # Unit 6
    "Hoe laat sta jij op?", "Ik sta altijd om zes uur op.",
    "Wat doe je dan?", "Ik ontbijt en dan ga ik naar mijn werk.",
    "En 's avonds?", "'s Avonds kook ik en soms ga ik vroeg slapen.",
    "opstaan", "ontbijten", "werken", "slapen", "altijd",
    "soms", "'s avonds", "naar school gaan",
    "Ik ontbijt om zeven uur.", "Mijn dochter gaat om acht uur naar school.",
]

# Texts spoken by a male speaker (male dialogue lines + male-voiced prompts).
# "Leuk je te ontmoeten!" is intentionally NOT here: it shares a slug with the
# female vocab card, so we keep that clip female.
MALE_TEXTS = {
    "Hoi Fatima, ik ben Youssef.", "Ik kom uit Marokko. En jij?",
    "Heb jij een grote familie?", "Ben je getrouwd?", "Ik ben getrouwd. Ik heb een dochter.",
    "Waar woon je, Fatima?", "Hoeveel kamers heeft de flat?", "Klinkt gezellig!", "Waar woon je?",
    "Wat wil je drinken?", "En wil je ook iets eten?", "De rekening, alstublieft!",
    "Twee euro per kilo.", "Nee, de melk is goedkoop. Één euro.", "Twee euro per kilo appels.",
    "Hoe laat sta jij op?", "Wat doe je dan?", "En 's avonds?",
}


def main():
    api_key = load_api_key()
    voices = load_voices()
    if not api_key or not voices:
        return
    female_voice = voices.get("Vrouwen", [None])[0]
    male_voice = voices.get("Mannen", [None])[0]
    if not female_voice or not male_voice:
        print("Fout: Kon geen stemmen laden uit stemmen.json"); return

    os.makedirs(AUDIO_DIR, exist_ok=True)
    seen = set()
    counts = {'ok': 0, 'skip': 0, 'err': 0}
    for text in ALL_TEXTS:
        slug = slugify(text)
        if slug in seen:
            continue
        seen.add(slug)
        voice = male_voice if text in MALE_TEXTS else female_voice
        result = generate_speech(text, voice, api_key, os.path.join(AUDIO_DIR, f"{slug}.mp3"))
        counts[result] = counts.get(result, 0) + 1

    print(f"\n🎉 Klaar! {counts['ok']} gegenereerd, {counts['skip']} overgeslagen, {counts['err']} fouten.")


if __name__ == "__main__":
    main()
