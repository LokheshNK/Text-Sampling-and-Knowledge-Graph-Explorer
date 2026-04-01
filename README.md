# Text Sampling & Knowledge Graph Explorer

A state-of-the-art web application for text generation and semantic analysis. This project combines traditional statistical bigram models with modern Word2Vec embeddings and interactive knowledge mapping.

## ✨ Features

-   **Dual-Core Intelligence**: 
    -   **Bigram Logic**: Statistical prediction based on word frequency.
    -   **Word2Vec Embeddings**: Semantic prediction based on vector similarity in an N-dimensional space.
-   **Advanced Sampling Methods**:
    -   **Likelihood (Bigram)**: Predicts the most probable next word based on historical counts.
    -   **Vector Semantic (Word2Vec)**: Finds conceptually related successors, perfect for creative and abstract generation.
    -   **Random**: Uniform selection for pure creativity.
-   **Semantic Knowledge Graph**:
    -   Analyze any article or text snippet in real-time.
    -   **NLP Extraction**: Automatically filters important Entities and Proper Nouns (People, Places, Organizations).
    -   **Hybrid Links**: Connects concepts using both semantic similarity weights and sentence-based co-occurrence.
    -   **Interactive Visualization**: Explore the web of concepts with a high-performance, stabilized network graph.
-   **Premium Interface**:
    -   Modern Dark Mode with Glassmorphism aesthetics.
    -   Real-time generation feedback and log-likelihood scoring.
    -   Responsive design for various screen sizes.

## 🚀 Installation & Setup

### Prerequisites

-   Python 3.8+
-   `pip` (Python package manager)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/LokheshNK/Text-Sampling.git
    cd Text-Sampling
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Training Data**:
    By default, the app uses *War and Peace* for training the initial models.
    ```bash
    python download_data.py
    ```

### Starting the Server

```bash
python app.py
```

> [!NOTE]
> On the first run, the app will download necessary NLTK language packages and train the `w2v.model` locally. This may take 10-20 seconds depending on your internet speed. Subsequent starts will be nearly instantaneous.

## 📁 Project Structure

-   `app.py`: The core Flask backend, housing the Word2Vec model and Knowledge Graph logic.
-   `download_data.py`: Utility to fetch large-scale literature from Project Gutenberg.
-   `templates/index.html`: The interactive NexusAI web interface.
-   `requirements.txt`: Manages all AI and Web dependencies.
-   `w2v.model`: The persisted Word2Vec model trained on the corpus.

## 🛠️ Technology Stack

-   **Backend**: Flask (Python)
-   **AI/NLP**: Gensim (Word2Vec), NLTK (Tokenization/POS Tagging)
-   **Frontend**: Vis.js (Network Visualization), Vanilla CSS/HTML/JS
-   **Visuals**: Outfit/JetBrains Mono Typography, CSS Glassmorphism

## 📄 License

This project is licensed under the MIT License - using public domain literature from Project Gutenberg.

---
*Built for the Advanced AI Package Development Course*
