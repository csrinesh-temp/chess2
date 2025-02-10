# Chess² Application

Chess² is a graphical chess interface built using Python, `tkinter`, and the `chess` Python library. It allows players to interact with a chessboard, make moves, and receive evaluation insights supported by the Stockfish chess engine.

## Features

- **Basic Chess GUI**: Allows users to interact with a visual chessboard to play a game of chess.
- **Move Validation**: Ensures only legal chess moves are executed on the board.
- **Stockfish Integration**: Provides real-time game evaluation using the Stockfish engine.
- **Evaluation Bar**: Visual representation of the evaluation score from Stockfish, indicating which side has an advantage.
- **Board Reset**: Quickly reset the game to start a new match.
- **Piece Images**: Displays aesthetically pleasing images for each of the chess pieces.

## Requirements

- Python 3.x
- `tkinter` library for GUI elements
- `chess` library for managing chess logic
- Stockfish engine for move analysis

## Installation

1. **Clone the Repository**:  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/chess-app.git
   cd chess-app
   ```

2. **Install Required Python Libraries**:  
   Ensure you have `tkinter` and `chess` installed. You can install `chess` via pip:
   ```bash
   pip install python-chess
   ```

3. **Install Stockfish**:  
   Ensure Stockfish is installed and accessible at `/usr/local/bin/stockfish`. You can download it from [Stockfish's official website](https://stockfishchess.org/download/).

4. **Prepare Piece Images**:  
   Ensure there's an `images/` directory containing PNG images for chess pieces (e.g., `wp.png`, `wk.png`, `bp.png`, etc.)

## Usage

1. **Run the Application**:  
   Start the application by running the Python script:
   ```bash
   python main.py
   ```

2. **Play Chess**:  
   - Click a piece to select it and make a valid move by clicking another square.
   - The application will visualize the move and update the board, displaying a real-time evaluation score.
   - Use the "Reset Board" button to start a new game at any time.

## License

This project is open-source and available under the MIT license. Feel free to modify and contribute!

## Contributing

Contributions are welcome! If you have feedback, suggestions, or improvements, please open an issue or submit a pull request.

## Contact

For further questions or support, please contact the project maintainer at your-email@example.com.

---

Enjoy your game of chess and the power of evaluation with Chess²!