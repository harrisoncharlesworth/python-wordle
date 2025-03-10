#!/usr/bin/env python3
"""
Wordle Game - Command Line Interface
A Python implementation of the popular word-guessing game.
"""

import typer
from rich.console import Console
from rich.panel import Panel

from game.wordle import WordleGame
from ui.display import GameDisplay
from utils.config import GameConfig

app = typer.Typer(help="Wordle - A command line word guessing game")
console = Console()

@app.command()
def play(
    daily: bool = typer.Option(
        False,
        "--daily",
        "-d",
        help="Play the daily challenge word",
    ),
    hard_mode: bool = typer.Option(
        False,
        "--hard",
        "-h",
        help="Play in hard mode - must use revealed hints",
    ),
) -> None:
    """Start a new game of Wordle."""
    config = GameConfig(daily_mode=daily, hard_mode=hard_mode)
    game = WordleGame(config)
    display = GameDisplay(console)
    
    display.show_welcome()
    
    while not game.is_finished:
        display.show_board(game.board)
        guess = display.get_guess()
        result = game.make_guess(guess)
        display.show_result(result)
    
    display.show_game_over(game.stats)

if __name__ == "__main__":
    app() 