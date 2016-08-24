"""Utility finctions for reading/writing files

@author: Faegheh Hasibi
"""


def read_tagme_queries(dataset_file):
    """Returns the dictionary of snippets {id : snippet}"""
    queries = {}
    q_file = open(dataset_file, "r")
    for line in q_file:
        cols = line.strip().split("\t")
        queries[cols[0].strip()] = cols[1].strip()
    return queries