"""Simple, working GBoard-style next word predictor"""
from flask import Flask, render_template, jsonify, request
from pathlib import Path
from collections import defaultdict, Counter
import re

app = Flask(__name__)

# Simple tokenizer
def tokenize(text):
    return re.findall(r"\b\w+'\w+|\w+\b", text.lower())

# Load and train
print("Loading corpus...")
corpus_path = Path('data/corpus.txt')
if corpus_path.exists():
    text = corpus_path.read_text(encoding='utf-8', errors='ignore')
else:
    text = "hello world how are you i am fine thank you hello there how is it going i am doing great"

tokens = tokenize(text)
print(f"Tokens: {len(tokens):,}")

# Build simple bigram model (word -> next words)
word_following = defaultdict(Counter)
for i in range(len(tokens) - 1):
    word_following[tokens[i]][tokens[i + 1]] += 1

# Build vocabulary with frequencies
vocab_freq = Counter(tokens)
print(f"Vocabulary: {len(vocab_freq):,} unique words")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json.get('text', '')
    
    if not text:
        return jsonify({'suggestions': []})
    
    # Case 1: Text ends with space = predict NEXT word (like "i love ")
    if text.endswith(' '):
        text_stripped = text.strip()
        if not text_stripped:
            return jsonify({'suggestions': []})
        
        words = text_stripped.split()
        last_word = words[-1].lower()
        
        # Get words that follow the last word
        if last_word in word_following:
            next_words = word_following[last_word].most_common(5)
            suggestions = [word for word, count in next_words]
        else:
            # Fallback to most common words
            suggestions = [word for word, _ in vocab_freq.most_common(5)]
        
        return jsonify({'suggestions': suggestions})
    
    # Case 2: No space at end = autocomplete current word (like "hel")
    text_stripped = text.strip()
    if not text_stripped:
        return jsonify({'suggestions': []})
    
    words = text_stripped.split()
    if not words:
        return jsonify({'suggestions': []})
    
    partial = words[-1].lower()
    # Find word completions
    candidates = [(word, freq) for word, freq in vocab_freq.items() 
                 if word.startswith(partial) and word != partial]
    candidates.sort(key=lambda x: x[1], reverse=True)
    completions = [word for word, _ in candidates[:5]]
    
    return jsonify({'suggestions': completions})

if __name__ == '__main__':
    print("Starting GBoard Predictor...")
    print("Open http://localhost:5000")
    app.run(debug=True, port=5000)
