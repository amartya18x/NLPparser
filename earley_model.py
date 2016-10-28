from rule_reader import Reader


class earley_model(object):

    def __init__(self, rules=None):
        self.predict_dict = {}  # Used in predict function
        self.POS = []
        self.unit_rhs = {}  # Mapping the unit productions with rhs has key
        self.populate_tables(rules)
        self.POS = ['Verb',
                    'Noun',
                    'Det',
                    'Preposition',
                    'Aux',
                    'Proper-Noun',
                    'Pronoun']

    def populate_tables(self, rules):

        for i in xrange(len(rules)):
            if rules[i].unit_prod:
                if rules[i].rhs[0] not in self.unit_rhs.keys():
                    self.unit_rhs[rules[i].rhs[0]] = [i]
                else:
                    self.unit_rhs[rules[i].rhs[0]].append(i)
        for idx, rule in enumerate(rules):
            if rule.lhs not in self.predict_dict.keys():
                self.predict_dict[rule.lhs] = [(rule.rhs, idx)]
            else:
                self.predict_dict[rule.lhs].append((rule.rhs, idx))

    def get_dicts(self):
        return (self.predict_dict, self.POS, self.unit_rhs)

if __name__ == '__main__':
    reader = Reader()
    reader.read()
    rules, _, _ = reader.return_elements()
    earley_model = earley_model(rules)
    print(vars(earley_model))
    print(earley_model.predict_dict['S'])
