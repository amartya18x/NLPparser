import collections
import pydot
import json
import types


class ruleSet():

    def __init__(self, rules=[]):
        self.rule_arr = []
        self.current = -1
        self.end = len(rules) - 1

    def __iter__(self):
        return self

    def next(self):
        if self.current >= self.end:
            raise StopIteration
        else:
            self.current += 1
            return self.rule_arr[self.current]

    def __str__(self):
        return '\n'.join([str(x) for x in self.rule_arr])

    def add(self, new_rule):
        flag = False
        for rule in self.rule_arr:
            if rule == new_rule:
                flag = True
        if not flag:
            self.rule_arr.append(new_rule)
            self.end += 1


def earley_rec(rule):
    if isinstance(rule.child_nodes,
                  types.StringTypes):
        return rule.child_nodes
    temp_dict = {}
    # print rule

    for elem in rule.child_nodes:
        temp_dict[elem.lhs] = earley_rec(elem)
    return temp_dict


def print_pretty(parseTree):
    print(json.dumps(parseTree, indent=4))


def create_dict_rec(root):
    if root.unit_prod:
        return root.rhs
    else:
        l_child = create_dict_rec(root.child1)
        r_child = create_dict_rec(root.child2)
        temp = collections.OrderedDict()
        try:
            temp[root.child1.lhs] = l_child[0]
        except:
            temp[root.child1.lhs] = l_child
        try:

            temp[root.child2.lhs] = r_child[0]
        except:
            temp[root.child2.lhs] = r_child

        return temp


def draw(parent_name, child_name, graph):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)


def visit(node, graph, parent=None):
    for k, v in node.items():
        if isinstance(v, collections.OrderedDict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, k, graph)
            visit(v, graph, k)
        else:
            draw(parent, k, graph)
            draw(k, k + '_' + v, graph)


def draw_graph(src_graph):
    graph = pydot.Dot(graph_type='graph')
    visit(src_graph, graph)
    graph.write_png('parse_tree.png')
