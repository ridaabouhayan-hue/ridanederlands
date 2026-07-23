import os
import json
from _lessons_data import LESSONS_DATA

# Define the target directory (same directory as this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. LANDING PAGES METADATA
THEMES = {
    1: {
        "title": "Verhuizen",
        "desc": "Lessen over verhuizen, zinnen maken en de basisgrammatica van A2.",
        "icon": "📦",
        "active": True,
        "paragraphs": [
            ("1.1", "Nieuwe buren", "Woordenschat rondom verhuizen en buren ontmoeten."),
            ("1.2", "Zinnen maken", "De basisvolgorde van hoofdzinnen (S-V-R)."),
            ("1.3", "Dit is mijn familie.", "Gebruik van dit is, dat is, dit zijn, dat zijn."),
            ("1.4", "Huiswerk maken", "Leren praten over studeren en schoolwerk."),
            ("1.5", "Hoe gaat het?", "Vragen hoe het met iemand gaat en gepast antwoorden."),
            ("1.6", "Er is een tuin. – Er zijn drie kamers.", "Gebruik van er is (enkelvoud) en er zijn (meervoud)."),
            ("1.7", "En, maar, want, dus, of", "Zinnen verbinden met nevenschikkende voegwoorden."),
            ("1.8", "Marktplaats", "Kopen en verkopen van meubels en tweedehands spullen."),
            ("1.9", "De grote kast – de kleine spiegel", "Bijvoeglijke naamwoorden met de- en het-woorden."),
            ("1.10", "Op het station", "Treinreizen en stationsaanduidingen begrijpen."),
            ("1.11", "Ik begrijp, hij begrijpt, wij begrijpen", "Tegenwoordige tijd van regelmatige werkwoorden."),
            ("1.12", "Geld op je OV-chipkaart zetten", "Openbaar vervoer en in- en uitchecken."),
            ("1.13", "Woorden met -lijk", "Uitspraak en spelling van woorden op -lijk."),
            ("1.14", "Contact met de buren", "Korte gesprekjes en afspraken maken met buren."),
            ("1.15", "Klein, kleiner – groot, groter", "Vergrotende trap (comparatief) in vergelijkingen.")
        ]
    },
    2: {
        "title": "Nederland",
        "desc": "Lessen over gewoontes, het weer en de voltooide tijd.",
        "icon": "🇳🇱",
        "active": False,
        "paragraphs": [
            ("2.1", "Feesten en gewoontes", "Woordenschat en verhalen over feestdagen."),
            ("2.2", "Groot, groter, het grootst", "Overtreffende trap (superlatief)."),
            ("2.5", "Ik heb gewerkt – wij hebben gewoond", "Voltooide tijd (perfectum) van regelmatige werkwoorden."),
            ("2.7", "Ik bel morgen. – Morgen bel ik.", "Inversie bij tijdsaanduidingen."),
            ("2.13", "Zussen, zonen, kinderen", "Meervouden van zelfstandige naamwoorden."),
            ("2.15", "Jij hebt gegeten – wij zijn gegaan", "Voltooide tijd van onregelmatige werkwoorden.")
        ]
    },
    3: {
        "title": "Kinderen",
        "desc": "Lessen over familie, opvoeding en bijzinnen.",
        "icon": "👶",
        "active": False,
        "paragraphs": [
            ("3.2", "Omdat en als", "Bijzinnen met omdat en als (verba achteraan)."),
            ("3.4", "...om brood te kopen", "Doel uitdrukken met om ... te."),
            ("3.6", "Ik maak schoon. – De docent legt uit.", "Tegenwoordige tijd van scheidbare werkwoorden."),
            ("3.8", "Hij zegt dat... – Hij vraagt of...", "Indirecte rede met dat/of."),
            ("3.12", "Foto – foto’s, baby – baby’s", "Meervoud met apostrof -s.")
        ]
    },
    4: {
        "title": "Winkels",
        "desc": "Lessen over werkdagen, klachten en voornaamwoorden.",
        "icon": "🛒",
        "active": False,
        "paragraphs": [
            ("4.2", "Morgen moet ik werken. - Daarom moet ik vroeg opstaan.", "Inversie met daarom en modale werkwoorden."),
            ("4.4", "Hij, het, ze", "Persoonlijke voornaamwoorden als onderwerp."),
            ("4.10", "Tim helpt mij. – Hij koopt een boek voor mij.", "Persoonlijke voornaamwoorden als object (lijdend voorwerp)."),
            ("4.12", "Het ontbijt is klaar. – Olga zet het op tafel.", "Voornaamwoorden voor dingen (het, ze).")
        ]
    }
}

OVERVIEW_TEMPLATE = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="NT2 A2 Thema {num} — {title}. Kies een paragraaf om te beginnen.">
  <title>Thema {num} — {title} — NT2 A2</title>
  <link rel="stylesheet" href="style.css">
  <script>
      (function() {
          const currentTheme = localStorage.getItem('a2-theme') || 'light';
          document.documentElement.setAttribute('data-theme', currentTheme);
      })();
  </script>
</head>
<body>

  <!-- Language Bar -->
  <nav class="language-bar" aria-label="Taalkeuze">
    <button id="theme-toggle" class="lang-btn" style="cursor:pointer; border-color: var(--accent-purple); color: var(--accent-purple);">🌓</button>
    <span class="label">🌐 Taal:</span>
    <span class="lang-btn active" onclick="setPageLang('nl')">🇳🇱 Nederlands</span>
    <span class="lang-btn" onclick="setPageLang('en')">🇬🇧 English</span>
    <span class="lang-btn" onclick="setPageLang('ar')">🇸🇦 العربية</span>
    <span class="lang-btn" onclick="setPageLang('tr')">🇹🇷 Türkçe</span>
    <span class="lang-btn" onclick="setPageLang('dari')">🇦🇫 دری</span>
    <span class="lang-btn" onclick="setPageLang('thai')">🇹🇭 ไทย</span>
  </nav>

  <main class="page-container">
    <a href="index.html" class="back-link">← Terug naar alle thema's</a>

    <header class="page-header">
      <div class="breadcrumb">
        <a href="index.html">Thema's</a>
        <span>›</span>
        <span>Thema {num}</span>
      </div>
      <h1>{icon} Thema {num} — {title}</h1>
      <p class="subtitle" data-translate="subtitle">{desc}</p>
    </header>

    <div class="para-list">
      {para_list_html}
    </div>
  </main>

  <footer class="site-footer">
    NT2 A2 Leerplatform &copy; 2026
  </footer>

  <script>
    // === Voortgangsindicatoren ===
    function toonVoortgang() {
        const voltooid = JSON.parse(localStorage.getItem('nt2_voltooid') || '[]');
        voltooid.forEach(paraId => {
            const card = document.getElementById('paracard-' + paraId);
            if (card) {
                card.classList.add('para-voltooid');
                if (!card.querySelector('.para-check')) {
                    const check = document.createElement('span');
                    check.className = 'para-check';
                    check.textContent = '✅';
                    card.appendChild(check);
                }
            }
        });
    }

    // === Taalknop functionaliteit ===
    const PAGE_TRANS = {
        nl: {
            subtitle: 'Lessen over verhuizen, zinnen maken en de basisgrammatica van A2.',
            t11: '1.1 Nieuwe buren', d11: 'Woordenschat rondom verhuizen en buren ontmoeten.',
            t12: '1.2 Zinnen maken', d12: 'De basisvolgorde van hoofdzinnen (S-V-R).',
            t13: '1.3 Dit is mijn familie.', d13: 'Gebruik van dit is, dat is, dit zijn, dat zijn.',
            t14: '1.4 Huiswerk maken', d14: 'Leren praten over studeren en schoolwerk.',
            t15: '1.5 Hoe gaat het?', d15: 'Vragen hoe het met iemand gaat en gepast antwoorden.',
            t16: '1.6 Er is een tuin. – Er zijn drie kamers.', d16: 'Gebruik van er is (enkelvoud) en er zijn (meervoud).',
            t17: '1.7 En, maar, want, dus, of', d17: 'Zinnen verbinden met nevenschikkende voegwoorden.',
            t18: '1.8 Marktplaats', d18: 'Kopen en verkopen van meubels en tweedehands spullen.',
            t19: '1.9 De grote kast – de kleine spiegel', d19: 'Bijvoeglijke naamwoorden met de- en het-woorden.',
            t110: '1.10 Op het station', d110: 'Treinreizen en stationsaanduidingen begrijpen.',
            t111: '1.11 Ik begrijp, hij begrijpt, wij begrijpen', d111: 'Tegenwoordige tijd van regelmatige werkwoorden.',
            t112: '1.12 Geld op je OV-chipkaart zetten', d112: 'Openbaar vervoer en in- en uitchecken.',
            t113: '1.13 Woorden met -lijk', d113: 'Uitspraak en spelling van woorden op -lijk.',
            t114: '1.14 Contact met de buren', d114: 'Korte gesprekjes en afspraken maken met buren.',
            t115: '1.15 Klein, kleiner – groot, groter', d115: 'Vergrotende trap (comparatief) in vergelijkingen.'
        },
        en: {
            subtitle: 'Lessons about moving, making sentences, and basic Dutch grammar of A2.',
            t11: '1.1 New neighbors', d11: 'Vocabulary about moving and meeting neighbors.',
            t12: '1.2 Making sentences', d12: 'Basic word order of main clauses (S-V-R).',
            t13: '1.3 This is my family.', d13: 'Usage of this is, that is, these are, those are.',
            t14: '1.4 Doing homework', d14: 'Learning to talk about studying and schoolwork.',
            t15: '1.5 How are you?', d15: 'Asking how someone is doing and responding appropriately.',
            t16: '1.6 There is a garden. – There are three rooms.', d16: 'Using er is (singular) and er zijn (plural).',
            t17: '1.7 And, but, because, so, or', d17: 'Connecting sentences with coordinating conjunctions.',
            t18: '1.8 Marketplace', d18: 'Buying and selling furniture and second-hand items.',
            t19: '1.9 The big closet – the small mirror', d19: 'Adjectives with de- and het-words.',
            t110: '1.10 At the station', d110: 'Understanding train travel and station signs.',
            t111: '1.11 I understand, he understands, we understand', d111: 'Present tense of regular verbs.',
            t112: '1.12 Topping up your OV-chipcard', d112: 'Public transport and checking in and out.',
            t113: '1.13 Words ending in -lijk', d113: 'Pronunciation and spelling of words with -lijk.',
            t114: '1.14 Contact with neighbors', d114: 'Short conversations and making appointments with neighbors.',
            t115: '1.15 Small, smaller – big, bigger', d115: 'Comparative degree in comparisons.'
        },
        ar: {
            subtitle: 'دروس حول الانتقال، وبناء الجمل، والقواعد الأساسية للمستوى A2.',
            t11: '1.1 جيران جدد', d11: 'المفردات المتعلقة بالانتقال والتعرف على الجيران.',
            t12: '1.2 تكوين الجمل', d12: 'الترتيب الأساسي للكلمات في الجمل الرئيسية (S-V-R).',
            t13: '1.3 هذه عائلتي.', d13: 'استخدام أسماء الإشارة للقريب والبعيد.',
            t14: '1.4 كتابة الواجب', d14: 'تعلم التحدث عن الدراسة والواجبات المدرسية.',
            t15: '1.5 كيف حالك؟', d15: 'السؤال عن حال شخص ما والرد المناسب.',
            t16: '1.6 هناك حديقة. – هناك ثلاث غرف.', d16: 'استخدام هناك للمفرد والجمع.',
            t17: '1.7 و، ولكن، لأن، إذن، أو', d17: 'ربط الجمل باستخدام أدوات العطف.',
            t18: '1.8 السوق (ماركت بليتس)', d18: 'شراء وبيع الأثاث والأشياء المستعملة.',
            t19: '1.9 الخزانة الكبيرة – المرآة الصغيرة', d19: 'الصفات مع الكلمات التي تأخذ de و het.',
            t110: '1.10 في المحطة', d110: 'فهم السفر بالقطار وإشارات المحطة.',
            t111: '1.11 أنا أفهم، هو يفهم، نحن نفهم', d111: 'المضارع البسيط للأفعال المنتظمة.',
            t112: '1.12 شحن بطاقة المواصلات', d112: 'المواصلات العامة وتسجيل الدخول والخروج.',
            t113: '1.13 الكلمات التي تنتهي بـ -lijk', d113: 'نطق وكتابة الكلمات التي تنتهي بـ -lijk.',
            t114: '1.14 التواصل مع الجيران', d114: 'محادثات قصيرة وتحديد مواعيد مع الجيران.',
            t115: '1.15 صغير، أصغر – كبير، أكبر', d115: 'صيغة المقارنة في المقارنات.'
        },
        tr: {
            subtitle: 'Taşınma, cümle kurma ve A2 seviyesinin temel dil bilgisi konularını içeren dersler.',
            t11: '1.1 Yeni komşular', d11: 'Taşınma ve komşularla tanışma ile ilgili kelimeler.',
            t12: '1.2 Cümle kurma', d12: 'Temel cümlelerin kelime sırası (S-V-R).',
            t13: '1.3 Bu benim ailem.', d13: 'İşaret zamirlerinin kullanımı (tekil/çoğul, yakın/uzak).',
            t14: '1.4 Ödev yapmak', d14: 'Eğitim ve okul işleri hakkında konuşmayı öğrenmek.',
            t15: '1.5 Nasıl gidiyor?', d15: 'Birinin nasıl olduğunu sorma ve uygun şekilde cevap verme.',
            t16: '1.6 Bahçe var. – Üç oda var.', d16: 'Tekil ve çoğul varlık ifadelerinin kullanımı (er is / er zijn).',
            t17: '1.7 Ve, ama, çünkü, bu yüzden, veya', d17: 'Bağlaçlarla cümleleri birbirine bağlama.',
            t18: '1.8 İkinci el pazarı', d18: 'Mobilya og ikinci el eşya alım satımı.',
            t19: '1.9 Büyük dolap – küçük ayna', d19: 'de ve het kelimeleriyle sıfat çekimi.',
            t110: '1.10 İstasyonda', d110: 'Tren yolculuğu ve istasyon tabelalarını anlama.',
            t111: '1.11 Anlıyorum, anlıyor, anlıyoruz', d111: 'Düzenli fiillerin şimdiki zaman çekimi.',
            t112: '1.12 Toplu taşıma kartına para yükleme', d112: 'Toplu taşıma ve biniş-iniş işlemleri.',
            t113: '1.13 -lijk ile biten kelimeler', d113: '-lijk ile biten kelimelerin telaffuzu ve yazımı.',
            t114: '1.14 Komşularla iletişim', d114: 'Komşularla kısa konuşmalar ve randevulaşma.',
            t115: '1.15 Küçük, daha küçük – büyük, daha büyük', d115: 'Karşılaştırma sıfatlarının kullanımı.'
        },
        dari: {
            subtitle: 'درس‌ها درباره کوچ‌کشی، جمله‌سازی و گرامر ابتدایی سطح A2 هلندی.',
            t11: '1.1 همسایه‌های جدید', d11: 'واژگان مربوط به کوچ‌کشی و آشنا شدن با همسایه‌ها.',
            t12: '1.2 جمله‌سازی', d12: 'ترتیب اصلی کلمات در جملات اصلی (S-V-R).',
            t13: '1.3 این فامیل من است.', d13: 'استفاده از ضمیرهای اشاره برای اشاره به افراد و اشیاء.',
            t14: '1.4 انجام کارهای خانگی', d14: 'آموزش صحبت کردن درباره درس و کارهای مدرسه.',
            t15: '1.5 چطور هستید؟', d15: 'پرسیدن احوال دیگران و پاسخ دادن مناسب.',
            t16: '1.6 باغچه وجود دارد. – سه اتاق وجود دارد.', d16: 'استفاده از جملات وجودی برای مفرد و جمع.',
            t17: '1.7 و، اما، چون، پس، یا', d17: 'وصل کردن جملات با حروف ربط.',
            t18: '1.8 مارکت‌پلیس', d18: 'خرید و فروش فرنیچر و وسایل دست دوم.',
            t19: '1.9 الماری بزرگ – آیینه خورد', d19: 'صفت‌ها همراه با واژه‌های de و het.',
            t110: '1.10 در ایستگاه خط آهن', d110: 'فهمیدن سفر با قطار و علائم ایستگاه.',
            t111: '1.11 من می‌فهمم، او می‌فهمد، ما می‌فهمیم', d111: 'زمان حال افعال باقاعده.',
            t112: '1.12 پول انداختن در کارت ترانسپورت', d112: 'ترانسپورت عمومی و طریقه کارت زدن در ورود و خروج.',
            t113: '1.13 واژه‌های ختم شده به -lijk', d113: 'تلفظ و املای واژه‌هایی که به -lijk ختم می‌شوند.',
            t114: '1.14 ارتباط با همسایه‌ها', d114: 'گفتگوهای کوتاه و قرار ملاقات گذاشتن با همسایه‌ها.',
            t115: '1.15 خورد، خوردتر – کلان، کلانتر', d115: 'صفت‌های مقایسه‌ای در زبان هلندی.'
        },
        thai: {
            subtitle: 'บทเรียนเกี่ยวกับการย้ายบ้าน การแต่งประโยค และไวยากรณ์พื้นฐานระดับ A2 ภาษาดัตช์',
            t11: '1.1 เพื่อนบ้านใหม่', d11: 'คำศัพท์เกี่ยวกับการย้ายบ้านและการทำความรู้จักเพื่อนบ้าน',
            t12: '1.2 การแต่งประโยค', d12: 'โครงสร้างประโยคพื้นฐานของประโยคหลัก (S-V-R)',
            t13: '1.3 นี่คือครอบครัวของฉัน', d13: 'การใช้สรรพนามชี้เฉพาะในการแนะนำคนและสิ่งของ',
            t14: '1.4 การทำการบ้าน', d14: 'เรียนรู้การพูดคุยเกี่ยวกับการเรียนและการทำการบ้าน',
            t15: '1.5 เป็นอย่างไรบ้าง?', d15: 'การถามสารทุกข์สุกดิบและการตอบอย่างเหมาะสม',
            t16: '1.6 มีสวน – มีสามห้อง', d16: 'การใช้คำแสดงการมีอยู่สำหรับเอกพจน์และพหูพจน์ (er is / er zijn)',
            t17: '1.7 และ, แต่, เพราะว่า, ดังนั้น, หรือ', d17: 'การเชื่อมประโยคด้วยคำสันธานเชื่อมประโยคหลัก',
            t18: '1.8 มาร์กต์ปลาตส์ (ตลาดซื้อขายของมือสอง)', d18: 'การซื้อขายเฟอร์นิเจอร์และของมือสอง',
            t19: '1.9 ตู้ใบใหญ่ – กระจกบานเล็ก', d19: 'การใช้คำคุณศัพท์คู่กับคำนามประเภท de และ het',
            t110: '1.10 ที่สถานีรถไฟ', d110: 'ทำความเข้าใจเกี่ยวกับการเดินทางด้วยรถไฟและป้ายบอกทางในสถานี',
            t111: '1.11 ฉันเข้าใจ, เขาเข้าใจ, พวกเราเข้าใจ', d111: 'การผันคำกริยาปกติในกาลปัจจุบัน',
            t112: '1.12 การเติมเงินในบัตรโดยสารสาธารณะ (OV-chipkaart)', d112: 'การใช้บริการขนส่งสาธารณะและการแตะบัตรเข้า-ออก',
            t113: '1.13 คำที่ลงท้ายด้วย -lijk', d113: 'การออกเสียงและการสะกดคำที่ลงท้ายด้วย -lijk',
            t114: '1.14 การติดต่อกับเพื่อนบ้าน', d114: 'บทสนทนาสั้นๆ และการนัดหมายกับเพื่อนบ้าน',
            t115: '1.15 เล็ก, เล็กกว่า – ใหญ่, ใหญ่กว่า', d115: 'การเปรียบเทียบขั้นกว่า (Comparatief)'
        }
    };

    function setPageLang(l) {
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        if (event && event.target) {
            event.target.closest('.lang-btn').classList.add('active');
        }
        document.querySelectorAll('[data-translate]').forEach(el => {
            const k = el.getAttribute('data-translate');
            if (PAGE_TRANS[l] && PAGE_TRANS[l][k]) el.textContent = PAGE_TRANS[l][k];
        });
        if (PAGE_TRANS[l] && PAGE_TRANS[l].subtitle) {
            const sub = document.querySelector('.subtitle');
            if (sub) sub.textContent = PAGE_TRANS[l].subtitle;
        }
        document.documentElement.dir = (l === 'ar' || l === 'dari') ? 'rtl' : 'ltr';
    }

    document.addEventListener('DOMContentLoaded', toonVoortgang);
  </script>

  <!-- THEME TOGGLE SCRIPT -->
  <script>
      (function() {
          const themeToggle = document.getElementById('theme-toggle');
          if (!themeToggle) return;
          themeToggle.addEventListener('click', () => {
              let theme = document.documentElement.getAttribute('data-theme') || 'light';
              let newTheme = theme === 'light' ? 'dark' : 'light';
              document.documentElement.setAttribute('data-theme', newTheme);
              localStorage.setItem('a2-theme', newTheme);
          });
      })();
  </script>

</body>
</html>
"""

# Load the lesson template from external file
TEMPLATE_PATH = os.path.join(BASE_DIR, "lesson_template_src.html")
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    LESSON_TEMPLATE = f.read()

def generate_overview_pages():
    for num, info in THEMES.items():
        filename = f"thema{num}.html"
        filepath = os.path.join(BASE_DIR, filename)
        
        para_list_html = ""
        for p_num, p_title, p_desc in info["paragraphs"]:
            if info["active"]:
                link_href = f"thema{num}-{p_num.split('.')[1]}.html"
                card_style = ""
            else:
                link_href = "#"
                card_style = ' style="pointer-events:none;opacity:0.45;"'
                
            para_list_html += f"""
      <a href="{link_href}" class="para-card animate-in" id="paracard-{p_num}"{card_style}>
        <div class="para-num">{p_num}</div>
        <div class="para-info">
          <div class="para-title" data-translate="t{p_num.replace('.', '')}">{p_title}</div>
          <div class="para-desc" data-translate="d{p_num.replace('.', '')}">{p_desc}</div>
        </div>
      </a>"""

        html = (OVERVIEW_TEMPLATE
                .replace("{num}", str(num))
                .replace("{title}", info["title"])
                .replace("{desc}", info["desc"])
                .replace("{icon}", info["icon"])
                .replace("{para_list_html}", para_list_html))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created {filename}")

def generate_lesson_pages():
    for para, info in LESSONS_DATA.items():
        filename = f"thema1-{para}.html"
        filepath = os.path.join(BASE_DIR, filename)
        
        # Build JSON string safely
        lesson_data_json = json.dumps(info, ensure_ascii=False)
        
        html = (LESSON_TEMPLATE
                .replace("{para_num}", f"1.{para}")
                .replace("{para_id}", f"1.{para}")
                .replace("{title}", info["title"])
                .replace("{intro}", info["intro"])
                .replace("{lesson_data_json}", lesson_data_json))
                
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created {filename}")

if __name__ == "__main__":
    generate_overview_pages()
    generate_lesson_pages()
