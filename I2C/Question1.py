from machine import Pin, I2C

i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70

#Faites une fonction nommée allumerTout(i2c_bus) prenant l’instance du bus I2C en argument qui allume toutes les LED de la matrice.
def allumerTout(i2c_bus):
    # Activation de l'oscillateur et de l'affichage
    i2c_bus.writeto(adresse_matrice, bytes([0x21]))
    i2c_bus.writeto(adresse_matrice, bytes([0x81]))
    i2c_bus.writeto(adresse_matrice, bytes([0xEF]))
    
    # Remplissage de toute la mémoire d'affichage (16 octets à 0xFF) en une seule trame
    # Le premier octet (0x00) est l'adresse mémoire de départ, suivi de 16 octets à 255 (tous les bits à 1)
    i2c_bus.writeto(adresse_matrice, bytes([0x00] + [0xFF] * 16))

allumerTout(i2c)

