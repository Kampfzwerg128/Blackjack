import random
import tkinter as tk
from tkinter import messagebox

# Globale Variablen
points = 100
player_hand = []
dealer_hand = []

def draw_card():
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

def update_labels():
    """Aktualisiert die GUI-Labels."""
    player_label.config(text=f"Deine Karten: {player_hand} (Summe: {sum(player_hand)})")
    dealer_label.config(text=f"Dealer-Karten: {dealer_hand[0]}, ?")

def start_game():
    """Startet eine neue Runde Blackjack."""
    global player_hand, dealer_hand, points
    
    if points <= 0:
        messagebox.showinfo("Spiel vorbei", "Du hast keine Punkte mehr!")
        return
    
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    
    update_labels()

    # Buttons aktivieren, falls sie deaktiviert wurden
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)

def hit():
    """Spieler zieht eine Karte."""
    global player_hand, points
    player_hand.append(draw_card())
    update_labels()
    
    if sum(player_hand) > 21:
        messagebox.showwarning("Busted!", "Du hast über 21! Verloren. 😢")
        points_label.config(text=f"Punkte: {points - 10}")
        disable_buttons()

def stand():
    """Dealer zieht Karten und Gewinner wird bestimmt."""
    global dealer_hand, points
    
    while sum(dealer_hand) < 17:
        dealer_hand.append(draw_card())
    
    dealer_label.config(text=f"Dealer-Karten: {dealer_hand} (Summe: {sum(dealer_hand)})")
    
    if sum(dealer_hand) > 21 or sum(player_hand) > sum(dealer_hand):
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
