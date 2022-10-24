#!/usr/bin/env python3
"""
A very simple script returning the top N words in a text file

Arguments:
- n
- filename

CHANGES:
- Use argparse to parse the command line arguments
- Add a cleanup step to polish the words

"""
import sys
import os
import argparse

# NEW: cleanup function
def cleanup(word):
    """
    Clean up a word by removing punctuation and making it lowercase
    """
    stripped = word.strip(".,;:!?-").lower()
    # Unwanted suffixes
    suffixes = ["'s", "'d", "'ll", "'ve", "'re", "'m"]
    for suffix in suffixes:
        if stripped.endswith(suffix):
            stripped = stripped[:-len(suffix)]
            # Assume only one suffix
            break

    return stripped

# NEW: Use argparse to parse the command line arguments
args = argparse.ArgumentParser("A very simple script returning the top N words in a text file")
# Positional argument: filename (always required)
args.add_argument("filename", help="Input text file")
# Argument -n INT: required but a default is provided (10)
args.add_argument("-n", "--top", help="Number of words to return [default: %(default)s]", type=int, default=10)
# Flag/Switch
args.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

args = args.parse_args()


# Check that the file exists
if not os.path.exists(args.filename):
    print(f"ERROR: File {args.filename} not found", file=sys.stderr)
    exit(2)

# Read the file

with open(args.filename, mode="r", encoding="latin-1") as f:
    text = f.read()

# Add verbose output
if args.verbose:
    print(f"Read {len(text)} characters from {args.filename}", file=sys.stderr)

# Split the text into words
words = text.split()

# Add verbose output
if args.verbose:
    print(f"Read {len(words)} words from {args.filename}")


# Create a dictionary of word:count
word_counts = {}
for word in words:
    # NEW: Some cleanup
    word = cleanup(word)

    if word not in word_counts:
        word_counts[word] = 0
    word_counts[word] += 1

# Add verbose output
if args.verbose:
    print(f"Counted {len(word_counts)} unique words from {args.filename}")
    
# Sort the dictionary by value: see for example https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Print the top n words
for word, count in sorted_word_counts[:args.top]:

    frequency = count / len(words) * 100
    print(f"{word}\t{count}\t{frequency:.2f}%")
