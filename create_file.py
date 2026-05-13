import os

content = r'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nederlandse Voorzetsels - NT2 A1/A2</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --plaats-bg: #fff5f7;
            --plaats-main: #e91e63;
            --plaats-dark: #ad1457;
            --richting-bg: #f0fbfc;
            --richting-main: #0097a7;
            --richting-dark: #006064;
            --text-main: #2c3e50;
            --text-light: #5d6d7e;
            --white: #ffffff;
            --shadow: 0 15px 35px rgba(0,0,0,0.1);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Outfit', sans-serif; background-color: #f8fafc; color: var(--text-main); line-height: 1.6; overflow-x: hidden; }
        nav { position: fixed; top: 0; width: 100%; background: white; z-index: 1000; padding: 1.2rem; display: flex; justify-content: center; gap: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        nav a { text-decoration: none; font-weight: 800; color: var(--text-main); font-size: 1.1rem; padding: 0.5rem 1.2rem; border-radius: 50px; transition: var(--transition); }
        nav a:hover { background: #f1f5f9; }
        .lang-container { position: sticky; top: 70px; display: flex; justify-content: center; gap: 12px; padding: 20px; background: rgba(248, 250, 252, 0.98); backdrop-filter: blur(10px); z-index: 999; border-bottom: 2px solid #e2e8f0; }
        .lang-btn { border: 2px solid #e2e8f0; background: white; padding: 10px 20px; border-radius: 15px; cursor: pointer; font-weight: 800; font-size: 1rem; transition: var(--transition); }
        .lang-btn.active { background: var(--text-main); color: white; border-color: var(--text-main); }
        .hero { padding: 10rem 2rem 4rem; text-align: center; }
        .hero h1 { font-size: 4rem; font-weight: 800; margin-bottom: 1rem; background: linear-gradient(90deg, var(--plaats-main), var(--richting-main)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.4rem; color: var(--text-light); max-width: 800px; margin: 0 auto; }
        .container { max-width: 1300px; margin: 4rem auto; padding: 0 2rem; }
        .section-title { font-size: 3rem; margin-bottom: 4rem; text-align: center; font-weight: 800; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 3rem; }
        .card { background: white; border-radius: 40px; padding: 3rem; box-shadow: var(--shadow); display: flex; flex-direction: column; transition: var(--transition); border: 1px solid rgba(0,0,0,0.02); }
        .emoji-header { font-size: 5rem; text-align: center; margin-bottom: 2rem; }
        .card .word { font-size: 3rem; font-weight: 800; margin-bottom: 0.8rem; text-align: center; }
        .plaats .word { color: var(--plaats-main); }
        .richting .word { color: var(--richting-main); }
        .card .definition { font-size: 1.2rem; color: var(--text-light); margin-bottom: 2rem; text-align: center; }
        .card .example-item { margin-bottom: 15px; font-size: 1.1rem; font-weight: 500; }
        .translation-sub { font-size: 0.9rem; color: var(--text-light); margin-left: 25px; font-style: italic; margin-top: 2px; }
        .card .logic-box { padding: 1.5rem; border-radius: 20px; font-size: 1.1rem; font-weight: 700; margin-top: auto; }
        .plaats .logic-box { background: var(--plaats-bg); color: var(--plaats-dark); }
        .richting .logic-box { background: var(--richting-bg); color: var(--richting-dark); }
        .exercise-section { background: white; padding: 5rem 2rem; border-radius: 50px; box-shadow: var(--shadow); margin: 6rem auto; max-width: 1000px; }
        .exercise-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 3rem auto; max-width: 450px; background: #2c3e50; padding: 10px; border-radius: 15px; }
        .grid-cell { aspect-ratio: 1; background: white; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; border-radius: 8px; }
        .exercise-questions { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; }
        .q-row { background: #f1f5f9; padding: 20px; border-radius: 20px; display: flex; align-items: center; gap: 15px; }
        .q-row input { width: 80px; padding: 10px; border: 3px solid #cbd5e1; border-radius: 12px; text-align: center; font-weight: 800; font-size: 1.2rem; }
        .feedback { font-size: 1.8rem; margin-left: auto; }
        [lang]:not([lang="nl"]) { display: none; }
        .rtl-text { direction: rtl; text-align: right; }
        @media (max-width: 768px) { .cards-grid, .exercise-questions { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <nav>
        <a href="#intro">Start</a>
        <a href="#plaats">📍 <span lang="nl">Plaats</span><span lang="tr">Yer</span><span lang="ar">المكان</span><span lang="ps">ځای</span></a>
        <a href="#richting">🚀 <span lang="nl">Richting</span><span lang="tr">Yön</span><span lang="ar">الاتجاه</span><span lang="ps">لوری</span></a>
        <a href="#oefenen">✍️ <span lang="nl">Oefenen</span><span lang="tr">Pratik</span><span lang="ar">تمرین</span><span lang="ps">تمرین</span></a>
    </nav>
    <div class="lang-container">
        <button class="lang-btn active" id="btn-nl" onclick="setLang('nl')">🇳🇱 Nederlands</button>
        <button class="lang-btn" id="btn-tr" onclick="setLang('tr')">🇹🇷 Türkçe</button>
        <button class="lang-btn" id="btn-ar" onclick="setLang('ar')">🇸🇦 العربية</button>
        <button class="lang-btn" id="btn-ps" onclick="setLang('ps')">🇦🇫 پښتو</button>
    </div>
    <header class="hero" id="intro">
        <h1>
            <span lang="nl">Voorzetsels Leren</span>
            <span lang="tr">Edatları Öğrenin</span>
            <span lang="ar" class="rtl-text">تعلم حروف الجر</span>
            <span lang="ps" class="rtl-text">د حروفو زده کړه</span>
        </h1>
        <p>
            <span lang="nl">Leer het verschil tussen <strong>Plaats</strong> en <strong>Richting</strong>.</span>
            <span lang="tr"><strong>Yer</strong> ve <strong>Yön</strong> arasındaki farkı öğrenin.</span>
            <span lang="ar" class="rtl-text">تعلم الفرق tussen <strong>المكان</strong> و <strong>الاتجاه</strong>.</span>
            <span lang="ps" class="rtl-text">د <strong>ځای</strong> او <strong>لوري</strong> تر منځ توپیر زده کړئ.</span>
        </p>
    </header>
    <section class="container" id="plaats">
        <h2 class="section-title" style="color: var(--plaats-main);">📍 <span lang="nl">Plaats</span><span lang="tr">Yer</span><span lang="ar">المكان</span><span lang="ps">ځای</span></h2>
        <div class="cards-grid" id="plaats-container"></div>
    </section>
    <section class="container" id="richting">
        <h2 class="section-title" style="color: var(--richting-main);">🚀 <span lang="nl">Richting</span><span lang="tr">Yön</span><span lang="ar">الاتجاه</span><span lang="ps">لوری</span></h2>
        <div class="cards-grid" id="richting-container"></div>
    </section>
    <section class="exercise-section" id="oefenen">
        <h2 class="section-title">✍️ <span lang="nl">Oefenen</span><span lang="tr">Pratik</span><span lang="ar">تمرین</span><span lang="ps">تمرین</span></h2>
        <div id="exercise-container"></div>
    </section>
    <script>
        let currentLang = 'nl';
        const dataPlaats = [
            { word: "in", emoji: "📦", def: { nl: "In een holle ruimte.", tr: "Bir boşluk içinde.", ar: "داخل مساحة مجوفة.", ps: "په یو خالي ځای کې." }, 
              ex: [
                { nl: "De melk staat in de koelkast.", tr: "Süt buzdolabında.", ar: "الحليب في الثلاجة.", ps: "شیدې په یخچال کې دي." },
                { nl: "Ik ben in de supermarkt.", tr: "Süpermarketteyim.", ar: "أنا في السوبر ماركت.", ps: "زه په سوپر مارکیټ کې یم." },
                { nl: "De pen zit in de tas.", tr: "Kalem çantada.", ar: "القلم في الحقيبة.", ps: "قلم په بکس کې دی." }
              ], rule: { nl: "IN = Hol object.", tr: "IN = Boş nesne.", ar: "IN = شيء مجوف.", ps: "IN = خالي شی." } },
            { word: "op", emoji: "🪑", def: { nl: "Op een oppervlak.", tr: "Bir yüzeyin üzerinde.", ar: "فوق سطح ما.", ps: "د یوې سطحې پر سر." }, 
              ex: [
                { nl: "Het boek ligt op de tafel.", tr: "Kitap masanın üzerinde.", ar: "الكتاب على الطاولة.", ps: "کتاب په میز باندې دی." },
                { nl: "Ik zit op de bank.", tr: "Kanepede oturuyorum.", ar: "أنا جالس على الأريكة.", ps: "زه په کوچ باندې ناست یم." },
                { nl: "De appel ligt op het bord.", tr: "Elma tabakta.", ar: "التفاحة على الطبق.", ps: "مڼه په بشقاب کې ده." }
              ], rule: { nl: "OP = Contact met oppervlak.", tr: "OP = Yüzeyle temas.", ar: "OP = تلامس مع السطح.", ps: "OP = له سطحې سره تماس." } },
            { word: "boven", emoji: "☁️", def: { nl: "Hoger dan (geen contact).", tr: "Daha yüksekte.", ar: "أعلى (بدون تلامس).", ps: "پورته (بې له تماس)." }, 
              ex: [
                { nl: "De lamp hangt boven de tafel.", tr: "Lamba masanın üzerinde asılı.", ar: "المصباح معلق فوق الطاولة.", ps: "څراغ له میز څخه پورته ځړول شوی دی." },
                { nl: "De vogel vliegt boven de boom.", tr: "Kuş ağacın üzerinde uçuyor.", ar: "الطائر يطير فوق الشجرة.", ps: "مرغۍ د ونې په سر کې الوتنه کوي." },
                { nl: "De wolk zweeft boven de stad.", tr: "Bulut şehrin üzerinde süzülüyor.", ar: "السحابة تطفو فوق المدينة.", ps: "ورېځ د ښار په سر کې ده." }
              ], rule: { nl: "BOVEN = Zweeft erover.", tr: "BOVEN = Üzerinde süzülür.", ar: "BOVEN = يطفو فوقه.", ps: "BOVEN = له پاسه ځړېدل." } },
            { word: "onder", emoji: "👟", def: { nl: "Lager dan.", tr: "Daha aşağıda.", ar: "أسفل من.", ps: "لاندې." }, 
              ex: [
                { nl: "De kat zit onder de tafel.", tr: "Kedi masanın altında.", ar: "القط تحت الطاولة.", ps: "پیشو د میز لاندې ده." },
                { nl: "De schoenen staan onder de bank.", tr: "Ayakkabılar kanepenin altında.", ar: "الأحذية تحت الأريكة.", ps: "بوټان د کوچ لاندې دي." },
                { nl: "Ik sta onder de douche.", tr: "Duşun altındayım.", ar: "أنا تحت الدش.", ps: "زه تر شاور لاندې یم." }
              ], rule: { nl: "ONDER = Lager dan.", tr: "ONDER = Daha aşağıda.", ar: "ONDER = أسفل.", ps: "ONDER = لاندې." } },
            { word: "voor", emoji: "🚪", def: { nl: "Voorkant.", tr: "Ön.", ar: "أمام.", ps: "مخکې." }, 
              ex: [
                { nl: "De auto staat voor het huis.", tr: "Araba evin önünde.", ar: "السيارة أمام المنزل.", ps: "موټر د کور مخې ته ولاړ دی." },
                { nl: "Ik sta voor de deur.", tr: "Kapının önündeyim.", ar: "أنا أمام الباب.", ps: "زه د دروازې مخې te ولاړ یم." },
                { nl: "Jan zit voor de televisie.", tr: "Jan televizyonun önünde oturuyor.", ar: "يان يجلس أمام التلفاز.", ps: "جان د ټلویزیون مخې ته ناست دی." }
              ], rule: { nl: "VOOR = Voorkant.", tr: "VOOR = Ön.", ar: "VOOR = أمام.", ps: "VOOR = مخکې." } },
            { word: "achter", emoji: "🌳", def: { nl: "Achterkant.", tr: "Arka.", ar: "خلف.", ps: "شاته." }, 
              ex: [
                { nl: "De tuin is achter het huis.", tr: "Bahçe evin arkasında.", ar: "الحديقة خلف المنزل.", ps: "باغچه د کور شاته ده." },
                { nl: "De zon staat achter de wolken.", tr: "Güneş bulutların arkasında.", ar: "الشمس خلف الغيوم.", ps: "لمر تر ورېځو لاندې دی." },
                { nl: "Ik sta achter je.", tr: "Senin arkandayım.", ar: "أنا خلفك.", ps: "زه ستا شاته یم." }
              ], rule: { nl: "ACHTER = Achterkant.", tr: "ACHTER = Arka.", ar: "ACHTER = خلف.", ps: "ACHTER = شاته." } },
            { word: "naast", emoji: "🧍‍♂️", def: { nl: "Zijkant.", tr: "Yan.", ar: "بجانب.", ps: "څنګ ته." }, 
              ex: [
                { nl: "Ik zit naast mijn vriend.", tr: "Arkadaşımın yanında oturuyorum.", ar: "أنا أجلس بجانب صديقي.", ps: "زه د خپل ملګري څنګ ته ناست یم." },
                { nl: "De bakker is naast de bank.", tr: "Fırın bankanın yanında.", ar: "المخبز بجانب البنك.", ps: "ننداره د بانک څنګ ته ده." },
                { nl: "De bril ligt naast de laptop.", tr: "Gözlük dizüstü bilgisayarın yanında.", ar: "النظارات بجانب المحمول.", ps: "سترګۍ د لپ ټاپ څنګ ته دي." }
              ], rule: { nl: "NAAST = Opzij.", tr: "NAAST = Yan.", ar: "NAAST = بجانب.", ps: "NAAST = څنګ ته." } },
            { word: "tussen", emoji: "↔️", def: { nl: "In het midden van 2.", tr: "İkisinin arasında.", ar: "بين شيئين.", ps: "د دوو تر منځ." }, 
              ex: [
                { nl: "Ik sta tussen twee bomen.", tr: "İki ağacın arasındayım.", ar: "أنا أقف بين شجرتين.", ps: "زه د دوو ونو تر منځ ولاړ یم." },
                { nl: "Het kind slaapt tussen de ouders.", tr: "Çocuk ebeveynlerin arasında uyuyor.", ar: "الطفل ينام بين الوالدين.", ps: "ماشوم د مور او پلار تر منځ ویده دی." },
                { nl: "De sleutel ligt tussen de kussens.", tr: "Anahtar yastıkların arasında.", ar: "المفتاح بين الوسائد.", ps: "کیلي د بالښتونو تر منځ ده." }
              ], rule: { nl: "TUSSEN = Midden.", tr: "TUSSEN = Orta.", ar: "TUSSEN = في المنتصف.", ps: "TUSSEN = منځ." } },
            { word: "tegen", emoji: "🧱", def: { nl: "Leunend tegen.", tr: "Dayalı.", ar: "متكئ على.", ps: "پورې تکیه." }, 
              ex: [
                { nl: "De fiets staat tegen de muur.", tr: "Bisiklet duvara dayalı.", ar: "الدراجة مستندة إلى الحائط.", ps: "بایسکل د دېوال پورې تکیe دی." },
                { nl: "Ik leun tegen de kast.", tr: "Dolaba yaslanıyorum.", ar: "أنا أتكئ على الخزانة.", ps: "زه پر المارۍ تکیه کوم." },
                { nl: "De ladder staat tegen de boom.", tr: "Merdiven ağaca dayalı.", ar: "السلم مستند إلى الشجرة.", ps: "زینه د ونې پورې تکیه ده." }
              ], rule: { nl: "TEGEN = Contact.", tr: "TEGEN = Temas.", ar: "TEGEN = تلامس.", ps: "TEGEN = تماس." } },
            { word: "aan", emoji: "🖼️", def: { nl: "Vastzittend.", tr: "Bitişik/Asılı.", ar: "عند/على.", ps: "پورې nښتی." }, 
              ex: [
                { nl: "De klok hangt aan de muur.", tr: "Saat duvarda asılı.", ar: "الساعة معلقة على الحائط.", ps: "ګړۍ پر دېوال ځړېدلې ده." },
                { nl: "De jas hangt aan de kapstok.", tr: "Ceket askıda asılı.", ar: "المعطف معلق على المشجب.", ps: "جاکټ په المارۍ کې ځړول شوی دی." },
                { nl: "Ik woon aan het water.", tr: "Su kenarında yaşıyorum.", ar: "أنا أسكن بجانب الماء.", ps: "زه اوبو ته نږدې اوسېږم." }
              ], rule: { nl: "AAN = Bevestigd.", tr: "AAN = Sabitlenmiş.", ar: "AAN = مثبت.", ps: "AAN = نښلول شوی." } },
            { word: "dicht bij", emoji: "🏡", def: { nl: "Korte afstand.", tr: "Yakın.", ar: "قريب.", ps: "نږدې." }, 
              ex: [
                { nl: "Ik woon dicht bij school.", tr: "Okula yakın yaşıyorum.", ar: "أنا أسكن بالقرب من المدرسة.", ps: "زه ښوونځي ته نږدې اوسېږم." },
                { nl: "De bushalte is dicht bij.", tr: "Otobüs durağı yakın.", ar: "موقف الحافلات قريب.", ps: "د بس تمځای نږدې دی." },
                { nl: "Kom dicht bij mij staan.", tr: "Yanıma yakın gel.", ar: "تعال وقف بالقرب مني.", ps: "ما ته نږدې ودریږه." }
              ], rule: { nl: "DICHT BIJ = Nabij.", tr: "DICHT BIJ = Yakın.", ar: "DICHT BIJ = قريب.", ps: "DICHT BIJ = نږدې." } },
            { word: "ver van", emoji: "✈️", def: { nl: "Grote afstand.", tr: "Uzak.", ar: "بعيد.", ps: "لیرې." }, 
              ex: [
                { nl: "Ik woon ver van werk.", tr: "İşten uzak yaşıyorum.", ar: "أنا أسكن بعيداً عن العمل.", ps: "زه له کاره لیرې اوسېږم." },
                { nl: "De supermarkt is ver van hier.", tr: "Süpermarket buradan uzak.", ar: "السوبر ماركت بعيد من هنا.", ps: "سوپر مارکیټ له دې ځایه لیرې دی." },
                { nl: "Wij zijn ver van huis.", tr: "Evden uzağız.", ar: "نحن بعيدون عن المنزل.", ps: "موږ له کوره لیرې یو." }
              ], rule: { nl: "VER VAN = Afstand.", tr: "VER VAN = Uzak.", ar: "VER VAN = بعيد.", ps: "VER VAN = لیرې." } },
            { word: "links van", emoji: "👈", def: { nl: "Linkerkant.", tr: "Sol.", ar: "يسار.", ps: "کیڼ." }, 
              ex: [
                { nl: "De kast staat links.", tr: "Dolap solda.", ar: "الخزانة على اليسار.", ps: "المارۍ په کیڼ اړخ کې ده." },
                { nl: "Het toilet is links van de gang.", tr: "Tuvalet koridorun solunda.", ar: "المرحاض على يسار الممر.", ps: "تشناب د دهلېز په کیڼ اړخ کې دی." },
                { nl: "Zij zit links van mij.", tr: "Solumda oturuyor.", ar: "هي تجلس على يساري.", ps: "هغه زما په کیڼ اړخ کې ناسته ده." }
              ], rule: { nl: "LINKS = Linkerkant.", tr: "LINKS = Sol.", ar: "LINKS = يسار.", ps: "LINKS = کیڼ." } },
            { word: "rechts van", emoji: "👉", def: { nl: "Rechterkant.", tr: "Sağ.", ar: "يمين.", ps: "ښي." }, 
              ex: [
                { nl: "De bank staat rechts.", tr: "Banka sağda.", ar: "البنك على اليمين.", ps: "بانک په ښي اړخ کې دی." },
                { nl: "De keuken is rechts van de woonkamer.", tr: "Mutfak oturma odasının sağında.", ar: "المطبخ على يمين غرفة المعيشة.", ps: "پخلنځی د اوسېدو د خونې په ښي اړخ کې دی." },
                { nl: "Hij loopt rechts van de weg.", tr: "Yolun sağından yürüyor.", ar: "هو يمشي على يمين الطريق.", ps: "هغه d سړک په ښي اړخ کې روان دی." }
              ], rule: { nl: "RECHTS = Rechterkant.", tr: "RECHTS = Sağ.", ar: "RECHTS = يمين.", ps: "RECHTS = ښي." } }
        ];
        const dataRichting = [
            { word: "in", emoji: "📥", def: { nl: "Naar binnen.", tr: "İçeri.", ar: "للدخل.", ps: "دننه." }, 
              ex: [
                { nl: "Stap in de bus.", tr: "Otobüse bin.", ar: "اركب الحافلة.", ps: "بس ته پورته شه." },
                { nl: "Loop in de winkel.", tr: "Mağazaya gir.", ar: "ادخل إلى المتجر.", ps: "هټۍ ته ننوځه." },
                { nl: "Gooi het in de prullenbak.", tr: "Çöp kutusuna at.", ar: "ارمه في سلة المهملات.", ps: "دا په کثافاتو کې واچوه." }
              ], rule: { nl: "IN = Naar binnen.", tr: "IN = İçeri.", ar: "IN = للداخل.", ps: "IN = دننه." } },
            { word: "uit", emoji: "📤", def: { nl: "Naar buiten.", tr: "Dışarı.", ar: "للخارج.", ps: "باندې." }, 
              ex: [
                { nl: "Stap uit de bus.", tr: "Otobüsten in.", ar: "انزل من الحافلة.", ps: "له بسه کوz شه." },
                { nl: "Loop uit het gebouw.", tr: "Binadan çık.", ar: "اخرج من المبنى.", ps: "له ودانۍ بهر ووځه." },
                { nl: "Haal de melk uit de koelkast.", tr: "Sütü buzdolabından çıkar.", ar: "أخرج الحليب من الثلاجة.", ps: "شیدې له یخچال څخه وباسه." }
              ], rule: { nl: "UIT = Naar buiten.", tr: "UIT = Dışarı.", ar: "UIT = للخارج.", ps: "UIT = بهر." } },
            { word: "naar", emoji: "🎯", def: { nl: "Bestemming.", tr: "Hedef.", ar: "إلى.", ps: "ته." }, 
              ex: [
                { nl: "Ik ga naar huis.", tr: "Eve gidiyorum.", ar: "أنا ذاهب للمنزل.", ps: "زه کور ته ځم." },
                { nl: "Wij fietsen naar de stad.", tr: "Şehre bisikletle gidiyoruz.", ar: "نحن نركب الدراجة إلى المدينة.", ps: "موږ ښار ته په بایسکل ځو." },
                { nl: "Zij kijkt naar de film.", tr: "Film izliyor.", ar: "هي تشاهد الفيلم.", ps: "هغه فلم ګوري." }
              ], rule: { nl: "NAAR = Bestemming.", tr: "NAAR = Hedef.", ar: "NAAR = وجهة.", ps: "NAAR = هدف." } },
            { word: "van", emoji: "🏁", def: { nl: "Oorsprong.", tr: "Başlangıç.", ar: "من.", ps: "له." }, 
              ex: [
                { nl: "Ik kom van werk.", tr: "İşten geliyorum.", ar: "أنا قادم من العمل.", ps: "زه له کاره راځم." },
                { nl: "De trein komt van Amsterdam.", tr: "Tren Amsterdam'dan geliyor.", ar: "القطار قادم من أمستردام.", ps: "ریل ګاډی له امستردام څخه راځي." },
                { nl: "Ik kreeg een cadeau van Jan.", tr: "Jan'dan bir hediye aldım.", ar: "حصلت على هدية من يان.", ps: "ما له جان څخه dالۍ ترلاسه کړه." }
              ], rule: { nl: "VAN = Beginpunt.", tr: "VAN = Kaynak.", ar: "VAN = من.", ps: "VAN = سرچینه." } },
            { word: "naar boven", emoji: "⬆️", def: { nl: "Omhoog.", tr: "Yukarı.", ar: "للأعلى.", ps: "پورته." }, 
              ex: [
                { nl: "Ik ga naar boven.", tr: "Yukarı çıkıyorum.", ar: "أنا ذاهب للأعلى.", ps: "زه پورته ځم." },
                { nl: "De vogel vliegt naar boven.", tr: "Kuş yukarı uçuyor.", ar: "الطائر يطير للأعلى.", ps: "مرغۍ پورته الوتنه کوي." },
                { nl: "Zet de doos naar boven.", tr: "Kutuyu yukarı koy.", ar: "ضع الصندوق في الأعلى.", ps: "بکس پورته کېږده." }
              ], rule: { nl: "BOVEN = Omhoog.", tr: "BOVEN = Yukarı.", ar: "BOVEN = للأعلى.", ps: "BOVEN = پورته." } },
            { word: "naar beneden", emoji: "⬇️", def: { nl: "Omlaag.", tr: "Aşağı.", ar: "للأسفل.", ps: "ښکته." }, 
              ex: [
                { nl: "Ik ga naar beneden.", tr: "Aşağı iniyorum.", ar: "أنا ذاهب للأسفل.", ps: "زه ښکته ځم." },
                { nl: "De lift gaat naar beneden.", tr: "Asansör aşağı iniyor.", ar: "المصعد ينزل للأسفل.", ps: "لیفت ښکته ځي." },
                { nl: "Leg je boek naar beneden.", tr: "Kitabını aşağı koy.", ar: "ضع كتابك بالأسفل.", ps: "خپل کتاب ښکته کېږده." }
              ], rule: { nl: "BENEDEN = Omlaag.", tr: "BENEDEN = Aşağı.", ar: "BENEDEN = للأسفل.", ps: "BENEDEN = ښکته." } },
            { word: "over", emoji: "🌉", def: { nl: "Passeren.", tr: "Üzerinden.", ar: "عبر.", ps: "له پاسه." }, 
              ex: [
                { nl: "Ik loop over de brug.", tr: "Köprüden geçiyorum.", ar: "أنا أمشي عبر الجسر.", ps: "زه له پله څخه تېرېږم." },
                { nl: "Wij vliegen over de zee.", tr: "Denizin üzerinden uçuyoruz.", ar: "نحن نطير فوق البحر.", ps: "موږ د بحر له پاسه الوتنه کوو." },
                { nl: "Spring over het hek.", tr: "Çitin üzerinden atla.", ar: "اقفز فوق السياج.", ps: "له کټارې څخه پورته ټوپ کړه." }
              ], rule: { nl: "OVER = Passeren.", tr: "OVER = Üzerinden.", ar: "OVER = عبر.", ps: "OVER = تېرېدل." } },
            { word: "door", emoji: "🚇", def: { nl: "Ermiddenin.", tr: "İçinden.", ar: "من خلال.", ps: "له منځه." }, 
              ex: [
                { nl: "Ik rijd door de tunnel.", tr: "Tünelden geçiyorum.", ar: "أنا أقود عبر النفق.", ps: "زه د تونل له لارې موټر چلوم." },
                { nl: "Wij lopen door het park.", tr: "Parkın içinden yürüyoruz.", ar: "نحن نمشي عبر الحديقة.", ps: "موږ د پارک له لارې روان یو." },
                { nl: "Kijk door het raam.", tr: "Pencereden bak.", ar: "انظر من خلال النافذة.", ps: "له کړکۍ څخه بهر وګوره." }
              ], rule: { nl: "DOOR = Eruit komen.", tr: "DOOR = İçinden.", ar: "DOOR = من خلال.", ps: "DOOR = له منځه." } },
            { word: "rond", emoji: "🔄", def: { nl: "Cirkel.", tr: "Daire.", ar: "حول.", ps: "شاوخوا." }, 
              ex: [
                { nl: "Wij lopen rond het meer.", tr: "Gölün etrafında yürüyoruz.", ar: "نحن نمشي حول البحيرة.", ps: "موږ د جهيل په شاوخوا کې ګرځو." },
                { nl: "De auto rijdt rond de rotonde.", tr: "Araba kavşak etrafında dönüyor.", ar: "السيارة تدور حول الدوار.", ps: "موټر د چوک په شاوخوا کې ګرځي." },
                { nl: "Kijk eens rond in de kamer.", tr: "Odada bir etrafına bak.", ar: "ألقِ نظرة حول الغرفة.", ps: "په خونه کې شاوخوا وګوره." }
              ], rule: { nl: "ROND = Cirkel.", tr: "ROND = Daire.", ar: "ROND = حول.", ps: "ROND = شاوخوا." } },
            { word: "langs", emoji: "🛤️", def: { nl: "Parallel.", tr: "Boyunca.", ar: "على طول.", ps: "په اوږدو کې." }, 
              ex: [
                { nl: "Ik loop langs de weg.", tr: "Yol boyunca yürüyorum.", ar: "أنا أمشي على طول الطريق.", ps: "زه د سړک په اوږدو کې روان یم." },
                { nl: "De trein rijdt langs de kust.", tr: "Tren sahil boyunca gidiyor.", ar: "القطار يسير على طول الساحل.", ps: "ریل ګاډی د ساحل په اوږدو کې ځي." },
                { nl: "Kom even langs mijn huis.", tr: "Evime bir uğra.", ar: "مر على منزلي.", ps: "زما کور ته یو ځل راشه." }
              ], rule: { nl: "LANGS = Ernaast.", tr: "LANGS = Yanında.", ar: "LANGS = على طول.", ps: "LANGS = په اوږدو کې." } },
            { word: "weg van", emoji: "🏃‍♂️💨", def: { nl: "Afstand.", tr: "Uzaklaşmak.", ar: "بعيداً عن.", ps: "لیرې." }, 
              ex: [
                { nl: "Ik loop weg van het vuur.", tr: "Ateşten uzaklaşıyorum.", ar: "أنا أبتعد عن النار.", ps: "زه له اور څخه لیرې ځم." },
                { nl: "Rijd weg van de stad.", tr: "Şehirden uzaklaş.", ar: "قد بعيداً عن المدينة.", ps: "له ښار څخه لیرې موټر چلوه." },
                { nl: "Ga weg van de gevaarlijke plek.", tr: "Tehlikeli yerden uzaklaş.", ar: "ابتعد عن المكان الخطير.", ps: "له خطرناک ځای څخه لیرې شه." }
              ], rule: { nl: "WEG = Afstand.", tr: "WEG = Uzaklaşmak.", ar: "WEG = ابتعاد.", ps: "WEG = لیرې." } }
        ];
        function setLang(lang) {
            currentLang = lang;
            document.querySelectorAll('body [lang]').forEach(el => {
                const isMatch = el.getAttribute('lang') === lang;
                if (el.tagName === 'SPAN') { el.style.display = isMatch ? 'inline' : 'none'; }
                else { el.style.display = isMatch ? 'block' : 'none'; }
            });
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.toggle('active', btn.id === 'btn-' + lang);
            });
            renderCards();
            renderExercises();
        }
        function renderCards() {
            const labels = { nl: "Logische regel", tr: "Mantıksal kural", ar: "قاعدة منطقية", ps: "منطقي قاعده" };
            const pCont = document.getElementById('plaats-container');
            const rCont = document.getElementById('richting-container');
            if (!pCont || !rCont) return;
            const createContent = (item, type) => `
                <div class="card ${type}">
                    <div class="emoji-header">${item.emoji}</div>
                    <div class="word">${item.word}</div>
                    <div class="definition">${item.def[currentLang]}</div>
                    <div class="example-list">
                        ${item.ex.map(e => `
                            <div class="example-item">
                                <div>✅ ${e.nl}</div>
                                ${currentLang !== 'nl' ? `<div class="translation-sub">(${e[currentLang]})</div>` : ''}
                            </div>
                        `).join('')}
                    </div>
                    <div class="logic-box">💡 <strong>${labels[currentLang]}:</strong><br>${item.rule[currentLang]}</div>
                </div>`;
            pCont.innerHTML = dataPlaats.map(i => createContent(i, 'plaats')).join('');
            rCont.innerHTML = dataRichting.map(i => createContent(i, 'richting')).join('');
        }
        const exercises = [
            { grid: ["🐱", "1", "🛒", "2", "⚽", "3", "👟", "4", "🧦", "5", "☀️", "6", "🐟", "7", "📏", "8", "⏰", "9", "🛍️", "10", "🍾", "11", "🧢", "12", "📱"], qs: [{ q: "Kijk naar 🐱. Wat staat rechts?", a: "1" }, { q: "Kijk naar 🛒. Wat staat onder?", a: "4" }, { q: "Kijk naar ⏰. Wat staat links?", a: "8" }, { q: "Kijk naar ⏰. Wat staat onder?", a: "11" }, { q: "Kijk naar 🐟. Wat staat boven?", a: "4" }, { q: "Kijk naar 📱. Wat staat links?", a: "12" }] },
            { grid: ["🍎", "A", "🍌", "B", "🍇", "C", "🚗", "D", "🚲", "E", "🏠", "F", "🌳", "G", "🌸", "H", "🍦", "I", "🍕", "J", "🎾", "K", "🎸", "L", "🎨"], qs: [{ q: "Kijk naar 🍌. Wat staat rechts?", a: "B" }, { q: "Kijk naar 🌳. Wat staat rechts?", a: "G" }, { q: "Kijk naar 🚲. Wat staat boven?", a: "B" }, { q: "Kijk naar 🏠. Wat staat rechts?", a: "F" }, { q: "Kijk naar 🍦. Wat staat links?", a: "H" }, { q: "Kijk naar 🍕. Wat staat rechts?", a: "J" }] },
            { grid: ["🔴", "X", "🔵", "Y", "🟢", "Z", "T", "7", "W", "8", "S", "9", "M", "10", "D", "11", "H", "12", "V", "13", "L", "14", "P", "15", "K"], qs: [{ q: "Kijk naar 🔵. Wat staat rechts?", a: "Y" }, { q: "Kijk naar S. Wat staat onder?", a: "11" }, { q: "Kijk naar Z. Wat staat rechts?", a: "T" }, { q: "Kijk naar 9. Wat staat boven?", a: "T" }, { q: "Kijk naar 14. Wat staat links?", a: "L" }, { q: "Kijk naar V. Wat staat boven?", a: "10" }] },
            { grid: ["🚗", "10", "🚕", "20", "🚙", "30", "🚌", "40", "🚎", "50", "🏎️", "60", "🚓", "70", "🚑", "80", "🚒", "90", "🚐", "100", "🚲", "200", "🛴", "300", "🛵"], qs: [{ q: "Kijk naar 🚗. Wat staat rechts?", a: "10" }, { q: "Kijk naar 🚎. Wat staat onder?", a: "70" }, { q: "Kijk naar 🚌. Wat staat links?", a: "30" }, { q: "Kijk naar 🚒. Wat staat boven?", a: "60" }, { q: "Kijk naar 🚲. Wat staat rechts?", a: "200" }, { q: "Kijk naar 🛴. Wat staat rechts?", a: "300" }] },
            { grid: ["A", "1", "B", "2", "C", "D", "3", "E", "4", "F", "G", "5", "H", "6", "I", "J", "7", "K", "8", "L", "M", "9", "N", "10", "O"], qs: [{ q: "Kijk naar A. Wat staat rechts?", a: "1" }, { q: "Kijk naar D. Wat staat onder?", a: "G" }, { q: "Kijk naar 3. Wat staat links?", a: "D" }, { q: "Kijk naar 8. Wat staat boven?", a: "6" }, { q: "Kijk naar N. Wat staat rechts?", a: "10" }, { q: "Kijk naar K. Wat staat onder?", a: "N" }] }
        ];
        function renderExercises() {
            const cont = document.getElementById('exercise-container');
            if (!cont) return;
            cont.innerHTML = exercises.map((ex, idx) => `
                <div style="margin-bottom: 4rem;">
                    <h3 style="text-align:center; margin-bottom:1.5rem; font-size:1.8rem; font-weight:800;">Oefening ${idx + 1}</h3>
                    <div class="exercise-grid">${ex.grid.map(c => `<div class="grid-cell">${c}</div>`).join('')}</div>
                    <div class="exercise-questions">
                        ${ex.qs.map(q => `
                            <div class="q-row">
                                <span style="font-weight:700;">${q.q}</span>
                                <input type="text" oninput="check(this, '${q.a}')" placeholder="...">
                                <span class="feedback"></span>
                            </div>`).join('')}
                    </div>
                </div>`).join('');
        }
        function check(input, answer) {
            const f = input.nextElementSibling;
            if (input.value.trim().toLowerCase() === answer.toLowerCase()) {
                f.innerText = "✅"; f.style.color = "green"; input.style.borderColor = "green";
            } else if (input.value.length > 0) {
                f.innerText = "❌"; f.style.color = "red"; input.style.borderColor = "red";
            } else { f.innerText = ""; input.style.borderColor = "#cbd5e1"; }
        }
        setLang('nl');
    </script>
</body>
</html>'''

with open(r'h:\Mijn Drive\HTML FILES\voorzetsels.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("File created successfully!")
