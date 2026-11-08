import machine 
from pins import Pins 
import time 


bouton = machine.Pin(Pins.D10, machine.Pin.IN, machine.Pin.PULL_UP)
Blanche = machine.Pin(Pins.D5, machine.Pin.OUT)

Blanche.value(1)


mode = 0 
# 0 = LED eteint 
# 1 = LED allumé 
# 2 = LED clignote

while True:
    if bouton.value() == 0:
        mode = mode + 1
        if mode == 3:
            mode = 0
        time.sleep(1)  

    if mode == 0:
        Blanche.value(0)  
    elif mode == 1:
        Blanche.value(1)  
    elif mode == 2:
        Blanche.value(1)  
        time.sleep(0.1)  
        Blanche.value(0)  
        time.sleep(0.1)
