from cyk_model import cyk_model
from rule_reader import Reader
import copy
from utils import create_dict_rec, draw_graph, print_pretty


class Parser(object):

    def __init__(self):
        '''
        Creates the parsing matrix and parses the sentences
        '''
        self.matrix = []
        reader = Reader()
        reader.read('./big.grammar.cnf')
        rules_list, terminal, non_term = reader.return_elements()
        model = cyk_model(rules_list, non_term, terminal)
        self.terminal_ind, self.non_term_ind, self.rules = \
            model.get_dicts()
        self.rules_list = rules_list

    def reset_values(self):
        self.matrix = []

    def initialize_matrix(self, sent_len):
        # Populate the super diagonal entries
        for idx in xrange(sent_len):
            self.matrix.append([])
            for idy in xrange(sent_len + 1):
                self.matrix[idx].append([])

    def parse(self, sentence):
        rule_ind = self.rules
        sent_len = len(sentence)
        self.initialize_matrix(sent_len)

        # Starting the big looping
        for i in xrange(1, sent_len + 1):
            # For each word
            word = sentence[i - 1]
            try:
                non_terms_tup = rule_ind[tuple([word])]
            except:
                print "Sorry '"+word+"' is not present in the lexicon."
            # Iterate over all the rules than can cause this
            for diff_rules in non_terms_tup:
                temp_rule = self.rules_list[diff_rules[1]]
                self.matrix[i - 1][i].append((diff_rules[0][0],
                                              temp_rule))
                # Each cell contains a list of tuples
                # The first element of the tuple is the non-terminal
                # THe second is the rule object responsible for it

                # Go up the column
            for row_id in xrange(i - 2, -1, -1):
                # Looking at all possible conditions
                for inter_id in xrange(i - 1, row_id, -1):
                    left_tuple = self.matrix[row_id][inter_id]
                    right_tuple = self.matrix[inter_id][i]
                    for l_tuples in left_tuple:
                        for r_tuples in right_tuple:
                            left_elem = l_tuples[0]
                            right_elem = r_tuples[0]
                            poss_tuple = (left_elem, right_elem)
                            if poss_tuple in rule_ind.keys():
                                search_res = rule_ind[(left_elem, right_elem)]
                                # Iterate over all the rules than can cause
                                # this
                                for diff_rules in search_res:
                                    temp_rule = copy.deepcopy(
                                        self.rules_list[diff_rules[1]])
                                    self.matrix[row_id][i].append(
                                        (diff_rules[0][0],
                                         temp_rule))
                                    temp_rule.set_children(l_tuples[1],
                                                           r_tuples[1])
        return self.matrix

    def get_trees(self, sentence):
        parser.reset_values()
        parser.parse(line.split())
        treeList = []
        for trees in parser.matrix[0][-1]:
            if trees[0] == 'S':
                final_node = trees[1]
                src_graph = {'S': create_dict_rec(final_node)}
                treeList.append(src_graph)

        return treeList


if __name__ == '__main__':
    parser = Parser()
    with open('./example.txt') as f:
        lines = f.readlines()
        for line in lines:
            all_trees = parser.get_trees(line)
            if len(all_trees) == 0:
                print("sorry! It is not parsable")
            else:
                for graphs in all_trees:
                    print_pretty(graphs)
