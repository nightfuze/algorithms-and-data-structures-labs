"""
Требуется написать игру Крестики-Нолики с использованием граафической библиотекки tkinter.

"""

import tkinter as tk
from tkinter import ttk
from typing import List

PRIMARY_COLOR = "#39BEAD"
SECONDARY_COLOR = "#2FA293"
DARK_TEXT_COLOR = "#535353"
LIGHT_TEXT_COLOR = "#F3ECD5"
BG_COLOR = "#191919"


def is_moves_left(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                return True
    return False


def evaluate(board, player, opponent):
    size = len(board)
    score = 1

    for row in board:
        if row.count(player) == size:
            return score
        if row.count(opponent) == size:
            return -score

    for col in range(size):
        column = [board[row][col] for row in range(size)]
        if column.count(player) == size:
            return score
        if column.count(opponent) == size:
            return -score

    diagonal1 = [board[i][i] for i in range(size)]
    diagonal2 = [board[i][size - i - 1] for i in range(size)]
    if diagonal1.count(player) == size:
        return score
    if diagonal1.count(opponent) == size:
        return -score
    if diagonal2.count(player) == size:
        return score
    if diagonal2.count(opponent) == size:
        return -score

    return 0


def minimax(board, is_max, player, opponent):
    score = evaluate(board, player, opponent)
    if score == 1:
        return score
    if score == -1:
        return score
    if not is_moves_left(board):
        return 0
    size = len(board)
    if is_max:
        value = -1
        for row in range(size):
            for col in range(size):
                if board[row][col] == ' ':
                    board[row][col] = player
                    value = max(value, minimax(board, not is_max, player, opponent))
                    board[row][col] = ' '
        return value
    else:
        value = 1
        for row in range(size):
            for col in range(size):
                if board[row][col] == ' ':
                    board[row][col] = opponent
                    value = min(value, minimax(board, not is_max, player, opponent))
                    board[row][col] = ' '
        return value


def find_best_move(board, player):
    # print(board)
    opponent = 'X' if player == 'O' else 'O'
    best_val = -1
    best_move = (-1, -1)
    size = len(board)
    # start_time = perf_counter()

    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = player
                move_val = minimax(board, False, player, opponent)
                # print(move_val)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    # end_time = perf_counter()
    # print(end_time - start_time)
    # print("best move: " + str(best_move))

    return best_move


class Cell(tk.Frame):
    def __init__(self, parent, row, col, on_click):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.button = tk.Button(self, text=" ", width=4, highlightthickness=0, borderwidth=0, bg=PRIMARY_COLOR,
                                activebackground=PRIMARY_COLOR, fg="white", activeforeground="white", height=2,
                                font=("Sans", 32), padx=0, command=self.click)
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
        super().__init__(parent, bg=SECONDARY_COLOR, width=10, height=10, borderwidth=1)
        self.size = size
        self.callback = on_cell_click
        self.data: List[List[Cell]] = [[Cell(self, row, col, on_cell_click) for col in range(self.size)] for row in
                                       range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                self.data[row][col].grid(row=row, column=col, padx=5, pady=5)

    def get_size(self):
        return self.size

    def set_size(self, size):
        for row in range(self.size):
            for col in range(self.size):
                self.data[row][col].grid_forget()

        self.size = size
        self.data = [[Cell(self, row, col, self.callback) for col in range(self.size)] for row in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                self.data[row][col].grid(row=row, column=col, padx=5, pady=5)

    def is_cell_empty(self, row, col):
        return self.data[row][col].get_text() == " "

    def get_data(self):
        return [[row.get_text() for row in col] for col in self.data]

    def set_player(self, player, row, col, color=LIGHT_TEXT_COLOR):
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
        super().__init__(parent, padx=16, pady=8, bg=BG_COLOR, highlightbackground="#2e3032",
                         highlightthickness=2)
        self.player = tk.StringVar(value=player)
        self.score = tk.IntVar(value=0)
        self.label_player = tk.Label(self, textvariable=self.player, bg=BG_COLOR, fg="white", font=("Sans", 16))
        self.label_player.pack(side="left", padx=(0, 30))
        self.label_score = tk.Label(self, textvariable=self.score, bg=BG_COLOR, fg="#91a0a0", font=("Sans", 16))
        self.label_score.pack(side="right", padx=(30, 0))

    def activate(self):
        self.configure(highlightbackground=PRIMARY_COLOR)

    def deactivate(self):
        self.configure(highlightbackground="#2e3032")

    def increment(self):
        self.score.set(self.score.get() + 1)

    def reset(self):
        self.score.set(0)


class ResultDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PRIMARY_COLOR)
        self.label_x_winner = tk.Label(self, text="X", font=("Sans", 152, "bold"), bg=PRIMARY_COLOR, fg=DARK_TEXT_COLOR)
        self.label_o_winner = tk.Label(self, text="O", font=("Sans", 152, "bold"), bg=PRIMARY_COLOR,
                                       fg=LIGHT_TEXT_COLOR)
        self.frame_draw = tk.Frame(self)
        label_draw_x_winner = tk.Label(self.frame_draw, text="X", font=("Sans", 152, "bold"), bg=PRIMARY_COLOR,
                                       fg=DARK_TEXT_COLOR)
        label_draw_x_winner.pack(side="left")
        label_draw_o_winner = tk.Label(self.frame_draw, text="O", font=("Sans", 152, "bold"), bg=PRIMARY_COLOR,
                                       fg=LIGHT_TEXT_COLOR)
        label_draw_o_winner.pack(side="left")
        self.label_text = tk.Label(self, text="", font=("Sans", 52, "bold"), bg=PRIMARY_COLOR, fg=DARK_TEXT_COLOR)
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
        super().__init__(parent, bg=PRIMARY_COLOR)
        self.pack(fill=tk.BOTH, expand=True)

        self.winner = None
        self.game_over = False
        self.game_mode = tk.StringVar(self, value="Против компьютера")

        self.result_screen = ResultDisplay(self)

        self.current_player = tk.StringVar(self, value="X")
        self.current_player_color = DARK_TEXT_COLOR

        self.top_bar = tk.Frame(self, bg=BG_COLOR, pady=16)
        self.top_bar.pack(side="top", fill=tk.BOTH)

        self.game_mode_combobox = ttk.Combobox(self.top_bar, textvariable=self.game_mode,
                                               values=["Против компьютера", "Против игрока"], state="readonly",
                                               font=("Sans", 12), justify="center", width=20)
        self.game_mode_combobox.place(relx=0.03, rely=0.25, anchor="nw")
        self.game_mode_combobox.bind("<<ComboboxSelected>>", self.on_game_mode_change)

        self.frame_score_info = tk.Frame(self.top_bar, bg=BG_COLOR)
        self.frame_score_info.pack(pady=16)

        self.one_player_score = Score(self.frame_score_info, "X")
        self.one_player_score.pack(side="left", padx=(0, 10))
        self.one_player_score.activate()

        self.two_player_score = Score(self.frame_score_info, "O")
        self.two_player_score.pack(side="right", padx=(10, 0))

        self.frame_move_info = tk.Frame(self.top_bar)
        self.frame_move_info.pack()

        self.move_text = tk.StringVar(self, value="Ходит")
        self.label_move_text = tk.Label(self.frame_move_info, textvariable=self.move_text, fg="#91a0a0", bg=BG_COLOR)
        self.label_move_text.pack(side="left")

        self.label_move_player = tk.Label(self.frame_move_info, textvariable=self.current_player, fg="white",
                                          bg=BG_COLOR)
        self.label_move_player.pack(side="right")

        self.board = Board(self, on_cell_click=self.on_cell_click)
        self.board.place(relx=0.5, rely=0.5, anchor="center")

        self.bottom_bar = tk.Frame(self, bg=BG_COLOR, pady=16)
        self.bottom_bar.pack(side="bottom", fill=tk.BOTH)

        self.reset_btn = tk.Button(self.bottom_bar, text="Начать заново", command=self.reset_game, bg=BG_COLOR,
                                   fg=PRIMARY_COLOR, highlightthickness=0, borderwidth=0, activebackground=BG_COLOR,
                                   activeforeground=SECONDARY_COLOR, font=("Sans", 16, "bold"))
        self.reset_btn.pack()

    def on_game_mode_change(self, event):
        self.reset_game()
        self.reset_score()

    def on_cell_click(self, row, col):
        if self.game_over or not self.board.is_cell_empty(row, col):
            return
        if self.game_mode.get() == "Против игрока":
            self.board.set_player(self.current_player.get(), row, col, self.current_player_color)
            self.change_player()
        else:
            self.board.set_player(self.current_player.get(), row, col, self.current_player_color)
            self.change_player()
            self.ai_move()
            self.change_player()

    def ai_move(self):
        board_data = self.board.get_data()
        move = find_best_move(board_data, "O")
        self.board.set_player(self.current_player.get(), move[0], move[1], LIGHT_TEXT_COLOR)

    def check_winner(self):
        if self.board.check_winner(self.current_player.get()):
            self.winner = self.current_player.get()
            self.game_over = True
        elif self.board.check_draw():
            self.game_over = True

    def change_player(self):
        self.check_winner()
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
            self.current_player_color = LIGHT_TEXT_COLOR
            self.one_player_score.deactivate()
            self.two_player_score.activate()
        else:
            self.current_player.set("X")
            self.current_player_color = DARK_TEXT_COLOR
            self.one_player_score.activate()
            self.two_player_score.deactivate()

    def reset_score(self):
        self.one_player_score.reset()
        self.two_player_score.reset()

    def reset_game(self):
        self.board.place(relx=0.5, rely=0.5, anchor="center")
        self.result_screen.place_forget()
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.label_move_player.pack()
        self.move_text.set("Ходит")
        self.current_player.set("X")
        self.current_player_color = DARK_TEXT_COLOR
        self.one_player_score.activate()
        self.two_player_score.deactivate()

    def run(self):
        self.mainloop()


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Крестики-Нолики")
        self.geometry("800x600")

        combostyle = ttk.Style()
        combostyle.theme_create('combostyle',
                                settings={'TCombobox': {
                                    'configure': {
                                        'selectbackground': DARK_TEXT_COLOR,
                                        'fieldbackground': DARK_TEXT_COLOR,
                                        'background': PRIMARY_COLOR,
                                        'foreground': 'white',
                                        'padding': 5,
                                        'arrowcolor': PRIMARY_COLOR,
                                        'relief': 'flat',
                                        'font': ('Sans', 16),
                                        'highlightthickness': 0,
                                        'borderwidth': 0,
                                    }
                                }})
        combostyle.theme_use('combostyle')

        self.option_add('*TCombobox*Listbox.background', BG_COLOR)
        self.option_add('*TCombobox*Listbox.foreground', 'white')
        self.option_add('*TCombobox*Listbox.selectBackground', DARK_TEXT_COLOR)
        self.option_add('*TCombobox*Listbox.selectForeground', PRIMARY_COLOR)
        # self.option_add('*TCombobox*Listbox.highlightColor', PRIMARY_COLOR)
        self.option_add('*TCombobox*Listbox.highlightThickness', 0)
        self.option_add('*TCombobox*Listbox.font', ("Sans", 12))


if __name__ == "__main__":
    window = Window()
    game = TicTacToe(window)
    game.run()
