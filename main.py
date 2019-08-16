import argparse
import csv
import random
import re
import warnings
from typing import List, Set, Tuple

import pandas as pd
import wikipedia

import constants

warnings.filterwarnings(
    "ignore", category=UserWarning
)  # html parser throws warnings after DisambiguationError


def get_content(num_pages: int = constants.NUM_PAGES) -> Tuple[Set[str], List[str]]:
    """Retrieves page contents from random Wikipedia articles
    
    Args:
        num_pages: maximum number of pages to generate output from
    """
    all_words = set()  # type: Set[str]
    all_content = []  # type: List[str]

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


def build_one_hot_encoding(all_words: Set[str], all_content: List[str]):
    """Writes one hot encoding to csv file to be later analyzed
    
    Args:
        all_words: unique set of all articles words
        all_content: raw content for each article
    """

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


def analyze(limit: int = constants.LIMIT, max_freq: float = constants.FREQ):
    """Runs analysis on the generated one-hot encoding file
    
    Args:
        limit: maximum number of terms allowed in StopList
        max_freq: term frequeny needed for terms in StopList
    """
    df = pd.read_csv(constants.ONE_HOT_FILE)
    num_written = 0

    with open(constants.STOP_LIST_FILE, "w") as f:
        for column in df:
            if num_written == limit:
                break

            values = list(df[column].values)
            num_miss, num_hit = values.count(0), values.count(1)

            frequency = 0
            if num_miss > 0:
                frequency = num_hit / num_miss  # avoid division by zero

            if frequency > max_freq:
                f.write(f"{column.lower()}\n")
                num_written += 1


def run(args: argparse.Namespace):
    """Build a stoplist from contents"""
    all_words, all_content = get_content(num_pages=args.num)
    build_one_hot_encoding(all_words, all_content)
    analyze(limit=args.limit, max_freq=args.freq)


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
        help="term frequency percentage to include in StopList",
    )
    args = parser.parse_args()

    run(args)
