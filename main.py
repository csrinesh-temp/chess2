import pygame
import main
import chess.engine

pygame.init()

WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
GREEN = (118, 150, 86)
HIGHLIGHT = (186, 202, 68)
piece_images = {}
pieces = ['p', 'r', 'n', 'b', 'q', 'k']
colors = ['w', 'b']
for color in colors:
    for piece in pieces:
        image = pygame.image.load(f"images/{color}{piece}.png")
        piece_images[color + piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

board = main.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Move Chess Variant")
selected_square = None
move_history = []
current_turn_moves = []
game_over = False

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = main.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                piece_str = piece.symbol()
                color = 'w' if piece_str.isupper() else 'b'
                screen.blit(piece_images[color + piece_str.lower()], (col * SQ_SIZE, row * SQ_SIZE))

def highlight_moves(moves):
    for move in moves:
        row, col = 7 - main.square_rank(move.to_square), main.square_file(move.to_square)
        pygame.draw.circle(screen, HIGHLIGHT, (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2), 15)

def is_check_delivered():
    return board.is_check()

def handle_click(pos):
    global selected_square, move_history, current_turn_moves, game_over

    if game_over:
        return

    col, row = pos[0] // SQ_SIZE, pos[1] // SQ_SIZE
    square = main.square(col, 7 - row)

    if selected_square is None:
        piece = board.piece_at(square)
        if piece and piece.color == board.turn:
            selected_square = square
    else:
        move = main.Move(selected_square, square)
        for legal_move in board.legal_moves:
            if move == legal_move:
                board.push(move)
                current_turn_moves.append(move)
                if is_check_delivered():
                    move_history.append(current_turn_moves)
                    current_turn_moves = []
                if len(current_turn_moves) == 2:
                    move_history.append(current_turn_moves)
                    current_turn_moves = []
                    break
                selected_square = None
def check_game_over():
    global game_over
    if board.is_checkmate() or board.is_stalemate():
        game_over = True
running = True
while running:
    draw_board()
    draw_pieces()

    if selected_square:
        legal_moves = [m for m in board.legal_moves if m.from_square == selected_square]
        highlight_moves(legal_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    check_game_over()
    pygame.display.flip()

pygame.quit()

