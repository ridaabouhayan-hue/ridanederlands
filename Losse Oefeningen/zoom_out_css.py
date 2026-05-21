import os
import glob
import re

directory = r"g:\Mijn Drive\HTML FILES\Losse Oefeningen"
html_files = glob.glob(os.path.join(directory, "*.html"))

# We only want to touch files that have the modern styling template.
# A good indicator is having ".hero h1" or ".cards-grid".

replacements = [
    (r'padding:\s*10rem\s+2rem\s+4rem;', 'padding: 7rem 2rem 3rem;'),
    (r'\.hero h1 \{ font-size:\s*4rem;', '.hero h1 { font-size: 2.8rem;'),
    (r'\.hero h1 \{ font-size:\s*clamp\(2\.5rem,\s*5vw,\s*4rem\);', '.hero h1 { font-size: clamp(2rem, 4vw, 3rem);'),
    (r'\.hero p \{ font-size:\s*1\.4rem;', '.hero p { font-size: 1.15rem;'),
    
    (r'\.section-title \{ font-size:\s*3rem;', '.section-title { font-size: 2.2rem;'),
    (r'\.emoji-header \{ font-size:\s*5rem;', '.emoji-header { font-size: 3.5rem;'),
    (r'\.emoji-header \{ font-size:\s*4rem;', '.emoji-header { font-size: 3rem;'),
    
    (r'\.card \{[^}]*padding:\s*3rem;', lambda m: m.group(0).replace('padding: 3rem;', 'padding: 2rem;')),
    (r'\.card \.word \{ font-size:\s*3\.5rem;', '.card .word { font-size: 2.5rem;'),
    (r'\.card \.definition \{ font-size:\s*1\.25rem;', '.card .definition { font-size: 1.1rem;'),
    (r'\.example-item \{[^}]*font-size:\s*1\.15rem;', lambda m: m.group(0).replace('font-size: 1.15rem;', 'font-size: 1.05rem;')),
    (r'\.mistake-row div \{[^}]*font-size:\s*1\.15rem;', lambda m: m.group(0).replace('font-size: 1.15rem;', 'font-size: 1.05rem;')),
    
    (r'\.mistakes-title \{ color:[^;]+;\s*font-size:\s*2rem;', lambda m: m.group(0).replace('font-size: 2rem;', 'font-size: 1.6rem;')),
    (r'\.exercise-section \{[^}]*padding:\s*5rem\s+3rem;', lambda m: m.group(0).replace('padding: 5rem 3rem;', 'padding: 3.5rem 2rem;')),
    (r'\.q-row \{[^}]*padding:\s*22px;', lambda m: m.group(0).replace('padding: 22px;', 'padding: 16px;')),
    
    (r'\.q-sentence-container \{[^}]*font-size:\s*1\.25rem;', lambda m: m.group(0).replace('font-size: 1.25rem;', 'font-size: 1.1rem;')),
    (r'\.q-row input \{[^}]*font-size:\s*1\.2rem;', lambda m: m.group(0).replace('font-size: 1.2rem;', 'font-size: 1.05rem;')),
    (r'\.feedback \{ font-size:\s*1\.8rem;', '.feedback { font-size: 1.4rem;'),
    
    # Also adjust some Mobile specific queries that were already small, to make them slightly smaller too
    (r'@media \(max-width: 768px\) \{[\s\S]*?\.hero h1 \{ font-size:\s*2\.8rem; \}', lambda m: m.group(0).replace('2.8rem', '2.2rem')),
    (r'@media \(max-width: 768px\) \{[\s\S]*?\.section-title \{ font-size:\s*2\.2rem; \}', lambda m: m.group(0).replace('2.2rem', '1.8rem'))
]

modified_files = []

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if this is a modern template file
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
