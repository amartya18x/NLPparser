from model import cyk_model
from rule_reader import Reader


class Parser(object):

    def __init__(self):
        '''
        Creates the parsing matrix and parses the sentences
        '''
        self.matrix = []
        reader = Reader()
        reader.read()
        rules_list, terminal, non_term = reader.return_elements()
        model = cyk_model(rules_list, non_term, terminal)
        self.terminal_ind, self.non_term_ind, self.rules = \
            model.get_dicts()
        self.rules_list = rules_list
        print(self.terminal_ind)

    def reset_values(self):
        self.matrix = []

    def initialize_matrix(self, sent_len):
        # Populate the super diagonal entries
        for idx in xrange(sent_len):
            self.matrix.append([])
            for idy in xrange(sent_len + 1):
                self.matrix[idx].append([])

    def populate(self, sentence):
        non_term_ind = self.non_term_ind
        term_ind = self.terminal_ind
        rule_ind = self.rules
        sent_len = len(sentence)
        self.initialize_matrix(sent_len)

        # Starting the big looping
        for i in xrange(sent_len):
            # For each word
            word = sentence[i]
            non_terms_tup = rule_ind[tuple([word])]

            # Iterate over all the rules than can cause this
            for diff_rules in non_terms_tup:
                temp_rule = self.rules_list[diff_rules[1]]
                self.matrix[i][i + 1].append((diff_rules[0][0],
                                              temp_rule))
                # Each cell contains a list of tuples
                # The first element of the tuple is the non-terminal
                # THe second is the rule object responsible for it

                # Go up the column
            for row_id in xrange(i, -1, -1):
                
if __name__ == '__main__':
    parser = Parser()
    with open('./example.txt') as f:
        lines = f.readlines()
        for line in lines:
            parser.reset_values()
            parser.populate(line.split())
            print(parser.matrix)
