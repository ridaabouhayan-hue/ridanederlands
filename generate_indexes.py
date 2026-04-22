import os

folders = [
    'ALFA A1',
    'Chinees',
    'KNM',
    'NOS in Makkelijke Taal',
    'Voegwoorden',
    'Zinstructuren',
    'verleden tijd'
]

base_dir = r'h:\Mijn Drive\HTML FILES'

html_template = """<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{folder_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #f0ede6; --card-bg: #ffffff; --text-dark: #1e1e2e; --text-muted: #6b7280; --accent: #6C5CE7; --radius: 20px; }}
        body {{ font-family: 'Nunito', sans-serif; background: var(--bg); color: var(--text-dark); padding: 40px 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 10px; color: var(--accent); }}
        .back-link {{ display: inline-block; margin-bottom: 30px; text-decoration: none; color: var(--text-muted); font-weight: bold; padding: 10px 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
        .card {{ background: white; padding: 25px; border-radius: var(--radius); text-decoration: none; color: var(--text-dark); font-size: 1.1rem; font-weight: 700; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.2s, box-shadow 0.2s; border-left: 6px solid var(--accent); display: flex; align-items: center; justify-content: space-between; }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
        .card span {{ font-size: 1.5rem; }}
    </style>
</head>
<body>
    <a href="../index.html" class="back-link">← Terug naar Hoofdmenu</a>
    <h1>📂 {folder_name}</h1>
    <p style="margin-bottom: 30px; color: var(--text-muted); font-weight: 600;">Kies een oefening uit de lijst hieronder:</p>
    
    <div class="grid">
        {links}
    </div>
</body>
</html>"""

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.exists(folder_path):
        continue
    
    # Get all html files except index.html
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.html') and f.lower() != 'index.html'])
    
    links_html = ''
    if not files:
        links_html = '<p style="color: #6b7280; font-style: italic;">Nog geen oefeningen in deze map.</p>'
    else:
        for f in files:
            name_display = f.replace('.html', '').replace('_', ' ').replace('-', ' ').title()
            links_html += f'<a href="{f}" class="card">{name_display} <span>→</span></a>\n        '
            
    final_html = html_template.format(folder_name=folder.upper(), links=links_html)
    
    with open(os.path.join(folder_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_html)

print('Index pages created successfully.')
