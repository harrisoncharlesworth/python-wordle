"""
Configuration management for the Wordle game.
"""

from dataclasses import dataclass

@dataclass
class GameConfig:
    """Game configuration settings."""
    
    daily_mode: bool = False
    hard_mode: bool = False 