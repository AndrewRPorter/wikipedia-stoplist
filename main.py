import argparse
import csv
import random
import re
import warnings

import pandas as pd
import wikipedia

import constants

warnings.filterwarnings(
    "ignore"
)  # filter all warnings, html parser throws warnings after DisambiguationError


def get_content(num_pages=constants.NUM_PAGES):
    """Retrieves page contents from random Wikipedia articles"""
    all_words = set()  # should contain all unique values
    all_content = []

    for i in range(0, num_pages):
        page = None

        while page is None:
            try:
                topic = wikipedia.search(wikipedia.random(pages=1), results=1)
                page = wikipedia.page(topic)
            except wikipedia.exceptions.DisambiguationError as e:
                topic = wikipedia.search(
                    random.choice(e.options), results=1
                )  # use the first suggested page
                try:
                    page = wikipedia.page(topic)
                except wikipedia.exceptions.DisambiguationError:
                    # some topics always throw DisambiguationError like "Reference point"
                    pass
                except wikipedia.exceptions.PageError:
                    pass

        content = page.content
        words = re.findall(
            r"\d*[a-zA-Z]+\d*[a-zA-Z]+\d*", content
        )  # extract only words, not numbers
        all_content.append(content)
        all_words.update(words)

    return all_words, all_content


def build_one_hot_encoding(all_words, all_content):
    """Writes one hot encoding to csv file to be later analyzed"""

    with open(constants.ONE_HOT_FILE, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(all_words)

        for content in all_content:
            content_words = re.findall(
                r"\d*[a-zA-Z]+\d*[a-zA-Z]+\d*", content
            )  # extract only words, not numbers

            content_one_hot = []
            for word in all_words:
                if word in content_words:
                    content_one_hot.append(1)
                else:
                    content_one_hot.append(0)
            writer.writerow(content_one_hot)


def analyze(limit=constants.LIMIT, freq=constants.FREQ):
    """Runs analysis on the generated one-hot encoding file"""
    df = pd.read_csv(constants.ONE_HOT_FILE)
    mean_columns = sum(df.mean()) / len(df.mean())
    num_written = 0

    with open(constants.STOP_LIST_FILE, "w") as f:
        for column in df:
            if num_written == limit:
                break

            if df[column].mean() > mean_columns:
                f.write(f"{column.lower()}\n")
                num_written += 1


def run(args: argparse.Namespace):
    """Build a stoplist from contents"""
    all_words, all_content = get_content(num_pages=args.num)
    build_one_hot_encoding(all_words, all_content)
    analyze(limit=args.limit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num-pages",
        dest="num",
        type=int,
        default=constants.NUM_PAGES,
        help="specify number of pages used to generate StopList",
    )
    parser.add_argument(
        "-l",
        "--limit",
        dest="limit",
        type=int,
        default=constants.LIMIT,
        help="limit number of terms that appear in StopList",
    )
    parser.add_argument(
        "-t",
        "--term-freq",
        dest="freq",
        type=float,
        default=constants.FREQ,
        choices=range(0, 2),
        help="term frequency percentage to include in StopList",
    )
    args = parser.parse_args()

    run(args)
