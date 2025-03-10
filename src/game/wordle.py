"""
Core game logic for the Wordle game.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from utils.word_list import WordList

class LetterResult(Enum):
    """Possible results for each letter in a guess."""
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"

@dataclass
class GuessResult:
    """Result of a single guess."""
    word: str
    results: List[LetterResult]
    is_valid: bool
    is_correct: bool
    message: Optional[str] = None

class WordleGame:
    """Main game logic for Wordle."""
    
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    
    def __init__(self, config):
        """Initialize a new game."""
        self.word_list = WordList()
        self.config = config
        self.attempts: List[GuessResult] = []
        self.target_word = self._get_target_word()
        self.is_finished = False
    
    def _get_target_word(self) -> str:
        """Get the target word for this game."""
        if self.config.daily_mode:
            # Use the date to generate a consistent word for everyone
            seed = int(datetime.now().strftime("%Y%m%d"))
            return self.word_list.get_daily_word(seed)
        return self.word_list.get_random_word()
    
    def make_guess(self, guess: str) -> GuessResult:
        """Process a guess and return the result."""
        guess = guess.lower()
        
        # Validate the guess
        if len(guess) != self.WORD_LENGTH:
            return GuessResult(
                word=guess,
                results=[],
                is_valid=False,
                is_correct=False,
                message=f"Guess must be {self.WORD_LENGTH} letters long"
            )
            
        if not self.word_list.is_valid_word(guess):
            return GuessResult(
                word=guess,
                results=[],
                is_valid=False,
                is_correct=False,
                message="Not in word list"
            )
            
        if self.config.hard_mode and self.attempts:
            if not self._is_valid_hard_mode_guess(guess):
                return GuessResult(
                    word=guess,
                    results=[],
                    is_valid=False,
                    is_correct=False,
                    message="Must use revealed hints in hard mode"
                )
        
        # Process the guess
        results = []
        target_chars = list(self.target_word)
        guess_chars = list(guess)
        
        # First pass: find correct letters
        for i, (guess_char, target_char) in enumerate(zip(guess_chars, target_chars)):
            if guess_char == target_char:
                results.append(LetterResult.CORRECT)
                target_chars[i] = None  # Mark as used
            else:
                results.append(None)
        
        # Second pass: find present letters
        for i, (guess_char, result) in enumerate(zip(guess_chars, results)):
            if result is None:
                if guess_char in target_chars:
                    results[i] = LetterResult.PRESENT
                    target_chars[target_chars.index(guess_char)] = None
                else:
                    results[i] = LetterResult.ABSENT
        
        result = GuessResult(
            word=guess,
            results=results,
            is_valid=True,
            is_correct=guess == self.target_word
        )
        
        self.attempts.append(result)
        self._update_game_state(result)
        
        return result
    
    def _is_valid_hard_mode_guess(self, guess: str) -> bool:
        """Check if a guess is valid in hard mode."""
        last_result = self.attempts[-1]
        guess_chars = list(guess)
        
        for i, (result, prev_char) in enumerate(zip(last_result.results, last_result.word)):
            if result == LetterResult.CORRECT and guess_chars[i] != prev_char:
                return False
            if result == LetterResult.PRESENT and prev_char not in guess:
                return False
        return True
    
    def _update_game_state(self, result: GuessResult) -> None:
        """Update the game state after a guess."""
        if result.is_correct or len(self.attempts) >= self.MAX_ATTEMPTS:
            self.is_finished = True
    
    @property
    def board(self) -> List[GuessResult]:
        """Get the current game board."""
        return self.attempts
    
    @property
    def stats(self) -> dict:
        """Get the game statistics."""
        return {
            "won": any(attempt.is_correct for attempt in self.attempts),
            "attempts": len(self.attempts),
            "target_word": self.target_word if self.is_finished else None
        } 