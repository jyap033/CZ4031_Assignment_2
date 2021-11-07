#generating the annotations

from typing import List, Tuple
import json

class Node:
    def __init__(self, name):
        self.name = name

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__)

    def to_json_pretty(self):
        return json.dumps(self, default=lambda x: x.__dict__, indent=4)


# might want to do computations on these attributes so parse into correct type
estimated_parser = {
    "cost": lambda cost_str: [float(cost) for cost in cost_str.split("..")],
    "rows": int, 
    "width": int
}
actual_parser = {
    "actual time": lambda time_str: [float(cost) for cost in time_str.split("..")],
    "rows": int, 
    "loops": int
}

STEP = "  "
BIG_STEP = STEP * 3

def parse_node(lines: List[str], cur_lvl_start="") -> Tuple[Node, int]:
    splitted = lines[0].lstrip().lstrip("->").lstrip().split("  ")
    if len(splitted) == 2:
        node_name, costs = splitted
    else:
        raise ValueError(f"failed to parse line0 into node_name and costs: {lines[0]}")

    node = Node(node_name)

    splitted = costs.split(") (")
    if len(splitted) >= 2:
        estimated_cost = splitted[0][1:]
        if list(actual_parser.keys())[0] in splitted[1]:
            actual_cost = splitted[1][:-1]                                  # explain analyze
        else:
            actual_cost = ""                                                # explain but with some other stuffs like (not estimated)
    else:
        estimated_cost, actual_cost = splitted[0][1:-1], ""                 # explain
    estimated = {}
    for attr, parser in estimated_parser.items():
        val = parser(estimated_cost.split(f"{attr}=")[1].split(" ")[0])
        estimated[attr] = val
    setattr(node, "estimated", estimated)
    if actual_cost:
        actual = {}
        for attr, parser in actual_parser.items():
            val = parser(actual_cost.split(f"{attr}=")[1].split(" ")[0])
            actual[attr.replace(" ", "_")] = val
        setattr(node, "actual", actual)

    children = []
    subplans = []
    attr_start = cur_lvl_start + STEP
    line_idx = 1

    while line_idx < len(lines):
        line = lines[line_idx]
        if not line.startswith(attr_start):         # not within this node's scope
            break

        line_content = line[len(attr_start):]
        if line_content.startswith("->"):           # "->  HashAggregate  (cost=151746.99..151748.99, ...)"
            child, next_index = parse_node(lines[line_idx:], cur_lvl_start=cur_lvl_start+BIG_STEP)
            children.append(child)
            line_idx += next_index
        else:
            splitted = line_content.split(": ")
            if len(splitted) > 2:                   # "Worker 1:  Sort Method: quicksort  Memory: 27kB", ignore for now
                line_idx += 1
            elif len(splitted) == 2:                # "Rows Removed by Fileter: 1974218"
                setattr(node, splitted[0].replace(" ", "_"), splitted[1])
                line_idx += 1
            else:                                   # "Subplan"
                subplan, next_index = parse_node(lines[line_idx+1:], cur_lvl_start=attr_start+BIG_STEP)
                subplans.append(subplan)
                line_idx += next_index + 1

    if children:
        setattr(node, "children", children)
    if subplans:
        setattr(node, "subplans", subplans)

    return node, line_idx
