import pyglet

HIIRI_VASEN = pyglet.window.mouse.LEFT
HIIRI_OIKEA = pyglet.window.mouse.RIGHT
RYHMA_KENTTA = pyglet.graphics.OrderedGroup(0)
RYHMA_TEKSTI = pyglet.graphics.OrderedGroup(1)

resurssit = {
    "ikkuna": None,
    "kuvat": {},
    "spritet": [],
    "puskuri": None,
    "teksti": []
}

def luo_ikkuna(leveys, korkeus):
    """
    Luo peli-ikkuna annetun leveyden ja korkeuden mukaan.
    Aseta ikkunan otsikoksi "Miinantallaaja". Aseta peli-ikkuna
    päivittymään joka 0.2 sekuntti.
    """
    resurssit["ikkuna"] = pyglet.window.Window(leveys, korkeus, vsync=False,
                                               caption="Miinantallaaja")
    #pyglet.clock.schedule_interval(paivita_ikkuna, .2)
    #Peli-ikkuna lakkaa vastaamasta hiiren klikkauksiin suurella kentällä, mikäli
    #ruutua päivitetään säännöllisesti.

def luo_puskuri():
    """Luo puskuri, jonka avulla peli-ikkunan grafiikat piirretään."""
    resurssit["puskuri"] = pyglet.graphics.Batch()

def lataa_kuvat(polku):
    """Lataa peli-ikkunassa käytettävät grafiikat annetusta polusta"""
    pyglet.resource.path = [polku]
    kuvat = {}
    for i in range(9):
        kuvat[str(i)] = pyglet.resource.image("{}.png".format(str(i)))
    kuvat["x"] = pyglet.resource.image("miina.png")
    kuvat["f"] = pyglet.resource.image("lippu.png")
    kuvat[" "] = pyglet.resource.image("avaamaton.png")
    kuvat["hud"] = pyglet.resource.image("hud.png")
    resurssit["kuvat"] = kuvat

def maarita_hiiri(hiiren_klikkaus):
    """Määritä käsittelijäfunktio, jota kutsutaan aina hiirtä klikatessa"""
    resurssit["ikkuna"].on_mouse_press = hiiren_klikkaus

def maarita_piirto(piirra_kentta):
    """
    Määritä käsittelijäfunktio, jota kutsutaan aina,
    kun peli-ikkuna päivitetään.
    """
    resurssit["ikkuna"].on_draw = piirra_kentta

def luo_ruutu(ruutu, x, y):
    """Luo puskuriin lisättävä ruutu kohtaan (x, y)"""
    resurssit["spritet"].append(pyglet.sprite.Sprite(resurssit["kuvat"][str(ruutu)],
                                                     x,
                                                     y,
                                                     batch=resurssit["puskuri"],
                                                     group=RYHMA_KENTTA))

def luo_teksti(teksti, x, y, anchor_x, anchor_y, vari=(0,0,0,255), koko=14):
    """
    Luo puskuriin lisättävä teksti kohtaan (x, y).

    teksti -- piirrettävä teksti
    x -- tekstin ankkurin x-koordinaatti
    y -- tekstin ankkurin y-koordinaatti
    anchor_x -- tekstin x-ankkurin sijainti
    anchor_y -- tekstin y-ankkurin sijainti
    vari -- tekstin väri RGBA-arvona (default (0,0,0,255))
    koko -- tekstin fonttikoko (default 14)
    """

    pyglet.font.add_file("VCR_OSD_MONO.ttf")
    resurssit["teksti"].append(pyglet.text.Label(teksti,
                                                 font_name="VCR OSD MONO",
                                                 font_size=koko,
                                                 x=x, y=y,
                                                 anchor_x=anchor_x, anchor_y=anchor_y,
                                                 color=vari,
                                                 batch=resurssit["puskuri"],
                                                 group=RYHMA_TEKSTI))

def piirra():
    """Piirrä puskurin sisältö peli-ikkunaan"""
    resurssit["puskuri"].draw()
    resurssit["spritet"].clear()
    resurssit["teksti"].clear()

def paivita_ikkuna(dt):
    """Käytetään ikkunan piirron ajastamiseen"""

def tyhjenna_ikkuna():
    """Tyhjennä peli-ikkunan sisältö"""
    resurssit["ikkuna"].clear()

def sulje():
    """Sulje peli-ikkuna"""
    resurssit["ikkuna"].close()
    pyglet.app.exit()

def kaynnista():
    """Avaa peli-ikkuna"""
    pyglet.app.run()
