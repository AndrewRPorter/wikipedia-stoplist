import csv
import re

import wikipedia

one_hot_file = "one_hot_encoding.csv"

def prune(content):
    """Removes words from reference sections at the bottom of an article"""
    return content


def build_one_hot_encoding(all_words, all_content):
    """Writes one hot encoding to csv file to be later analyzed"""

    with open(one_hot_file, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(all_words)

        for content in all_content:
            content_words = re.findall(r"\w+", content)
            content_words = set(content_words)

            content_one_hot = []
            for word in all_words:
                if word in content_words:
                    content_one_hot.append(1)
                else:
                    content_one_hot.append(0)
            writer.writerow(content_one_hot)
                

def run():
    """Build a stoplist from contents"""
    all_words = set()
    all_content = []
    for i in range(0, 5):
        content = wikipedia.page(wikipedia.random(pages=1)).content
        content = prune(content)

        words = re.findall(r"\w+", content)

        all_content.append(content)
        all_words.update(words)

    build_one_hot_encoding(all_words, all_content)


if __name__ == "__main__":
    run()
