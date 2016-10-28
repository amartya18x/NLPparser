from rule_reader import Reader
from earley_model import earley_model
import copy


class Parser(object):

    def __init__(self):
        '''
        Create the parse table
        '''
        self.table = []
        reader = Reader()
        reader.read()
        rules_list, _, _ = reader.return_elements()
        model = earley_model(rules_list)
        self.predict_dict = model.get_dicts()
        self.rules_list = rules_list

    def parse(self, sent):
        print sent

    def predict(self, state):
        '''
        Add the returned list to the same list
        in self.table
        '''

        start_ind = state.start
        end_ind = state.end
        next_char = state.get_next_char()
        rules_list_temp = self.rules_list[next_char]

        def pred_modify(rule_id):
            new_rule = copy.deepcopy(self.rules_list[rule_id])
            new_rule.start = start_ind
            new_rule.end = end_ind

        modified_rules_list = [pred_modify(x[1]) for x in rules_list_temp]
        return modified_rules_list


if __name__ == '__main__':
    parser = Parser()
    with open('./example.txt') as f:
        lines = f.readlines()
        for line in lines:
            print parser.parse(line.split())
