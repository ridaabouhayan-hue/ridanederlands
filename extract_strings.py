import re
import json

filepath = r"g:\Mijn Drive\HTML FILES\praatplaat.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Extract from translations object (around line 2436 to 2732)
translations_match = re.search(r"const translations = \{.*?\n        \};", content, re.DOTALL)
if translations_match:
    print("Found translations object")

# Extract from themesData (around line 1506 to 2417)
# We can look for `nl: "..."` or `en: "..."`
nl_strings = set()
matches = re.finditer(r'nl:\s*"(.*?)"', content)
for m in matches:
    nl_strings.add(m.group(1))

# Also translations inside questions / dialogues: 
# nl: "Hoe heet je?", translations: { en: "What is your name?", tr: "..." }
matches = re.finditer(r'en:\s*"(.*?)"', content)
en_strings = set()
for m in matches:
    en_strings.add(m.group(1))

with open("strings_to_translate.json", "w", encoding="utf-8") as f:
    json.dump({"nl": list(nl_strings), "en": list(en_strings)}, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(nl_strings)} NL strings and {len(en_strings)} EN strings.")
