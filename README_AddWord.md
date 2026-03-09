# 📖 add_word.py Documentation

This script automates the process of adding new English words to your daily documentation files. It ensures that you don't enter the same word twice and handles the creation of daily files automatically.

## 🚀 Features

- **O(1) Performance**: Uses an index-based lookup to ensure instant duplicate checking regardless of word count.
- **Automated Indexing**: Automatically updates `index.md` whenever a new word is added.
- **Duplicate Prevention**: Checks the index first before adding any entry.
- **Interactive Mode**: Prompts for input if no word is provided as an argument.
- **Auto-File Creation**: Initializes daily files (`YYYY-MM-DD.md`) automatically.

## 🛠️ Usage

### Command Line Argument

Pass the word directly as an argument:

```bash
python add_word.py "Resilience"
```

### Interactive Mode

Just run the script, and it will ask for the word:

```bash
python add_word.py
```

## 📂 Requirements

- **Python**: Installed on your system.
- **template.md**: Must exist in the directory.
- **index.md**: Used as the primary search index (auto-created if missing).

## 🔍 How it Works

1. **Load Index**: Reads the first column of the table in `index.md` into a Python `set`.
2. **Instant Check**: Checks if the target word exists in the set (Constant Time).
3. **Daily Entry**: Appends the template to the current day's file.
4. **Auto-Update**: Appends the new word, date, and link to `index.md`.
