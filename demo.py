"""Non-interactive demo of the next-word predictor"""
from pathlib import Path
from src.tokenizer import tokenize
from src.model import NGramModel

# Use built-in sample text
text = """
i love machine learning and natural language processing
i love coding in python and building language models
language models can predict the next word
gboard predicts the next word while typing on the phone
"""

print("Training model on sample corpus...\n")
tokens = tokenize(text)
model = NGramModel(n=3)
model.fit(tokens)

print(f"Vocabulary size: {len(model.vocab)} tokens")
print(f"Total n-grams: {len(model.ngram_counts)}\n")

# Demo predictions
test_prefixes = [
    "i love",
    "language models",
    "the next",
    "gboard predicts",
]

print("=" * 60)
print("NEXT-WORD PREDICTIONS")
print("=" * 60)

for prefix in test_prefixes:
    preds = model.predict(tokenize(prefix), top_k=5)
    print(f"\nPrefix: '{prefix}'")
    if preds:
        for word, prob in preds:
            print(f"  → {word:15s} (probability: {prob:.3f})")
    else:
        print("  (no suggestions)")

print("\n" + "=" * 60)
