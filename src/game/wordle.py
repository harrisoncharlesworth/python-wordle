"""
Core game logic for the Wordle game.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple

from utils.word_list import WordList

class LetterState(Enum):
    """Represents the state of a letter in a guess."""
    CORRECT = "correct"        # Letter is in correct position
    PRESENT = "present"        # Letter exists in word but wrong position
    ABSENT = "absent"          # Letter does not exist in word

@dataclass
class GuessResult:
    """Represents the result of a guess."""
    word: str
    states: List[LetterState]
    is_correct: bool

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
    
    def make_guess(self, guess: str) -> Optional[GuessResult]:
        """
        Make a guess and return the result.
        
        Args:
            guess: The word being guessed
            
        Returns:
            GuessResult object containing the evaluation of the guess
            None if the game is over or guess is invalid
        """
        if len(self.attempts) >= self.MAX_ATTEMPTS or self.is_finished:
            return None
            
        guess = guess.lower()
        if len(guess) != self.WORD_LENGTH:
            return None
            
        if not self.word_list.is_valid_word(guess):
            return None
            
        if self.config.hard_mode and self.attempts:
            if not self._is_valid_hard_mode_guess(guess):
                return None
        
        # Evaluate each letter
        states: List[LetterState] = []
        remaining_letters = list(self.target_word)
        
        # First pass: Find correct letters
        for guess_letter, word_letter in zip(guess, self.target_word):
            if guess_letter == word_letter:
                states.append(LetterState.CORRECT)
                remaining_letters.remove(guess_letter)
            else:
                states.append(LetterState.ABSENT)
        
        # Second pass: Find present letters
        for i, (guess_letter, state) in enumerate(zip(guess, states)):
            if state == LetterState.ABSENT and guess_letter in remaining_letters:
                states[i] = LetterState.PRESENT
                remaining_letters.remove(guess_letter)
        
        result = GuessResult(
            word=guess,
            states=states,
            is_correct=all(state == LetterState.CORRECT for state in states)
        )
        
        self.attempts.append(result)
        self.is_finished = result.is_correct or len(self.attempts) >= self.MAX_ATTEMPTS
        return result
    
    def _is_valid_hard_mode_guess(self, guess: str) -> bool:
        """Check if a guess is valid in hard mode."""
        last_result = self.attempts[-1]
        guess_chars = list(guess)
        
        for i, (result, prev_char) in enumerate(zip(last_result.states, self.target_word)):
            if result == LetterState.CORRECT and guess_chars[i] != prev_char:
                return False
            if result == LetterState.PRESENT and prev_char not in guess:
                return False
        return True
    
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
    
    @property
    def game_over(self) -> bool:
        """Check if the game is over."""
        return self.is_finished
    
    @property
    def remaining_attempts(self) -> int:
        """Get the number of remaining attempts."""
        return self.MAX_ATTEMPTS - len(self.attempts)
    
    def get_game_state(self) -> Tuple[bool, bool, int]:
        """
        Get the current game state.
        
        Returns:
            Tuple of (is_game_over, is_won, remaining_attempts)
        """
        return (self.game_over, any(attempt.is_correct for attempt in self.attempts), self.remaining_attempts) 