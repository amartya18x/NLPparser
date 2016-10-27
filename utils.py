import collections

def create_dict_rec(root):
    if root.unit_prod:
        return root.rhs
    else:
        l_child = create_dict_rec(root.child1)
        r_child = create_dict_rec(root.child2)
        print(l_child, r_child, "lls")
        temp = collections.OrderedDict()
        temp[root.child1.lhs] = l_child
        temp[root.child2.lhs] = r_child
        return temp
