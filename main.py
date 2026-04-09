import tkinter as tk
from tkinter import messagebox
import random

# ---------- Color Palette ----------
BG_COLOR = "#0B0B0B"
PANEL_COLOR = "#111111"
PANEL_ALT = "#1A1A1A"
CARD_HIDDEN = "#2A2A2A"
CARD_HOVER = "#3A3A3A"
CARD_REVEALED = "#F5F5DC"
CARD_MATCHED = "#8BC34A"
TEXT_PRIMARY = "#F5F5DC"
TEXT_SECONDARY = "#CFC7B5"
ACCENT_BLUE = "#F5F5DC"
ACCENT_RED = "#E57373"
ACCENT_GOLD = "#EAD8A6"
BUTTON_COLOR = "#F5F5DC"
BUTTON_HOVER = "#EAD8A6"


class MemoryGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Memory Game")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # ---------- Make window fit the current screen ----------
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        win_w = min(520, screen_w - 80)
        win_h = min(760, screen_h - 100)

        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.symbol_pool = ['🍎', '🍌', '🍉', '🍇', '🍓', '🍒', '🍍', '🥝']
        self.buttons = []
        self.flipped_indices = []
        self.matched_indices = []
        self.ai_memory = {}
        self.turn = "Player"
        self.player_score = 0
        self.ai_score = 0
        self.move_count = 0
        self.locked = False

        self.setup_game()
        self.build_ui()
        self.update_scoreboard()

    def setup_game(self):
        self.symbols = self.symbol_pool * 2
        random.shuffle(self.symbols)

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", pady=(12, 8), padx=16)

        title = tk.Label(
            header,
            text="🧠 AI Memory Game",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Match pairs before the AI does",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        )
        subtitle.pack(pady=(2, 0))

        info_panel = tk.Frame(
            self.root,
            bg=PANEL_COLOR,
            highlightthickness=1,
            highlightbackground="#223047"
        )
        info_panel.pack(fill="x", padx=16, pady=(6, 10), ipady=8)

        self.player_label = tk.Label(
            info_panel,
            text="🧑 Player: 0",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL_COLOR,
            fg=ACCENT_BLUE
        )
        self.player_label.grid(row=0, column=0, padx=18, pady=(4, 2), sticky="w")

        self.ai_label = tk.Label(
            info_panel,
            text="🤖 AI: 0",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL_COLOR,
            fg=TEXT_PRIMARY
        )
        self.ai_label.grid(row=0, column=1, padx=18, pady=(4, 2), sticky="e")

        self.turn_label = tk.Label(
            info_panel,
            text="Your Turn",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL_COLOR,
            fg=ACCENT_GOLD
        )
        self.turn_label.grid(row=1, column=0, padx=18, pady=(4, 2), sticky="w")

        self.moves_label = tk.Label(
            info_panel,
            text="Moves: 0",
            font=("Segoe UI", 10),
            bg=PANEL_COLOR,
            fg=TEXT_SECONDARY
        )
        self.moves_label.grid(row=1, column=1, padx=18, pady=(4, 2), sticky="e")

        info_panel.grid_columnconfigure(0, weight=1)
        info_panel.grid_columnconfigure(1, weight=1)

        board_outer = tk.Frame(self.root, bg=BG_COLOR)
        board_outer.pack(pady=6)

        board_title = tk.Label(
            board_outer,
            text="Game Board",
            font=("Segoe UI", 11, "bold"),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        board_title.pack(pady=(0, 8))

        self.board_frame = tk.Frame(
            board_outer,
            bg=PANEL_ALT,
            padx=10,
            pady=10,
            highlightthickness=1,
            highlightbackground="#223047"
        )
        self.board_frame.pack()

        for i in range(16):
            btn = tk.Button(
                self.board_frame,
                text="❓",
                width=3,
                height=1,
                font=("Segoe UI Emoji", 20, "bold"),
                bg=CARD_HIDDEN,
                fg=TEXT_PRIMARY,
                activebackground=CARD_REVEALED,
                activeforeground="#000000",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda idx=i: self.player_click(idx)
            )

            btn.bind("<Enter>", lambda e, b=btn, idx=i: self.on_hover(b, idx))
            btn.bind("<Leave>", lambda e, b=btn, idx=i: self.on_leave(b, idx))
            btn.grid(row=i // 4, column=i % 4, padx=6, pady=6, ipadx=6, ipady=8)
            self.buttons.append(btn)

        controls = tk.Frame(self.root, bg=BG_COLOR)
        controls.pack(fill="x", padx=16, pady=(12, 6))

        self.restart_button = tk.Button(
            controls,
            text="🔄 Restart Game",
            font=("Segoe UI", 11, "bold"),
            bg=BUTTON_COLOR,
            fg="#0B0B0B",
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=8,
            command=self.restart_game
        )
        self.restart_button.pack()

        self.restart_button.bind("<Enter>", lambda e: self.restart_button.config(bg=BUTTON_HOVER))
        self.restart_button.bind("<Leave>", lambda e: self.restart_button.config(bg=BUTTON_COLOR))

        footer = tk.Label(
            self.root,
            text="Tip: The AI remembers revealed cards, so plan carefully.",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        )
        footer.pack(pady=(6, 10))

    def on_hover(self, btn, index):
        if index not in self.flipped_indices and index not in self.matched_indices and not self.locked:
            btn.config(bg=CARD_HOVER)

    def on_leave(self, btn, index):
        if index not in self.flipped_indices and index not in self.matched_indices:
            btn.config(bg=CARD_HIDDEN)

    def update_scoreboard(self):
        self.player_label.config(text=f"🧑 Player: {self.player_score}")
        self.ai_label.config(text=f"🤖 AI: {self.ai_score}")
        self.moves_label.config(text=f"Moves: {self.move_count}")

        if self.turn == "Player":
            self.turn_label.config(text="Your Turn", fg=ACCENT_GOLD)
            self.player_label.config(fg=ACCENT_BLUE)
            self.ai_label.config(fg=TEXT_PRIMARY)
        else:
            self.turn_label.config(text="AI is thinking...", fg=ACCENT_RED)
            self.player_label.config(fg=TEXT_PRIMARY)
            self.ai_label.config(fg=ACCENT_RED)

    def remember_card(self, index):
        symbol = self.symbols[index]
        if symbol not in self.ai_memory:
            self.ai_memory[symbol] = []
        if index not in self.ai_memory[symbol]:
            self.ai_memory[symbol].append(index)

    def reveal_card(self, index):
        self.buttons[index].config(text=self.symbols[index], bg=CARD_REVEALED, fg="#0B0B0B")
        self.remember_card(index)

    def hide_cards(self):
        for idx in self.flipped_indices:
            self.buttons[idx].config(text="❓", bg=CARD_HIDDEN, fg=TEXT_PRIMARY)
        self.flipped_indices = []

    def player_click(self, index):
        if self.locked or self.turn == "AI" or index in self.flipped_indices or index in self.matched_indices:
            return

        self.reveal_card(index)
        self.flipped_indices.append(index)

        if len(self.flipped_indices) == 2:
            self.locked = True
            self.move_count += 1
            self.update_scoreboard()
            self.root.after(850, self.check_match, "Player")

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
                self.root.after(850, self.ai_turn)
        else:
            self.hide_cards()
            self.turn = "AI" if current_turn == "Player" else "Player"
            self.locked = False
            self.update_scoreboard()

            if self.turn == "AI":
                self.root.after(850, self.ai_turn)

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
            self.root.after(700, self.ai_second_flip, choice2)
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
        self.root.after(700, self.ai_smart_second_flip, choice1)

    def ai_smart_second_flip(self, choice1):
        symbol1 = self.symbols[choice1]
        known_matches = [i for i in self.ai_memory[symbol1] if i != choice1 and i not in self.matched_indices]

        if known_matches:
            choice2 = known_matches[0]
        else:
            known_all = []
            for indices in self.ai_memory.values():
                known_all.extend(indices)

            unknown_cards = [i for i in range(16) if i not in self.matched_indices and i not in known_all and i != choice1]

            if unknown_cards:
                choice2 = random.choice(unknown_cards)
            else:
                available = [i for i in range(16) if i not in self.matched_indices and i != choice1]
                choice2 = random.choice(available)

        self.reveal_card(choice2)
        self.flipped_indices.append(choice2)
        self.root.after(850, self.check_match, "AI")

    def ai_second_flip(self, choice2):
        self.reveal_card(choice2)
        self.flipped_indices.append(choice2)
        self.root.after(850, self.check_match, "AI")

    def check_game_over(self):
        if len(self.matched_indices) == 16:
            if self.player_score > self.ai_score:
                result = "🎉 You Won!"
            elif self.ai_score > self.player_score:
                result = "🤖 AI Won!"
            else:
                result = "🤝 It's a Tie!"

            messagebox.showinfo(
                "Game Over",
                f"{result}\n\nFinal Score:\nPlayer: {self.player_score}\nAI: {self.ai_score}\nMoves: {self.move_count}"
            )

    def restart_game(self):
        self.symbols = self.symbol_pool * 2
        random.shuffle(self.symbols)

        self.flipped_indices = []
        self.matched_indices = []
        self.ai_memory = {}
        self.turn = "Player"
        self.player_score = 0
        self.ai_score = 0
        self.move_count = 0
        self.locked = False

        for btn in self.buttons:
            btn.config(text="❓", bg=CARD_HIDDEN, fg=TEXT_PRIMARY)

        self.update_scoreboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGameApp(root)
    root.mainloop()