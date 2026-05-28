import os
import re
import sys

from html.parser import HTMLParser

class CardExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.current_card = []
        self.depth = 0
        self.in_card = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if not self.in_card:
            if tag == 'div' and (attr_dict.get('class') == 'topic-card' or attr_dict.get('class') == 'vocab-exercise-section'):
                self.in_card = True
                self.depth = 1
                attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
                self.current_card.append(f'<{tag}{attr_str}>')
                return
        else:
            if tag == 'div':
                self.depth += 1
            attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
            self.current_card.append(f'<{tag}{attr_str}>')

    def handle_endtag(self, tag):
        if self.in_card:
            if tag == 'div':
                self.depth -= 1
                
            self.current_card.append(f'</{tag}>')
            
            if self.depth == 0:
                self.in_card = False
                self.cards.append("".join(self.current_card))
                self.current_card = []

    def handle_startendtag(self, tag, attrs):
        if self.in_card:
            attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
            self.current_card.append(f'<{tag}{attr_str}/>')

    def handle_data(self, data):
        if self.in_card:
            self.current_card.append(data)

    def handle_entityref(self, name):
        if self.in_card:
            self.current_card.append(f'&{name};')

    def handle_charref(self, name):
        if self.in_card:
            self.current_card.append(f'&#{name};')

    def handle_comment(self, data):
        if self.in_card:
            self.current_card.append(f'<!--{data}-->')

    def handle_decl(self, decl):
        if self.in_card:
            self.current_card.append(f'<!{decl}>')

def build_meelezen():
    nos_dir = "g:\\Mijn Drive\\HTML FILES\\NOS in Makkelijke Taal"
    aligned_html_file = os.path.join(nos_dir, "transcript_nos_26mei_aligned.html")
    meelezen_file = os.path.join(nos_dir, "meelezen.html")
    
    if not os.path.exists(aligned_html_file):
        print(f"Lijn-bestand '{aligned_html_file}' nog niet gevonden. We wachten tot whisper klaar is.")
        return False
        
    print(f"Lezen van aligned HTML: {aligned_html_file}")
    with open(aligned_html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("Cards extraheren via HTMLParser...")
    extractor = CardExtractor()
    extractor.feed(content)
    
    transcript_html = "\n\n".join(extractor.cards)
    
    # Let's write the complete meelezen.html
    meelezen_html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meelezen - NOS in Makkelijke Taal</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="transcript_style.css">
    <style>
        .meelezen-layout {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 30px;
            margin-top: 30px;
            align-items: start;
        }}
        
        /* Sidebar dates list */
        .dates-sidebar {{
            background: white;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(67, 97, 238, 0.06);
            border: 1px solid rgba(67, 97, 238, 0.1);
        }}
        
        .sidebar-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 15px;
            border-bottom: 2px solid var(--bg);
            padding-bottom: 10px;
        }}
        
        .dates-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .date-btn {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid transparent;
            background: var(--bg);
            border-radius: 12px;
            text-align: left;
            font-family: inherit;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-dark);
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .date-btn:hover {{
            background: var(--primary-light);
            border-color: rgba(67, 97, 238, 0.2);
        }}
        
        .date-btn.active {{
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
        }}
        
        /* Audio Player Styling */
        .player-card {{
            background: white;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(67, 97, 238, 0.08);
            border: 1px solid rgba(67, 97, 238, 0.1);
            margin-bottom: 24px;
            position: sticky;
            top: 20px;
            z-index: 10;
        }}
        
        .player-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        
        .player-info-title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--primary);
        }}
        
        .meelezen-player {{
            width: 100%;
            border-radius: 12px;
            outline: none;
        }}
        
        /* Main View */
        .content-panel {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}
        
        .placeholder-card {{
            background: white;
            border-radius: 18px;
            padding: 50px 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(67, 97, 238, 0.06);
            border: 1px solid rgba(67, 97, 238, 0.1);
            color: var(--text-gray);
            font-weight: 700;
        }}
        
        .placeholder-icon {{
            font-size: 3rem;
            margin-bottom: 15px;
        }}
        
        @media (max-width: 768px) {{
            .meelezen-layout {{
                grid-template-columns: 1fr;
            }}
            .player-card {{
                position: static;
            }}
        }}
    </style>
</head>
<body>

<div class="container">
    
    <!-- BACK TO INDEX -->
    <a href="index.html" class="back-link" style="margin-bottom: 20px;">← Terug naar NOS menu</a>
    
    <div class="header" style="padding: 30px 20px; margin-bottom: 20px;">
        <h1>📖 Meelezen met de nieuwslezeres</h1>
        <p>Volg het transcript van het NOS Journaal in Makkelijke Taal</p>
    </div>

    <!-- LANGUAGE SWITCHER -->
    <div class="lang-switcher" aria-label="Taalkeuze" style="margin-bottom: 20px;">
        <button class="lang-btn active" data-lang="nl">Geen Vertaling</button>
        <button class="lang-btn" data-lang="en">🇬🇧 ENG</button>
        <button class="lang-btn" data-lang="tr">🇹🇷 TR</button>
        <button class="lang-btn" data-lang="ar">🇸🇦 AR</button>
        <button class="lang-btn" data-lang="fa">🇮🇷 Farsi</button>
        <button class="lang-btn" data-lang="da">🇦🇫 Dari</button>
        <button class="lang-btn" data-lang="vi">🇻🇳 VN</button>
    </div>

    <div class="meelezen-layout">
        <!-- Left: Dates Sidebar -->
        <div class="dates-sidebar">
            <div class="sidebar-title">📅 Kies een datum</div>
            <ul class="dates-list">
                <li>
                    <button class="date-btn" onclick="selectDate('26mei', 'nos_26mei.mp3')">
                        <span>Dinsdag 26 mei</span>
                        <span>🔊</span>
                    </button>
                </li>
            </ul>
        </div>
        
        <!-- Right: Player + Transcript Content -->
        <div class="content-panel">
            <!-- Audio Player Card (Hidden until a date is selected) -->
            <div id="active-player-card" class="player-card" style="display: none;">
                <div class="player-header">
                    <span class="player-info-title" id="player-date-title">Journaal voorlezen</span>
                    <span style="font-size: 1.2rem;">🎙️</span>
                </div>
                <audio id="meelezen-audio" class="meelezen-player" controls></audio>
                <!-- Sync Adjuster -->
                <div class="sync-adjuster" style="margin-top: 15px; font-size: 0.9rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; border-top: 1px solid #f1f5f9; padding-top: 15px;">
                    <span style="font-weight: 700; color: var(--text-gray); display: flex; align-items: center; gap: 6px;">⏱️ Verschuiving: <span id="sync-offset-val" style="color: var(--primary); font-weight: 800;">-8.8s</span></span>
                    <div style="display: flex; gap: 8px;">
                        <button class="lang-btn" style="padding: 4px 10px; font-size: 0.8rem; margin: 0;" onclick="adjustSync(-0.5)">-0.5s</button>
                        <button class="lang-btn" style="padding: 4px 10px; font-size: 0.8rem; margin: 0;" onclick="adjustSync(0.5)">+0.5s</button>
                        <button class="lang-btn" style="padding: 4px 10px; font-size: 0.8rem; margin: 0; border-color: #cbd5e1; color: #64748b;" onclick="resetSync()">Reset</button>
                    </div>
                </div>
            </div>
            
            <!-- Dynamic Transcript Container -->
            <div id="transcript-display">
                <div class="placeholder-card">
                    <div class="placeholder-icon">📖</div>
                    Kies een datum aan de linkerkant om te beginnen met meelezen.
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Embedded Transcripts Storage (Hidden from view) -->
<div id="transcripts-storage" style="display: none;">
    <div id="stored-26mei">
        {transcript_html}
    </div>
</div>

<script src="player_sync.js"></script>
<script>
    let currentLang = 'nl';
    window.currentAudioOffset = -8.8; // Standaard verschuiving voor 26 mei

    window.adjustSync = function(amount) {{
        window.currentAudioOffset = parseFloat((window.currentAudioOffset + amount).toFixed(1));
        document.getElementById('sync-offset-val').textContent = window.currentAudioOffset + 's';
        // Re-align highlights immediately
        const audio = document.getElementById('meelezen-audio');
        if (audio && window.initPlayerSync) {{
            window.initPlayerSync();
        }}
    }};

    window.resetSync = function() {{
        window.currentAudioOffset = -8.8;
        document.getElementById('sync-offset-val').textContent = window.currentAudioOffset + 's';
        const audio = document.getElementById('meelezen-audio');
        if (audio && window.initPlayerSync) {{
            window.initPlayerSync();
        }}
    }};

    function selectDate(dateKey, audioSrc) {{
        // Set active button
        document.querySelectorAll('.date-btn').forEach(btn => {{
            btn.classList.remove('active');
        }});
        event.currentTarget.classList.add('active');
        
        // Show player card
        const playerCard = document.getElementById('active-player-card');
        playerCard.style.display = 'block';
        
        // Set audio source
        const audio = document.getElementById('meelezen-audio');
        audio.src = audioSrc;
        audio.load();
        
        // Set title
        const titles = {{
            '26mei': 'Dinsdag 26 mei'
        }};
        document.getElementById('player-date-title').textContent = titles[dateKey] || 'Nieuws';
        
        // Copy transcript from storage to display
        const display = document.getElementById('transcript-display');
        const stored = document.getElementById('stored-' + dateKey);
        if (stored) {{
            display.innerHTML = stored.innerHTML;
        }}

        // Genereer de vocabulaire tabel rijen dynamically
        const tbody = document.querySelector('#vocabTable tbody');
        if (tbody) {{
            tbody.innerHTML = `
                <tr>
                    <td><textarea class="v-word" placeholder="Woord" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'">regering</textarea></td>
                    <td><textarea class="v-lang" placeholder="Vertaling" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                    <td><textarea class="v-easy" placeholder="Uitleg" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'">de mensen die het land besturen</textarea></td>
                    <td><textarea class="v-sent" placeholder="Zin" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'">De regering maakt wetten.</textarea></td>
                </tr>
            `;
            for (let i = 1; i < 10; i++) {{
                tbody.innerHTML += `
                    <tr>
                        <td><textarea class="v-word" placeholder="Woord" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                        <td><textarea class="v-lang" placeholder="Vertaling" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                        <td><textarea class="v-easy" placeholder="Uitleg" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                        <td><textarea class="v-sent" placeholder="Zin" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                    </tr>
                `;
            }}
            setTimeout(() => {{
                document.querySelectorAll('#vocabTable textarea').forEach(ta => {{
                    if(ta.value) {{
                        ta.style.height = 'auto';
                        ta.style.height = ta.scrollHeight + 'px';
                    }}
                }});
            }}, 100);
        }}
        
        // Re-initialize dynamic tooltips and quiz logic in the newly injected HTML
        initDynamicLogic();
        
        // Restart audio synchronization
        if (window.initPlayerSync) {{
            window.initPlayerSync();
        }}
    }}

    function initDynamicLogic() {{
        const vocabWords = document.querySelectorAll('.vocab');
        
        // Setup vocab tooltips
        vocabWords.forEach(word => {{
            // Remove existing tooltips to avoid duplicates
            word.querySelectorAll('.tooltip').forEach(t => t.remove());
            
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            word.appendChild(tooltip);

            word.addEventListener('click', (e) => {{
                e.stopPropagation();
                vocabWords.forEach(w => {{
                    if (w !== word) w.classList.remove('show-tooltip');
                }});

                if (currentLang === 'nl') return;

                const translation = word.getAttribute('data-' + currentLang);
                if (translation) {{
                    tooltip.textContent = translation;
                    word.classList.toggle('show-tooltip');
                }}
            }});
        }});
    }}

    // Close tooltips on body click
    document.addEventListener('click', () => {{
        document.querySelectorAll('.vocab').forEach(w => w.classList.remove('show-tooltip'));
    }});

    // Setup Language switcher
    document.querySelectorAll('.lang-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLang = btn.getAttribute('data-lang');
            
            // Close all tooltips
            document.querySelectorAll('.vocab').forEach(w => w.classList.remove('show-tooltip'));

            // Vertaal de instructie tekst als die er is
            const instr = document.getElementById('vocab-instruction');
            if (instr) {{
                if (currentLang === 'nl') {{
                    instr.textContent = instr.getAttribute('data-nl');
                }} else {{
                    const t = instr.getAttribute('data-' + currentLang);
                    if (t) instr.textContent = t;
                }}
            }}
        }});
    }});
    
    // Fallback Quiz Answers
    window.checkAnswers = function(sectionId, correctAnswers) {{
        let score = 0;
        let total = Object.keys(correctAnswers).length;
        for (let q in correctAnswers) {{
            const selected = document.querySelector(`input[name="${{q}}"]:checked`);
            const labels = document.querySelectorAll(`input[name="${{q}}"]`);
            labels.forEach(r => {{ 
                r.parentElement.style.border='2px solid transparent'; 
                r.parentElement.style.backgroundColor='#ffffff'; 
            }});
            if (selected) {{
                if (selected.value === correctAnswers[q]) {{
                    score++;
                    selected.parentElement.style.border='2px solid #2ecc71';
                    selected.parentElement.style.backgroundColor='#eafaf1';
                }} else {{
                    selected.parentElement.style.border='2px solid #e74c3c';
                    selected.parentElement.style.backgroundColor='#fdedec';
                    document.querySelector(`input[name="${{q}}"][value="${{correctAnswers[q]}}"]`).parentElement.style.border='2px solid #2ecc71';
                }}
            }} else {{
                document.querySelector(`input[name="${{q}}"][value="${{correctAnswers[q]}}"]`).parentElement.style.border='2px dashed #f39c12';
            }}
        }}
        const resultDiv = document.getElementById(sectionId);
        resultDiv.classList.add('show');
        if (score===total) {{ 
            resultDiv.innerHTML=`🎉 Super goed! Je hebt alles goed (${{score}}/${{total}}).`; 
            resultDiv.style.color='#2ecc71'; 
            resultDiv.style.background='#eafaf1'; 
        }}
        else if (score>=total/2) {{ 
            resultDiv.innerHTML=`👍 Goed gedaan! Je score is ${{score}}/${{total}}.`; 
            resultDiv.style.color='#4361ee'; 
            resultDiv.style.background='#e8f0fe'; 
        }}
        else {{ 
            resultDiv.innerHTML=`💪 Blijf oefenen! Je score is ${{score}}/${{total}}.`; 
            resultDiv.style.color='#e74c3c'; 
            resultDiv.style.background='#fdedec'; 
        }}
    }};

    window.checkAnswers1 = function() {{ checkAnswers('quiz-result-1', {{ q1:'b', q2:'b', q3:'b' }}); }};
    window.checkAnswers2 = function() {{ checkAnswers('quiz-result-2', {{ q4:'b', q5:'a', q6:'b' }}); }};
    window.checkAnswers3 = function() {{ checkAnswers('quiz-result-3', {{ q7:'b', q8:'b', q9:'c' }}); }};

    window.addVocabRow = function() {{
        const tb = document.querySelector('#vocabTable tbody');
        if (tb) {{
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><textarea class="v-word" placeholder="Woord" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                <td><textarea class="v-lang" placeholder="Vertaling" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                <td><textarea class="v-easy" placeholder="Uitleg" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
                <td><textarea class="v-sent" placeholder="Zin" rows="1" oninput="this.style.height='';this.style.height=this.scrollHeight+'px'"></textarea></td>
            `;
            tb.appendChild(tr);
        }}
    }};

    window.sendToWhatsApp = function() {{
        const studentName = document.getElementById('studentName').value.trim() || 'Onbekend';
        let message = `Huiswerk NOS in Makkelijke Taal\nNaam: ${{studentName}}\n\n`;
        
        let hasWords = false;
        const rows = document.querySelectorAll('#vocabTable tbody tr');
        rows.forEach((row, index) => {{
            const word = row.querySelector('.v-word').value.trim();
            const lang = row.querySelector('.v-lang').value.trim();
            const easy = row.querySelector('.v-easy').value.trim();
            const sent = row.querySelector('.v-sent').value.trim();
            
            if (word || lang || easy || sent) {{
                hasWords = true;
                message += `*Woord ${{index + 1}}:* ${{word}}\n`;
                if(lang) message += `- Mijn taal: ${{lang}}\n`;
                if(easy) message += `- Uitleg: ${{easy}}\n`;
                if(sent) message += `- Zin: ${{sent}}\n`;
                message += `\n`;
            }}
        }});

        if (!hasWords) {{
            alert('Vul eerst wat woorden in voordat je het verstuurt!');
            return;
        }}

        const encodedMsg = encodeURIComponent(message);
        const waLink = `https://wa.me/31626211106?text=${{encodedMsg}}`;
        window.open(waLink, '_blank');
    }};
</script>

</body>
</html>
"""
    
    with open(meelezen_file, 'w', encoding='utf-8') as f:
        f.write(meelezen_html)
        
    print(f"Succesvol meelezen.html gebouwd op: {meelezen_file}")
    return True

if __name__ == '__main__':
    build_meelezen()
