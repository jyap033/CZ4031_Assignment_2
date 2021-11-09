# generating the annotations

from typing import Dict, List, Tuple
import json


class Node:
    """A simple data structure that represents Operator node in QEP"""
    def __init__(self, name) -> None:
        self.name = name

    def to_json_pretty(self) -> str:
        return json.dumps(self, default=lambda x: x.__dict__, indent=4)

    def to_dict(self) -> Dict:
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))


STEP = "  "
BIG_STEP = STEP * 3


class QepParser:
    """Holds the methods that parse qep to tree of Nodes"""
    total_steps = 0

    def parse(self, lines: List[str], cur_lvl_start="") -> Node:
        """Parse and add steps to the qep"""
        node, _ = self._parse_to_node(lines, cur_lvl_start)
        self.total_steps = 0
        self._traverse_count_step(node)
        self._traverse_add_step(node)
        return node

    def _parse_to_node(self, lines: List[str], cur_lvl_start="") -> Tuple[Node, int]:
        """Parse the qep into a tree of Nodes"""
        splitted = lines[0].lstrip().lstrip("->").lstrip().split("  ")
        if len(splitted) == 2:
            node_name, _ = splitted
        else:
            raise ValueError(
                f"failed to parse node_name from line: {lines[0]}")

        node = Node(node_name)
        children = []
        subplans = []
        attr_start = cur_lvl_start + STEP
        line_idx = 1

        while line_idx < len(lines):
            line = lines[line_idx]

            # not within this node's scope
            if not line.startswith(attr_start):
                break

            line_content = line[len(attr_start):]
            # "->  HashAggregate  (cost=151746.99..151748.99, ...)"
            if line_content.startswith("->"):
                child, next_index = self._parse_to_node(
                    lines[line_idx:], cur_lvl_start=cur_lvl_start+BIG_STEP)
                children.append(child)
                line_idx += next_index
                continue

            splitted = line_content.split(": ")
            # "Worker 1:  Sort Method: quicksort  Memory: 27kB" -> ignore
            if len(splitted) > 2:
                line_idx += 1
            # "Rows Removed by Fileter: 1974218" -> add attribute
            elif len(splitted) == 2:
                setattr(node, splitted[0].replace(" ", "_"), splitted[1])
                line_idx += 1
            # "Subplan" -> parse subplan
            else:
                subplan, next_index = self._parse_to_node(
                    lines[line_idx+1:], cur_lvl_start=attr_start+BIG_STEP)
                subplans.append(subplan)
                line_idx += next_index + 1

        if children:
            setattr(node, "children", children)
        if subplans:
            setattr(node, "subplans", subplans)

        return node, line_idx

    def _traverse_count_step(self, node):
        ''' Traverse through parsed qep to count steps'''
        self.total_steps += 1
        if getattr(node, "children", None):
            for i in range(len(node.children)):
                self._traverse_count_step(node.children[i])
        if getattr(node, "subplans", None):
            for i in range(0, len(node.subplans)):
                self._traverse_count_step(node.subplans[i])

    def _traverse_add_step(self, node):
        ''' Traverse through parsed qep to add the step '''
        setattr(node, "step", self.total_steps)
        self.total_steps -= 1
        if getattr(node, "subplans", None):
            for i in range(len(node.subplans) - 1, -1, -1):
                self._traverse_add_step(node.subplans[i])
        if getattr(node, "children", None):
            for i in range(len(node.children) - 1, -1, -1):
                self._traverse_add_step(node.children[i])
