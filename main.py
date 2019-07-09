import csv
import re

import pandas as pd
import wikipedia

one_hot_file = "one_hot_encoding.csv"

def get_content(num_pages=2):
    """Retrieves page contents from random Wikipedia articles"""
    all_words = set()
    all_content = []

    for i in range(0, num_pages):
        content = wikipedia.page(wikipedia.random(pages=1)).content
        words = re.findall(r"\d*[a-zA-Z]+\d*[a-zA-Z]+\d*", content)  # extract only words, not numbers
        all_content.append(content)
        all_words.update(words)
    
    return all_words, all_content


def build_one_hot_encoding(all_words, all_content):
    """Writes one hot encoding to csv file to be later analyzed"""

    with open(one_hot_file, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(all_words)

        for content in all_content:
            content_words = re.findall(r"\d*[a-zA-Z]+\d*[a-zA-Z]+\d*", content)  # extract only words, not numbers
            content_words = set(content_words)

            content_one_hot = []
            for word in all_words:
                if word in content_words:
                    content_one_hot.append(1)
                else:
                    content_one_hot.append(0)
            writer.writerow(content_one_hot)
                

def analyze():
    """Runs analysis on the generated one-hot encoding file"""
    df = pd.read_csv(one_hot_file)
    print(df.head())
    print(df.mean())


def run():
    """Build a stoplist from contents"""
    all_words, all_content = get_content()
    build_one_hot_encoding(all_words, all_content)
    analyze()


if __name__ == "__main__":
    run()
