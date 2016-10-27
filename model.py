from rule_reader import Reader


class cyk_model(object):

    def __init__(self, rules=None, non_term=None, terminal=None):
        '''
        Create the preprocessing tables
        non_term_ind : Gives a numerical index to each non_terminal
        terminal_ind : Gives a numerical index to each terminal
        find_lhs : a table to find the lhs given the rhs for CNF
        '''

        self.non_term_ind = {}
        self.terminal_ind = {}
        self.find_lhs = {}
        self.populate_tables(terminal, non_term, rules)

    def populate_tables(self, terminal, non_term, rules):

        # Populate the terminal dictionary
        for idx, val in enumerate(terminal):
            self.terminal_ind[val] = idx

        # Populate the non-terminal dictionary
        for idx, val in enumerate(non_term):
            self.non_term_ind[val] = idx

        # Stored as a dictionary where the key is a tuple
        for idx, rule in enumerate(rules):
            if tuple(rule.rhs) not in self.find_lhs.keys():
                self.find_lhs[tuple(rule.rhs)] = [([rule.lhs], idx)]
            else:
                self.find_lhs[tuple(rule.rhs)].append(([rule.lhs], idx))

    def get_dicts(self):

        return (self.terminal_ind, self.non_term_ind, self.find_lhs)

if __name__ == '__main__':
    reader = Reader()
    reader.read()
    rules, terminal, non_term = reader.return_elements()
    cyk_model = cyk_model(rules, non_term, terminal)
    print(vars(cyk_model))
