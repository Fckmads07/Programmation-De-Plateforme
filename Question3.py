import machine
from pins import Pins
import time

bouton = machine.Pin(Pins.D8, machine.Pin.IN, machine.Pin.PULL_UP)
rgb_blue = machine.Pin(Pins.D4, machine.Pin.OUT)
rgb_vert = machine.Pin(Pins.D3, machine.Pin.OUT)
rgb_rouge = machine.Pin(Pins.D5, machine.Pin.OUT)



def led(rouge, vert, blue):
    rgb_rouge.value(rouge)
    rgb_vert.value(vert)
    rgb_blue.value(blue)


def afficher():
    # si la led est allumer on l'eteint
    if not allumee:
        led(1, 1, 1)                 # éteinte
    elif couleur == 0:
        led(1, 1, 0)                 # bleu
    elif couleur == 1:
        led(0, 1, 1)                 # rouge
    else:
        led(1, 0, 1)                 # vert


# savoir si la led est allumer ou pas 
allumee = False         
# savoir qu'elle couleur est selectionné
couleur = 0              
# le nombre de clic 
nb_clics = 0        
# memoire du dernier clic mis      
temps_dernier_clic = 0   
# sa prend le dernier clic     
old_etat = 1            

afficher()


while True:
    ticks = time.ticks_ms()
    btn = bouton.value()
    if old_etat == 1 and btn == 0:
        time.sleep(0.1)                     
        if ticks + 1000 > 100:         
            nb_clics = nb_clics + 1
            temps_dernier_clic = ticks

    
    elif old_etat == 0 and btn == 1:
        time.sleep(0.01)                   
    old_etat = btn
    if nb_clics > 0 and ticks - temps_dernier_clic > 800:
        if nb_clics == 1:
            allumee =  not allumee
        else:
            couleur = couleur + 1
            if couleur >= 3 :
                 couleur = 0 

            allumee = True
            fin_double = ticks 
        afficher()
        nb_clics = 0