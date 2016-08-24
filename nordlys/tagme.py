"""
TAGME implementation

@author: Faegheh Hasibi (faegheh.hasibi@idi.ntnu.no)
@author: Krisztian Balog (krisztian.balog@uis.no)

"""
from __future__ import division
import argparse
import json
import math
from collections import defaultdict

from nordlys.config import OUTPUT_DIR, CMN_STATS
from nordlys import config
from nordlys.query import Query
from nordlys.utils import read_tagme_queries


class Tagme(object):
    total_entities = 3051661

    def __init__(self, rho_th=0.1):
        self.cmn_stats = json.load(open(CMN_STATS, "r"))
        self.commonness = dict()
        self.relatedness = dict()

    def annotate(self, query, qid=""):
        """Performs entity linking and annotates the query."""
        mention_ens = self.parse(query, qid)
        Tagme.debug_mention_detection(mention_ens)

        # TODO perform entity linking based on commonness

        disamb_ens = self.disambiguate(mention_ens)

        return mention_ens

    @staticmethod
    def debug_mention_detection(candidate_ens):
        print("---")
        print("Mention detection")
        print("---")
        for k, v in candidate_ens.iteritems():
            print("\t'" + k + "'\t" + ", ".join(v))


    def parse(self, query, qid=""):
        """
        Parses the query and returns all candidate mention-entity pairs.

        :return: candidate entities {men:{en:cmn, ...}, ...}
        """
        query = Query(qid, query)
        candidate_ens = defaultdict(list)
        for ngram in query.get_ngrams():
            for en in self.cmn_stats.get(ngram, {}):
                if en != "_total":
                    candidate_ens[ngram].append(en)
        return candidate_ens

    def disambiguate(self, candidate_entities):
        """
        Performs disambiguation and link each mention to a single entity.

        :param candidate_entities: dictionary {men:[en1, ...], ...}
        :return: disambiguated entities {men:en, ...}
        """
        # TODO

    def compute_commonness(self, men, en):
        """Computes commonness for a given mention and entity."""
        linke_e_m = self.cmn_stats[men][en]
        link_m = self.cmn_stats[men]["_total"]
        cmn = linke_e_m / link_m if link_m != 0 else 0
        return cmn

    def __get_commonness(self, men, en):
        """Returns the commonness score"""
        if (men, en) not in self.commonness:
            self.commonness[(men, en)] = self.compute_commonness(men, en)
        return self.commonness[(men, en)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-th", "--threshold", help="score threshold", type=float, default=0)
    args = parser.parse_args()

    queries = read_tagme_queries(config.SNIPPETS)

    out_file_name = OUTPUT_DIR + "/tagme.txt"
    open(out_file_name, "w").close()
    out_file = open(out_file_name, "a")
    tagme = Tagme(args.threshold)

    linked_ens = defaultdict(dict)
    for qid, query in sorted(queries.items(), key=lambda item: int(item[0])):
        print("[" + qid + "]\t" + query)
        linked_ens = tagme.annotate(query, qid)
        #print(linked_ens)
        print("------")

        # write results to output file
        #out_str = ""
        #for men, (en, score) in linked_ens.iteritems():
        #    out_str += str(qid) + "\t" + str(score) + "\t" + en + "\t" + men + "\tpage-id" + "\n"
        #print(out_str)
        #out_file.write(out_str)

    print("output written to", out_file_name)


if __name__ == "__main__":
    main()