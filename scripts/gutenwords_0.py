#!/usr/bin/env python3
"""
A very simple script returning the top N words in a text file

Arguments:
- n
- filename

"""
import sys
import os


# The program requires two arguments: let's check we got them
if len(sys.argv) != 3:
    print("Usage: python3 words.py n filename")
    print("ERROR: Supply two arguments")
    exit(1)

# Retrieve the two parameters from the command line using sys.argv
filename, n = sys.argv[1], int(sys.argv[2])

# Check that the file exists
if not os.path.exists(filename):
    print(f"ERROR: File {filename} not found")
    exit(2)

# Read the file
with open(filename, mode="r", encoding="latin-1") as f:
    text = f.read()

# Split the text into words
words = text.split()

# Create a dictionary of word:count
word_counts = {}
for word in words:
    # TODO: We can consider doing some cleaning of the words here (e.g. stripping punctuation)
    if word not in word_counts:
        word_counts[word] = 0
    word_counts[word] += 1

# Sort the dictionary by value: see for example https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Print the top n words
for word, count in sorted_word_counts[:n]:
    frequency = count / len(words) * 100
    print(f"{word}\t{count}\t{frequency:.2f}%")
