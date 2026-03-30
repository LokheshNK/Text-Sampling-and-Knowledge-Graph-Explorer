from flask import Flask, render_template, request, jsonify
import random, re, math, os
from collections import Counter, defaultdict

app = Flask(__name__)
DATA_FILE = "war_and_peace.txt"

def load_model(filename):
    if not os.path.exists(filename):
        return [], [], {}
    text = open(filename, encoding='utf-8').read()
    tokens = re.findall(r"\b[\w']+\b", text.lower())
    bigrams = defaultdict(Counter)
    for i in range(len(tokens) - 1):
        bigrams[tokens[i]][tokens[i + 1]] += 1
    return tokens, list(set(tokens)), bigrams

tokens, vocab, bigram_map = load_model(DATA_FILE)

def next_word(word, method):
    if method == "random" or word not in bigram_map:
        return random.choice(vocab), 0.0
    candidates = bigram_map[word]
    total = sum(candidates.values())
    words, weights = zip(*[(w, c / total) for w, c in candidates.items()])
    chosen = random.choices(words, weights=weights, k=1)[0]
    return chosen, math.log(candidates[chosen] / total)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not vocab:
        return jsonify({"error": "No data loaded."}), 500
    data = request.json
    prompt_words = data.get("prompt", "the").lower().split() or ["the"]
    method = data.get("method", "likelihood")
    length = int(data.get("length", 20))
    result, score = prompt_words, 0
    for _ in range(length):
        w, lh = next_word(result[-1], method)
        result.append(w)
        score += lh
    return jsonify({"output": " ".join(result), "score": round(score, 2), "method": method})

if __name__ == '__main__':
    app.run(debug=True)