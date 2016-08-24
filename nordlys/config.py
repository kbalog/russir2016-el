"""
Global nordlys config.

@author: Krisztian Balog (krisztian.balog@uis.no)
"""

from os import path

NORDLYS_DIR = path.dirname(path.abspath(__file__))
DATA_DIR = path.dirname(path.dirname(path.abspath(__file__))) + "/data"
OUTPUT_DIR = path.dirname(path.dirname(path.abspath(__file__))) + "/data"


CMN_STATS = DATA_DIR + "/commonness_stats.json"

SNIPPETS = DATA_DIR + "/snippets.txt"
