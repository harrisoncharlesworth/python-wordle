"""
User interface components for the Wordle game.
"""

from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from game.wordle import GuessResult, LetterResult

class GameDisplay:
    """Handles the display of game elements."""
    
    COLORS = {
        LetterResult.CORRECT: "green",
        LetterResult.PRESENT: "yellow",
        LetterResult.ABSENT: "white"
    }
    
    def __init__(self, console: Console):
        """Initialize the display with a Rich console."""
        self.console = console
    
    def show_welcome(self) -> None:
        """Display the welcome message."""
        welcome_text = """
[bold green]WORDLE[/bold green]
Guess the word in 6 tries.
- Each guess must be a valid 5-letter word
- Colors indicate how close your guess was:
  [green]Green[/green]: Letter is correct and in right position
  [yellow]Yellow[/yellow]: Letter is in word but wrong position
  [white]White[/white]: Letter is not in word
        """
        self.console.print(Panel(welcome_text, title="Welcome"))
    
    def show_board(self, attempts: List[GuessResult]) -> None:
        """Display the current game board."""
        self.console.clear()
        
        for attempt in attempts:
            self._render_guess(attempt)
        
        # Show empty rows for remaining attempts
        remaining = 6 - len(attempts)
        for _ in range(remaining):
            self.console.print("□ □ □ □ □")
        
        self.console.print()
    
    def _render_guess(self, guess: GuessResult) -> None:
        """Render a single guess with colored squares."""
        if not guess.is_valid:
            self.console.print(f"[red]{guess.message}[/red]")
            return
        
        text = Text()
        for letter, result in zip(guess.word.upper(), guess.results):
            color = self.COLORS[result]
            text.append(f" {letter} ", style=f"bold {color} on black")
        
        self.console.print(text)
    
    def get_guess(self) -> str:
        """Get a guess from the user."""
        return self.console.input("\nEnter your guess: ").strip()
    
    def show_result(self, result: GuessResult) -> None:
        """Show the result of a guess."""
        if not result.is_valid and result.message:
            self.console.print(f"[red]{result.message}[/red]")
    
    def show_game_over(self, stats: dict) -> None:
        """Display the game over message."""
        if stats["won"]:
            msg = f"[green]Congratulations! You won in {stats['attempts']} attempts![/green]"
        else:
            msg = f"[red]Game Over! The word was {stats['target_word']}[/red]"
        
        self.console.print(Panel(msg, title="Game Over")) 