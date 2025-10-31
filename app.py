"""Flask web app for GBoard-like next-word prediction"""
from flask import Flask, render_template, jsonify, request
from pathlib import Path
from src.tokenizer import tokenize
from src.model import NGramModel
import sys

app = Flask(__name__)

print("=" * 60)
print("Loading GBoard Next Word Predictor...")
print("=" * 60)

# Train model on startup
corpus_path = Path('data/corpus.txt')
if corpus_path.exists():
    print(f"📖 Loading corpus from {corpus_path}...")
    text = corpus_path.read_text(encoding='utf-8', errors='ignore')
    word_count = len(text.split())
    print(f"✓ Loaded {word_count:,} words")
else:
    print("⚠️  No corpus.txt found. Using small sample.")
    print("   Run 'python download_corpus.py' to get a large dataset!")
    text = """
    i love machine learning and natural language processing
    i love coding in python and building language models
    language models can predict the next word
    gboard predicts the next word while typing on the phone
    python is a great programming language
    machine learning models need lots of data
    natural language processing is fun
    i enjoy building cool projects
    the cat sat on the mat
    the dog ran in the park
    i want to go to the store
    can you help me with this
    """

print("🔄 Tokenizing text...")
tokens = tokenize(text)
print(f"✓ Generated {len(tokens):,} tokens")

print("🧠 Training n-gram model...")
model = NGramModel(n=3)
model.fit(tokens)
print(f"✓ Vocabulary: {len(model.vocab):,} unique words")
print(f"✓ N-grams: {len(model.ngram_counts):,} trigrams learned")
print("=" * 60)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '').strip()
    top_k = 5  # Always return exactly 5 suggestions
    
    if not text:
        # No text yet - don't return suggestions
        return jsonify({'suggestions': []})
    
    # Check if the last word is incomplete (no space after it)
    words = text.split()
    if text.endswith(' '):
        # Complete word + space = predict next word
        tokens = tokenize(text)
        preds = model.predict(tokens, top_k=top_k, partial_word='')
    else:
        # Incomplete word = autocomplete current word
        if len(words) == 0:
            return jsonify({'suggestions': []})
        
        partial = words[-1]  # Last incomplete word
        completed_text = ' '.join(words[:-1]) if len(words) > 1 else ''
        tokens = tokenize(completed_text) if completed_text else []
        preds = model.predict(tokens, top_k=top_k, partial_word=partial)
    
    # Ensure unique suggestions (remove duplicates)
    seen = set()
    suggestions = []
    for word, prob in preds:
        if word not in seen:
            seen.add(word)
            suggestions.append(word)
    
    return jsonify({'suggestions': suggestions[:top_k]})

if __name__ == '__main__':
    print("Starting GBoard-like Next Word Predictor...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
