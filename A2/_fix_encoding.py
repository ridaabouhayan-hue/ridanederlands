import os, re

css_path = r'h:\Mijn Drive\HTML FILES\A2\style.css'
html_path = r'h:\Mijn Drive\HTML FILES\A2\thema5-9.html'

# Read CSS
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Read HTML as bytes and fix double-CR issue
with open(html_path, 'rb') as f:
    raw = f.read()

# Fix double \r\r\n -> \r\n
raw = raw.replace(b'\r\r\n', b'\r\n')

# Decode
html = raw.decode('utf-8')

# Fix mojibake: â€" -> — (em-dash)
html = html.replace('\u00e2\u0080\u0094', '\u2014')

# Replace the link tag with embedded style
html = html.replace(
    '<link rel="stylesheet" href="style.css">',
    '<style>\n' + css + '\n    </style>'
)

# Write clean file
with open(html_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(html)

# Verify
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Size: {os.path.getsize(html_path)} bytes")
print(f"Contains em-dash correctly: {chr(8212) in content}")
print(f"Contains <style>: {'<style>' in content}")
print(f"Contains mojibake: {'â€' in content}")
# Show first 15 lines
lines = content.split('\n')
for i, line in enumerate(lines[:15]):
    print(f"  {i+1}: {line.rstrip()}")
