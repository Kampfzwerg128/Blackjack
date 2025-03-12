import random
import tkinter as tk
from tkinter import messagebox

# Globale Variablen
points = 100
player_hand = []
dealer_hand = []

CARD_SUITS = ["♥", "♦", "♣", "♠"]  # Herz, Karo, Kreuz, Pik
CARD_VALUES = {11: "A", 10: "10", 9: "9", 8: "8", 7: "7", 6: "6", 5: "5", 4: "4", 3: "3", 2: "2"}


def draw_card():
    """Zieht eine zufällige Karte."""
    value = random.choice(list(CARD_VALUES.keys()))
    suit = random.choice(CARD_SUITS)
    return value, f"[{CARD_VALUES[value]}{suit}]"


def calculate_hand_value(hand):
    """Berechnet die Summe der Karten und berücksichtigt Asse."""
    total = sum(card[0] for card in hand)
    aces = sum(1 for card in hand if card[0] == 11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def update_labels():
    """Aktualisiert die GUI-Labels."""
    player_label.config(
        text=f"Deine Karten (Summe: {calculate_hand_value(player_hand)}): {' '.join(card[1] for card in player_hand)}"
    )
    dealer_label.config(text=f"Dealer-Karten: {dealer_hand[0][1]} ?")


def start_game():
    """Startet eine neue Runde Blackjack."""
    global player_hand, dealer_hand, points

    if points <= 0:
        messagebox.showinfo("Spiel vorbei", "Du hast keine Punkte mehr!")
        return

    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]

    update_labels()
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)


def hit():
    """Spieler zieht eine Karte."""
    global player_hand, points
    player_hand.append(draw_card())
    update_labels()

    if calculate_hand_value(player_hand) > 21:
        messagebox.showwarning("Busted!", "Du hast über 21! Verloren. 😢")
        points -= 10
        points_label.config(text=f"Punkte: {points}")
        disable_buttons()


def stand():
    """Dealer zieht Karten und Gewinner wird bestimmt."""
    global dealer_hand, points

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card())

    dealer_label.config(
        text=f"Dealer-Karten (Summe: {calculate_hand_value(dealer_hand)}): {' '.join(card[1] for card in dealer_hand)}"
    )

    if calculate_hand_value(dealer_hand) > 21 or calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
        messagebox.showinfo("Gewonnen!", "Du hast gewonnen! 🎉")
        points += 10
    else:
        messagebox.showinfo("Verloren", "Der Dealer hat gewonnen.")
        points -= 10

    points_label.config(text=f"Punkte: {points}")
    disable_buttons()


def disable_buttons():
    """Deaktiviert die Buttons nach Spielende."""
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)


# GUI erstellen
root = tk.Tk()
root.title("Blackjack")

# Labels
points_label = tk.Label(root, text=f"Punkte: {points}", font=("Arial", 14))
points_label.pack()

player_label = tk.Label(root, text="Deine Karten: ", font=("Arial", 12))
player_label.pack()

dealer_label = tk.Label(root, text="Dealer-Karten: ", font=("Arial", 12))
dealer_label.pack()

# Buttons
start_button = tk.Button(root, text="Neue Runde", command=start_game, font=("Arial", 12))
start_button.pack()

hit_button = tk.Button(root, text="Hit (Karte ziehen)", command=hit, font=("Arial", 12), state=tk.DISABLED)
hit_button.pack()

stand_button = tk.Button(root, text="Stand (Passen)", command=stand, font=("Arial", 12), state=tk.DISABLED)
stand_button.pack()

# Haupt-Loop starten
root.mainloop()
