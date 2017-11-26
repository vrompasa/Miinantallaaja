import pyglet
import time

HIIRI_VASEN = pyglet.window.mouse.LEFT
HIIRI_KESKI = pyglet.window.mouse.MIDDLE
HIIRI_OIKEA = pyglet.window.mouse.RIGHT

resurssit = {
    "ikkuna": None,
    "kuvat": {},
    "spritet": [],
    "puskuri": pyglet.graphics.Batch(),
    "teksti": None
}

def luo_ikkuna(leveys, korkeus):
    resurssit["ikkuna"] = pyglet.window.Window(leveys, korkeus)

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

def maarita_hiiri(hiiren_klikkaus, hiiri_liike):
    resurssit["ikkuna"].on_mouse_press = hiiren_klikkaus
    resurssit["ikkuna"].on_mouse_motion = hiiri_liike

def maarita_piirto(kasittelija):
    resurssit["ikkuna"].on_draw = kasittelija

def lisaa_puskuriin(avain, x, y):
    resurssit["spritet"].append(pyglet.sprite.Sprite(resurssit["kuvat"][str(avain)], x, y, batch=resurssit["puskuri"]))

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
                                            color=color)
    resurssit["teksti"].draw()

def paivita_ikkuna(dt):
    resurssit["ikkuna"].on_draw()

def tyhjenna_ikkuna():
    resurssit["ikkuna"].clear()

def sulje():
    pyglet.app.exit()

def kaynnista():
    pyglet.clock.schedule_interval(paivita_ikkuna, .1)
    pyglet.app.run()
