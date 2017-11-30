import pyglet

HIIRI_VASEN = pyglet.window.mouse.LEFT
HIIRI_OIKEA = pyglet.window.mouse.RIGHT

resurssit = {
    "ikkuna": None,
    "kuvat": {},
    "spritet": [],
    "puskuri": None,
    "teksti": None
}

ryhma_kentta = pyglet.graphics.OrderedGroup(0)
ryhma_teksti = pyglet.graphics.OrderedGroup(1)

def luo_ikkuna(leveys, korkeus):
    resurssit["ikkuna"] = pyglet.window.Window(leveys, korkeus)
    resurssit["ikkuna"].set_caption("Miinantallaaja")

def luo_puskuri():
    resurssit["puskuri"] = pyglet.graphics.Batch()

def lataa_kuvat(polku):
    pyglet.resource.path = [polku]
    kuvat = {}
    kuvat["0"] = pyglet.resource.image("tyhja.png")
    for i in range(1, 9):
        kuvat[str(i)] = pyglet.resource.image("{}.png".format(str(i)))
    kuvat["x"] = pyglet.resource.image("miina.png")
    kuvat["f"] = pyglet.resource.image("lippu.png")
    kuvat[" "] = pyglet.resource.image("avaamaton.png")
    kuvat["hud"] = pyglet.resource.image("hud.png")
    resurssit["kuvat"] = kuvat

def maarita_hiiri(hiiren_klikkaus):
    resurssit["ikkuna"].on_mouse_press = hiiren_klikkaus

def maarita_piirto(piirra_kentta):
    resurssit["ikkuna"].on_draw = piirra_kentta
    pyglet.clock.schedule_interval(paivita_ikkuna, 0.1)

def lisaa_puskuriin(avain, x, y):
    resurssit["spritet"].append(pyglet.sprite.Sprite(resurssit["kuvat"][str(avain)], x, y, batch=resurssit["puskuri"], group=ryhma_kentta))

def piirra():
    resurssit["puskuri"].draw()
    resurssit["spritet"].clear()

def luo_teksti(teksti, leveys, korkeus, anchor_x, anchor_y, color=(0,0,0,255), koko=14):
    pyglet.font.add_file("VCR_OSD_MONO.ttf")
    resurssit["teksti"] = pyglet.text.Label(teksti,
                                            font_name="VCR OSD MONO",
                                            font_size=koko,
                                            x=leveys, y=korkeus,
                                            anchor_x=anchor_x, anchor_y=anchor_y,
                                            color=color,
                                            group=ryhma_teksti)
    resurssit["teksti"].draw()

def paivita_ikkuna(dt):
    resurssit["ikkuna"].clear()
    resurssit["teksti"].draw()

def tyhjenna_ikkuna():
    resurssit["ikkuna"].clear()

def sulje():
    resurssit["ikkuna"].close()
    pyglet.app.exit()

def kaynnista():
    pyglet.app.run()
