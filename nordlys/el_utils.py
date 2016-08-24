"""
Entity linking utilities.

@author: Krisztian Balog (krisztian.balog@uis.no)
"""


class ELUtils(object):

    @staticmethod
    def debug_mention_detection(candidate_ens):
        print("---")
        print("Mention detection")
        print("---")
        for k, v in candidate_ens.iteritems():
            print("\t'" + k + "'\t" + ", ".join(v))

    @staticmethod
    def debug_disambiguation(disamb_ens):
        print("---")
        print("Disambiguation")
        print("---")
        for m, (e, score) in disamb_ens.iteritems():
            print("\t'" + m + "' => " + e + " (" + str(score) + ")")

    @staticmethod
    def write_to_file(doc_id, out_file, linked_ens):
        """Writes entity linking results to output file."""
        out_str = ""
        for men, (en, score) in linked_ens.iteritems():
            out_str += str(doc_id) + "\t" + str(score) + "\t" + en + "\t" + men + "\tpage-id" + "\n"
        out_file.write(out_str)
