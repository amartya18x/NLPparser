from rule_reader import Reader
from earley_model import earley_model
from utils import ruleSet, earley_rec, print_pretty, draw_graph
import copy
from rule_reader import Rule


class Parser(object):

    def __init__(self):
        '''
        Create the parse table
        '''
        self.table = []
        reader = Reader()
        reader.read()
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
        next_char = state.get_next_char()
        if next_char not in self.non_terminal:
            return []
        else:
            rules_list_temp = self.predict_dict[next_char]

        def pred_modify(rule_id, state):
            new_rule = copy.deepcopy(self.rules_list[rule_id])
            new_rule.start = idx
            new_rule.end = 0
            return new_rule

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
        prod_rule_id = self.unit_rhs[word][0]
        if next_char == self.rules_list[prod_rule_id].lhs:
            prod_rule = copy.deepcopy(self.rules_list[prod_rule_id])
            prod_rule.start = state.start
            prod_rule.end = 1
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
        for states in self.table[start_ind].rule_arr:
            if states.isFinished():
                continue
            if states.get_next_char() == completed_char:
                temp_rule = copy.deepcopy(states)
                temp_rule.end = states.end + 1
                advanced_rules.append(temp_rule)
                temp_rule.child_nodes.append(state)
        return advanced_rules

    def parse(self, sent):
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


if __name__ == '__main__':
    parser = Parser()
    with open('./example.txt') as f:
        lines = f.readlines()
        for line in lines:
            print "Parsing " + line
            count = 0
            matrix = parser.parse(line.split())
            for idx, x in enumerate(matrix):
                print
                print("State " + str(idx))
                print(x)

            for rules in matrix[-1].rule_arr:
                if rules.lhs == 'GAMMA':
                    count = count + 1
                    print(" ==================== ")
                    tree = earley_rec(rules)
                    print_pretty(tree)
                    print("======================")
                    print
            if count == 0:
                print "It cannot be parsed!"
