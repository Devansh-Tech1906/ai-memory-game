import tkinter as tk
from tkinter import messagebox
import random

BG_COLOR = "#1E1E1E"
CARD_HIDDEN = "#333333"
CARD_HOVER = "#4A4A4A"
CARD_REVEALED = "#FFFFFF"
CARD_MATCHED = "#4CAF50"
TEXT_COLOR = "#FFFFFF"
ACCENT_BLUE = "#58A6FF"
ACCENT_RED = "#FF7B72"


class MemoryGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Memory Game")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("450x700")

        self.symbols = ['🍎', '🍌', '🍉', '🍇', '🍓', '🍒', '🍍', '🥝'] * 2
        random.shuffle(self.symbols)

        self.buttons = []
        self.flipped_indices = []
        self.matched_indices = []
        self.ai_memory = {}

        self.turn = "Player"
        self.player_score = 0
        self.ai_score = 0
        self.locked = False

        score_frame = tk.Frame(root, bg=BG_COLOR)
        score_frame.pack(pady=(20, 10))

        self.player_label = tk.Label(score_frame, text=f"🧑 Player: 0", font=("Segoe UI", 16, "bold"), bg=BG_COLOR,
                                     fg=ACCENT_BLUE)
        self.player_label.grid(row=0, column=0, padx=20)

        self.ai_label = tk.Label(score_frame, text=f"🤖 AI: 0", font=("Segoe UI", 16, "bold"), bg=BG_COLOR,
                                 fg=TEXT_COLOR)
        self.ai_label.grid(row=0, column=1, padx=20)

        self.turn_label = tk.Label(root, text="Your Turn!", font=("Segoe UI", 14, "italic"), bg=BG_COLOR,
                                   fg=ACCENT_BLUE)
        self.turn_label.pack(pady=(0, 20))

        board_frame = tk.Frame(root, bg=BG_COLOR)
        board_frame.pack()

        for i in range(16):
            btn = tk.Button(board_frame, text="❓", width=4, height=2, font=("Segoe UI", 28),
                            bg=CARD_HIDDEN, fg=TEXT_COLOR, cursor="hand2",
                            relief="flat", bd=0, activebackground=CARD_REVEALED)

            btn.bind("<Enter>", lambda e, b=btn, idx=i: self.on_hover(b, idx))
            btn.bind("<Leave>", lambda e, b=btn, idx=i: self.on_leave(b, idx))
            btn.configure(command=lambda idx=i: self.player_click(idx))

            btn.grid(row=(i // 4), column=i % 4, padx=8, pady=8)
            self.buttons.append(btn)

    def on_hover(self, btn, index):
        if index not in self.flipped_indices and index not in self.matched_indices and not self.locked:
            btn.config(bg=CARD_HOVER)

    def on_leave(self, btn, index):
        if index not in self.flipped_indices and index not in self.matched_indices:
            btn.config(bg=CARD_HIDDEN)

    def update_scoreboard(self):
        self.player_label.config(text=f"🧑 Player: {self.player_score}")
        self.ai_label.config(text=f"🤖 AI: {self.ai_score}")

        if self.turn == "Player":
            self.turn_label.config(text="Your Turn!", fg=ACCENT_BLUE)
            self.player_label.config(fg=ACCENT_BLUE)
            self.ai_label.config(fg=TEXT_COLOR)
        else:
            self.turn_label.config(text="AI is thinking...", fg=ACCENT_RED)
            self.player_label.config(fg=TEXT_COLOR)
            self.ai_label.config(fg=ACCENT_RED)

    def remember_card(self, index):
        symbol = self.symbols[index]
        if symbol not in self.ai_memory:
            self.ai_memory[symbol] = []
        if index not in self.ai_memory[symbol]:
            self.ai_memory[symbol].append(index)

    def player_click(self, index):
        if self.locked or self.turn == "AI" or index in self.flipped_indices or index in self.matched_indices:
            return

        self.reveal_card(index)
        self.flipped_indices.append(index)

        if len(self.flipped_indices) == 2:
            self.locked = True
            self.root.after(1000, self.check_match, "Player")

    def reveal_card(self, index):
        self.buttons[index].config(text=self.symbols[index], bg=CARD_REVEALED, fg="black")
        self.remember_card(index)

    def hide_cards(self):
        for idx in self.flipped_indices:
            self.buttons[idx].config(text="❓", bg=CARD_HIDDEN, fg=TEXT_COLOR)
        self.flipped_indices = []

    def check_match(self, current_turn):
        idx1, idx2 = self.flipped_indices

        if self.symbols[idx1] == self.symbols[idx2]:
            self.buttons[idx1].config(bg=CARD_MATCHED, fg="white")
            self.buttons[idx2].config(bg=CARD_MATCHED, fg="white")
            self.matched_indices.extend([idx1, idx2])
            self.flipped_indices = []

            if current_turn == "Player":
                self.player_score += 1
            else:
                self.ai_score += 1

            self.locked = False
            self.update_scoreboard()
            self.check_game_over()

            if current_turn == "AI" and len(self.matched_indices) < 16:
                self.root.after(1000, self.ai_turn)
        else:
            self.hide_cards()
            self.turn = "AI" if current_turn == "Player" else "Player"
            self.update_scoreboard()
            self.locked = False

            if self.turn == "AI":
                self.root.after(1000, self.ai_turn)

    def ai_turn(self):
        if len(self.matched_indices) == 16:
            return

        self.locked = True

        known_pair = None
        for symbol, indices in self.ai_memory.items():
            valid_indices = [i for i in indices if i not in self.matched_indices]
            if len(valid_indices) == 2:
                known_pair = valid_indices
                break

        if known_pair:
            choice1, choice2 = known_pair
            self.reveal_card(choice1)
            self.flipped_indices.append(choice1)
            self.root.after(800, self.ai_second_flip, choice2)
            return

        known_all = []
        for indices in self.ai_memory.values():
            known_all.extend(indices)

        unknown_cards = [i for i in range(16) if i not in self.matched_indices and i not in known_all]

        if unknown_cards:
            choice1 = random.choice(unknown_cards)
        else:
            available = [i for i in range(16) if i not in self.matched_indices]
            choice1 = random.choice(available)

        self.reveal_card(choice1)
        self.flipped_indices.append(choice1)

        self.root.after(800, self.ai_smart_second_flip, choice1)

    def ai_smart_second_flip(self, choice1):
        symbol1 = self.symbols[choice1]

        known_matches = [i for i in self.ai_memory[symbol1] if i != choice1 and i not in self.matched_indices]

        if known_matches:
            choice2 = known_matches[0]
        else:
            known_all = []
            for indices in self.ai_memory.values():
                known_all.extend(indices)

            unknown_cards = [i for i in range(16) if
                             i not in self.matched_indices and i not in known_all and i != choice1]

            if unknown_cards:
                choice2 = random.choice(unknown_cards)
            else:
                available = [i for i in range(16) if i not in self.matched_indices and i != choice1]
                choice2 = random.choice(available)

        self.reveal_card(choice2)
        self.flipped_indices.append(choice2)
        self.root.after(1000, self.check_match, "AI")

    def ai_second_flip(self, choice2):
        self.reveal_card(choice2)
        self.flipped_indices.append(choice2)
        self.root.after(1000, self.check_match, "AI")

    def check_game_over(self):
        if len(self.matched_indices) == 16:
            if self.player_score > self.ai_score:
                result = "🎉 You Won!"
            elif self.ai_score > self.player_score:
                result = "💀 AI Won!"
            else:
                result = "🤝 It's a Tie!"
            messagebox.showinfo("Game Over", f"{result}\n\nFinal Score:\nYou: {self.player_score}\nAI: {self.ai_score}")
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = MemoryGameApp(root)
    root.mainloop()