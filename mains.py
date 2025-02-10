import tkinter as tk
from tkinter import Canvas
import chess

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess")
        self.board = chess.Board()
        self.canvas = Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.sq_size = 50
        self.selected_square = None
        self.create_board()
        
    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
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
            self.canvas.create_text(x + self.sq_size // 2, y + self.sq_size // 2, text=piece.symbol(), tags="piece", font=("Arial", 24))

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
            else:
                print(f"Invalid move from {chess.square_name(self.selected_square)} to {chess.square_name(clicked_square)}")
                self.selected_square = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()