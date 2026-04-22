import os
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Bestand met jouw links
LINKS_FILE = "youtube_links.txt"
# Map waar de teksten worden opgeslagen
OUTPUT_DIR = "transcripties"

def get_video_id(url):
    """Haal de video ID uit verschillende YouTube URL formaten"""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        parsed_url = urlparse(url)
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]
    return url.strip() # Als het al losse ID's zijn

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            f.write("# Plak hier al jouw YouTube links, 1 per regel.\n")
            f.write("# Bijvoorbeeld: https://www.youtube.com/watch?v=dQw4w9WgXcQ\n")
        print(f"Ik heb het bestand '{LINKS_FILE}' voor je aangemaakt.")
        print("Plak daar al je YouTube links in en draai dit script nog een keer!")
        return

    with open(LINKS_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

    if not lines:
        print(f"Het bestand '{LINKS_FILE}' is leeg. Voeg eerst links toe!")
        return

    print(f"Gevonden: {len(lines)} links. Starten met downloaden...\n")

    for count, link in enumerate(lines, 1):
        video_id = get_video_id(link)
        if not video_id:
            print(f"[{count}/{len(lines)}] FOUT: Kon Video-ID niet vinden in '{link}'")
            continue

        filename = os.path.join(OUTPUT_DIR, f"{video_id}.txt")
        if os.path.exists(filename):
            print(f"[{count}/{len(lines)}] Bestaat al: {video_id}.txt (Sla ik over)")
            continue

        print(f"[{count}/{len(lines)}] Downloaden: {link} (ID: {video_id})")
        
        try:
            # We proberen de Nederlandse transcriptie op te halen (of automatisch gegenereerd NL)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['nl', 'nl-NL'])
            
            # Alle regels tekst achter elkaar plakken tot 1 leesbaar verhaal
            full_text = "\n".join([item['text'] for item in transcript])
            
            with open(filename, 'w', encoding='utf-8') as out_f:
                out_f.write(f"Link: https://www.youtube.com/watch?v={video_id}\n")
                out_f.write("-" * 50 + "\n\n")
                out_f.write(full_text)
                
            print(f"  -> Succes! Opgeslagen als {filename}")
        except Exception as e:
            err_msg = str(e)
            if "NoTranscriptFound" in err_msg or "TranscriptsDisabled" in err_msg:
                print(f"  -> Mislukt: Geen (Nederlandse) ondertiteling/transcriptie beschikbaar of video is privé.")
            else:
                print(f"  -> Mislukt: Foutmelding: {err_msg}")

    print("\nKLAAR! Bekijk de map 'transcripties' voor al je teksten.")

if __name__ == "__main__":
    main()
