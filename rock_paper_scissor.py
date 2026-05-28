import random
import tkinter as tk
from tkinter import messagebox

# ASCII Art representations formatted for the text display
ROCK_ART = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

PAPER_ART = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

SCISSORS_ART = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

ART_MAP = {"rock": ROCK_ART, "paper": PAPER_ART, "scissors": SCISSORS_ART}


class RockPaperScissorsGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Rock, Paper, Scissors Ultimate")
        self.root.geometry("600x650")
        self.root.configure(bg="#2c3e50")

        # Game State Variables
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(
            self.root,
            text="ROCK, PAPER, SCISSORS",
            font=("Helvetica", 20, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50",
        )
        title_label.pack(pady=15)

        # Score Frame
        score_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief="groove")
        score_frame.pack(pady=10, fill="x", padx=40)

        self.score_label = tk.Label(
            score_frame,
            text="You: 0  |  Computer: 0  |  Ties: 0",
            font=("Helvetica", 14, "bold"),
            fg="#f1c40f",
            bg="#34495e",
        )
        self.score_label.pack(pady=10)

        # Visual Display Frame (For ASCII Art)
        display_frame = tk.Frame(self.root, bg="#2c3e50")
        display_frame.pack(pady=15)

        # Player Choice Display
        self.player_display = tk.Text(
            display_frame,
            width=22,
            height=8,
            font=("Courier", 10),
            bg="#1a252f",
            fg="#2ecc71",
            bd=0,
        )
        self.player_display.grid(row=0, column=0, padx=10)
        self.player_display.insert(tk.END, "\n\n   YOUR CHOICE\n   APPEARS HERE")
        self.player_display.config(state="disabled")

        # VS Label
        vs_label = tk.Label(
            display_frame,
            text="VS",
            font=("Helvetica", 18, "bold"),
            fg="#e74c3c",
            bg="#2c3e50",
        )
        vs_label.grid(row=0, column=1, padx=10)

        # Computer Choice Display
        self.computer_display = tk.Text(
            display_frame,
            width=22,
            height=8,
            font=("Courier", 10),
            bg="#1a252f",
            fg="#e74c3c",
            bd=0,
        )
        self.computer_display.grid(row=0, column=2, padx=10)
        self.computer_display.insert(
            tk.END, "\n\n  COMPUTER CHOICE\n   APPEARS HERE"
        )
        self.computer_display.config(state="disabled")

        # Result Announcement Label
        self.result_label = tk.Label(
            self.root,
            text="Make your move to start the game!",
            font=("Helvetica", 13, "italic"),
            fg="#ecf0f1",
            bg="#2c3e50",
            wraplength=500,
        )
        self.result_label.pack(pady=20)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=10)

        btn_style = {
            "font": ("Helvetica", 12, "bold"),
            "width": 12,
            "height": 2,
            "fg": "#ffffff",
            "activebackground": "#7f8c8d",
            "activeforeground": "#ffffff",
            "cursor": "hand2",
        }

        rock_btn = tk.Button(
            btn_frame,
            text="🪨 Rock",
            bg="#c0392b",
            command=lambda: self.play_round("rock"),
            **btn_style,
        )
        rock_btn.grid(row=0, column=0, padx=10)

        paper_btn = tk.Button(
            btn_frame,
            text="📄 Paper",
            bg="#2980b9",
            command=lambda: self.play_round("paper"),
            **btn_style,
        )
        paper_btn.grid(row=0, column=1, padx=10)

        scissors_btn = tk.Button(
            btn_frame,
            text="✂️ Scissors",
            bg="#27ae60",
            command=lambda: self.play_round("scissors"),
            **btn_style,
        )
        scissors_btn.grid(row=0, column=2, padx=10)

        # Reset & Quit Buttons
        action_frame = tk.Frame(self.root, bg="#2c3e50")
        action_frame.pack(pady=30)

        reset_btn = tk.Button(
            action_frame,
            text="Reset Scores",
            font=("Helvetica", 10),
            bg="#7f8c8d",
            fg="white",
            command=self.reset_game,
        )
        reset_btn.grid(row=0, column=0, padx=10)

        quit_btn = tk.Button(
            action_frame,
            text="Quit Game",
            font=("Helvetica", 10),
            bg="#95a5a6",
            fg="white",
            command=self.root.quit,
        )
        quit_btn.grid(row=0, column=1, padx=10)

    def play_round(self, player_choice):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)

        # Update Visual Text Boxes
        self.update_display(self.player_display, ART_MAP[player_choice])
        self.update_display(self.computer_display, ART_MAP[computer_choice])

        # Determine Winner
        if player_choice == computer_choice:
            self.ties += 1
            self.result_label.config(
                text=f"🤝 It's a tie! Both chose {player_choice.upper()}.",
                fg="#f1c40f",
            )
        elif (
            (player_choice == "rock" and computer_choice == "scissors")
            or (player_choice == "paper" and computer_choice == "rock")
            or (player_choice == "scissors" and computer_choice == "paper")
        ):
            self.player_score += 1
            self.result_label.config(
                text=f"🔥 You win! {player_choice.upper()} beats {computer_choice.upper()}.",
                fg="#2ecc71",
            )
        else:
            self.computer_score += 1
            self.result_label.config(
                text=f"💀 Computer wins! {computer_choice.upper()} beats {player_choice.upper()}.",
                fg="#e74c3c",
            )

        # Update Scoreboard
        self.score_label.config(
            text=f"You: {self.player_score}  |  Computer: {self.computer_score}  |  Ties: {self.ties}"
        )

    def update_display(self, text_widget, art_text):
        """Helper method to safely update text in the disabled ASCII boxes."""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, art_text)
        text_widget.config(state="disabled")

    def reset_game(self):
        """Resets scores and window layout."""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the scores?"):
            self.player_score = 0
            self.computer_score = 0
            self.ties = 0
            self.score_label.config(text="You: 0  |  Computer: 0  |  Ties: 0")
            self.result_label.config(
                text="Scores cleared! Make your move.", fg="#ecf0f1"
            )

            self.player_display.config(state="normal")
            self.player_display.delete("1.0", tk.END)
            self.player_display.insert(tk.END, "\n\n   YOUR CHOICE\n   APPEARS HERE")
            self.player_display.config(state="disabled")

            self.computer_display.config(state="normal")
            self.computer_display.delete("1.0", tk.END)
            self.computer_display.insert(
                tk.END, "\n\n  COMPUTER CHOICE\n   APPEARS HERE"
            )
            self.computer_display.config(state="disabled")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = RockPaperScissorsGUI(main_root)
    main_root.mainloop()
