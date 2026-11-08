import machine
from pins import Pins
import time

# Mise en place
rgb_vert = machine.Pin(Pins.D2, machine.Pin.OUT)
rgb_rouge = machine.Pin(Pins.D3, machine.Pin.OUT)
rgb_blue = machine.Pin(Pins.D4, machine.Pin.OUT)

btn_A = machine.Pin(Pins.D11, machine.Pin.IN, machine.Pin.PULL_DOWN)

def millis():
    return time.ticks_ms()

# LED RGB éteinte au départ (1 = éteint)
rgb_vert.value(1)
rgb_rouge.value(1)
rgb_blue.value(1)

def allume_couleur_rgb(couleur):
    # On éteint tout, puis on allume la bonne couleur (0 = allumé)
    rgb_rouge.value(1)
    rgb_vert.value(1)
    rgb_blue.value(1)
    if couleur == "bleu":
        rgb_blue.value(0)
    elif couleur == "rouge":
        rgb_rouge.value(0)
    elif couleur == "vert":
        rgb_vert.value(0)

def eteint_rgb():
    rgb_rouge.value(1)
    rgb_vert.value(1)
    rgb_blue.value(1)

tableau_couleur = ["bleu", "rouge", "vert"]
compteur_rgb = 0
allumee = False

attente = False      # True = 1er clic reçu, on attend un 2e
t_premier = 0        # moment du 1er clic
t_double = -1000     # moment du dernier double clic
t_appui = 0          # pour l'anti-rebond
prev_A = btn_A.value()

def afficher():
    if allumee:
        allume_couleur_rgb(tableau_couleur[compteur_rgb])
    else:
        eteint_rgb()

while True:
    now = millis()

    # Un appui = le bouton passe de 0 à 1 (PULL_DOWN), anti-rebond 50 ms
    cur_A = btn_A.value()
    appui = False
    if cur_A != prev_A and cur_A == 1 and time.ticks_diff(now, t_appui) > 50:
        appui = True
        t_appui = now
    prev_A = cur_A

    # Ignorer les appuis pendant 1 s après un double clic
    if time.ticks_diff(now, t_double) < 1000:
        appui = False

    if appui:
        if not attente:
            attente = True                                   # 1er clic
            t_premier = now
        else:
            compteur_rgb = (compteur_rgb + 1) % len(tableau_couleur)  # double clic
            attente = False
            t_double = now
            afficher()

    # 0,8 s sans 2e clic = clic simple
    if attente and time.ticks_diff(now, t_premier) >= 800:
        allumee = not allumee
        attente = False
        afficher()