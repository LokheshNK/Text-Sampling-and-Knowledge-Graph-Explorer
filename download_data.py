import urllib.request
import re

# URLs for large public domain books
BOOK_URLS = {
    "sherlock_holmes": "https://www.gutenberg.org/files/1661/1661-0.txt",  # ~100k words
        # ~75k words
}

def download_book(url, filename):
    """Download text from Project Gutenberg and save to file"""
    print(f"🔽 Downloading from {url}...")
    
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
        
        # Remove Project Gutenberg header/footer
        start_marker = "*** START OF"
        end_marker = "*** END OF"
        
        start_idx = text.find(start_marker)
        end_idx = text.find(end_marker)
        
        if start_idx != -1:
            # Skip to the line after the marker
            text = text[start_idx:]
            text = text[text.find('\n') + 1:]
        
        if end_idx != -1:
            text = text[:end_idx]
        
        # Count words
        word_count = len(re.findall(r"\b[\w']+\b", text.lower()))
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Saved to '{filename}' ({word_count:,} words)")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return False

def download_all_books():
    """Download all books from the URL dictionary"""
    print("=" * 60)
    print("📚 PROJECT GUTENBERG BOOK DOWNLOADER")
    print("=" * 60)
    
    for book_name, url in BOOK_URLS.items():
        filename = f"{book_name}.txt"
        download_book(url, filename)
        print()
    
    print("=" * 60)
    print("✅ All downloads complete!")
    print("=" * 60)

def download_single_book(book_name):
    """Download a single book by name"""
    if book_name not in BOOK_URLS:
        print(f"❌ Book '{book_name}' not found.")
        print(f"Available books: {', '.join(BOOK_URLS.keys())}")
        return False
    
    filename = f"{book_name}.txt"
    return download_book(BOOK_URLS[book_name], filename)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Download specific book: python download_data.py war_and_peace
        book_name = sys.argv[1]
        download_single_book(book_name)
    else:
        # Download all books
        download_all_books()