import miinantallaaja_UI
import random
import time

vaikeustaso = {
    "helppo": (9, 9, 10),
    "normaali": (16, 16, 40),
    "vaikea": (30, 16, 99)
}

peli = {
    "kesto": None,
    "aika_aloitus": None,
    "aika_lopetus": None,
    "ensimmainen_ruutu": True,
    "voitettu": False,
    "havitty": False,
    "paattynyt": False
}

def laske_miinat(x, y):
    """
    Laskee annetussa kentässa yhden ruudun ympärillä olevat miinat ja palauttaa niiden lukumäärän.
    """

    miinoja_ymparilla = 0
    viereiset_ruudut = []
    if tarkista_koordinaatit(x, y):
        for i in range (-1,2):
            for j in range(-1,2):
                if tarkista_koordinaatit(x + j, y + i):
                    viereiset_ruudut.append((x + j, y + i))
        for x, y in viereiset_ruudut:
            if tarkista_koordinaatit(x, y) and (x, y) in miinojen_koordinaatit:
                    miinoja_ymparilla += 1
        return miinoja_ymparilla

def avaa_ruutu(x_klikkaus, y_klikkaus):
    """
    Avaa ruudun kohdasta (x, y). Mikäli ruutu on tyhjä, avataan kaikki ympäröivät ruudut numeroruutuihin asti.
    Jos avatussa ruudussa on miina, peli asetetaan hävityksi.
    """

    if tarkista_koordinaatit(x_klikkaus, y_klikkaus):
        if kentta[y_klikkaus][x_klikkaus] != "f" and (x_klikkaus, y_klikkaus) not in miinojen_koordinaatit:
            tuntematon = [(x_klikkaus, y_klikkaus)]
            while tuntematon != []:
                x, y = tuntematon[-1]
                del tuntematon[-1]
                miinoja_ymparilla = laske_miinat(x, y)
                kentta[y][x] = str(miinoja_ymparilla)
                if miinoja_ymparilla == 0:
                    ymparoivat_ruudut = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if tarkista_koordinaatit(x + i, y + j) and (x + i, y + j) != (x, y):
                                ymparoivat_ruudut.append((x + i, y + j))
                    for (x, y) in ymparoivat_ruudut:
                        if tarkista_koordinaatit(x, y) and (x, y) not in miinojen_koordinaatit and kentta[y][x] == " ":
                            tuntematon.append((x, y))

        elif kentta[y_klikkaus][x_klikkaus] != "f" and (x_klikkaus, y_klikkaus) in miinojen_koordinaatit:
            for x, y in miinojen_koordinaatit:
                kentta[y][x] = "x"
            peli["havitty"] = True
            peli["paattynyt"] = True
            peli["aika_lopetus"] = time.time()

def kello():
    if not peli["paattynyt"]:
        aika = time.localtime(time.time() - peli["aika_aloitus"])
        kello = time.strftime("%M:%S", aika)
    else:
        peli["kesto"] = time.localtime(peli["aika_lopetus"] - peli["aika_aloitus"])
        kello = time.strftime("%M:%S", peli["kesto"])
    return kello

def aseta_lippu(x, y):
    """
    Asettaa lipun tyhjään ruutuun tai poistaa jo asetetun lipun.
    """

    global miinoja_jaljella

    if not peli["ensimmainen_ruutu"]:
        if kentta[y][x] == " ":
            kentta[y][x] = "f"
            miinoja_jaljella -= 1
        elif kentta[y][x] == "f":
            kentta[y][x] = " "
            miinoja_jaljella += 1

def avaa_kaikki():
    """
    Avaa kaikki kentällä olevat ruudut ja asettaa pelin päättyneeksi.
    """

    tuntematon = []
    for x in range(len(kentta[0])):
        for y in range(len(kentta) - 1):
            tuntematon.append((x, y))
    while tuntematon != []:
        x, y = tuntematon[-1]
        del tuntematon[-1]
        if (x, y) in miinojen_koordinaatit and kentta[y][x] != "f":
            kentta[y][x] = "x"
            peli["havitty"] = True
        elif kentta[y][x] != "f":
            miinoja_ymparilla = laske_miinat(x, y)
            kentta[y][x] = str(miinoja_ymparilla)
    peli["paattynyt"] = True

def tarkista_koordinaatit(x, y):
    """
    Tarkistaa ovatko annetut x, y -koordinaatit annettujen rajojen sisällä.
    Palauttaa True, jos koordinaatit ovat rajojen sisällä; muuten palautetaan False.
    """

    if x >= leveys or y >= korkeus or x < 0 or y < 0 or kentta[y][x] == "hud":
        return False
    else:
        return True

def miinoita(x_klikkaus, y_klikkaus):
    """
    Asettaa kentälle n kpl miinoja satunnaisiin koordinaatteihin.
    Miinoja ei aseteta klikkausta ympäröiviin ruutuihin.
    """

    vapaat_ruudut = []
    for x in range(len(kentta[0])):
        for y in range(len(kentta) - 1):
            vapaat_ruudut.append((x, y))

    for i in range(-1, 2):
        for j in range(-1, 2):
            if tarkista_koordinaatit(x_klikkaus + i, y_klikkaus + j):
                vapaat_ruudut.remove((x_klikkaus + i, y_klikkaus + j))

    for i in range(miinojen_lkm):
        x, y = random.choice(vapaat_ruudut)
        miinojen_koordinaatit.append((x, y))
        vapaat_ruudut.remove((x, y))

def luo_kentta():
    kentta = []
    for i in range(korkeus):
        rivi = []
        for j in range(leveys):
            rivi.append(" ")
        kentta.append(rivi)
    hud = []
    for i in range(leveys):
        hud.append("hud")
    kentta.append(hud)
    return kentta

def kysy_arvot():
    while True:
        try:
            leveys = int(input("Anna kentän leveys: "))
            if leveys <= 0:
                print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
                continue
        except ValueError:
            print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
        else:
            break
    while True:
        try:
            korkeus = int(input("Anna kentän korkeus: "))
            if korkeus <= 0:
                print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
                continue
        except ValueError:
            print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
        else:
            break
    while True:
        try:
            miinojen_lkm = int(input("Anna miinojen lukumäärä: "))
            if miinojen_lkm <= 0:
                print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
                continue
            if miinojen_lkm >= leveys * korkeus:
                print("Noin monta miinaa ei mahdu valitsemallesi kentälle")
                continue
        except ValueError:
            print("Syötetyn arvon täytyy olla positiivinen kokonaisluku")
        else:
            return leveys, korkeus, miinojen_lkm

def kysy_vaikeustaso():
    print("Valitse vaikeustaso:")
    print("(H)elppo")
    print("(N)ormaali")
    print("(V)aikea")
    while True:
        syote = input().lower()
        if syote == "h":
            return vaikeustaso["helppo"]
        elif syote == "n":
            return vaikeustaso["normaali"]
        elif syote == "v":
            return vaikeustaso["vaikea"]
        else:
            print("Täysin kelvoton syöte")
            continue

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """

    miinantallaaja_UI.tyhjenna_ikkuna()
    for y, rivi in enumerate(kentta):
        for x, avain in enumerate(rivi):
            miinantallaaja_UI.lisaa_puskuriin(avain, x * 40, y * 40)
    miinantallaaja_UI.piirra()
    miinantallaaja_UI.luo_teksti("MIINOJA: {}".format(miinoja_jaljella), 5, korkeus * 40 + 20, "left", "center")
    if peli["ensimmainen_ruutu"]:
        miinantallaaja_UI.luo_teksti("AIKA: 00:00", leveys * 40 - 5, korkeus * 40 + 20, "right", "center")
    else:
        miinantallaaja_UI.luo_teksti("AIKA: {}".format(kello()), leveys * 40 - 5, korkeus * 40 + 20, "right", "center")
    if peli["havitty"]:
        miinantallaaja_UI.luo_teksti("HÄVISIT PELIN!", leveys * 20, korkeus * 20 + 40, "center", "center", (255,0,0,255), 20)
    if peli["voitettu"]:
        miinantallaaja_UI.luo_teksti("OLET VOITTAJA!", leveys * 20, korkeus * 20 + 40, "center", "center", (0,255,0,255), 20)

def hiiri_liike(x, y, dx, dy):
    """
    Kutsutaan hiiren liikkuessa ikkunan sisällä.
    """

    x = int(x / 40)
    y = int(y / 40)

    #print("Hiiren koordinaatit: ", x, y)

def hiiren_klikkaus(x, y, painike, muokkausnappain):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
    """

    x = int(x / 40)
    y = int(y / 40)

    if not peli["paattynyt"]:
        if painike == miinantallaaja_UI.HIIRI_VASEN:
            if peli["ensimmainen_ruutu"] and kentta[y][x] == " ":
                miinoita(x, y)
                peli["aika_aloitus"] = time.time()
                peli["ensimmainen_ruutu"] = False
            avaa_ruutu(x, y)

        elif painike == miinantallaaja_UI.HIIRI_OIKEA:
            aseta_lippu(x, y)

    elif peli["paattynyt"]:
        if painike == miinantallaaja_UI.HIIRI_VASEN:
            miinantallaaja_UI.sulje()

def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirto- ja hiirikäsittelijät.
    """

    leveys_pikseleina = leveys * 40
    korkeus_pikseleina = korkeus * 40

    miinantallaaja_UI.lataa_kuvat("spritet")
    miinantallaaja_UI.luo_ikkuna(leveys_pikseleina, korkeus_pikseleina + 40)
    miinantallaaja_UI.maarita_piirto(piirra_kentta)
    miinantallaaja_UI.maarita_hiiri(hiiren_klikkaus, hiiri_liike)
    miinantallaaja_UI.kaynnista()

if __name__ == "__main__":
    leveys, korkeus, miinojen_lkm = kysy_vaikeustaso()
    kentta = luo_kentta()
    miinoja_jaljella = miinojen_lkm
    miinojen_koordinaatit = []
    main()
