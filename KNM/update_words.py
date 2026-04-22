import re

data = {
    "Afsluitdijk": ("32 km lange dam tussen Noord-Holland en Friesland.", "Afsluitdijk", "32-kilometrowa tama między Holandią P. a Fryzją."),
    "Bevolking": ("Alle mensen die in een land wonen.", "Populacja", "Wszyscy ludzie mieszkający w danym kraju."),
    "Bevrijden": ("Iemand of iets vrijmaken.", "Wyzwolić", "Uczynić kogoś lub coś wolnym."),
    "Bezetten": ("De macht overnemen in een ander land.", "Okupować", "Przejęcie władzy w innym kraju."),
    "Christelijk": ("Geloven in God, Jezus en de Bijbel.", "Chrześcijański", "Wiara w Boga, Jezusa i Biblię."),
    "Concentratiekamp": ("Gevangenis en vernietigingskamp van de nazi's.", "Obóz koncentracyjny", "Nazistowskie więzienie i miejsce zagłady."),
    "Dagboek": ("Boek om gedachten en acties in op te schrijven.", "Pamiętnik / Dziennik", "Książka do zapisywania przemyśleń i działań."),
    "Deltawerken": ("Grote dammen en waterkeringen in Zeeland en Zuid-Holland.", "Plan Delta", "Tamy i bariery w Zelandii i Holandii Południowej."),
    "Democratie": ("Systeem waarbij mensen hun leiders kiezen.", "Demokracja", "System, w którym ludzie wybierają swoich przywódców."),
    "Dichtbevolkt": ("Veel mensen in een kleine ruimte.", "Gęsto zaludniony", "Wiele osób na małej przestrzeni."),
    "Dijk": ("Muur die het water tegenhoudt.", "Wał przeciwpowodziowy / Tama", "Ściana zatrzymująca wodę."),
    "Duin": ("Zandheuvel langs de kust.", "Wydma", "Piaszczyste wzgórze wzdłuż wybrzeża."),
    "Emancipatie": ("Gelijke rechten krijgen.", "Emancypacja", "Uzyskanie równych praw."),
    "EU (Europese Unie)": ("Samenwerking tussen Europese landen.", "UE (Unia Europejska)", "Współpraca między krajami europejskimi."),
    "Gastarbeider": ("Mensen die in de jaren 60 en 70 kwamen werken.", "Gastarbeiter", "Osoby przybyłe do pracy w latach 60. i 70."),
    "Geallieerden": ("Landen die tegen Duitsland vochten in WOII.", "Alianci", "Kraje walczące z Niemcami w II wojnie światowej."),
    "Gelijkheid": ("Iedereen is even belangrijk en heeft dezelfde rechten.", "Równość", "Wszyscy są równie ważni i mają równe prawa."),
    "Godsdienst": ("Een geloof (bijv. Islam, Christendom).", "Religia", "Wiara (np. islam, chrześcijaństwo)."),
    "Gouden Eeuw": ("Periode van grote welvaart (1600-1700).", "Złoty Wiek", "Okres wielkiego bogactwa (1600-1700)."),
    "Gracht": ("Vaarweg of waterweg in de stad.", "Kanał", "Droga wodna w mieście."),
    "Grondwet": ("De belangrijkste wet van een land.", "Konstytucja", "Najważniejsze prawo kraju."),
    "Handel": ("Kopen en verkopen van goederen.", "Handel", "Kupowanie i sprzedawanie towarów."),
    "Hongerwinter": ("Laatste winter van WOII met veel honger in Nederland.", "Zima głodowa", "Ostatnia zima II wojny światowej z wielkim głodem."),
    "Jood / Joden": ("Persoon behorend tot het Joodse volk of geloof.", "Żyd / Żydzi", "Osoba wyznania żydowskiego / naród żydowski."),
    "Katholiek": ("Christen die de Paus volgt.", "Katolik", "Chrześcijanin podążający za papieżem."),
    "Kolonie": ("Gebied dat bestuurd wordt door een ander land overzee.", "Kolonia", "Obszar kontrolowany przez inny kraj."),
    "Landbouw": ("Het werk van boeren met het verbouwen van gewassen.", "Rolnictwo", "Praca rolników (uprawa roślin)."),
    "Macht": ("In staat zijn om anderen te vertellen wat ze moeten doen.", "Władza", "Zdolność mówienia innym, co mają robić."),
    "Minister": ("Lid van de regering.", "Minister", "Członek rządu."),
    "Onafhankelijk": ("Voor jezelf beslissen, niet onder controle van anderen.", "Niezależny", "Decydowanie za siebie, brak szefa."),
    "Onderduiken": ("Zich in het geheim verstoppen in oorlogstijd.", "Ukrywać się", "Ukrywanie się w tajnym miejscu."),
    "Opstand": ("Protest tegen de leiders.", "Powstanie / Bunt", "Protest przeciwko przywódcom."),
    "Organisatie": ("Een groep die samenwerkt om iets te regelen.", "Organizacja", "Grupa wspólnie organizująca rzeczy."),
    "Overstroming": ("Water dat het land bedekt.", "Powódź", "Woda pokrywająca ląd."),
    "Parlement": ("Groep die wetten maakt en de regering controleert.", "Parlament", "Grupa tworząca prawa i kontrolująca rząd."),
    "Polder": ("Een stuk land dat is drooggemaakt.", "Polder", "Osuszony ląd (wcześniej była to woda)."),
    "Politiek": ("Hoe we beslissingen nemen over het land.", "Polityka", "Sposób decydowania o kraju."),
    "Protestant": ("Christen die de Paus niet volgt.", "Protestant", "Chrześcijanin nie podążający za papieżem."),
    "Randstad": ("Stedelijk gebied (Amsterdam, Rotterdam, Den Haag, Utrecht).", "Randstad", "Obszar miejski z Amsterdamem, Rotterdamem, Hagą i Utrechtem."),
    "Recht / Rechten": ("Dingen die je volgens de wet mag.", "Prawo / Prawa", "Rzeczy, które możesz robić zgodnie z prawem."),
    "Republiek": ("Land zonder koning, mensen kiezen een leider.", "Republika", "Kraj bez króla, ludzie wybierają przywódcę."),
    "Schip": ("Grote boot.", "Statek", "Duża łódź."),
    "Slachtoffer": ("Iemand die is gedood of gewond.", "Ofiara", "Ktoś zabity lub ranny."),
    "Slaaf / Slavernij": ("Niet vrij zijn, werken zonder betaling.", "Niewolnik / Niewolnictwo", "Brak wolności, praca bez zapłaty."),
    "Stemmen": ("Officieel kiezen in verkiezingen.", "Głosowanie", "Oficjalne wybieranie w wyborach."),
    "Veeteelt": ("Het werk van boeren met dieren.", "Hodowla zwierząt", "Rolnictwo ze zwierzętami."),
    "Vervoeren": ("Dingen verplaatsen van A naar B.", "Transportować", "Transportowanie rzeczy z punktu A do punktu B."),
    "Vluchteling": ("Iemand die vlucht voor gevaar in het eigen land.", "Uchodźca", "Osoba uciekająca przed niebezpieczeństwem we własnym kraju."),
    "VN (Verenigde Naties)": ("Wereldwijde organisatie van landen.", "ONZ (Organizacja N. Zjednoczonych)", "Światowa organizacja krajów."),
    "V.O.C.": ("Grote Nederlandse handelscompagnie (Gouden Eeuw).", "Holenderska Kompania Wschodnioindyjska", "Duża firma handlowa z czasów Złotego Wieku."),
    "Watersnoodramp": ("Grote overstroming in 1953.", "Wielka Powódź z 1953", "Potężna powódź w Holandii w 1953 roku.")
}

import sys

file_path = r'h:\Mijn Drive\HTML FILES\KNM\woordenlijst-knm.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

def replacer(match):
    full_str = match.group(0)
    word_nl = match.group(1)
    
    if word_nl in data:
        nlX, pl, plX = data[word_nl]
        left_pad = 27 - len(pl)
        if left_pad < 1: left_pad = 1
        return f'{{nl:"{word_nl}",\n   nlX:"{nlX}",\n   pl:"{pl}",{" "*left_pad}plX:"{plX}",'
    return full_str

new_text = re.sub(r'\{nl:"([^"]+)",', replacer, text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Words updated")
