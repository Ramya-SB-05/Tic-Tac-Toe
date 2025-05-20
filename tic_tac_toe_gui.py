import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player_starts = "X"
        self.play_with_robot = False
        self.current_player = None
        self.buttons = [[None]*3 for _ in range(3)]

        self.create_instructions_page()

    def create_instructions_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Welcome to Tic Tac Toe", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        instructions = (
            "Instructions:\n"
            "- 3x3 grid game where players take turns to place X or O.\n"
            "- First to get 3 in a row (horizontal, vertical, diagonal) wins.\n"
            "- If board fills up without a winner, it's a draw.\n"
            "- You can play against another player or the robot.\n"
        )
        instr_label = tk.Label(self.root, text=instructions, font=("Arial", 14), justify="left")
        instr_label.pack(padx=20)

        next_btn = tk.Button(self.root, text="Next", font=("Arial", 16), command=self.create_choice_page)
        next_btn.pack(pady=20)

    def create_choice_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Choose Game Settings", font=("Arial", 20, "bold"))
        title.pack(pady=15)

        # Who starts first
        start_frame = tk.LabelFrame(self.root, text="Who plays first?", font=("Arial", 14))
        start_frame.pack(pady=10)

        self.first_player_var = tk.StringVar(value="X")
        tk.Radiobutton(start_frame, text="Player X", variable=self.first_player_var, value="X", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(start_frame, text="Player O", variable=self.first_player_var, value="O", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)

        # Play mode (vs player or vs robot)
        mode_frame = tk.LabelFrame(self.root, text="Play Mode", font=("Arial", 14))
        mode_frame.pack(pady=10)

        self.play_mode_var = tk.StringVar(value="player")
        tk.Radiobutton(mode_frame, text="Two Players", variable=self.play_mode_var, value="player", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
        tk.Radiobutton(mode_frame, text="Play with Robot", variable=self.play_mode_var, value="robot", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)

        start_btn = tk.Button(self.root, text="Start Game", font=("Arial", 16), command=self.start_game)
        start_btn.pack(pady=20)

    def start_game(self):
        self.player_starts = self.first_player_var.get()
        self.play_with_robot = self.play_mode_var.get() == "robot"
        self.current_player = self.player_starts
        self.create_game_board()

        # If robot starts first, make its move immediately
        if self.play_with_robot and self.current_player == "O":
            self.robot_move()

    def create_game_board(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack()

        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 40), width=5, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.status_label = tk.Label(self.root, text=f"Player {self.current_player}'s turn", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Restart Game", font=("Arial", 14), command=self.reset_game)
        self.reset_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back to Menu", font=("Arial", 14), command=self.back_to_menu)
        self.back_button.pack(pady=5)

    def on_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "" and not self.check_winner():
            btn["text"] = self.current_player
            if self.check_winner():
                self.status_label.config(text=f"Player {self.current_player} wins!")
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.disable_buttons()
            elif self.is_draw():
                self.status_label.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.switch_player()
                if self.play_with_robot and self.current_player == "O":
                    self.root.after(500, self.robot_move)  # Robot moves after 0.5 sec

    def robot_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner():
                self.status_label.config(text=f"Player {self.current_player} (Robot) wins!")
                messagebox.showinfo("Game Over", f"Player {self.current_player} (Robot) wins!")
                self.disable_buttons()
            elif self.is_draw():
                self.status_label.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.switch_player()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s turn")

    def check_winner(self):
        b = self.buttons
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return True
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return True
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return True
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return True
        return False

    def is_draw(self):
        for row in self.buttons:
            for btn in row:
                if btn["text"] == "":
                    return False
        return True

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal")
        self.current_player = self.player_starts
        self.status_label.config(text=f"Player {self.current_player}'s turn")

        # If robot starts first, robot makes the first move
        if self.play_with_robot and self.current_player == "O":
            self.root.after(500, self.robot_move)

    def back_to_menu(self):
        self.create_choice_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()



