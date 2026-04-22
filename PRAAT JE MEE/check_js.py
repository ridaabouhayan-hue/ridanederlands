import sys
html_file = r"h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-5-1-2ster.html"
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

script_start = html.find("<script>") + len("<script>")
script_end = html.find("</script>")
script = html[script_start:script_end]

with open("test.js", "w", encoding="utf-8") as f:
    f.write(script)
