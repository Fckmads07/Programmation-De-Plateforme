from machine import Pin, I2C, ADC, PWM
from time import sleep


pwm_r = PWM(Pin(Pin.board.A1, Pin.OUT))
pwm_g = PWM(Pin(Pin.board.A0, Pin.OUT))
pwm_b = PWM(Pin(Pin.board.A2, Pin.OUT))

pwm_r.freq(1000)
pwm_g.freq(1000)
pwm_b.freq(1000)

MAX_DUTY = 1023 

# Veuillez activer les 3 lignes associ?es ? l'?tat « ?teint » selon le type de commutateur RGD utilis?.

# pwm_r.duty(MAX_DUTY)
# pwm_g.duty(MAX_DUTY)
# pwm_b.duty(MAX_DUTY)

# pwm_r.duty(0)
# pwm_g.duty(0)
# pwm_b.duty(0)

adc = ADC(Pin(Pin.board.A3))
adc.atten(ADC.ATTN_11DB)  


i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70  

i2c.writeto(adresse_matrice, bytes([0x21])) 
i2c.writeto(adresse_matrice, bytes([0x81])) 
i2c.writeto(adresse_matrice, bytes([0xE4])) 


def rgb(chiffre):
    """Pilote l'intensit? lumineuse d'une LED RVB par paliers et transitions.

    Cette fonction ?value une valeur num?rique d'entr?e (consid?r?e ici comme
    une grandeur ou une consigne) et ajuste dynamiquement le rapport cyclique 
    (PWM) des trois canaux de couleur (Rouge, Vert, Bleu) selon une ?chelle 
    d?coup?e en 5 tranches de 20 (de 0 ? 100).

    Args:
        chiffre (int ou float): La valeur num?rique ? ?valuer, repr?sentant 
            la position dans l'?chelle de contr?le (ex: 0 ? 100).

    Comportement par intervalles :
        - 0 < chiffre < 20 : 
          Rouge et Bleu ?teints, Vert allum? ? 100 %.
        
        - 20 <= chiffre < 40 : 
          Transition progressive du vert vers le bleu :
          - ? 20 : Vert = 100 %, Bleu = 0 %
          - ? 30 : Vert = 50 %, Bleu = 50 %
          - ? 40 : Vert = 0 %, Bleu = 100 %
          (L'?volution est proportionnelle pour toutes les valeurs interm?diaires).
        
        - 40 <= chiffre < 60 : 
          Rouge et Vert ?teints, Bleu allum? ? 100 %.
        
        - 60 <= chiffre < 80 : 
          Transition progressive du bleu vers le rouge 
          (?volution proportionnelle similaire ? la tranche pr?c?dente).
        
        - chiffre >= 80 : 
          Bleu et Vert ?teints, Rouge allum? ? 100 %.

    Note:
        Les valeurs de sortie du PWM sont strictement born?es entre 0 et 
        la constante globale `MAX_DUTY`.
    """



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
    """Affiche un nombre ? deux chiffres sur un dispositif ? double matrice via I2C.

    Cette fonction d?compose un nombre entier en dizaines et en unit?s, r?cup?re 
    les motifs graphiques associ?s depuis une table de correspondance, combine 
    les donn?es des deux matrices au sein d'un m?me octet, puis les transmet 
    ligne par ligne au composant via le bus I2C.

    Args:
        i2c: L'objet de communication I2C utilis? pour envoyer les trames 
            vers le p?riph?rique.
        chiffre (int): La valeur num?rique enti?re ? afficher (g?n?ralement 
            comprise entre 0 et 99).
    """



# Boucle principale

