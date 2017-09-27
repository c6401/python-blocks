def walk_json(
    tree,
    dict_hook=lambda x: x,
    list_hook=lambda x: x,
):
    if tree is None:
        return tree
    elif isinstance(tree, (int, float)):
        return tree
    elif isinstance(tree, str):
        return tree
    elif isinstance(tree, list):
        return list_hook([
            walk_json(el, dict_hook=dict_hook)
            for el
            in tree
        ])
    elif isinstance(tree, dict):
        return dict_hook({
            k: walk_json(v, dict_hook=dict_hook)
            for k, v
            in tree.items()
        })

def group_by(iterable, key):
    groups = {}
    for item in iterable:
        groups.setdefault(key(item), []).append(item)
    return groups
