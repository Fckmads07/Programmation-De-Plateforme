import machine 
from pins import Pins 
import time 


bouton1 = machine.Pin(Pins.D7, machine.Pin.IN, machine.Pin.PULL_UP)
bouton2 = machine.Pin(Pins.D9, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(Pins.D5, machine.Pin.OUT)

while True:
    a_appuye = bouton1.value() == 0
    b_appuye = bouton2.value() == 0

    if a_appuye and b_appuye:
        led.value(1)   
    else:
        led.value(0)  

    time.sleep_ms(10) 