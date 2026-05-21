import os

html_content = """<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inversie & TOP Systeem - NT2</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --subj-bg: #f0fdf4; --subj-main: #16a34a; --subj-dark: #14532d;
            --verb-bg: #fff1f2; --verb-main: #e11d48; --verb-dark: #9f1239;
            --time-bg: #eff6ff; --time-main: #3b82f6; --time-dark: #1e40af;
            --obj-bg:  #fffbeb; --obj-main:  #f59e0b; --obj-dark:  #b45309;
            --place-bg:#f5f3ff; --place-main:#8b5cf6; --place-dark:#5b21b6;
            
            --text-main: #2c3e50;
            --text-light: #5d6d7e;
            --white: #ffffff;
            --shadow: 0 15px 35px rgba(0,0,0,0.08);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Outfit', sans-serif; background-color: #f8fafc; color: var(--text-main); line-height: 1.6; overflow-x: hidden; }
        
        nav { position: fixed; top: 0; width: 100%; background: white; z-index: 1000; padding: 0.8rem; display: flex; justify-content: center; gap: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); flex-wrap: wrap; }
        nav a { text-decoration: none; font-weight: 800; color: var(--text-main); font-size: 1.1rem; padding: 0.5rem 1.2rem; border-radius: 50px; transition: var(--transition); }
        nav a:hover { background: #f1f5f9; }
        
        .lang-container { position: sticky; top: 70px; display: flex; justify-content: center; gap: 12px; padding: 10px; background: rgba(248, 250, 252, 0.98); backdrop-filter: blur(10px); z-index: 999; border-bottom: 2px solid #e2e8f0; flex-wrap: wrap; }
        .lang-btn { border: 2px solid #e2e8f0; background: white; padding: 10px 20px; border-radius: 15px; cursor: pointer; font-weight: 800; font-size: 1rem; transition: var(--transition); display: flex; align-items: center; gap: 8px; }
        .lang-btn.active { background: var(--text-main); color: white; border-color: var(--text-main); }
        
        .hero { padding: 5rem 1.5rem 2rem; text-align: center; }
        .hero h1 { font-size: 3rem; font-weight: 800; margin-bottom: 1rem; background: linear-gradient(90deg, var(--verb-main), var(--time-main)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.2rem; color: var(--text-light); max-width: 800px; margin: 0 auto; }
        
        .container { max-width: 1200px; margin: 1rem auto; padding: 0 1.5rem; }
        .section-title { font-size: 2.2rem; margin-bottom: 1.5rem; text-align: center; font-weight: 800; color: var(--text-main); }
        
        /* Blocks Styling */
        .block-legend { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 3rem; }
        .b-leg { padding: 10px 20px; border-radius: 20px; font-weight: 800; font-size: 1.1rem; border: 2px solid transparent; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        
        .c-subj { background: var(--subj-bg); color: var(--subj-dark); border-color: var(--subj-main); }
        .c-verb { background: var(--verb-bg); color: var(--verb-dark); border-color: var(--verb-main); }
        .c-time { background: var(--time-bg); color: var(--time-dark); border-color: var(--time-main); }
        .c-obj  { background: var(--obj-bg); color: var(--obj-dark); border-color: var(--obj-main); }
        .c-place{ background: var(--place-bg); color: var(--place-dark); border-color: var(--place-main); }
        
        /* Visual Sentence Cards */
        .sentence-card { background: white; border-radius: 40px; padding: 2.5rem; box-shadow: var(--shadow); margin-bottom: 2rem; border: 2px solid #f1f5f9; text-align: center; }
        .sentence-card h3 { font-size: 1.6rem; font-weight: 800; margin-bottom: 1.5rem; color: var(--text-main); }
        
        .sent-wrapper { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 1.5rem; }
        .sent-part { padding: 15px 25px; border-radius: 15px; font-size: 1.4rem; font-weight: 800; box-shadow: 0 5px 15px rgba(0,0,0,0.05); display: flex; flex-direction: column; align-items: center; }
        .sent-part small { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin-top: 5px; font-weight: 600; }
        
        .arrow-down { font-size: 3rem; color: #cbd5e1; text-align: center; margin: -10px 0 10px; }
        
        /* Interactive Builder */
        .builder-section { background: white; padding: 3rem; border-radius: 40px; box-shadow: var(--shadow); margin-top: 3rem; border: 3px solid #e2e8f0; }
        .b-header { text-align: center; margin-bottom: 2rem; }
        .b-header p { font-size: 1.2rem; color: var(--text-light); }
        
        .exercise-box { background: #f8fafc; border-radius: 25px; padding: 2rem; margin-bottom: 1.5rem; border: 2px dashed #cbd5e1; }
        .ex-instruction { font-size: 1.3rem; font-weight: 800; color: var(--text-main); margin-bottom: 1.5rem; text-align: center; }
        
        .word-bank { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; min-height: 60px; padding: 15px; background: white; border-radius: 15px; border: 2px solid #e2e8f0; margin-bottom: 1rem; }
        .drop-zone { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; min-height: 80px; padding: 15px; background: #f1f5f9; border-radius: 15px; border: 3px dashed #94a3b8; transition: var(--transition); }
        .drop-zone.active { border-color: var(--time-main); background: #e0f2fe; }
        
        .draggable-word { padding: 10px 20px; border-radius: 12px; font-size: 1.2rem; font-weight: 700; background: white; border: 2px solid #cbd5e1; cursor: grab; box-shadow: 0 4px 6px rgba(0,0,0,0.05); user-select: none; transition: transform 0.1s; }
        .draggable-word:active { cursor: grabbing; transform: scale(1.05); }
        
        .feedback { text-align: center; font-size: 1.4rem; font-weight: 800; min-height: 35px; margin-top: 10px; }
        .controls { display: flex; justify-content: center; gap: 15px; margin-top: 2rem; }
        .btn { padding: 12px 25px; font-size: 1.1rem; font-weight: 800; border: none; border-radius: 15px; cursor: pointer; transition: var(--transition); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-check { background: var(--text-main); color: white; }
        .btn-check:hover { background: #1a252f; transform: translateY(-2px); }
        .btn-next { background: var(--time-main); color: white; display: none; }
        .btn-next:hover { background: var(--time-dark); transform: translateY(-2px); }
        
        [lang]:not([lang="nl"]) { display: none; }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.2rem; }
            .sent-part { font-size: 1.1rem; padding: 10px 15px; }
            .builder-section { padding: 1.5rem; }
            .draggable-word { font-size: 1rem; padding: 8px 15px; }
        }
    </style>
</head>
<body>
    <nav>
        <a href="#intro">Intro</a>
        <a href="#top-systeem">💡 <span lang="nl">Systeem</span><span lang="en">System</span><span lang="pl">System</span></a>
        <a href="#inversie">🔄 <span lang="nl">Inversie</span><span lang="en">Inversion</span><span lang="pl">Inwersja</span></a>
        <a href="#oefenen">✍️ <span lang="nl">Oefenen</span><span lang="en">Practice</span><span lang="pl">Ćwiczenia</span></a>
    </nav>
    
    <div class="lang-container">
        <button class="lang-btn active" id="btn-nl" onclick="setLang('nl')">🇳🇱 Nederlands</button>
        <button class="lang-btn" id="btn-en" onclick="setLang('en')">🇬🇧 English</button>
        <button class="lang-btn" id="btn-pl" onclick="setLang('pl')">🇵🇱 Polski</button>
    </div>

    <header class="hero" id="intro">
        <h1>
            <span lang="nl">Inversie & het T.O.P. Systeem</span>
            <span lang="en">Inversion & the T.O.P. System</span>
            <span lang="pl">Inwersja i system T.O.P.</span>
        </h1>
        <p>
            <span lang="nl">Leer hoe je perfecte zinnen bouwt met Inversie (Tijd op de eerste plaats).</span>
            <span lang="en">Learn how to build perfect sentences with Inversion (Time in the first place).</span>
            <span lang="pl">Naucz się budować idealne zdania z inwersją (Czas na pierwszym miejscu).</span>
        </p>
    </header>

    <main class="container">
        <!-- LEGENDA -->
        <div class="block-legend">
            <div class="b-leg c-subj">👤 <span lang="nl">Onderwerp</span><span lang="en">Subject</span><span lang="pl">Podmiot</span></div>
            <div class="b-leg c-verb">🔥 <span lang="nl">Werkwoord</span><span lang="en">Verb</span><span lang="pl">Czasownik</span></div>
            <div class="b-leg c-time">🕒 <span lang="nl">Tijd</span><span lang="en">Time</span><span lang="pl">Czas</span></div>
            <div class="b-leg c-obj">📦 <span lang="nl">Object</span><span lang="en">Object</span><span lang="pl">Obiekt</span></div>
            <div class="b-leg c-place">📍 <span lang="nl">Plaats</span><span lang="en">Place</span><span lang="pl">Miejsce</span></div>
        </div>

        <section id="top-systeem">
            <h2 class="section-title">
                <span lang="nl">1. De Normale Zin (TOP Systeem)</span>
                <span lang="en">1. The Normal Sentence (TOP System)</span>
                <span lang="pl">1. Zwykłe Zdanie (System TOP)</span>
            </h2>
            
            <div class="sentence-card">
                <h3>
                    <span lang="nl">Onderwerp + Werkwoord + Tijd + Object + Plaats</span>
                    <span lang="en">Subject + Verb + Time + Object + Place</span>
                    <span lang="pl">Podmiot + Czasownik + Czas + Obiekt + Miejsce</span>
                </h3>
                
                <div class="sent-wrapper">
                    <div class="sent-part c-subj">Ik <small><span lang="nl">Onderwerp</span><span lang="en">Subject</span><span lang="pl">Podmiot</span></small></div>
                    <div class="sent-part c-verb">werk <small><span lang="nl">Werkwoord</span><span lang="en">Verb</span><span lang="pl">Czasownik</span></small></div>
                    <div class="sent-part c-time">vandaag <small><span lang="nl">Tijd</span><span lang="en">Time</span><span lang="pl">Czas</span></small></div>
                    <div class="sent-part c-obj">aan een project <small><span lang="nl">Object</span><span lang="en">Object</span><span lang="pl">Obiekt</span></small></div>
                    <div class="sent-part c-place">op kantoor <small><span lang="nl">Plaats</span><span lang="en">Place</span><span lang="pl">Miejsce</span></small></div>
                </div>
                
                <p style="color: var(--text-light); font-size: 1.1rem; font-weight: 600; margin-top: 1rem;">
                    <span lang="nl">Dit is de standaard Nederlandse zinsvolgorde. Tijd komt altijd vóór Plaats.</span>
                    <span lang="en">This is the standard Dutch word order. Time always comes before Place.</span>
                    <span lang="pl">To jest standardowy szyk w języku holenderskim. Czas zawsze jest przed Miejscem.</span>
                </p>
            </div>
        </section>

        <section id="inversie">
            <div class="arrow-down">⬇️</div>
            
            <h2 class="section-title">
                <span lang="nl">2. Inversie (Tijd op positie 1)</span>
                <span lang="en">2. Inversion (Time in position 1)</span>
                <span lang="pl">2. Inwersja (Czas na 1 pozycji)</span>
            </h2>
            
            <div class="sentence-card" style="border-color: var(--time-main);">
                <h3>
                    <span lang="nl">Als TIJD op 1 staat ➔ Werkwoord + Onderwerp (Inversie!)</span>
                    <span lang="en">If TIME is 1st ➔ Verb + Subject (Inversion!)</span>
                    <span lang="pl">Jeśli CZAS jest 1 ➔ Czasownik + Podmiot (Inwersja!)</span>
                </h3>
                
                <div class="sent-wrapper">
                    <div class="sent-part c-time">Vandaag <small><span lang="nl">Tijd</span><span lang="en">Time</span><span lang="pl">Czas</span></small></div>
                    <div class="sent-part c-verb">werk <small><span lang="nl">Werkwoord</span><span lang="en">Verb</span><span lang="pl">Czasownik</span></small></div>
                    <div class="sent-part c-subj">ik <small><span lang="nl">Onderwerp</span><span lang="en">Subject</span><span lang="pl">Podmiot</span></small></div>
                    <div class="sent-part c-obj">aan een project <small><span lang="nl">Object</span><span lang="en">Object</span><span lang="pl">Obiekt</span></small></div>
                    <div class="sent-part c-place">op kantoor <small><span lang="nl">Plaats</span><span lang="en">Place</span><span lang="pl">Miejsce</span></small></div>
                </div>
                
                <div style="background: var(--verb-bg); padding: 15px; border-radius: 15px; border-left: 5px solid var(--verb-main); margin-top: 2rem; font-size: 1.15rem; font-weight: 700; text-align: left; color: var(--verb-dark);">
                    <span lang="nl">⚠️ Let op: Het werkwoord staat <b>ALTIJD</b> op de 2e plaats in een hoofdzin. Als je begint met Tijd, schuift het onderwerp naar de 3e plaats. Dit heet <b>Inversie</b>.</span>
                    <span lang="en">⚠️ Note: The verb is <b>ALWAYS</b> in the 2nd position in a main clause. If you start with Time, the Subject moves to the 3rd position. This is called <b>Inversion</b>.</span>
                    <span lang="pl">⚠️ Uwaga: Czasownik jest <b>ZAWSZE</b> na 2 pozycji w zdaniu głównym. Jeśli zaczniesz od Czasu, Podmiot przesuwa się na 3 pozycję. Nazywa się to <b>Inwersją</b>.</span>
                </div>
            </div>
            
            <div class="sentence-card" style="border-color: var(--place-main);">
                <h3>
                    <span lang="nl">Ook met PLAATS op positie 1!</span>
                    <span lang="en">Also with PLACE in position 1!</span>
                    <span lang="pl">Również z MIEJSCEM na pozycji 1!</span>
                </h3>
                
                <div class="sent-wrapper">
                    <div class="sent-part c-place">Op kantoor <small><span lang="nl">Plaats</span><span lang="en">Place</span><span lang="pl">Miejsce</span></small></div>
                    <div class="sent-part c-verb">werk <small><span lang="nl">Werkwoord</span><span lang="en">Verb</span><span lang="pl">Czasownik</span></small></div>
                    <div class="sent-part c-subj">ik <small><span lang="nl">Onderwerp</span><span lang="en">Subject</span><span lang="pl">Podmiot</span></small></div>
                    <div class="sent-part c-time">vandaag <small><span lang="nl">Tijd</span><span lang="en">Time</span><span lang="pl">Czas</span></small></div>
                    <div class="sent-part c-obj">aan een project <small><span lang="nl">Object</span><span lang="en">Object</span><span lang="pl">Obiekt</span></small></div>
                </div>
            </div>
        </section>

        <section class="builder-section" id="oefenen">
            <div class="b-header">
                <h2 class="section-title">
                    <span lang="nl">✍️ Zinsbouwer: Oefen Inversie</span>
                    <span lang="en">✍️ Sentence Builder: Practice Inversion</span>
                    <span lang="pl">✍️ Budowniczy Zdań: Ćwicz Inwersję</span>
                </h2>
                <p>
                    <span lang="nl">Klik op de woorden in de juiste volgorde om een correcte inversie-zin te maken. <b>(Tijd op 1!)</b></span>
                    <span lang="en">Click the words in the correct order to make a correct inversion sentence. <b>(Time on 1!)</b></span>
                    <span lang="pl">Kliknij słowa w odpowiedniej kolejności, aby utworzyć poprawne zdanie z inwersją. <b>(Czas na 1!)</b></span>
                </p>
            </div>

            <div class="exercise-box">
                <div class="ex-instruction" id="ex-trans">
                    <!-- Javascript sets instruction -->
                </div>
                
                <div class="drop-zone" id="drop-zone">
                    <!-- Words go here -->
                </div>
                
                <div class="word-bank" id="word-bank">
                    <!-- Words spawned here -->
                </div>
                
                <div class="feedback" id="feedback"></div>
                
                <div class="controls">
                    <button class="btn btn-check" onclick="checkSentence()">
                        <span lang="nl">Controleren</span>
                        <span lang="en">Check</span>
                        <span lang="pl">Sprawdź</span>
                    </button>
                    <button class="btn btn-next" id="btn-next" onclick="nextQuestion()">
                        <span lang="nl">Volgende Oefening ➔</span>
                        <span lang="en">Next Exercise ➔</span>
                        <span lang="pl">Następne Ćwiczenie ➔</span>
                    </button>
                </div>
            </div>
        </section>

    </main>

    <script>
        const exercises = [
            {
                words: ["gaan", "wij", "morgen", "naar de supermarkt"],
                correct: ["morgen", "gaan", "wij", "naar de supermarkt"],
                translation: {
                    nl: "Maak een inversie-zin: Wij gaan morgen naar de supermarkt.",
                    en: "Make an inversion sentence: We are going to the supermarket tomorrow.",
                    pl: "Ułóż zdanie z inwersją: Jutro idziemy do supermarketu."
                }
            },
            {
                words: ["ik", "in het weekend", "slaap", "lang"],
                correct: ["in het weekend", "slaap", "ik", "lang"],
                translation: {
                    nl: "Maak een inversie-zin: Ik slaap lang in het weekend.",
                    en: "Make an inversion sentence: I sleep late on the weekend.",
                    pl: "Ułóż zdanie z inwersją: W weekend śpię długo."
                }
            },
            {
                words: ["drinkt", "vaak", "koffie", "hij", "thuis"],
                correct: ["vaak", "drinkt", "hij", "koffie", "thuis"],
                translation: {
                    nl: "Maak een inversie-zin (Begin met Tijd/Frequentie): Hij drinkt vaak koffie thuis.",
                    en: "Make an inversion sentence (Start with Time): He often drinks coffee at home.",
                    pl: "Ułóż zdanie z inwersją (Zacznij od Czasu): On często pije kawę w domu."
                }
            },
            {
                words: ["om 8 uur", "begint", "de vergadering"],
                correct: ["om 8 uur", "begint", "de vergadering"],
                translation: {
                    nl: "Maak een inversie-zin: De vergadering begint om 8 uur.",
                    en: "Make an inversion sentence: The meeting starts at 8 o'clock.",
                    pl: "Ułóż zdanie z inwersją: Spotkanie zaczyna się o 8:00."
                }
            },
            {
                words: ["een email", "schrijf", "nu", "ik", "aan mijn baas"],
                correct: ["nu", "schrijf", "ik", "een email", "aan mijn baas"],
                translation: {
                    nl: "Maak een inversie-zin: Ik schrijf nu een email aan mijn baas.",
                    en: "Make an inversion sentence: I am writing an email to my boss now.",
                    pl: "Ułóż zdanie z inwersją: Piszę teraz e-mail do szefa."
                }
            }
        ];

        let currentEx = 0;
        let selectedLang = 'nl';

        function shuffle(array) {
            let currentIndex = array.length,  randomIndex;
            while (currentIndex != 0) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;
                [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
            }
            return array;
        }

        function renderExercise() {
            const ex = exercises[currentEx];
            
            document.getElementById('ex-trans').innerHTML = `
                <span lang="nl" style="display:${selectedLang === 'nl' ? 'inline' : 'none'}">${ex.translation.nl}</span>
                <span lang="en" style="display:${selectedLang === 'en' ? 'inline' : 'none'}">${ex.translation.en}</span>
                <span lang="pl" style="display:${selectedLang === 'pl' ? 'inline' : 'none'}">${ex.translation.pl}</span>
            `;

            const wordBank = document.getElementById('word-bank');
            const dropZone = document.getElementById('drop-zone');
            wordBank.innerHTML = '';
            dropZone.innerHTML = '';
            document.getElementById('feedback').innerHTML = '';
            document.getElementById('btn-next').style.display = 'none';

            let words = [...ex.words];
            shuffle(words);

            words.forEach(w => {
                let div = document.createElement('div');
                div.className = 'draggable-word';
                div.textContent = w;
                div.onclick = function() {
                    if (this.parentElement.id === 'word-bank') {
                        dropZone.appendChild(this);
                    } else {
                        wordBank.appendChild(this);
                    }
                };
                wordBank.appendChild(div);
            });
        }

        function checkSentence() {
            const ex = exercises[currentEx];
            const dropZone = document.getElementById('drop-zone');
            const userWords = Array.from(dropZone.children).map(c => c.textContent);
            const feedback = document.getElementById('feedback');

            if (userWords.length < ex.correct.length) {
                feedback.innerHTML = `
                    <span lang="nl" style="color:var(--obj-main); display:${selectedLang === 'nl' ? 'inline' : 'none'}">⚠️ Gebruik alle woorden!</span>
                    <span lang="en" style="color:var(--obj-main); display:${selectedLang === 'en' ? 'inline' : 'none'}">⚠️ Use all words!</span>
                    <span lang="pl" style="color:var(--obj-main); display:${selectedLang === 'pl' ? 'inline' : 'none'}">⚠️ Użyj wszystkich słów!</span>
                `;
                return;
            }

            let isCorrect = true;
            for (let i = 0; i < ex.correct.length; i++) {
                if (userWords[i] !== ex.correct[i]) {
                    isCorrect = false;
                    break;
                }
            }

            if (isCorrect) {
                feedback.innerHTML = `
                    <span lang="nl" style="color:var(--subj-main); display:${selectedLang === 'nl' ? 'inline' : 'none'}">✅ Perfecte inversie!</span>
                    <span lang="en" style="color:var(--subj-main); display:${selectedLang === 'en' ? 'inline' : 'none'}">✅ Perfect inversion!</span>
                    <span lang="pl" style="color:var(--subj-main); display:${selectedLang === 'pl' ? 'inline' : 'none'}">✅ Idealna inwersja!</span>
                `;
                document.getElementById('btn-next').style.display = 'inline-block';
            } else {
                feedback.innerHTML = `
                    <span lang="nl" style="color:var(--verb-main); display:${selectedLang === 'nl' ? 'inline' : 'none'}">❌ Fout. Vergeet niet: Tijd/Plaats -> Werkwoord -> Onderwerp!</span>
                    <span lang="en" style="color:var(--verb-main); display:${selectedLang === 'en' ? 'inline' : 'none'}">❌ Incorrect. Remember: Time/Place -> Verb -> Subject!</span>
                    <span lang="pl" style="color:var(--verb-main); display:${selectedLang === 'pl' ? 'inline' : 'none'}">❌ Błąd. Pamiętaj: Czas/Miejsce -> Czasownik -> Podmiot!</span>
                `;
            }
        }

        function nextQuestion() {
            currentEx++;
            if (currentEx >= exercises.length) {
                currentEx = 0; // loop back
            }
            renderExercise();
        }

        function setLang(lang) {
            selectedLang = lang;
            document.querySelectorAll('[lang]').forEach(el => {
                if(el.tagName.toLowerCase() !== 'html') {
                    el.style.display = 'none';
                }
            });
            document.querySelectorAll(`[lang="${lang}"]`).forEach(el => {
                if(el.tagName.toLowerCase() !== 'html') {
                    el.style.display = el.tagName.toLowerCase() === 'span' ? 'inline' : 'block';
                }
            });

            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${lang}`).classList.add('active');
        }

        window.onload = () => {
            setLang('nl');
            renderExercise();
        };
    </script>
</body>
</html>
"""

with open(r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\inversie.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated inversie.html successfully!")
