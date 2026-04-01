from flask import Flask, render_template, request, jsonify
import random, re, math, os
from collections import Counter, defaultdict
from gensim.models import Word2Vec
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Setup NLTK (needed for first cold start on Vercel)
def setup_nltk():
    try:
        # On Vercel, the homedir is /tmp for writable data
        if os.environ.get('VERCEL'):
            nltk.data.path.append("/tmp/nltk_data")
        pkgs = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'maxent_ne_chunker', 'words']
        for pkg in pkgs:
           try:
               nltk.data.find(pkg)
           except:
               nltk.download(pkg, quiet=True)
    except:
        pass

setup_nltk()

app = Flask(__name__)
DATA_FILE = "war_and_peace.txt"
# Vercel needs writable /tmp for model storage
MODEL_FILE = "/tmp/w2v.model" if os.environ.get('VERCEL') else "w2v.model"

def load_models(filename):
    if not os.path.exists(filename):
        return [], [], {}, None
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    tokens = re.findall(r"\b[\w']+\b", text.lower())
    bigrams = defaultdict(Counter)
    for i in range(len(tokens) - 1):
        bigrams[tokens[i]][tokens[i + 1]] += 1
    if os.path.exists(MODEL_FILE):
        w2v = Word2Vec.load(MODEL_FILE)
    else:
        sentences = [re.findall(r"\b[\w']+\b", line.lower()) for line in text.split('\n') if len(line) > 10]
        w2v = Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)
        w2v.save(MODEL_FILE)
    return tokens, list(set(tokens)), bigrams, w2v

tokens, vocab, bigram_map, w2v_model = load_models(DATA_FILE)

def next_word(word, method):
    if method == "embeddings" and w2v_model and word in w2v_model.wv:
        similars = w2v_model.wv.most_similar(word, topn=10)
        words, weights = zip(*[(w, float((s + 1) / 2)) for w, s in similars])
        total = sum(weights)
        norm_weights = [w/total for w in weights]
        chosen = random.choices(words, weights=norm_weights, k=1)[0]
        sim = float(w2v_model.wv.similarity(word, chosen))
        return chosen, math.log(max(sim, 0.001))
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
    result = list(prompt_words)
    score = 0
    for _ in range(length):
        w, lh = next_word(result[-1], method)
        result.append(w)
        score += lh
    return jsonify({"output": " ".join(result), "score": round(float(score), 2), "method": method})

@app.route('/kg', methods=['POST'])
def get_kg():
    data = request.json
    text = data.get("article", "")
    if not text:
        return jsonify({"nodes": [], "edges": []})
    
    try:
        tokens_raw = word_tokenize(text)
        tagged = nltk.pos_tag(tokens_raw)
    except:
        words = re.findall(r"\b[\w']+\b", text)
        tagged = [(w, 'NNP' if w[0].isupper() else 'NN') for w in words]
    
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = {"the", "and", "this", "that", "with", "from", "said"}
    
    extended_stops = {"president", "administration", "said", "added", "think", "people", "thing", 
                      "extraordinary", "according", "news", "today", "possible", "already", "within", "weeks", "month"}
    stop_words.update(extended_stops)
    
    weighted_counts = Counter()
    for w, tag in tagged:
        wl = w.lower()
        if wl in stop_words or len(wl) < 3: continue
        if tag in ('NNP', 'NNPS'):
            weighted_counts[w] += 3  
        elif tag in ('NN', 'NNS') and len(wl) > 4:
            weighted_counts[wl] += 1
            
    top_terms = [w for w, c in weighted_counts.most_common(20)]
    
    nodes = []
    for term in top_terms:
        nodes.append({
            "id": term, 
            "label": term, 
            "size": int(weighted_counts[term]) * 2 + 15
        })
        
    sentences = [re.findall(r"\b[\w']+\b", line.lower()) for line in text.split('.') if len(line) > 5]
    edges = []
    seen_edges = set()
    
    for i, w1 in enumerate(top_terms):
        for w2 in top_terms[i+1:]:
            sim = 0.0
            wl1, wl2 = w1.lower(), w2.lower()
            if w2v_model and wl1 in w2v_model.wv and wl2 in w2v_model.wv:
                sim = float(w2v_model.wv.similarity(wl1, wl2))
            
            co_occurrence = 0.0
            for s in sentences:
                if wl1 in s and wl2 in s:
                    co_occurrence += 0.5
            
            total_weight = float(sim + co_occurrence)
            
            if total_weight > 0.4:
                edge_id = tuple(sorted((w1, w2)))
                if edge_id not in seen_edges:
                    edges.append({"from": w1, "to": w2, "value": total_weight})
                    seen_edges.add(edge_id)
                            
    return jsonify({"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug=True)