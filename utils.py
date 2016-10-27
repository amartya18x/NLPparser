import collections
import pydot
import json


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
