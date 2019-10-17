wikipedia-stoplist
==================

This project will serve as an exploration into building robust stoplists from Wikipedia article contents.

Usage
=====

`$ python main.py --num-pages 50 --term-freq 0.6 --limit 200`

This will generate a csv file called output.csv. You can pass this CSV file in to be analyzed again
with:

`$ python main.py --input output.csv --term-freq 0.6 --limit 200`