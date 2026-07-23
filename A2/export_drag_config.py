"""
Exporteert alle drag-zinnen naar drag_alt_config.json.
Dit is de bron van waarheid voor de admin review-pagina.
Draai dit als je de config wil bijwerken na een wijziging in _lessons_data.py.
"""
import sys, json, importlib
sys.path.insert(0, r"c:\Users\rabou\Mijn Drive\HTML FILES\A2")
import _lessons_data; importlib.reload(_lessons_data)
from _lessons_data import LESSONS_DATA

config = {}
for lesson_id, data in LESSONS_DATA.items():
    config[lesson_id] = []
    drag_alt = data.get("drag_alt", {})
    for i, sentence in enumerate(data["drag"]):
        config[lesson_id].append({
            "index": i,
            "primary": sentence,
            "approved_alts": drag_alt.get(str(i), [])
        })

OUT_PATH = r"c:\Users\rabou\Mijn Drive\HTML FILES\A2\drag_alt_config.json"
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

total_alts = sum(
    len(entry["approved_alts"])
    for lesson in config.values()
    for entry in lesson
)
print("Geexporteerd naar drag_alt_config.json")
print("Totaal lessen:", len(config))
print("Totaal zinnen:", sum(len(v) for v in config.values()))
print("Totaal goedgekeurde alternatieven:", total_alts)
