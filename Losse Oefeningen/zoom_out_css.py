import os
import glob
import re

directory = r"g:\Mijn Drive\HTML FILES\Losse Oefeningen"
html_files = glob.glob(os.path.join(directory, "*.html"))

replacements = [
    (r'padding:\s*7rem\s+2rem\s+3rem;', 'padding: 4rem 1.5rem 1.5rem;'),
    (r'margin-bottom:\s*3rem;', 'margin-bottom: 1.5rem;'),
    (r'gap:\s*3rem;\s*margin-bottom:\s*4rem;', 'gap: 1.5rem; margin-bottom: 2.5rem;'),
    (r'gap:\s*4rem;\s*margin-bottom:\s*4rem;', 'gap: 2rem; margin-bottom: 2.5rem;'),
    (r'gap:\s*3rem;', 'gap: 1.5rem;'),
    (r'gap:\s*2\.5rem;', 'gap: 1.25rem;'),
    (r'\.card \{[^}]*padding:\s*2rem;', lambda m: m.group(0).replace('padding: 2rem;', 'padding: 1.5rem;')),
    (r'\.container \{[^}]*margin:\s*2rem\s+auto;\s*padding:\s*0\s+2rem;', lambda m: m.group(0).replace('margin: 2rem auto;', 'margin: 1rem auto;').replace('padding: 0 2rem;', 'padding: 0 1.5rem;')),
    (r'\.lang-container \{[^}]*padding:\s*20px;', lambda m: m.group(0).replace('padding: 20px;', 'padding: 10px;')),
    (r'nav \{[^}]*padding:\s*1\.2rem;', lambda m: m.group(0).replace('padding: 1.2rem;', 'padding: 0.8rem;')),
    (r'\.exercise-section \{[^}]*padding:\s*3\.5rem\s+2rem;', lambda m: m.group(0).replace('padding: 3.5rem 2rem;', 'padding: 2rem 1.5rem;')),
    (r'\.exercise-section \{[^}]*margin:\s*6rem\s+auto;', lambda m: m.group(0).replace('margin: 6rem auto;', 'margin: 3rem auto;')),
    (r'\.mistakes-section \{[^}]*padding:\s*3rem;', lambda m: m.group(0).replace('padding: 3rem;', 'padding: 2rem;')),
    (r'\.mistakes-section \{[^}]*margin-bottom:\s*6rem;', lambda m: m.group(0).replace('margin-bottom: 6rem;', 'margin-bottom: 3rem;'))
]

modified_files = []

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '.hero h1' in content or '.cards-grid' in content:
        original_content = content
        
        for pattern, replacement in replacements:
            if callable(replacement):
                content = re.sub(pattern, replacement, content)
            else:
                content = re.sub(pattern, replacement, content)
                
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_files.append(os.path.basename(file_path))

print(f"Modified {len(modified_files)} files: {', '.join(modified_files)}")
