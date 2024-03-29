from rule_reader import Reader
from earley_model import earley_model
from utils import ruleSet, earley_rec, print_pretty
import copy
from rule_reader import Rule


class Parser(object):

    def __init__(self):
        '''
        Create the parse table
        '''
        self.table = []
        reader = Reader()
        reader.read('./big.grammar.early')
        rules_list, terminal, non_terminal = reader.return_elements()
        model = earley_model(rules_list)
        self.predict_dict, self.POS, self.unit_rhs = model.get_dicts()
        self.rules_list = rules_list
        self.beg_state = Rule(lhs='GAMMA', rhs=['S'])
        self.non_terminal = non_terminal

    def predict(self, state, idx):
        '''
        Add the returned list to the same list
        in self.table
        '''
        # Check whether the next character is POS
        if self.isPOS(state):
            return []

        start_ind = state.start

        # Get the next character after the dot
        next_char = state.get_next_char()
        if next_char not in self.non_terminal:
            return []
        else:
            # All rules with the next_char as the LHS
            rules_list_temp = self.predict_dict[next_char]

        def pred_modify(rule_id, state):
            '''
            Create the new rule object
            by creating a deepcopy
            and setting the start and end
            '''
            new_rule = copy.deepcopy(self.rules_list[rule_id])
            new_rule.start = idx
            new_rule.end = 0
            return new_rule

        # Create a list of all the states to be added
        modified_rules_list = [pred_modify(x[1],
                                           start_ind) for x in rules_list_temp]
        return modified_rules_list

    def isPOS(self, state):
        '''
        Complete this
        '''
        next_char = state.get_next_char()
        return next_char in self.POS

    def scanner(self, state, word, idx):
        '''
        Scanner action
        Add in the same list of the table
        '''
        next_char = state.get_next_char()
        try:
            # Check if the non-terminal is generated
            # If yes, get the rule ids
            prod_rule_id = self.unit_rhs[word][0]
        except:
            print "Sorry '" + word + "' is not present in the grammar"
            exit(0)

        # See if the next_char(POS)
        # matches the LHS of the rule that
        # generates the non-terminal
        if next_char == self.rules_list[prod_rule_id].lhs:
            prod_rule = copy.deepcopy(self.rules_list[prod_rule_id])
            prod_rule.start = state.start
            prod_rule.end = 1
            # Add the non-terminal to be later printed
            # in the parse tree
            prod_rule.child_nodes = str(prod_rule.rhs[0])
            prod_rule.string = word
            return prod_rule
        else:
            return None

    def add_state_list(self, state, ind, printer=False, source=None):
        '''
        Add the state in the ind column
        of the table
        '''
        if printer:
            print(state)
            print("From : " + source + " in " + str(ind))
            print len(self.table)
        try:
            # This adds the state to a list od rules
            # Ensuring that it is unique
            self.table[ind].add(state)
        except:
            pass

    def completed(self, state):
        '''
        Compelete the rule
        Add the list to the same state list
        '''
        completed_char = state.lhs
        start_ind = state.start
        advanced_rules = []

        # Iterated over all incomplete states
        # That begin where the completed rule started
        for states in self.table[start_ind].rule_arr:
            if states.isFinished():
                continue
            # If the next non-terminal matches the lhs
            # of the completed rule
            # Advance the dot
            if states.get_next_char() == completed_char:
                temp_rule = copy.deepcopy(states)
                temp_rule.end = states.end + 1
                advanced_rules.append(temp_rule)
                temp_rule.child_nodes.append(state)
        return advanced_rules

    def parse(self, sent):
        '''
        Parse the text
        '''

        # Add the ruleSet object for each state column
        for word in xrange(len(sent) + 1):
            self.table.append(ruleSet())
        self.add_state_list(self.beg_state, 0)

        for idx, column in enumerate(self.table):
            for rules in column:
                if not rules.isFinished():
                    if not self.isPOS(rules):
                        getPredList = self.predict(rules, idx)
                        for x in getPredList:
                            self.add_state_list(x, idx, False, "Predictor")
                    else:
                        if idx != len(sent):
                            getScanRule = self.scanner(rules, sent[idx], idx)
                            if getScanRule is not None:
                                self.add_state_list(
                                    getScanRule, idx + 1, False, "Scanner")
                else:
                    advanced_rules = self.completed(rules)
                    for rules in advanced_rules:
                        self.add_state_list(rules, idx, False, "Completer")
        return self.table

    def get_trees(self, sentence):
        matrix = parser.parse(line.split())
        States = {}
        allTrees = []
        for idx, x in enumerate(matrix):
            States[idx] = x

        for rules in matrix[-1].rule_arr:
            if rules.lhs == 'GAMMA':
                tree = earley_rec(rules)
                allTrees.append(tree)
        return allTrees, States


if __name__ == '__main__':
    parser = Parser()
    with open('./example.txt') as f:
        lines = f.readlines()
        for line in lines:
            print "Parsing " + line
            all_trees, States = parser.get_trees(line)
            for k in States.keys():
                print "States " + str(k)
                print States[k]
                print
                print
            print "Parse Trees coming"
            print
            if len(all_trees) == 0:
                print "It cannot be parsed!"
            else:
                for trees in all_trees:
                    print_pretty(trees)
