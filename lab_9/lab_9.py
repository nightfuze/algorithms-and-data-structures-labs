"""
Требуется написать игру Крестики-Нолики с использованием граафической библиотекки tkinter.

"""

import tkinter as tk
from typing import List


class Cell(tk.Frame):
    def __init__(self, parent, row, col, on_click):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.button = tk.Button(self, text=" ", width=4, highlightthickness=0, borderwidth=0, bg="#39bead",
                                activebackground="#39bead", fg="white", activeforeground="white", height=2,
                                font=("Sans", 46), padx=0, command=self.click)
        self.button.pack()
        self.on_click = on_click

    def click(self):
        self.on_click(self.row, self.col)

    def set_text(self, text):
        if self.button["text"] == " ":
            self.button.configure(text=text)

    def get_text(self):
        return self.button["text"]

    def clear(self):
        self.button.configure(text=" ")

    def set_color(self, color):
        self.button.configure(fg=color, activeforeground=color)


class Board(tk.Frame):
    def __init__(self, parent, size=3, on_cell_click=None):
        super().__init__(parent, bg="#2fa293", width=10, height=10, borderwidth=1)
        self.size = size
        self.data: List[List[Cell]] = [[Cell(self, row, col, on_cell_click) for col in range(self.size)] for row in
                                       range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                self.data[row][col].grid(row=row, column=col, padx=5, pady=5)

    def set_player(self, player, row, col, color="#f3ecd5"):
        self.data[row][col].set_text(player)
        self.data[row][col].set_color(color)

    def reset(self):
        for row in range(self.size):
            for col in range(self.size):
                self.data[row][col].clear()

    def check_winner(self, player) -> bool:
        return self.check_rows(player) or self.check_cols(player) or self.check_diags(player)

    def is_full(self) -> bool:
        return all([self.data[row][col].get_text() != " " for col in range(self.size) for row in range(self.size)])

    def check_draw(self):
        return self.is_full() and not self.check_winner("X") and not self.check_winner("O")

    def check_rows(self, player) -> bool:
        for row in range(self.size):
            if all([self.data[row][col].get_text() == player for col in range(self.size)]):
                return True
        return False

    def check_cols(self, player) -> bool:
        for col in range(self.size):
            if all([self.data[row][col].get_text() == player for row in range(self.size)]):
                return True
        return False

    def check_diags(self, player) -> bool:
        return self.check_main_diag(player) or self.check_side_diag(player)

    def check_main_diag(self, player) -> bool:
        return all([self.data[row][row].get_text() == player for row in range(self.size)])

    def check_side_diag(self, player) -> bool:
        return all([self.data[row][self.size - row - 1].get_text() == player for row in range(self.size)])


class Score(tk.Frame):
    def __init__(self, parent, player):
        super().__init__(parent, padx=16, pady=8, bg="#191919", highlightbackground="#2e3032",
                         highlightthickness=2)
        self.player = tk.StringVar(value=player)
        self.score = tk.IntVar(value=0)
        self.label_player = tk.Label(self, textvariable=self.player, bg="#191919", fg="white", font=("Sans", 16))
        self.label_player.pack(side="left", padx=(0, 30))
        self.label_score = tk.Label(self, textvariable=self.score, bg="#191919", fg="#91a0a0", font=("Sans", 16))
        self.label_score.pack(side="right", padx=(30, 0))

    def activate(self):
        self.configure(highlightbackground="#39bead")

    def deactivate(self):
        self.configure(highlightbackground="#2e3032")

    def increment(self):
        self.score.set(self.score.get() + 1)


class ResultDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#39bead")
        self.label_x_winner = tk.Label(self, text="X", font=("Sans", 152, "bold"), bg="#39bead", fg="#535353")
        self.label_o_winner = tk.Label(self, text="O", font=("Sans", 152, "bold"), bg="#39bead", fg="#f3ecd5")
        self.frame_draw = tk.Frame(self)
        label_draw_x_winner = tk.Label(self.frame_draw, text="X", font=("Sans", 152, "bold"), bg="#39bead",
                                       fg="#535353")
        label_draw_x_winner.pack(side="left")
        label_draw_o_winner = tk.Label(self.frame_draw, text="O", font=("Sans", 152, "bold"), bg="#39bead",
                                       fg="#f3ecd5")
        label_draw_o_winner.pack(side="left")
        self.label_text = tk.Label(self, text="", font=("Sans", 52, "bold"), bg="#39bead", fg="#535353")
        self.label_x_winner.pack()
        self.label_o_winner.pack()
        self.label_text.pack()

    def set_winner(self, winner: str):
        self.label_text.pack_forget()
        self.label_x_winner.pack_forget()
        self.label_o_winner.pack_forget()
        self.frame_draw.pack_forget()
        if winner:
            if winner == "X":
                self.label_x_winner.pack()
            else:
                self.label_o_winner.pack()
            self.label_text.configure(text="ПОБЕДИТЕЛЬ!")
        else:
            self.frame_draw.pack()
            self.label_text.configure(text="НИЧЬЯ!")
        self.label_text.pack()


class TicTacToe(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#39bead")
        self.pack(fill=tk.BOTH, expand=True)

        self.winner = None
        self.game_over = False

        self.result_screen = ResultDisplay(self)

        self.current_player = tk.StringVar(self, value="X")
        self.current_player_color = "#535353"

        self.top_bar = tk.Frame(self, bg="#191919", pady=16)
        self.top_bar.pack(side="top", fill=tk.BOTH)

        self.frame_score_info = tk.Frame(self.top_bar, bg="#191919")
        self.frame_score_info.pack(pady=16)

        self.one_player_score = Score(self.frame_score_info, "X")
        self.one_player_score.pack(side="left", padx=(0, 10))
        self.one_player_score.activate()

        self.two_player_score = Score(self.frame_score_info, "O")
        self.two_player_score.pack(side="right", padx=(10, 0))

        self.frame_move_info = tk.Frame(self.top_bar)
        self.frame_move_info.pack()

        self.move_text = tk.StringVar(self, value="Ходит")
        self.label_move_text = tk.Label(self.frame_move_info, textvariable=self.move_text, fg="#91a0a0", bg="#191919")
        self.label_move_text.pack(side="left")

        self.label_move_player = tk.Label(self.frame_move_info, textvariable=self.current_player, fg="white",
                                          bg="#191919")
        self.label_move_player.pack(side="right")

        self.board = Board(self, on_cell_click=self.on_cell_click)
        self.board.place(relx=0.5, rely=0.5, anchor="center")

        self.bottom_bar = tk.Frame(self, bg="#191919", pady=16)
        self.bottom_bar.pack(side="bottom", fill=tk.BOTH)

        self.reset_btn = tk.Button(self.bottom_bar, text="Начать заново", command=self.reset_game, bg="#191919",
                                   fg="#39bead", highlightthickness=0, borderwidth=0, activebackground="#191919",
                                   activeforeground="#2fa293", font=("Sans", 16, "bold"))
        self.reset_btn.pack()

    def on_cell_click(self, row, col):
        if self.game_over:
            return
        self.board.set_player(self.current_player.get(), row, col, self.current_player_color)
        if self.board.check_winner(self.current_player.get()):
            self.winner = self.current_player.get()
            self.game_over = True
        elif self.board.check_draw():
            self.game_over = True
        self.change_player()

    def change_player(self):
        if self.game_over:
            self.board.place_forget()
            self.result_screen.set_winner(self.winner)
            self.result_screen.place(relx=0.5, rely=0.5, anchor="center")
            self.move_text.set("Игра окончена")
            self.label_move_player.pack_forget()

            if self.winner == "X":
                self.one_player_score.increment()
            elif self.winner == "O":
                self.two_player_score.increment()

        elif self.current_player.get() == "X":
            self.current_player.set("O")
            self.current_player_color = "#f3ecd5"
            self.one_player_score.deactivate()
            self.two_player_score.activate()
        else:
            self.current_player.set("X")
            self.current_player_color = "#535353"
            self.one_player_score.activate()
            self.two_player_score.deactivate()

    def reset_game(self):
        self.board.place(relx=0.5, rely=0.5, anchor="center")
        self.result_screen.place_forget()
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.label_move_player.pack()
        self.move_text.set("Ходит")
        self.current_player.set("X")
        self.current_player_color = "#535353"
        self.one_player_score.activate()
        self.two_player_score.deactivate()

    def run(self):
        self.mainloop()


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Крестики-Нолики")
        self.geometry("1280x800")


if __name__ == "__main__":
    window = Window()
    game = TicTacToe(window)
    game.run()
