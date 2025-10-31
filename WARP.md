# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
A next-word prediction system similar to GBoard, starting with n-gram language models and designed to scale to larger corpora. This is a college minor project with a modular structure for future neural model upgrades.

## Environment Setup

### Virtual Environment (Windows PowerShell)
```powershell
# Create virtual environment
py -3 -m venv .venv

# Activate (PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### CLI Demo
```powershell
# Basic usage with default parameters (n=3, top-k=5)
python -m src.cli --corpus data/corpus.txt --n 3 --top-k 5

# Run with built-in sample corpus (if data/corpus.txt doesn't exist)
python -m src.cli

# Custom n-gram order and number of suggestions
python -m src.cli --corpus data/corpus.txt --n 2 --top-k 10
```

The CLI provides an interactive prompt where you can type word prefixes and get next-word predictions with probabilities.

## Architecture

### Core Components

1. **Tokenizer (`src/tokenizer.py`)**
   - Simple regex-based word tokenizer
   - Lowercases input and preserves contractions (e.g., "I'm" → "i'm")
   - Pattern: `\b\w+'\w+|\w+\b`

2. **N-Gram Model (`src/model.py`)**
   - Implements an n-gram language model with Laplace (add-one) smoothing
   - Key data structures:
     - `ngram_counts`: Counter for n-gram frequencies
     - `context_counts`: Counter for (n-1)-gram context frequencies
     - `vocab`: Set of all unique tokens
   - Uses a sliding window approach during training
   - Prediction uses last (n-1) tokens as context

3. **CLI Interface (`src/cli.py`)**
   - Click-based command-line interface
   - Handles corpus loading with fallback to built-in sample
   - Interactive prediction loop

### Data Flow
```
Text File → tokenize() → List[str] → NGramModel.fit() → 
User Input → tokenize() → NGramModel.predict() → Ranked Predictions
```

### Smoothing Strategy
The model uses Laplace smoothing: `P(w|context) = (count(context, w) + 1) / (count(context) + V)` where V is vocabulary size. This prevents zero probabilities for unseen n-grams.

## Project Structure
```
src/
  cli.py         # Entry point and interactive demo
  model.py       # NGramModel implementation
  tokenizer.py   # Text tokenization utilities
data/
  corpus.txt     # Training corpus (not tracked in git)
notebooks/       # Empty directory for experimentation
tests/           # Empty directory for future tests
```

## Development Notes

### Adding Corpora
- Place plain text files in `data/corpus.txt`
- The CLI uses UTF-8 encoding with error ignore mode
- Binary files (`.bin`, `.pkl`, `.jsonl`) in data/ are gitignored

### Testing
Currently no test suite exists. When adding tests:
- Tests directory is created but empty
- No testing framework is currently installed
- Consider adding `pytest` to requirements.txt for future test development

### Future Extensions (from roadmap)
- Data pipeline for large corpora (streaming, shards)
- Advanced smoothing (Kneser-Ney interpolation)
- Neural language models (HuggingFace Transformers)
- On-device optimization (pruning/quantization)
- Mobile inference packaging
