import machine
import time

# --- Broches ---
btn = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
led_r = machine.PWM(machine.Pin(15), freq=1000)
led_g = machine.PWM(machine.Pin(2),  freq=1000)
led_b = machine.PWM(machine.Pin(4),  freq=1000)

# --- Séquence Couleurs : Bleu -> Rouge -> Vert ---
couleurs = [
    (0, 0, 1023),   # Bleu
    (1023, 0, 0),   # Rouge
    (0, 1023, 0)    # Vert
]
index_couleur = 0
led_allumee = False

# --- Variables de contrôle ---
dernier_double_clic = 0  # Pour la pause de 1 seconde obligatoire

def appliquer_couleur():
    """Allume ou éteint la LED selon l'état actuel"""
    if not led_allumee:
        led_r.duty(0); led_g.duty(0); led_b.duty(0)
    else:
        r, g, b = couleurs[index_couleur]
        led_r.duty(r); led_g.duty(g); led_b.duty(b)

# Initialisation
appliquer_couleur()

while True:
    # 1. Attente du premier appui
    if btn.value() == 0:  # Bouton pressé
        time.sleep_ms(50) # Anti-rebond basique
        
        # Attente du relâchement du premier clic
        while btn.value() == 0:
            time.sleep_ms(10)

        # 2. Fenêtre de 0.8 seconde pour détecter un 2ème clic
        nb_clics = 1
        debut_fenetre = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), debut_fenetre) < 800:
            if btn.value() == 0:  # Un 2ème appui survient !
                nb_clics = 2
                time.sleep_ms(50) # Anti-rebond
                while btn.value() == 0: # Attente relâchement
                    time.sleep_ms(10)
                break  # Sortie de la fenêtre d'attente

        temps_actuel = time.ticks_ms()

        # 3. Action selon le nombre de clics détectés
        if nb_clics == 2:
            # Vérification de la pause obligatoire de 1 seconde entre 2 double clics
            if time.ticks_diff(temps_actuel, dernier_double_clic) >= 1000:
                index_couleur = (index_couleur + 1) % len(couleurs) # Couleur suivante
                led_allumee = True
                dernier_double_clic = temps_actuel
                print("Double Clic : Changement de couleur")
            else:
                print("Double Clic ignoré (pause de 1s non respectée)")

        elif nb_clics == 1:
            # Clic Simple : Toggle ON/OFF
            led_allumee = not led_allumee
            print("Clic Simple : ON/OFF")

        # Mise à jour matérielle de la LED
        appliquer_couleur()

    time.sleep_ms(20) # Petite pause pour économiser le processeur