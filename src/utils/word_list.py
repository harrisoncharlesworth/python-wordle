"""
Word list management for the Wordle game.
"""

import json
import random
from pathlib import Path
from typing import List, Set

class WordList:
    """Manages the list of valid words for the game."""
    
    def __init__(self):
        """Initialize the word list from data files."""
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self._load_words()
    
    def _load_words(self) -> None:
        """Load words from data files."""
        # Load target words (words that can be answers)
        target_words_path = self.data_dir / "target_words.json"
        with open(target_words_path, "r", encoding="utf-8") as f:
            self.target_words: List[str] = json.load(f)
        
        # Load valid words (words that are valid guesses)
        valid_words_path = self.data_dir / "valid_words.json"
        with open(valid_words_path, "r", encoding="utf-8") as f:
            valid_words: List[str] = json.load(f)
        
        # Create a set of all valid words for faster lookup
        self.valid_words: Set[str] = set(valid_words + self.target_words)
    
    def get_random_word(self) -> str:
        """Get a random target word."""
        return random.choice(self.target_words)
    
    def get_daily_word(self, seed: int) -> str:
        """Get the daily word using a seed."""
        # Use the seed to get a consistent word for the day
        random.seed(seed)
        word = random.choice(self.target_words)
        random.seed()  # Reset the seed
        return word
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word is in the valid words list."""
        return word.lower() in self.valid_words 