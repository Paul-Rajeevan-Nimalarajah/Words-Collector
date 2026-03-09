import sys
import os
import re
from datetime import datetime

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
INDEX_FILE = "index.md"
TEMPLATE_FILE = "template.md"
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')

def get_word():
    """Gets the word to add from CLI or interactive input."""
    if len(sys.argv) >= 2:
        return sys.argv[1].strip()
    else:
        word = input("Enter the word you want to add: ").strip()
        if not word:
            print("Error: No word provided.")
            sys.exit(1)
        return word

def load_index(current_dir):
    """
    Parses index.md to extract a list of already documented words.
    Returns a set of lowercase words for O(1) lookup.
    """
    index_path = os.path.join(current_dir, INDEX_FILE)
    words = set()
    
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Matches markdown table rows: | Word | Date | Link |
                    # We look for the first column.
                    match = re.search(r'^\|\s*([^\|\s#]+)\s*\|', line)
                    if match:
                        word = match.group(1).strip().lower()
                        if word and word != "word" and ":" not in word:
                            words.add(word)
            return words
        except Exception as e:
            print(f"Warning: Could not read index.md ({e}). Falling back to file scan.")
    
    return None

def scan_files_for_duplicates(current_dir, target_word):
    """
    Fallback method: Scans all daily files for a duplicate.
    Slow (O(N)), but used if index.md is missing.
    """
    print("Performing deep scan of all files...")
    target_lower = target_word.lower()
    for filename in os.listdir(current_dir):
        if DATE_PATTERN.match(filename):
            file_path = os.path.join(current_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                if re.search(f'^## {re.escape(target_word)}', f.read(), re.IGNORECASE | re.MULTILINE):
                    return filename
    return None

def update_index(current_dir, word, date, filename):
    """Appends the new word to the index.md table."""
    index_path = os.path.join(current_dir, INDEX_FILE)
    new_row = f"| {word} | {date} | [{filename}](#{word.lower()}) |\n"
    
    # If the index doesn't exist, create it with headers
    if not os.path.exists(index_path):
        header = "# 🗂️ English Vocabulary Index\n\n| Word | Date Added | Link |\n| :--- | :--- | :--- |\n"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(header)
    
    with open(index_path, 'a', encoding='utf-8') as f:
        f.write(new_row)

def add_word():
    """Main logic for adding a word with O(1) check and O(1) update."""
    word = get_word()
    current_dir = os.getcwd()
    
    # 1. Faster Duplicate Check (via Index)
    indexed_words = load_index(current_dir)
    
    if indexed_words is not None:
        if word.lower() in indexed_words:
            print(f"Duplicate detected via index! Word '{word}' already exists.")
            sys.exit(0)
    else:
        # Fallback to file scan if index is missing/corrupted
        duplicate_file = scan_files_for_duplicates(current_dir, word)
        if duplicate_file:
            print(f"Duplicate found in {duplicate_file}!")
            sys.exit(0)

    # 2. File Initialization
    today = datetime.now().strftime("%Y-%m-%d")
    today_filename = f"{today}.md"
    today_path = os.path.join(current_dir, today_filename)
    template_path = os.path.join(current_dir, TEMPLATE_FILE)

    if not os.path.exists(today_path):
        print(f"Creating daily file: {today_filename}")
        with open(today_path, 'w', encoding='utf-8') as f:
            f.write(f"# 📚 English Vocabulary - {today}\n\n")

    if not os.path.exists(template_path):
        print(f"Error: {TEMPLATE_FILE} missing!")
        sys.exit(1)

    # 3. Add to Daily File
    print(f"Adding '{word}' to {today_filename}...")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    new_entry = template_content.replace("Word", word)

    with open(today_path, 'a', encoding='utf-8') as f:
        # Simple spacing check
        f.write("\n" + new_entry)

    # 4. Update the Index automatically
    print("Updating index.md...")
    update_index(current_dir, word, today, today_filename)
    
    print(f"Success! Entry added for '{word}'.")

if __name__ == "__main__":
    try:
        add_word()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
