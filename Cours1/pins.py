# Fichier de correspondance pour Arduino Nano ESP32 générique
from machine import Pin as _Pin

class Pins:
    OUT = _Pin.OUT
    IN = _Pin.IN
    PULL_UP = _Pin.PULL_UP
    PULL_DOWN = _Pin.PULL_DOWN
    
    # Correspondance des broches (Sérigraphie -> GPIO)
    D0 = 44
    D1 = 43
    D2 = 5
    D3 = 6
    D4 = 7
    D5 = 8
    D6 = 9
    D7 = 10
    D8 = 17
    D9 = 18
    D10 = 21
    D11 = 38
    D12 = 47
    D13 = 48
    A0 = 1
    A1 = 2
    A2 = 3
    A3 = 4
    A4 = 11
    A5 = 12
    A6 = 13
    A7 = 14