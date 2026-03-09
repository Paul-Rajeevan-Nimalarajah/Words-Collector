# 🚀 Indexing Strategy for Performance

This document explains the technical approach used in `add_word.py` to ensure it stays fast even as your word collection grows.

## ⚖️ The Problem: Linear Growth (O(N))

In the first version of the script, it searched for duplicates by opening every daily file and scanning all the text inside.

- **Year 1**: ~365 files. Fast (~0.1s).
- **Year 5**: ~1,800 files. Slower (~1.0s).
- **Year 10**: ~3,650 files. Noticeable lag (~2.5s).

This is called **Linear Search** or `O(N)` complexity, where the time taken grows directly with the number of entries.

## 🛠️ The Solution: Constant Time (O(1))

The optimized version uses a **Central Index** (`index.md`). Instead of scanning many files, it reads one single file.

### 1. Hash Map (Set) Lookup

The script reads `index.md` and stores all words in a Python `set`.

- Looking up a word in a `set` takes **Constant Time** (`O(1)`).
- Whether you have 10 words or 100,000 words, checking for a duplicate takes the **same amount of time** (fractions of a millisecond).

### 2. Automated Indexing

Every time you add a new word:

1. The script appends the entry to today's file.
2. The script **instantly appends** a new row to `index.md`.
3. This keeps the index perfectly in sync without you having to do anything manually.

### 3. Graceful Fallback

If `index.md` is accidentally deleted or corrupted:

- The script detects this and performs a one-time "Deep Scan" (the old method).
- It then **rebuilds** the `index.md` for you to restore performance for the next run.

## 📊 Summary

| Action                 | Old Method (No Index)       | New Method (With Index)   |
| :--------------------- | :-------------------------- | :------------------------ |
| **Search Speed**       | O(N) - Slows down over time | **O(1) - Constant speed** |
| **System Interaction** | Opens hundreds of files     | **Opens only 2 files**    |
| **User Effort**        | Manual index updates        | **Fully Automated**       |
