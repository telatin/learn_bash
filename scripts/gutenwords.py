#!/usr/bin/env python3
"""
Given a set of text files from the Gutenberg project, analyse the frequency of words
from the "start" of the manuscript to its "end". The "start" and "end" are defined
as after "*** START" and before "*** END" respectively.

Usage:
gutenwords.py --plot-file plot.png -n 100 FILE1.txt FILE2.txt ...
"""

import logging

def lines(file, from_line="***START OF", to_line="***END OF"):
    """
    Iterator on file lines (stripped from newlines):
    Given a text file will return all the lines between line starting with
    'from_line' and line starting with 'to_line'
    """
    can_yield = False
    try:
        with open(file, mode="r", encoding="latin-1") as f:
            for line in f:
                if line.startswith(to_line):
                    break
                elif can_yield:
                    yield line.strip()
                else:
                    can_yield = line.startswith(from_line)
    except FileNotFoundError:
        logging.error("[lines] File %s not found", file)
    except Exception as e:
        logging.error("[lines] Error reading %s: %s", file, e)

def words(line):
    """
    Return words from a line stripping punctuation
    """
    for word in line.split():
        try:
            w = word.strip(".,;:?!()[]_*{}\"'").lower()
            # Strip 's and 'll from the end of words
            if w.endswith("'s"):
                w = w[:-2]
            if w.endswith("'ll"):
                w = w[:-3]
            # Discard hypenated words
            if "-" in w:
                continue
            # Check for digits
            if any(c.isdigit() for c in w):
                continue
            yield w
        except AttributeError:
            pass

def top_n_words(dict, n=10, reverse=False):
    """
    Given a dictionary of key:counts, return a dictionary
    with the top n key:values
    """
    rev = not reverse
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=rev)[:n]}

if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser("Analyse the frequency of words in a set of Gutenberg files")
    args.add_argument("FILES", help="Input files", nargs="+")
    args.add_argument("-n", "--num", help="Number of top words to report", type=int, default=10)
    args.add_argument("--start", help="Start of the manuscript", default="***START OF")
    args.add_argument("--end", help="End of the manuscript", default="***END OF")
    args.add_argument("--plot-file", help="Plot the top words as png file")
    args.add_argument("--verbose", help="Verbose output", action="store_true")
    args.add_argument("--debug", help="Debug output", action="store_true")
    args = args.parse_args()

    # Logger
    logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if args.debug:
        logging.basicConfig(format=logFormat, level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(format=logFormat, level=logging.INFO)
    else:
        logging.basicConfig(format=logFormat, level=logging.WARNING)
    

    # Create logger with formatter
  
    logger = logging.getLogger("gutenwords")

    word_count = {}
    for file in args.FILES:
        logger.info("Processing file %s" % file)
        for line in lines(file):
            for word in words(line):
                word_count[word] = 1 if word not in word_count else word_count[word] + 1
    
    total_words = sum(word_count.values())
    
    for w, c in top_n_words(word_count, n=args.num, reverse=False).items():
        print("%s\t%s\t%s" % (w, c, c/total_words))
    print("---")
    for w, c in top_n_words(word_count, n=args.num, reverse=True).items():
        print("%s\t%s\t%s" % (w, c, 100*c/total_words))


    if args.plot_file:
        """
        Plot the top n words in a line plot, save as {args.plot_file}.png
        only if args.plot_file is supplied (--plot-file FILE)
        """
        import matplotlib.pyplot as plt
        import numpy as np
        top_words = top_n_words(word_count, n=args.num, reverse=False)
        plot_title = "Top %s words out of %s in %s files" % (args.num, len(word_count), len(args.FILES))
        plt.title(plot_title)
        # Plot the top words having their counts as y axis
        plt.figure(figsize=(20, 8))
        plt.bar(top_words.keys(), top_words.values())
        plt.xticks(rotation=90)
        plt.savefig(args.plot_file)
