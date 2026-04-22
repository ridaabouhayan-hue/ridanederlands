import sys

files = [
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-3ster.html"
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    idx = text.find("waMsg:")
    if idx != -1:
        # Get the snippet
        snippet = text[idx:idx+80]
        # Dump it hex encoded to avoid console issues
        print(fpath)
        print("waMsg snippet:", repr(snippet))
    
    idx2 = text.find("waVoiceTip:")
    if idx2 != -1:
        snippet2 = text[idx2:idx2+80]
        print("waVoiceTip snippet:", repr(snippet2))
