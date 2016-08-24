"""
Entity linking using commonness.

@author: Krisztian Balog (krisztian.balog@uis.no)
@author: Faegheh Hasibi (faegheh.hasibi@idi.ntnu.no)

"""
from __future__ import division
from collections import defaultdict
import csv

from nordlys.config import SNIPPETS, OUTPUT_DIR, STATS_MENTION_ENTITY
from nordlys.document import Document
from nordlys.el_utils import ELUtils


class ELCmn(object):

    def __init__(self):
        self.commonness = dict()
        self.get_commonness()

    def get_commonness(self):
        """Loads statistics and computes commonness."""
        # load mention-entity stat
        with open(STATS_MENTION_ENTITY, 'rb') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                mention, entity, freq = row[0], row[1], int(row[2])
                if mention not in self.commonness:
                    self.commonness[mention] = dict()
                self.commonness[mention][entity] = freq

        # compute commonness by normalizing with total value
        for m in self.commonness.keys():
            for e in self.commonness[m].keys():
                norm = self.commonness[m].get("_total", 0)
                if e != "_total" and norm != 0:
                    self.commonness[m][e] /= norm

    def annotate(self, doc, doc_id):
        """Performs entity linking and annotates the query."""
        mention_ens = self.parse(doc, doc_id)
        ELUtils.debug_mention_detection(mention_ens)

        disamb_ens = self.disambiguate(mention_ens)
        ELUtils.debug_disambiguation(disamb_ens)

        return disamb_ens

    def parse(self, doc, doc_id):
        """Parses the document and returns all candidate mention-entity pairs.

        :return: candidate entities {men:{en:cmn, ...}, ...}
        """
        query = Document(doc_id, doc)
        candidate_ens = defaultdict(list)
        for ngram in query.get_ngrams():
            for en in self.commonness.get(ngram, {}):
                if en != "_total":
                    candidate_ens[ngram].append(en)
        return candidate_ens

    def disambiguate(self, candidate_entities):
        """
        Performs disambiguation and link each mention to a single entity.

        :param candidate_entities: dictionary {men:[en1, ...], ...}
        :return: disambiguated entities {men:en, ...}
        """
        disamb_ens = {}
        # For each mention, select the entity with the highest commonness score
        for m in candidate_entities.keys():
            max_cmn = 0
            max_en = None
            for e in candidate_entities[m]:
                if self.commonness[m][e] > max_cmn:
                    max_cmn = self.commonness[m][e]
                    max_en = e
            if max_en is not None:
                disamb_ens[m] = (max_en, max_cmn)
        return disamb_ens


def main():
    snippets = Document.load_test_snippets(SNIPPETS)

    out_file_name = OUTPUT_DIR + "/output_cmn.txt"
    out_file = open(out_file_name, "w")
    el = ELCmn()

    for doc_id, doc in sorted(snippets.items(), key=lambda item: int(item[0])):
        print("[" + doc_id + "]\t" + doc)
        linked_ens = el.annotate(doc, doc_id)
        ELUtils.write_to_file(doc_id, out_file, linked_ens)
        print("------")

    print("output written to", out_file_name)


if __name__ == "__main__":
    main()