import machine
from pins import Pins 
import time

# Configuration d'une broche en entrée avec une résistance Pull-Up interne
# Par défaut, le bouton renverra 1 (relâché) et 0 (pressé)
bouton_led = machine.Pin(Pins.D5, machine.Pin.IN, machine.Pin.PULL_UP)
bouton_RGB = machine.Pin(Pins.D12, machine.Pin.IN, machine.Pin.PULL_UP)


Led = machine.Pin(Pins.D8, machine.Pin.OUT)
couleurs = [machine.Pin(Pins.D10, machine.Pin.OUT),
             machine.Pin(Pins.D3, machine.Pin.OUT),
             machine.Pin(Pins.D2, machine.Pin.OUT)]


index = 0 


while True:
    if bouton_led.value() == 0:
        Led.value(not Led.value())  # Inverse l'état de la LED
        time.sleep(0.5)  # Anti-rebond pour éviter les multiples déclenche
   
    if bouton_RGB.value() == 0:
        couleurs[0].value(not couleurs[0].value())  # Inverse l'état de la couleur actuelle
       
        couleurs[1].value(not couleurs[1].value())  # Inverse l'état de la couleur actuelle
        
        couleurs[2].value(not couleurs[2].value())  # Inverse l'état de la couleur actuelle
        

        couleurs[index].value(1)  # Allume la couleur actuelle

        index = (index + 1) % len(couleurs) 

        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide
        


   

    

