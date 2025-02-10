import os
import tkinter as tk
from tkinter import Canvas, PhotoImage, Label, Button
import chess
import chess.engine

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("chess\u00B2")
        self.board = chess.Board()
        self.sq_size = int(75)
        self.canvas = Canvas(root, width=self.sq_size*8, height=self.sq_size*8)
        self.canvas.pack(side=tk.LEFT)
        self.eval_bar = Canvas(root, width=100, height=self.sq_size*8, bg='gray')
        self.eval_bar.pack(side=tk.RIGHT)
        self.eval_label = Label(root, text="", font=("Helvetica", 12))
        self.eval_label.pack()
        self.reset_button = Button(root, text="Reset Board", command=self.reset_board)
        self.reset_button.pack()
        self.selected_square = None
        self.piece_images = {}
        self.load_images()
        self.create_board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.analysis_depth = 15

    def load_images(self):
        pieces = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
        map = {'K': 'wk', 'Q': 'wq', 'R': 'wr', 'B': 'wb', 'N': 'wkn', 'P': 'wp',
               'k': 'bk', 'q': 'bq', 'r': 'br', 'b': 'bb', 'n': 'bkn', 'p': 'bp'}
        for piece in pieces:
            piece_name = map.get(piece, None)
            self.piece_images[piece] = PhotoImage(file=os.path.join('images', f'{piece_name}.png'))

    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'goldenrod'
                self.canvas.create_rectangle(col * self.sq_size, row * self.sq_size,
                                             (col + 1) * self.sq_size, (row + 1) * self.sq_size, fill=color)

        self.update_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

    def update_pieces(self):
        self.canvas.delete("piece")
        piece_symbols = self.board.piece_map()
        for square, piece in piece_symbols.items():
            x = chess.square_file(square) * self.sq_size
            y = (7 - chess.square_rank(square)) * self.sq_size
            image = self.piece_images[piece.symbol()]
            self.canvas.create_image(x + self.sq_size // 2, y + self.sq_size // 2, image=image, tags="piece")

    def on_click(self, event):
        col = event.x // self.sq_size
        row = 7 - (event.y // self.sq_size)
        clicked_square = chess.square(col, row)

        if self.selected_square is None:
            if self.board.piece_at(clicked_square) is not None:
                self.selected_square = clicked_square
                print(f"Selected: {chess.square_name(clicked_square)}")
        else:
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                print(f"Moved from {chess.square_name(self.selected_square)} to {chess.square_name(clicked_square)}")
                self.selected_square = None
                self.update_pieces()
                self.update_eval_bar()
            else:
                print(f"Invalid move from {chess.square_name(self.selected_square)} to {chess.square_name(clicked_square)}")
                self.selected_square = None

    def update_eval_bar(self):
        self.eval_bar.delete("eval")
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=self.analysis_depth))
        score = info["score"].relative.score(mate_score=10000)
        if score is not None:
            self.eval_label.config(text=f"Score: {score} centipawns")
            mid_position = self.sq_size * 4
            max_eval = 20
            eval_score = max(-max_eval * 100, min(max_eval * 100, score))
            eval_y = mid_position - (eval_score / (max_eval * 100) * mid_position)
            self.eval_bar.create_rectangle(0, eval_y, 100, self.sq_size*8, fill='black', tags="eval")

    def reset_board(self):
        self.board.reset()
        self.update_pieces()
        self.eval_label.config(text="")
        self.eval_bar.delete("eval")

    def __del__(self):
        self.engine.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
