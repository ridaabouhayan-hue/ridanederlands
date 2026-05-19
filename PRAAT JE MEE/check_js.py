import os
import sys
html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thema-5-1-2ster.html")
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

script_start = html.find("<script>") + len("<script>")
script_end = html.find("</script>")
script = html[script_start:script_end]

with open("test.js", "w", encoding="utf-8") as f:
    f.write(script)
