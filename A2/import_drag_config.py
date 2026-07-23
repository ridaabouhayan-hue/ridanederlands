"""
Leest drag_alt_config.json en schrijft de goedgekeurde alternatieven
terug naar _lessons_data.py. Daarna moet je _build_lessons.py draaien.
"""
import sys, json, importlib
sys.path.insert(0, r"c:\Users\rabou\Mijn Drive\HTML FILES\A2")
import _lessons_data; importlib.reload(_lessons_data)
from _lessons_data import LESSONS_DATA

CONFIG_PATH = r"c:\Users\rabou\Mijn Drive\HTML FILES\A2\drag_alt_config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

total_imported = 0
for lesson_id, entries in config.items():
    if lesson_id not in LESSONS_DATA:
        continue
    drag_alt = {}
    for entry in entries:
        idx = str(entry["index"])
        alts = entry.get("approved_alts", [])
        if alts:
            drag_alt[idx] = alts
            total_imported += len(alts)
    if drag_alt:
        LESSONS_DATA[lesson_id]["drag_alt"] = drag_alt
    elif "drag_alt" in LESSONS_DATA[lesson_id]:
        del LESSONS_DATA[lesson_id]["drag_alt"]

DATA_PATH = r"c:\Users\rabou\Mijn Drive\HTML FILES\A2\_lessons_data.py"
with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n\nLESSONS_DATA = ")
    f.write(json.dumps(LESSONS_DATA, indent=4, ensure_ascii=False))
    f.write("\n")

print("Klaar! " + str(total_imported) + " alternatieven geimporteerd naar _lessons_data.py")
print("Draai nu: python _build_lessons.py")
