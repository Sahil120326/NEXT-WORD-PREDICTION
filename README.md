# GBoard-like Next Word Predictor

A minimal next-word prediction project (college minor) that suggests the next word like Gboard. Starts with an n-gram baseline and is structured to scale to larger corpora (millions of words).

## Features
- Simple tokenizer and n-gram language model baseline
- CLI demo for quick experimentation
- Modular structure to upgrade to neural models later (e.g., Transformers)

## Getting started
1. Create a Python virtual environment (optional but recommended):
   - Windows PowerShell:
     - `py -3 -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
   - Or with Python:
     - `python -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Prepare a corpus (plain text) at `data/corpus.txt` (one or more large text files concatenated is fine).
4. Run the CLI demo:
   - `python -m src.cli --corpus data/corpus.txt --n 3 --top-k 5`

## Roadmap
- Data pipeline for large corpora (streaming, shards)
- Smarter smoothing (e.g., Kneser–Ney)
- Mobile-friendly inference packaging
- Optional neural LM (HF Transformers) and on-device pruning/quantization
