import miinantallaaja
import sys

vaikeustaso = {
    "helppo": (9, 9, 10),
    "normaali": (16, 16, 40),
    "vaikea": (30, 16, 99)
}

def kysy_vaikeustaso():
    print("\nValitse vaikeustaso:\n")
    print("(H)elppo")
    print("(N)ormaali")
    print("(V)aikea")
    print("\n(M)ukautettu\n")
    while True:
        syote = input("Valitse syöttämällä suluissa annettu kirjain: ").lower()
        if syote == "h":
            return vaikeustaso["helppo"]
        elif syote == "n":
            return vaikeustaso["normaali"]
        elif syote == "v":
            return vaikeustaso["vaikea"]
        elif syote == "m":
            leveys, korkeus, miinojen_lkm = kysy_arvot()
            return leveys, korkeus, miinojen_lkm
        else:
            print("Täysin kelvoton syöte\n")
            continue

def kysy_arvot():
    while True:
        try:
            leveys = int(input("\nAnna kentän leveys väliltä 8-36: "))
            if leveys < 8 or leveys > 36:
                print("\nSyötetyn arvon täytyy olla välillä 8-36")
                continue
        except ValueError:
            print("\nSyötetyn arvon täytyy olla luku välillä 8-36")
        else:
            break
    while True:
        try:
            korkeus = int(input("\nAnna kentän korkeus väliltä 3-20: "))
            if korkeus < 3 or korkeus > 20:
                print("\nSyötetyn arvon täytyy olla välillä 3-20")
                continue
        except ValueError:
            print("\nSyötetyn arvon täytyy olla luku väliltä 3-20")
        else:
            break
    while True:
        try:
            miinojen_lkm = int(input("\nAnna miinojen lukumäärä väliltä 1-{}: ".format(leveys * korkeus - 10)))
            if miinojen_lkm < 1:
                print("\nAnna kokonaisluku väliltä 1-{}".format(leveys * korkeus - 10))
                continue
            if miinojen_lkm > leveys * korkeus - 10:
                print("\nLiikaa miinoja!")
                continue
        except ValueError:
            print("\nAnna kokonaisluku väliltä 1-{}".format(leveys * korkeus - 10))
        else:
            return leveys, korkeus, miinojen_lkm

def lataa_tilastot():
    data = []
    try:
        with open("tilastot.csv") as f:
            for rivi in f.readlines():
                data.append(rivi.strip("\n"))
    except IOError:
        print("\nTilastot sisältävän tiedoston avaaminen epäonnistui")
    return data

def nayta_tilastot(data):
    for rivi in data:
        pmv, kesto, siirrot, lopputulos, kentta, miinat = rivi.split(",")
        print("––––––––––––––––––––––––––––––––––––––––––––––")
        print("{}        {}".format(pmv, lopputulos))
        print("Kesto: {}          Siirtoja: {}".format(kesto, siirrot))
        print("Kentta: {}        Miinojen määrä: {}".format(kentta, miinat))

def paavalikko():
    while True:
        print("\nTervetuloa pelaamaan miinantallaajaa!")
        while True:
            print("\n(P)elaa")
            print("(T)ilastot")
            print("(S)ulje")
            syote = input("\nValitse syöttämällä suluissa annettu kirjain: ").lower()
            if syote == "p":
                miinantallaaja.kentta["leveys"], miinantallaaja.kentta["korkeus"], miinantallaaja.kentta["miinojen_lkm"] = kysy_vaikeustaso()
                miinantallaaja.main()
                miinantallaaja.alusta()
                break
            elif syote == "t":
                data = lataa_tilastot()
                nayta_tilastot(data)
            elif syote == "s":
                sys.exit(0)
            else:
                print("\nSyötä suluissa annettu kirjain")
                continue
