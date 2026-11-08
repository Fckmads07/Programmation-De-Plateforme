from machine import Pin, I2C, ADC, PWM
from time import sleep


MAX_DUTY = 1023 

led = PWM(Pin(Pin.board.A7, Pin.OUT))

btn = Pin(Pin.board.A6)

adc = ADC(Pin(Pin.board.A3))
adc.atten(ADC.ATTN_11DB)  

i2c = I2C(0, scl=Pin(Pin.board.A5), sda=Pin(Pin.board.A4))
adresse_matrice = 0x70  

i2c.writeto(adresse_matrice, bytes([0x21])) 
i2c.writeto(adresse_matrice, bytes([0x81]))
i2c.writeto(adresse_matrice, bytes([0xE4])) 

lettreMapping = {
    'A': [0b111, 0b101, 0b111, 0b101, 0b101],
    'B': [0b011, 0b101, 0b011, 0b101, 0b011],
    'C': [0b111, 0b001, 0b001, 0b001, 0b111],
    'D': [0b011, 0b101, 0b101, 0b101, 0b011],
    'E': [0b111, 0b001, 0b111, 0b001, 0b111],
    'F': [0b111, 0b001, 0b111, 0b001, 0b001],
    'G': [0b111, 0b001, 0b101, 0b101, 0b111],
    'H': [0b101, 0b101, 0b111, 0b101, 0b101],
    'I': [0b111, 0b010, 0b010, 0b010, 0b111],
    'J': [0b100, 0b100, 0b100, 0b101, 0b111],
    'K': [0b101, 0b011, 0b001, 0b011, 0b101],
    'L': [0b001, 0b001, 0b001, 0b001, 0b111],
    'M': [0b101, 0b111, 0b101, 0b101, 0b101],
    'N': [0b101, 0b111, 0b111, 0b101, 0b101],
    'O': [0b111, 0b101, 0b101, 0b101, 0b111],
    'P': [0b111, 0b101, 0b111, 0b001, 0b001],
    'Q': [0b111, 0b101, 0b101, 0b111, 0b100],
    'R': [0b111, 0b101, 0b011, 0b101, 0b101],
    'S': [0b111, 0b001, 0b111, 0b100, 0b111],
    'T': [0b111, 0b010, 0b010, 0b010, 0b010],
    'U': [0b101, 0b101, 0b101, 0b101, 0b111],
    'V': [0b101, 0b101, 0b101, 0b101, 0b010],
    'W': [0b101, 0b101, 0b101, 0b111, 0b101],
    'X': [0b101, 0b101, 0b010, 0b101, 0b101],
    'Y': [0b101, 0b101, 0b010, 0b010, 0b010],
    'Z': [0b111, 0b100, 0b010, 0b001, 0b111]
}

def set_white_brightness(brightness):
    """
    Modifie la luminosité de la led blanche

    Args:
        brightness (float):Valeur entre 0 et 1 [0,1] qui représente l'intensité de la lumière blanche en pourcentage.

    """
    if brightness < 0:
        brightness = 0
    if brightness > 1:
        brightness = 1
    # Règle de trois : [0, 1] -> [0, 1023]
    led.duty(int(brightness * MAX_DUTY))


def fermeTout(matrice):
    """
    Ferme toutes les leds de la matrice 8x8

    Args:
        i2c (I2C): Instance de la classe I2C représentant la matrice de leds 8x8 
    """
    for reg in range(0, 16, 2):   # registres pairs : 0, 2, ..., 14
        matrice.writeto(adresse_matrice, bytes([reg, 0b00000000]))

def allumeTout(matrice):
    """
    Allume toutes les leds de la matrice 8x8

    Args:
        i2c (I2C): Instance de la classe I2C représentant la matrice de leds 8x8 
    """
    for reg in range(0, 16, 2):
        matrice.writeto(adresse_matrice, bytes([reg, 0b11111111]))

fermeTout(i2c)


def afficherLettre(i2c, lettre, lettreMapping):
    """
    Affiche une lettre sur la led 8x8

    Args:
        i2c (I2C): Instance de la classe I2C représentant la matrice de leds 8x8 
        lettre (char): la lettre à afficher
        lettreMapping (dict): Le dictionnaire qui permet d'obtenir la représentation en binaire nécessaire pour allumer sur la led de chaque lettre 
    """
    
    motif = lettreMapping[lettre]          # 5 rangées de 3 bits
    for ligne in range(8):
        octet = 0
        # La lettre occupe les rangées 1 à 5 (centrée verticalement)
        if 1 <= ligne <= 5:
            valeur = motif[ligne - 1]
            for bit in range(3):
                if valeur & (1 << bit):
                    # bit 0 du motif = colonne de gauche ; la colonne 0 de la
                    # matrice est le bit de poids fort. Lettre sur colonnes 2 à 4.
                    octet = octet | (0b10000000 >> (2 + bit))
        i2c.writeto(adresse_matrice, bytes([ligne << 1, octet]))

MOT_SECRET = "PYTHON" 
index_lettre_actuelle = 0
lettres_trouvees = ["_"] * len(MOT_SECRET)
MAX_VALUE_ADC = 4095

print("\033[2J\033[H", end="") 
print("=== JEU : TROUVE LE MOT ===")
print("Tournez le potentiometre pour faire defiler les lettres (A-Z).")
print("Restez stable sur une lettre pour valider.")
print("Mot :", " ".join(lettres_trouvees), "\n")

last_lettre = ''
flash_toggle = False

cur_btn_state = btn.value()
last_btn_state = cur_btn_state

# ----------------------- PARTIE AJOUTÉE -----------------------
from time import ticks_ms, ticks_diff

DEMI_PERIODE_MS = 50          # on inverse la LED aux 50 ms -> 10 clignotements/s
dernier_toggle = ticks_ms()

led.freq(1000)                # 1 kHz : aucun scintillement visible (cours)
set_white_brightness(0)

# Précisions pour le joueur (le texte ci-dessus ne dit pas comment valider)
print("PRECISION : pour valider, APPUYEZ sur le BOUTON (pas besoin de rester stable).")
print("LED blanche : plus elle est BRILLANTE, plus vous etes PROCHE de la bonne lettre.")
print("LED qui CLIGNOTE vite : c'est la bonne lettre, appuyez sur le bouton !\n")
print("Cherchez la lettre 1 sur", len(MOT_SECRET), "\n")

try:
    while index_lettre_actuelle < len(MOT_SECRET):
        # 1. Potentiomètre -> lettre (26 portions égales de la plage)
        valeur = adc.read()
        index = valeur * 26 // (MAX_VALUE_ADC + 1)
        if index > 25:
            index = 25
        lettre = chr(ord('A') + index)

        # 2. On rafraîchit la matrice seulement quand la lettre change
        if lettre != last_lettre:
            afficherLettre(i2c, lettre, lettreMapping)
            last_lettre = lettre

        # 3. Indice avec la LED blanche
        cible = MOT_SECRET[index_lettre_actuelle]
        if lettre == cible:
            # Clignotement non bloquant à ~10 Hz
            maintenant = ticks_ms()
            if ticks_diff(maintenant, dernier_toggle) >= DEMI_PERIODE_MS:
                flash_toggle = not flash_toggle
                dernier_toggle = maintenant
            set_white_brightness(1 if flash_toggle else 0)
        else:
            ecart = abs(ord(lettre) - ord(cible))     # 1 à 25
            set_white_brightness(1 - ecart / 26)      # plus proche = plus brillant

        # 4. Bouton (module : 1 = relâché, 0 = appuyé) -> on détecte l'APPUI
        cur_btn_state = btn.value()
        if last_btn_state == 1 and cur_btn_state == 0:
            if lettre == cible:
                lettres_trouvees[index_lettre_actuelle] = lettre
                index_lettre_actuelle += 1
                print("\033[2J\033[H", end="")
                print("=== JEU : TROUVE LE MOT ===")
                print("BRAVO ! La lettre", lettre, "est correcte !")
                print("Mot :", " ".join(lettres_trouvees), "\n")
                if index_lettre_actuelle < len(MOT_SECRET):
                    print("Cherchez la lettre", index_lettre_actuelle + 1, "sur", len(MOT_SECRET), "\n")
            else:
                print("Mauvaise lettre :", lettre, "- regardez la LED : plus elle est brillante, plus vous etes proche.")
        last_btn_state = cur_btn_state

        sleep(0.01)   # anti-rebond logiciel (comme dans le cours)

    # 5. Victoire : tous les éléments visuels au maximum
    allumeTout(i2c)
    set_white_brightness(1)
    print("\n*** VICTOIRE ! Le mot secret est :", "".join(lettres_trouvees), "***")

    while True:       # on laisse tout allumé jusqu'au Ctrl+C
        sleep(0.1)

except KeyboardInterrupt:
    # Nettoyage matériel (même principe que dans le chapitre PWM)
    fermeTout(i2c)
    set_white_brightness(0)
    led.deinit()
    print("\nJeu interrompu. Materiel eteint.")