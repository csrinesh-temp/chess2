import random
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
        self.game_over = False

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
        self.initialize_eval_bar()
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
        if self.game_over:
            return

        col = event.x // self.sq_size
        row = 7 - (event.y // self.sq_size)
        clicked_square = chess.square(col, row)

        if self.selected_square is None:
            if self.board.piece_at(clicked_square) is not None:
                self.selected_square = clicked_square
        else:
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.update_pieces()
                self.update_eval_bar()
                if self.board.is_checkmate():
                    self.eval_label.config(text="CHECKMATE!")
                    self.game_over = True
                    self.drop_confetti()
                elif self.board.is_stalemate():
                    self.eval_label.config(text="STATEMATE!")
                    self.game_over = True
            else:
                self.selected_square = None

    def update_eval_bar(self):
        self.eval_bar.delete("border")
        self.eval_bar.delete("eval")

        self.eval_bar.create_rectangle(
            0, 0, 100, self.sq_size * 8, outline='black', tags="border"
        )

        info = self.engine.analyse(self.board, chess.engine.Limit(depth=self.analysis_depth))
        score = info["score"].relative.score(mate_score=10000)

        if score is not None:
            mid_position = self.sq_size * 4
            max_eval = 20
            eval_score = max(-max_eval * 100, min(max_eval * 100, score))
            eval_y = mid_position - (eval_score / (max_eval * 100) * mid_position)

            self.eval_bar.create_rectangle(
                1, 1, 99, self.sq_size * 8 - 1, outline='', fill='#6666FF', tags="background"
            )

            self.eval_bar.create_rectangle(
                1, eval_y, 99, self.sq_size * 8 - 1, outline='', fill='black', tags="eval"
            )

    def initialize_eval_bar(self):
        self.eval_bar.delete("border")
        self.eval_bar.delete("eval")

        self.eval_bar.create_rectangle(
            0, 0, 100, self.sq_size * 8, outline='black', tags="border"
        )

        self.eval_bar.create_rectangle(
            1, 1, 99, self.sq_size * 8 - 1, outline='', fill='#6666FF', tags="background"
        )

        mid_position = self.sq_size * 4
        self.eval_bar.create_rectangle(
            1, mid_position, 99, self.sq_size * 8 - 1, outline='', fill='black', tags="eval"
        )

    def reset_board(self):
        self.board.reset()
        self.update_pieces()
        self.initialize_eval_bar()
        self.eval_label.config(text="")
        self.game_over = False
        self.remove_confetti()

    def drop_confetti(self):
        self.confetti_particles = []
        for _ in range(100):
            x = random.randint(0, self.sq_size * 8)
            y = random.randint(-80, 0)
            dx = random.uniform(-1, 1)
            dy = random.uniform(2, 5)
            color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
            particle = {
                'rectangle': self.canvas.create_rectangle(x, y, x+4, y+4, fill=color, outline=''),
                'dx': dx,
                'dy': dy
            }
            self.confetti_particles.append(particle)
        self.animate_confetti()

    def animate_confetti(self):
        for particle in self.confetti_particles:
            self.canvas.move(particle['rectangle'], particle['dx'], particle['dy'])
            pos = self.canvas.coords(particle['rectangle'])
            if pos[3] > self.sq_size * 8:
                self.canvas.moveto(particle['rectangle'], random.randint(0, self.sq_size * 8), random.randint(-80, 0))
        if self.game_over:
            self.root.after(50, self.animate_confetti)

    def remove_confetti(self):
        for particle in self.confetti_particles:
            self.canvas.delete(particle['rectangle'])
        self.confetti_particles = []

    def __del__(self):
        self.engine.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
