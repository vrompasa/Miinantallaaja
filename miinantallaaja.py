import miinantallaaja_GUI
import miinantallaaja_menu

import random
import time

kentta = {
    "kentta": [],
    "leveys": None,
    "korkeus": None,
    "miinoja_jaljella": None,
    "miinojen_lkm": None,
    "miinojen_koordinaatit": []
}

peli = {
    "kesto": None,
    "aika_aloitus": None,
    "aika_lopetus": None,
    "ensimmainen_ruutu": True,
    "siirtojen_maara": 0,
    "voitettu": False,
    "havitty": False,
    "paattynyt": False
}

def laske_miinat(x, y):
    """
    Laske yhden ruudun ympärillä olevat miinat ja
    palauta niiden lukumäärä.
    """
    miinoja_ymparilla = 0
    viereiset_ruudut = []
    if tarkista_koordinaatit(x, y):
        for i in range (-1,2):
            for j in range(-1,2):
                if tarkista_koordinaatit(x + j, y + i):
                    viereiset_ruudut.append((x + j, y + i))
        for x, y in viereiset_ruudut:
            if (tarkista_koordinaatit(x, y) and
                (x, y) in kentta["miinojen_koordinaatit"]):
                miinoja_ymparilla += 1
        return miinoja_ymparilla

def avaa_ruutu(x_klikkaus, y_klikkaus):
    """
    Avaa ruutu kohdasta (x, y). Mikäli ruutu on tyhjä,
    avataan kaikki ympäröivät ruudut numeroruutuihin asti.
    Jos avatussa ruudussa on miina, peli asetetaan hävityksi.
    """

    if tarkista_koordinaatit(x_klikkaus, y_klikkaus):
        if (kentta["kentta"][y_klikkaus][x_klikkaus] != "f" and
            (x_klikkaus, y_klikkaus) not in kentta["miinojen_koordinaatit"]):
            tuntematon = [(x_klikkaus, y_klikkaus)]
            while tuntematon != []:
                x, y = tuntematon[-1]
                del tuntematon[-1]
                miinoja_ymparilla = laske_miinat(x, y)
                kentta["kentta"][y][x] = str(miinoja_ymparilla)
                if miinoja_ymparilla == 0:
                    ymparoivat_ruudut = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (tarkista_koordinaatit(x + i, y + j) and
                                (x + i, y + j) != (x, y)):
                                ymparoivat_ruudut.append((x + i, y + j))
                    for (x, y) in ymparoivat_ruudut:
                        if (tarkista_koordinaatit(x, y) and
                            (x, y) not in kentta["miinojen_koordinaatit"] and
                            kentta["kentta"][y][x] == " "):
                            tuntematon.append((x, y))

        elif (kentta["kentta"][y_klikkaus][x_klikkaus] != "f" and
            (x_klikkaus, y_klikkaus) in kentta["miinojen_koordinaatit"]):
            for x, y in kentta["miinojen_koordinaatit"]:
                kentta["kentta"][y][x] = "x"
            peli["havitty"] = True
            peli["paattynyt"] = True
            peli["aika_lopetus"] = time.time()

def kello():
    """Päivitä ja muotoile peli-ikkunassa näkyvä aika."""
    if not peli["paattynyt"]:
        aika = time.localtime(time.time() - peli["aika_aloitus"])
        kello = time.strftime("%M:%S", aika)
    else:
        peli["kesto"] = time.localtime(peli["aika_lopetus"] - peli["aika_aloitus"])
        kello = time.strftime("%M:%S", peli["kesto"])
    return kello

def aseta_lippu(x, y):
    """Aseta lippu tyhjään ruutuun tai poista jo asetettu lippu."""
    if not peli["ensimmainen_ruutu"]:
        if kentta["kentta"][y][x] == " ":
            kentta["kentta"][y][x] = "f"
            kentta["miinoja_jaljella"] -= 1
            peli["siirtojen_maara"] += 1
        elif kentta["kentta"][y][x] == "f":
            kentta["kentta"][y][x] = " "
            kentta["miinoja_jaljella"] += 1
            peli["siirtojen_maara"] += 1

def tarkista_koordinaatit(x, y):
    """
    Tarkista ovatko annetut x, y -koordinaatit määritettyjen rajojen sisällä.
    Palauttaa True, jos koordinaatit ovat rajojen sisällä; muuten palautetaan False.
    """

    if (x >= kentta["leveys"] or y >= kentta["korkeus"] or
        x < 0 or y < 0 or kentta["kentta"][y][x] == "hud"):
        return False
    else:
        return True

def miinoita(x_klikkaus, y_klikkaus):
    """
    Aseta kentälle n kpl miinoja satunnaisiin koordinaatteihin.
    Miinoja ei aseteta klikkausta ympäröiviin koordinaatteihin.
    """

    vapaat_ruudut = []
    for x in range(kentta["leveys"]):
        for y in range(kentta["korkeus"]):
            vapaat_ruudut.append((x, y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if tarkista_koordinaatit(x_klikkaus + i, y_klikkaus + j):
                vapaat_ruudut.remove((x_klikkaus + i, y_klikkaus + j))
    for i in range(kentta["miinojen_lkm"]):
        x, y = random.choice(vapaat_ruudut)
        kentta["miinojen_koordinaatit"].append((x, y))
        vapaat_ruudut.remove((x, y))

def luo_kentta():
    """Luo kentta annetun leveyden ja korkeuden perusteella."""
    for i in range(kentta["korkeus"]):
        rivi = []
        for j in range(kentta["leveys"]):
            rivi.append(" ")
        kentta["kentta"].append(rivi)
    hud = []
    for i in range(kentta["leveys"]):
        hud.append("hud")
    kentta["kentta"].append(hud)

def piirra_kentta():
    """Käsittelijäfunktio grafiikkojen piirtämiselle peli-ikkunaan."""
    miinantallaaja_GUI.tyhjenna_ikkuna()
    miinantallaaja_GUI.luo_puskuri()
    for y, rivi in enumerate(kentta["kentta"]):
        for x, ruutu in enumerate(rivi):
            miinantallaaja_GUI.luo_ruutu(ruutu, x, y)
    miinantallaaja_GUI.luo_teksti("MIINOJA: {}".format(kentta["miinoja_jaljella"]),
                                  5,
                                  kentta["korkeus"] * 40 + 20,
                                  "left",
                                  "center")
    if peli["ensimmainen_ruutu"]:
        miinantallaaja_GUI.luo_teksti("AIKA: 00:00",
                                      kentta["leveys"] * 40 - 5,
                                      kentta["korkeus"] * 40 + 20,
                                      "right",
                                      "center")
    else:
        miinantallaaja_GUI.luo_teksti("AIKA: {}".format(kello()),
                                      kentta["leveys"] * 40 - 5,
                                      kentta["korkeus"] * 40 + 20,
                                      "right",
                                      "center")
    if peli["havitty"]:
        miinantallaaja_GUI.luo_teksti("HÄVISIT PELIN!",
                                      kentta["leveys"] * 20,
                                      kentta["korkeus"] * 20 + 40,
                                      "center", "center",
                                      (255,255,255,255),
                                      26)
    if peli["voitettu"]:
        miinantallaaja_GUI.luo_teksti("VOITIT PELIN!",
                                      kentta["leveys"] * 20,
                                      kentta["korkeus"] * 20 + 40,
                                      "center",
                                      "center",
                                      (255,255,255,255),
                                      26)
    if peli["paattynyt"]:
        miinantallaaja_GUI.luo_teksti("KLIKKAA PALATAKSESI PÄÄVALIKKOON",
                                      kentta["leveys"] * 20,
                                      kentta["korkeus"] * 20,
                                      "center",
                                      "center",
                                      (255,255,255,255),
                                      14)
    miinantallaaja_GUI.piirra()

def hiiren_klikkaus(x, y, painike, muokkausnappain):
    """
    Käsittelijäfunktio hiiren klikkaamiselle.

    Jos painetaan hiiren vasenta painiketta, kutsutaan avaa_ruutu-funktiota ja
    tarkistetaan onko peli voitettu. Enismmäisellä klikkauksella kutsutaan
    lisäksi miinoita-funktiota ja määritellään pelin aloitusajankohta.
    Hiiren oikeata painiketta painettaessa kutsutaan aseta_lippu-funktiota.
    Mikäli peli on päättynyt, peli-ikkuna suljetaan hiiren vasenta painiketta painamalla.
    """

    x = int(x / 40)
    y = int(y / 40)

    if not peli["paattynyt"]:
        if (painike == miinantallaaja_GUI.HIIRI_VASEN and
            kentta["kentta"][y][x] == " "):
            if peli["ensimmainen_ruutu"] and kentta["kentta"][y][x] == " ":
                miinoita(x, y)
                peli["aika_aloitus"] = time.time()
                peli["ensimmainen_ruutu"] = False
            peli["siirtojen_maara"] += 1
            avaa_ruutu(x, y)
            if not peli["havitty"]:
                tarkista_voitto()
        elif painike == miinantallaaja_GUI.HIIRI_OIKEA:
            aseta_lippu(x, y)
    elif peli["paattynyt"]:
        tallenna_tilastot()
        if painike == miinantallaaja_GUI.HIIRI_VASEN:
            miinantallaaja_GUI.sulje()

def tarkista_voitto():
    """Tarkistaa ovatko kaikki miinattomat ruudut avattu."""
    avaamattomat_ruudut = 0
    for rivi in kentta["kentta"]:
        avaamattomat_ruudut += rivi.count(" ")
    if avaamattomat_ruudut <= kentta["miinoja_jaljella"]:
        peli["voitettu"] = True
        peli["paattynyt"] = True
        peli["aika_lopetus"] = time.time()

def tallenna_tilastot():
    pvm = time.strftime("%d.%m.%Y %H:%M", time.localtime(peli["aika_lopetus"]))
    kesto = time.strftime("%M:%S", peli["kesto"])
    siirrot = str(peli["siirtojen_maara"])
    if peli["voitettu"]:
        lopputulos = "Voitto"
    elif peli["havitty"]:
        lopputulos = "Häviö"
    kentan_koko = "{} x {}".format(kentta["leveys"], kentta["korkeus"])
    miinojen_lkm = str(kentta["miinojen_lkm"])

    try:
        with open("tilastot.csv", "a") as f:
            f.write("{},{},{},{},{},{}\n".format(pvm, kesto,
                                                 siirrot, lopputulos,
                                                 kentan_koko, miinojen_lkm))
    except IOError:
        print("\nTallentaminen epäonnistui")

def alusta():
    """Asettaa pelin parametrit oletusarvoihin."""
    kentta["kentta"] = []
    kentta["leveys"] = None
    kentta["korkeus"] = None
    kentta["koordinaatit"] = []
    kentta["miinojen_koordinaatit"] = []
    kentta["miinojen_lkm"] = 0
    kentta["miinoja_jaljella"] = None
    peli["kesto"] = None
    peli["aika_aloitus"] = None
    peli["aika_lopetus"] = None
    peli["ensimmainen_ruutu"] = True
    peli["siirtojen_maara"] = 0
    peli["voitettu"] = False
    peli["havitty"] = False
    peli["paattynyt"] = False

def main():
    while True:
        (kentta["leveys"],
         kentta["korkeus"],
         kentta["miinojen_lkm"]) = miinantallaaja_menu.paavalikko()
        kentta["miinoja_jaljella"] = kentta["miinojen_lkm"]
        leveys_pikseleina = kentta["leveys"] * 40
        korkeus_pikseleina = kentta["korkeus"] * 40
        luo_kentta()
        miinantallaaja_GUI.lataa_kuvat("spritet")
        miinantallaaja_GUI.luo_ikkuna(leveys_pikseleina, korkeus_pikseleina + 40)
        miinantallaaja_GUI.maarita_piirto(piirra_kentta)
        miinantallaaja_GUI.maarita_hiiri(hiiren_klikkaus)
        miinantallaaja_GUI.kaynnista()
        alusta()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOhjelma lopetettu\n") 
