"""
Entity linking using commonness.

@author: Krisztian Balog (krisztian.balog@uis.no)
@author: Faegheh Hasibi (faegheh.hasibi@idi.ntnu.no)

"""
from __future__ import division

from math import log
from collections import defaultdict

from lazy import lazy

from nordlys.config import SNIPPETS, OUTPUT_DIR, STATS_MENTION_ENTITY, \
    ENTITY_INLINKS, ENTITY_PAIRS_INLINKS
from nordlys.document import Document
from nordlys.el_utils import ELUtils


class ELCmn(object):
    def __init__(self):
        self.commonness = dict()
        self.get_commonness()

    def get_commonness(self):
        """Loads statistics and computes commonness."""
        self.__load_mentioned_entities()
        self.__normalize_commonness()

    def __normalize_commonness(self):
        for m, ents in self.commonness.iteritems():
            norma = self.commonness[m].get('_total', 1)
            for e in ents:
                if e != '_total':
                    self.commonness[m][e] /= float(norma)

    def __load_mentioned_entities(self):
        with ELUtils.tsv_reader(STATS_MENTION_ENTITY) as reader:
            for row in reader:
                mention, entity, freq = row[0], row[1], int(row[2])
                if mention not in self.commonness:
                    self.commonness[mention] = dict()
                self.commonness[mention][entity] = freq

    @lazy
    def entities_inlinks(self):
        with ELUtils.tsv_reader(ENTITY_INLINKS) as reader:
            return {row[0]: int(row[1]) for row in reader}

    @lazy
    def entities_pairs_inlinks(self):
        with ELUtils.tsv_reader(ENTITY_PAIRS_INLINKS) as reader:
            return {self.__get_entity_pair_key(row[0], row[1]): int(row[2])
                    for row in reader}

    def __get_entity_pair_key(self, e1, e2):
        return tuple(sorted((e1, e2)))

    @property
    def entities_total_count(self):
        return len(self.entities_inlinks)

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
        top_count = 10
        disambiguated_dict = {}
        for i, (mention, entities) in enumerate(candidate_entities.iteritems()):
            scores = [(e, sum(
                self.vote(m, candidate_entities[m], e)
                for j, m in enumerate(candidate_entities.iterkeys()) if j != i))
                      for e in entities]
            candidates = [(e, self.commonness[mention][e]) for e, _ in
                          sorted(scores, key=lambda x: x[1], reverse=True)[
                          :top_count]]
            disambiguated_dict[mention] = max(candidates, key=lambda x: x[1])

        return disambiguated_dict

    def vote(self, mention, candidates, entity):
        candidate_votes = sum(
            self.commonness[mention][e] * self.calculate_wlm(entity, e)
            for e in candidates)
        return candidate_votes / float(len(candidates))

    MINUS_INFINITY = -1000000000000000000000

    def calculate_wlm(self, entity, entity1):
        pair_key = self.__get_entity_pair_key(entity, entity1)

        entity_links = self.entities_inlinks[entity]
        entity1_links = self.entities_inlinks[entity1]
        common_links = self.entities_pairs_inlinks.get(pair_key)

        x = log(min(entity_links, entity1_links)) if (
            entity_links and entity1_links) else self.MINUS_INFINITY
        y = log(max(entity_links, entity1_links)) if (
            entity_links and entity1_links) else self.MINUS_INFINITY
        z = log(common_links) if common_links else self.MINUS_INFINITY
        frac = (y - z) / (log(self.entities_total_count) - x)
        return 1 - frac


def main():
    snippets = Document.load_test_snippets(SNIPPETS)

    out_file_name = OUTPUT_DIR + "/output_cmn_vote.txt"
    with open(out_file_name, "w") as out_file:
        el = ELCmn()

        for doc_id, doc in sorted(snippets.items(),
                                  key=lambda item: int(item[0])):
            print("[" + doc_id + "]\t" + doc)
            linked_ens = el.annotate(doc, doc_id)
            ELUtils.write_to_file(doc_id, out_file, linked_ens)
            print("------")

    print("output written to", out_file_name)


if __name__ == "__main__":
    main()
