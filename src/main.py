#!/usr/bin/env python3
"""
Wordle Game - Command Line Interface
A Python implementation of the popular word-guessing game.
"""

import random
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from game.wordle import Wordle
from ui.game_ui import WordleUI
from utils.config import GameConfig

app = typer.Typer(help="Wordle - A command line word guessing game")
console = Console()

def load_word_list() -> list[str]:
    """Load the word list from data file."""
    word_file = Path(__file__).parent.parent / "data" / "words.txt"
    with open(word_file, "r") as f:
        return [word.strip().lower() for word in f if len(word.strip()) == 5]

@app.command()
def play(
    daily: bool = typer.Option(False, "--daily", "-d", help="Play the daily challenge"),
    word: Optional[str] = typer.Option(None, "--word", "-w", help="Specify a word (for testing)")
):
    """Play a game of Wordle."""
    words = load_word_list()
    
    if word:
        target_word = word.lower()
    elif daily:
        # Use the date as seed for daily challenge
        random.seed(typer.get_app_dir("wordle"))
        target_word = random.choice(words)
    else:
        target_word = random.choice(words)
        
    game = Wordle(target_word)
    ui = WordleUI()
    
    while not game.game_over:
        ui.display_game(game)
        
        guess = Prompt.ask("Enter your guess").lower()
        result = game.make_guess(guess)
        
        if result is None:
            typer.echo("Invalid guess! Try again.")
            continue
            
    # Show final state
    ui.display_game(game)

if __name__ == "__main__":
    app() 