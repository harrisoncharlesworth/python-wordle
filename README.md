# Python Wordle

A Python implementation of the popular word-guessing game Wordle.

## Features

- Command-line interface for playing Wordle
- Rich text output with color-coded feedback
- Extensive word dictionary
- Score tracking and statistics
- Daily challenge mode

## Installation

```bash
# Clone the repository
git clone https://github.com/harrisoncharlesworth/python-wordle.git
cd python-wordle

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the game
python src/main.py

# Run in daily challenge mode
python src/main.py --daily

# Show help
python src/main.py --help
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run type checking
mypy src/

# Run linting
flake8 src/
```

## Project Structure

```
python-wordle/
├── data/           # Word lists and game data
├── src/            # Source code
│   ├── game/       # Game logic
│   ├── ui/         # User interface
│   └── utils/      # Utility functions
├── tests/          # Test files
└── docs/           # Documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 