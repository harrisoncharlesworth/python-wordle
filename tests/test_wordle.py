"""
Tests for the Wordle game logic.
"""

import pytest
from unittest.mock import Mock, patch

from src.game.wordle import WordleGame, GuessResult, LetterResult
from src.utils.config import GameConfig

@pytest.fixture
def game():
    """Create a game instance with a fixed target word."""
    config = GameConfig()
    game = WordleGame(config)
    game.target_word = "hello"
    return game

def test_correct_guess(game):
    """Test a correct guess."""
    result = game.make_guess("hello")
    assert result.is_valid
    assert result.is_correct
    assert all(r == LetterResult.CORRECT for r in result.results)

def test_partially_correct_guess(game):
    """Test a partially correct guess."""
    result = game.make_guess("helps")
    assert result.is_valid
    assert not result.is_correct
    assert result.results[:3] == [LetterResult.CORRECT] * 3
    assert result.results[3:] == [LetterResult.ABSENT] * 2

def test_invalid_word_length(game):
    """Test a guess with invalid length."""
    result = game.make_guess("hi")
    assert not result.is_valid
    assert "must be 5 letters" in result.message.lower()

@pytest.mark.parametrize("mode,guess,expected_valid", [
    (True, "helps", True),   # Uses revealed H
    (True, "world", False),  # Doesn't use revealed H
    (False, "world", True),  # Not in hard mode
])
def test_hard_mode(mode, guess, expected_valid):
    """Test hard mode validation."""
    config = GameConfig(hard_mode=mode)
    game = WordleGame(config)
    game.target_word = "hello"
    
    # Make first guess to reveal some letters
    game.make_guess("hello")
    
    # Try second guess
    result = game.make_guess(guess)
    assert result.is_valid == expected_valid

def test_game_over_conditions(game):
    """Test game over conditions."""
    # Win condition
    result = game.make_guess("hello")
    assert game.is_finished
    assert game.stats["won"]
    
    # Loss condition
    game = WordleGame(GameConfig())  # New game
    game.target_word = "hello"
    for _ in range(6):
        game.make_guess("world")
    assert game.is_finished
    assert not game.stats["won"]

@patch("src.utils.word_list.WordList")
def test_daily_word(mock_word_list):
    """Test daily word generation."""
    mock_instance = Mock()
    mock_word_list.return_value = mock_instance
    mock_instance.get_daily_word.return_value = "daily"
    
    config = GameConfig(daily_mode=True)
    game = WordleGame(config)
    
    assert game.target_word == "daily"
    mock_instance.get_daily_word.assert_called_once() 