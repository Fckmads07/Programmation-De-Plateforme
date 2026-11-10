from machine import Pin, I2C, ADC, PWM
from time import sleep


pwm_r = PWM(Pin(Pin.board.A0, Pin.OUT))
pwm_g = PWM(Pin(Pin.board.A2, Pin.OUT))
pwm_b = PWM(Pin(Pin.board.A1, Pin.OUT))

pwm_r.freq(1000)
pwm_g.freq(1000)
pwm_b.freq(1000)

MAX_DUTY = 1023 

# Veuillez activer les 3 lignes associées ? l'état « éteint » selon le type de commutateur RGD utilisé.


ANODE_COMMUNE = True 

 
def duty(position):
    duty = int(position * MAX_DUTY)
    if ANODE_COMMUNE:
        duty = MAX_DUTY - duty
    return duty

def set_couleur(r,g,b):
    pwm_r.duty(duty(r))
    pwm_g.duty(duty(g))
    pwm_b.duty(duty(b))

def eteindre():
   set_couleur(0,0,0)

eteindre()



adc = ADC(Pin(Pin.board.A3))
adc.atten(ADC.ATTN_11DB)  


i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70  

i2c.writeto(adresse_matrice, bytes([0x21])) 
i2c.writeto(adresse_matrice, bytes([0x81])) 
i2c.writeto(adresse_matrice, bytes([0xE4])) 


def rgb(chiffre):
    """Pilote l'intensité lumineuse d'une LED RVB par paliers et transitions.

    Cette fonction à value une valeur numérique d'entrée (considérée ici comme
    une grandeur ou une consigne) et ajuste dynamiquement le rapport cyclique 
    (PWM) des trois canaux de couleur (Rouge, Vert, Bleu) selon une échelle 
    découpée en 5 tranches de 20 (de 0 à 100).

    Args:
        chiffre (int ou float): La valeur numérique à évaluer, représentant 
            la position dans l'échelle de contrôle (ex: 0 à 100).

    Comportement par intervalles :
        - 0 < chiffre < 20 : 
          Rouge et Bleu éteints, Vert allumé à 100 %.
        
        - 20 <= chiffre < 40 : 
          Transition progressive du vert vers le bleu :
          - à 20 : Vert = 100 %, Bleu = 0 %
          - à 30 : Vert = 50 %, Bleu = 50 %
          - à 40 : Vert = 0 %, Bleu = 100 %
          (L'évolution est proportionnelle pour toutes les valeurs intermédiaires).


        
        - 40 <= chiffre < 60 : 
          Rouge et Vert éteints, Bleu allumé à 100 %.
        
        - 60 <= chiffre < 80 : 
          Transition progressive du bleu vers le rouge 
          (évolution proportionnelle similaire à la tranche précédente).
        
        - chiffre >= 80 : 
          Bleu et Vert éteints, Rouge allumé à 100 %.

    Note:
        Les valeurs de sortie du PWM sont strictement bornées entre 0 et 
        la constante globale `MAX_DUTY`.
    """

    #Comportement par intervalles :
    #       - 0 < chiffre < 20 : 
    #        Rouge et Bleu éteints, Vert allumé à 100 %.
    if chiffre < 20:
        set_couleur(0, 1, 0)  # Vert à 100 %

    elif chiffre < 40:
        color_change = (chiffre - 20) / 20
        set_couleur(0, 1 - color_change, color_change)

    elif chiffre < 60:
        set_couleur(0, 0, 1)  # Bleu à 100 %

    elif chiffre < 80:
        color_change = (chiffre - 60) / 20
        set_couleur(color_change, 0, 1 - color_change)

    else:
        set_couleur(1, 0, 0)  # Rouge à 100 %




def fermeTout():
    for i in range(0, 16, 2):
        i2c.writeto(adresse_matrice, bytes([i, 0x00]))
def allumeTout():
    for i in range(0, 16, 2):
        i2c.writeto(adresse_matrice, bytes([i, 0xFF]))

fermeTout()

chiffreMapping = {
    0 : [
            0b111,
            0b101,
            0b101,
            0b101,
            0b111,
        ],
    1 : [
            0b010,
            0b011,
            0b010,
            0b010,
            0b111
        ],
    2 : [
            0b111,
            0b100,
            0b111,
            0b001,
            0b111
        ],
    3 : [
            0b111,
            0b100,
            0b111,
            0b100,
            0b111,
        ],
    4 : [
            0b101,
            0b101,
            0b111,
            0b100,
            0b100,
        ], 
    5 : [
            0b111,
            0b001,
            0b111,
            0b100,
            0b111,
        ],
    6 : [
            0b111,
            0b001,
            0b111,
            0b101,
            0b111,
        ],
    7 : [
            0b111,
            0b100,
            0b100,
            0b100,
            0b100,
        ],
    8 : [
            0b111,
            0b101,
            0b111,
            0b101,
            0b111,
        ],
    9 : [
            0b111,
            0b101,
            0b111,
            0b100,
            0b100,
        ]
}


def afficherChiffre(i2c, chiffre):
    """Affiche un nombre à deux chiffres sur un dispositif à double matrice via I2C.

    Cette fonction décompose un nombre entier en dizaines et en unités, récupère 
    les motifs graphiques associés depuis une table de correspondance, combine 
    les données des deux matrices au sein d'un même octet, puis les transmet 
    ligne par ligne au composant via le bus I2C.

    Args:
        i2c: L'objet de communication I2C utilisé pour envoyer les trames 
            vers le périphérique.
        chiffre (int): La valeur numérique entière à afficher (généralement 
            comprise entre 0 et 99).
    """
    chiffre = int(chiffre)

    dizaines = chiffre // 10
    unites = chiffre % 10

    for i in range(8):
        if i < 5:
            octet = chiffreMapping[dizaines][i]
            octet = octet | (chiffreMapping[unites][i] << 4)
        else:
            octet = 0

        i2c.writeto(adresse_matrice, bytes([i * 2, octet]))

    # verifie que le chiffre est bien de 4 octet et non plus 


# Boucle principale

dernier_chiffre = -1  # Initialisation pour forcer l'affichage du premier chiffre

try:
    while True:

        chiffre = int(adc.read() / 4095 * 99)

        rgb(chiffre)

        if chiffre != dernier_chiffre:
            if chiffre >= 99:
                allumeTout()
            else:
                afficherChiffre(i2c, chiffre)
            dernier_chiffre = chiffre

        sleep(0.05)
except KeyboardInterrupt:
    eteindre()
    fermeTout()

    pwm_r.deinit()
    pwm_g.deinit()
    pwm_b.deinit()

    adc.deinit()


