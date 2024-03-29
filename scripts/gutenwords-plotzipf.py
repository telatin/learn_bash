#!/usr/bin/env python3
"""
Version modeled after
https://www.thepythoncode.com/article/plot-zipfs-law-using-matplotlib-python
but keeping the original data structure
"""

import logging
import re
def title_lines(file, from_line="", to_line=""):
    """
    Iterator on file lines (stripped from newlines):
    Return title, and words
    """
    title = "UNDEFINED"
    text = ""
    store_line = False if from_line  != "" else True
    
    try:
        with open(file, mode="r", encoding="latin-1") as f:
            for line in f:
                # Check if line matches regex "from_line"
                if from_line != "" and re.match(from_line, line):
                #if line.startswith(to_line):
                    # the title is what follows "EBOOK"
                    if "EBOOK" in line:
                        title = line.split("EBOOK")[1].strip().strip("* ")
                    store_line = True
                elif to_line  != "" and re.match(to_line, line):
                    store_line = False
                    break
                elif store_line:
                    text += line

        # Strip non A-Z characters from title
        title = "".join(c for c in title if c.isalpha() or c.isspace()) if title != "UNDEFINED" else os.path.basename(file)
        return title, text
    except FileNotFoundError:
        logging.error("[lines] File %s not found", file)
        return "ERROR1", "ERROR"
    except Exception as e:
        logging.error("[lines] Error reading %s: %s", file, e)
        return "ERROR2", "ERROR"

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

 
if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser("Analyse the frequency of words in a set of Gutenberg files")
    args.add_argument("FILES", help="Input files", nargs="+")
    args.add_argument("-o", "--output", help="Plot the top words as png file", required=True)
    args.add_argument("-m", "--max", help="Max files to process, 0 for all [default: %(default)s]", type=int, default=1000)
    args.add_argument("-p", "--max-plot", help="Max files to plot, 0 for all [default: %(default)s]", type=int, default=20)
    
    args.add_argument("--start", help="Start of the manuscript [default: %(default)s]", default="\*\*\*\s?START OF")
    args.add_argument("--end", help="End of the manuscript [default: %(default)s]", default="\*\*\*\s?END OF")
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


    if True:
        # Imports
        import os
        from matplotlib import pyplot as plt
        import string
        import numpy as np
        from scipy.interpolate import make_interp_spline

        # define some dictionaries
        texts = {}
        textlengths = {}
        textwordamounts = {}

        unwantedCharacters = list(string.punctuation)

        # How many ranks we'll show
        depth = 50
        xAxis = [str(number) for number in range(1, depth+1)]

        allText = ""
        texts["ALL"] = ""
        for file in args.FILES:
            # Process at most args.max files
            if args.max > 0 and len(texts) >= args.max:
                break

           
            title, text = title_lines(file, from_line=args.start, to_line=args.end)

            if title == "UNDEFINED":
                logger.warning("Title not found in %s: skipping", file)
                continue
            texts[title] = text
            allText += " " + text
            
        
        texts["ALL"] = allText

        
        # Remove duplicates
        files_to_process = args.FILES
        files_to_process = list(dict.fromkeys(files_to_process))

        # Cleaning and counting the Text
        done = 0
        denominator = int(len(files_to_process) / 15)
        denominator = 1 if denominator == 0 else denominator
        for text in texts:
            done = done + 1
            perc = 100 * done / len(files_to_process)
            if done == 1 or done % denominator == 0:
                logger.info("%d%%: Processing file #%d: %s" % (perc, done, text))
            # Remove unwanted characters from the texts
            for character in unwantedCharacters:
                texts[text] = texts[text].replace(character, '').lower()
            
            #splittedText = texts[text].split(' ')
            splittedText = list(words(texts[text]))
            # Saving the text length to show in the label of the line later
            textlengths[text] = len(splittedText)
            # Here will be the amount of occurence of each word stored
            textwordamounts[text] = {}
            # Loop through all words in the text
            for i in splittedText:
                # Add to the word at the given position if it already exists
                # Else set the amount to one essentially making a new item in the dict
                if i in textwordamounts[text].keys():
                    textwordamounts[text][i] += 1
                else:
                    textwordamounts[text][i] = 1
            # Sorting the dict by the values with sorted
            # define custom key so the function knows what to use when sorting
            textwordamounts[text] = dict(
                sorted(
                    textwordamounts[text ].items(),
                    key=lambda x: x[1],
                    reverse=True)[0:depth]
                )
        
        # Get the percentage value of a given max value
        def percentify(value, max):
            return round(value / max * 100)

        # Generate smooth curvess
        def smoothify(yInput):
            x = np.array(range(0, depth))
            y = np.array(yInput)
            # define x as 600 equally spaced values between the min and max of original x
            x_smooth = np.linspace(x.min(), x.max(), 600) 
            # define spline with degree k=3, which determines the amount of wiggle
            spl = make_interp_spline(x, y, k=3)
            y_smooth = spl(x_smooth)
            # Return the x and y axis
            return x_smooth, y_smooth


        # Make the perfect Curve
        logger.info("Smoothing curve...")
        ziffianCurveValues = [100/i for i in range(1, depth+1)]
        x, y = smoothify(ziffianCurveValues)
        logger.info("Preparing plot")
        # Set plot size
        plt.figure(figsize=(20, 10))
        plt.plot(x, y, label='Ziffian Curve', ls=':', color='grey')


        # Plot the texts
        # Get the first ten keys of 
        keys_top = list(textwordamounts.keys())[0:args.max_plot]
        keys_top[0] = "ALL" if not "ALL" in keys_top else keys_top[0]
        for i in keys_top:
            logger.info("Plotting %s" % i)
            maxValue = list(textwordamounts[i].values())[0]
            yAxis = [percentify(value, maxValue) for value in list(textwordamounts[i].values())]
            x, y = smoothify(yAxis)
            if i == "ALL":
                plt.plot(x, y, label='%s (%d words)' % (i, textlengths[i]), lw=2, color='black')
            else:
                plt.plot(x, y, label=i+f' [{textlengths[i]}]', lw=1, alpha=0.5)
        
        
        plt.xticks(range(0, depth), xAxis)

        plt.legend()
        plt.savefig(args.output, dpi=300)
