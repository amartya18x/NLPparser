import sys


class Rule(object):

    def __init__(self, lhs=None, rhs=None):
        self.unit_prod = False
        self.lhs = lhs
        self.rhs = rhs
        self.set_flags()
        self.child1 = None
        self.child2 = None
        self.child_nodes = []
        self.start = 0
        self.end = 0

    def __str__(self):
        rhs = " ".join(self.rhs)
        return self.lhs + " -> " + rhs + \
            "  " + str(self.start) + "," + str(self.end)

    def get_next_char(self):
        return self.rhs[self.end]

    def set_flags(self):
        '''
        Assume that all rules are in CNF
        '''

        if len(self.rhs) == 1:
            self.unit_prod = True

    def set_children(self, child1, child2):
        try:
            if child2 is not None and self.unit_prod:
                raise Exception
        except:
            print("Trying to open unit productions")
            sys.exit(0)

        self.child1 = child1
        self.child2 = child2

    def isFinished(self):
        '''
        Checks whether the rule is finished
        '''
        if self.end == len(self.rhs):
            return True
        else:
            return False

    def __eq__(self, other):
        '''
        For comparing objects
        '''
        return self.__dict__ == other.__dict__


class Reader(object):

    def __init__(self):
        self.rules = []
        self.non_terminal = []
        self.terminal = []

    def read(self, filename='./big.grammar'):
        with open(filename, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                split_line = line.split()
                tmp_rule = Rule(split_line[0], split_line[2:])
                self.non_terminal.append(tmp_rule.lhs)
                if tmp_rule.unit_prod:
                    self.terminal.append(tmp_rule.rhs[0])
                else:
                    self.non_terminal += tmp_rule.rhs
                self.rules.append(tmp_rule)
        self.postProcess()

    def postProcess(self):
        self.non_terminal = list(set(self.non_terminal))
        self.terminal = list(set(self.terminal))

    def return_elements(self):
        return self.rules, self.terminal, self.non_terminal


if __name__ == '__main__':
    reader = Reader()
    reader.read()
    for rules in reader.rules:
        print(vars(rules))
    print(reader.non_terminal)
    print(reader.terminal)
