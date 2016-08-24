"""
Entity linking using TAGME's disgambiguation approach.

@author: Krisztian Balog (krisztian.balog@uis.no)
@author: Faegheh Hasibi (faegheh.hasibi@idi.ntnu.no)

"""
from __future__ import division
from collections import defaultdict
import csv
import math

from nordlys.config import SNIPPETS, OUTPUT_DIR, STATS_MENTION_ENTITY, STATS_ENTITY_INLINKS, STATS_ENTITY_PAIRS_INLINKS, ENTITY_COUNT
from nordlys.document import Document
from nordlys.el_utils import ELUtils


class ELTagme(object):

    def __init__(self):
        self.commonness = dict()
        self.get_commonness()
        self.entity_inlinks = dict()
        self.entity_pairs_inlinks = dict()
        self.load_inlinks_stat()
        self.k_th = 0.3  # score threshold parameter (default value)

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

    def load_inlinks_stat(self):
        """Loads inlinks statistics."""
        # entity inlink count
        with open(STATS_ENTITY_INLINKS, 'rb') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                entity, cnt = row[0], int(row[1])
                self.entity_inlinks[entity] = cnt

        # entity pairs inlink count
        with open(STATS_ENTITY_PAIRS_INLINKS, 'rb') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                e1, e2, cnt = row[0], row[1], int(row[2])
                # we store it both ways for more convenient access
                if e1 not in self.entity_pairs_inlinks:
                    self.entity_pairs_inlinks[e1] = {}
                if e2 not in self.entity_pairs_inlinks:
                    self.entity_pairs_inlinks[e2] = {}
                self.entity_pairs_inlinks[e1][e2] = cnt
                self.entity_pairs_inlinks[e2][e1] = cnt

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
        # For each mention
        for m in candidate_entities.keys():
            # 1) compute the voting-based score
            score = {}
            for e in candidate_entities[m]:
                score[e] = 0
                # TODO score(m,e) = \sum_{m' \in  M_d\{m} } vote(m',e)

            # 2) Consider the top-k percent of entities with the highest score
            # and select the one with the highest commonness score
            top_k_ens = self.get_top_k(score)
            print(m, top_k_ens)
            max_cmn = -1
            max_en = None
            for en in top_k_ens:
                cmn = self.commonness[m][en]
                if cmn > max_cmn:
                    max_en = en
                    max_cmn = cmn
            if max_en is not None:
                disamb_ens[m] = (max_en, max_cmn)

        return disamb_ens

    def vote(self, e, m_, Em_):
        """Computes voting score.
        vote(m',e) = \sum_{e' \in E_m' \mathrm{WLM}(e,e') P(e'|m') / |E_m'|

        :param e: candidate entity e
        :param m_: mention m'
        :param Em_: candidate entities for the mention m' (E_m')
        """
        # TODO complete
        return 0

    def get_top_k(self, score):
        """Returns top-k percent of the entities based on score(e,m)."""
        k = int(round(len(score.keys()) * self.k_th))
        k = 1 if k == 0 else k
        sorted_rel_scores = sorted(score.items(), key=lambda item: item[1], reverse=True)
        top_k_ens = []
        count = 1
        prev_rel_score = sorted_rel_scores[0][1]
        for en, rel_score in sorted_rel_scores:
            if rel_score != prev_rel_score:
                count += 1
            if count > k:
                break
            top_k_ens.append(en)
            prev_rel_score = rel_score
        return top_k_ens

    def get_relatedness(self, e1, e2):
        """Returns the relatedness score between two entities."""

        # TODO complete
        return 0


def main():
    snippets = Document.load_test_snippets(SNIPPETS)

    out_file_name = OUTPUT_DIR + "/output_tagme.txt"
    out_file = open(out_file_name, "w")
    el = ELTagme()

    for doc_id, doc in sorted(snippets.items(), key=lambda item: int(item[0])):
        print("[" + doc_id + "]\t" + doc)
        linked_ens = el.annotate(doc, doc_id)
        ELUtils.write_to_file(doc_id, out_file, linked_ens)
        print("------")

    print("output written to", out_file_name)


if __name__ == "__main__":
    main()