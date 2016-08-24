"""
Utility class for input documents.

@author: Krisztian Balog (krisztian.balog@uis.no)
@author: Faegheh Hasibi (faegheh.hasibi@idi.ntnu.no)
"""

import re


class Document(object):
    def __init__(self, doc_id, doc):
        self.id = doc_id
        self.doc = self.preprocess(doc).lower()

    @staticmethod
    def preprocess(input_str):
        """Pre-processes the document and removes some special chars."""
        input_str = re.sub('[^A-Za-z0-9]+', ' ', input_str)
        input_str = input_str.replace(" OR ", " ").replace(" AND ", " ")
        # removing multiple spaces
        cleaned_str = ' '.join(input_str.split())
        return cleaned_str

    def get_ngrams(self):
        """Finds all n-grams of the document.

        :return list of n-grams
        """
        con = self.doc.strip().split()
        ngrams = []
        for i in range(1, len(con) + 1):  # number of words
            for start in range(0, len(con) - i + 1):  # start point
                ngram = con[start]
                for j in range(1, i):  # builds the sub-string
                    ngram += " " + con[start + j]
                ngrams.append(ngram)
        return ngrams

    @staticmethod
    def load_test_snippets(snippets_file):
        """Loads the test document snippets and resturns them as a dictionary {id : snippet}"""
        docs = {}
        q_file = open(snippets_file, "r")
        for line in q_file:
            cols = line.strip().split("\t")
            docs[cols[0].strip()] = cols[1].strip()
        return docs