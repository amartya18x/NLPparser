from rule_reader import Reader


class earley_model(object):

    def __init__(self, rules=None):
        self.predict_dict = {}
        self.populate_tables(rules)

    def populate_tables(self, rules):
        for idx, rule in enumerate(rules):
            if rule.lhs not in self.predict_dict.keys():
                self.predict_dict[rule.lhs] = [(rule.rhs, idx)]
            else:
                self.predict_dict[rule.lhs].append((rule.rhs, idx))

    def get_dicts(self):
        return (self.predict_dict)

if __name__ == '__main__':
    reader = Reader()
    reader.read()
    rules, _, _ = reader.return_elements()
    earley_model = earley_model(rules)
    print(vars(earley_model))
    print(earley_model.predict_dict['S'])
