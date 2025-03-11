from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from game.wordle import GuessResult, LetterState, Wordle

class WordleUI:
    """Handles the display of the Wordle game in the terminal."""

    def __init__(self):
        self.console = Console()
        
    def display_game(self, game: Wordle):
        """Display the current game state."""
        self._clear_screen()
        self._display_header()
        self._display_board(game)
        self._display_keyboard(game)
        self._display_status(game)
        
    def _clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()
        
    def _display_header(self):
        """Display the game header."""
        header = Panel.fit(
            Text("WORDLE", style="bold white", justify="center"),
            style="green"
        )
        self.console.print(header)
        self.console.print()
        
    def _display_board(self, game: Wordle):
        """Display the game board with guesses."""
        table = Table(
            show_header=False,
            show_lines=False,
            box=None,
            padding=(0, 1)
        )
        
        # Add guesses
        for attempt in game.attempts:
            row = self._format_guess(attempt)
            table.add_row(*row)
            
        # Add empty rows for remaining attempts
        for _ in range(game.remaining_attempts):
            table.add_row(*["⬜️" * 5])
            
        self.console.print(table)
        self.console.print()
        
    def _format_guess(self, guess: GuessResult) -> List[str]:
        """Format a guess with colored squares."""
        result = []
        for letter, state in zip(guess.word, guess.states):
            if state == LetterState.CORRECT:
                result.append("🟩")
            elif state == LetterState.PRESENT:
                result.append("🟨")
            else:
                result.append("⬛️")
        return result
        
    def _display_keyboard(self, game: Wordle):
        """Display the keyboard with color-coded keys."""
        keyboard = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        # Build letter states from all guesses
        letter_states = {}
        for attempt in game.attempts:
            for letter, state in zip(attempt.word, attempt.states):
                if letter not in letter_states or state == LetterState.CORRECT:
                    letter_states[letter] = state
                    
        # Display keyboard rows
        for row in keyboard:
            text = Text()
            for letter in row:
                letter = letter.lower()
                if letter in letter_states:
                    state = letter_states[letter]
                    if state == LetterState.CORRECT:
                        text.append(letter.upper(), style="bold green")
                    elif state == LetterState.PRESENT:
                        text.append(letter.upper(), style="bold yellow")
                    else:
                        text.append(letter.upper(), style="bold dim")
                else:
                    text.append(letter.upper(), style="bold")
                text.append(" ")
            self.console.print(text, justify="center")
        self.console.print()
        
    def _display_status(self, game: Wordle):
        """Display game status and remaining attempts."""
        if game.game_over:
            if game.won:
                msg = Text("Congratulations! You won! 🎉", style="bold green")
            else:
                msg = Text(f"Game Over! The word was {game.word.upper()}", style="bold red")
        else:
            msg = Text(f"Remaining attempts: {game.remaining_attempts}", style="bold blue")
            
        self.console.print(msg, justify="center")
        self.console.print() 