# Text Sampling

A web-based text generation application that uses bigram models to sample and generate text based on statistical patterns from literature. Built with Flask and featuring an interactive web interface for real-time text generation.

## Features

- **Bigram Model**: Analyzes word pairs from text corpora to predict next words
- **Two Sampling Methods**:
  - **Likelihood Sampling**: Context-aware generation based on statistical probabilities
  - **Random Sampling**: Uniform random selection for creative outputs
- **Interactive Web Interface**: Clean, modern UI with real-time generation
- **Customizable Prompts**: Start generation with your own seed words
- **Adjustable Length**: Generate text from 5 to 1000 tokens
- **Data Downloader**: Built-in script to download public domain books from Project Gutenberg

## Installation

### Prerequisites

- Python 3.7 or higher
- Flask (`pip install flask`)

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install flask
   ```
3. Download training data (optional - see Data section below):
   ```bash
   python download_data.py
   ```

## Usage

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter a prompt word(s) in the text field
4. Select your preferred sampling method
5. Adjust the number of tokens to generate (5-1000)
6. Click "Generate →" to create text

### Data

The application uses "War and Peace" by Leo Tolstoy as default training data. The text file `war_and_peace.txt` should be in the root directory.

To use different books, run:
```bash
python download_data.py
```

Available books include:
- Sherlock Holmes
- Pride and Prejudice
- Moby Dick
- War and Peace (default)
- Alice's Adventures in Wonderland
- Frankenstein

## Project Structure

```
text-sampling/
├── app.py                 # Main Flask application
├── download_data.py       # Data download script
├── war_and_peace.txt      # Training data (War and Peace)
├── templates/
│   └── index.html         # Web interface
└── README.md             # This file
```

## How It Works

1. **Model Training**: The application loads text and creates a bigram frequency map
2. **Text Generation**: For each new word, it either:
   - Uses likelihood sampling: Selects next word based on observed frequencies
   - Uses random sampling: Chooses uniformly from vocabulary
3. **Scoring**: Tracks log-likelihood scores for generated sequences

## Technical Details

- **Language**: Python 3
- **Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Model**: Bigram language model with frequency-based probabilities
- **Tokenization**: Word-level using regex pattern `\b[\w']+\b`

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project uses public domain text from Project Gutenberg. The code is available under the MIT License.