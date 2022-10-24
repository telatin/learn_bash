#!/usr/bin/env python3
"""
A very simple script returning the top N words in a text file

Arguments:
- n
- filename

CHANGES:
- Multiple input files allowed
"""
import sys
import os
import argparse

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



args = argparse.ArgumentParser("A very simple script returning the top N words in a text file")

# Positional argument: filename (always required)
args.add_argument("filenames", help="Input text file", nargs="+")   # NEW: multiple arguments with nargs="+"
# Argument -n INT: required but a default is provided (10)
args.add_argument("-n", "--top", help="Number of words to return [default: %(default)s]", type=int, default=10)
# Flag/Switch
args.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

args = args.parse_args()


# Check that all the file exist
for file in args.filenames:
    if not os.path.exists(file):
        print(f"ERROR: File {file} not found", file=sys.stderr)
        exit(2)

# Read the file
text = ""
for file in args.filenames:
    if args.verbose:
        print(f"# Reading {file}...", file=sys.stderr)

    with open(file, mode="r", encoding="latin-1") as f:
        text += " " + f.read()

# Add verbose output
if args.verbose:
    print(f"# Read {len(text)} characters from {len(args.filenames)} file(s)", file=sys.stderr)

# Split the text into words
words = text.split()

# Add verbose output
if args.verbose:
    print(f"# Read {len(words)} words from {len(args.filenames)} file(s)")

# cleanup all the words
words = [cleanup(word) for word in words]

# Create a dictionary of word:count
word_counts = {}

for word in words:
    if word not in word_counts:
        word_counts[word] = 0
    word_counts[word] += 1

# Add verbose output
if args.verbose:
    print(f"# Counted {len(word_counts)} unique words from {len(args.filenames)} file(s)")
    
# Sort the dictionary by value: see for example https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Print the top n words
for word, count in sorted_word_counts[:args.top]:

    frequency = count / len(words) * 100
    print(f"{word}\t{count}\t{frequency:.2f}%")
