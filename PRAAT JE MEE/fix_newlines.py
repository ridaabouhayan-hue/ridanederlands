import os
import re

files = [
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html",
    r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-3ster.html"
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Replace the broken literal newlines inside the ar JS strings
    text = re.sub(r"waMsg:'مرحباً أستاذ! هذه جملي:\r?\n',", r"waMsg:'مرحباً أستاذ! هذه جملي:\\n',", text)
    text = re.sub(r"waFreeMsg:'مرحباً أستاذ! هذا نصي:\r?\n',", r"waFreeMsg:'مرحباً أستاذ! هذا نصي:\\n',", text)
    text = re.sub(r"waVoiceTip:'\r?\n\r?\n🎤 سأرسل أيضاً رسالة صوتية!',", r"waVoiceTip:'\\n\\n🎤 سأرسل أيضاً رسالة صوتية!',", text)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(text)
print("Fix applied to all 3 files.")
