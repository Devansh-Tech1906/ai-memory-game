# 🧠 Smart AI Memory Game

## 1. Brief Description
A modern take on the classic Memory Card matching game, but with a major twist: you play against a "Smart AI" opponent. Instead of just guessing randomly, the AI actively watches your moves, remembers the cards you flip over, and strategically uses that photographic memory to steal your matches if you leave a pair exposed!

## 2. Technologies
* **Python 3:** The core programming language.
* **Tkinter:** Python's built-in GUI library used to build the visual interface and handle mouse-click events. (No external installations required!)

## 3. Features
* **🧠 "Smart AI" Opponent:** An algorithm that uses a Python Dictionary to log and track every card revealed on the board, allowing it to make strategic, guaranteed matches.
* **🌙 Modern GUI:** A sleek, dark-mode "frosted glass" aesthetic with flat design and hover effects.
* **📊 Live Scoreboard:** A dynamic scoreboard that tracks points and clearly indicates whose turn it is.
* **🔀 Dynamic Boards:** The 16-card grid uses a randomized layout of emoji pairs every single time you play.

## 4. Keyboard Shortcuts
This game is designed to be fully accessible via mouse. 
* **Left Click:** Reveal a card.
* *(Note: There are no keyboard shortcuts required to play this game.)*

## 5. The Process
I built this project iteratively. 
1. I started by planning the core game loop and state management (tracking which cards were flipped vs. matched).
2. I built the visual interface using Tkinter, moving from standard 3D buttons to a cleaner, modern dark-mode aesthetic. 
3. The final and most complex phase was designing the AI logic. I had to transition the AI from making simple random guesses to actually logging data into a "memory" dictionary and evaluating that data before making its moves.

## 6. What I Learned
Building this game was a fantastic exercise in logical structuring and GUI development. Key takeaways include:
* **Event-Driven Programming:** Shifting from standard `while` loops to writing code that waits and responds to user mouse clicks.
* **State Management:** Keeping visual elements on the screen perfectly synced with internal backend variables (like tracking indices in Python lists).
* **Asynchronous Timing:** Using Tkinter's `.after()` method to create timed delays (like letting you look at mismatched cards for 1 second) without freezing or crashing the entire application window.

## 7. Improvements
Future updates to this project could include:
* **Difficulty Levels:** Limiting the AI's memory capacity (e.g., it only remembers the last 4 cards) so it isn't impossible to beat.
* **Theme Selector:** A main menu to let the player choose different emoji decks (Fruits, Animals, Games, etc.).
* **Audio Feedback:** Adding simple sound effects for flipping cards, finding a match, and winning/losing the game.

## 8. How to Run the Project
Because this uses Python's built-in libraries, running it is incredibly simple!

1. Make sure you have **Python 3** installed on your computer.
2. Clone this repository or download the `main.py` file.
3. Open your terminal or command prompt.
4. Navigate to the folder where you saved the file.
5. Run the following command:
   ```bash
   python main.py
