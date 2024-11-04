import xml.etree.ElementTree as ET
from collections import defaultdict, Counter


#######################################################################################################################

def parse_rs3(file_path):
    """
    Parses an RS3 file to extract segments, groups, and relation information.

    This function reads the RS3 file at `file_path`, extracting text segments, grouping information, and relation types.
    It returns dictionaries for segments and groups, a nested dictionary tracking relation counts and directions,
    and lists of 'rst' and 'multinuc' relation types.

    Parameters:
    -----------
    file_path : str
        Path to the RS3 XML file.

    Returns:
    --------
    tuple : (dict, dict, dict, list, list)
        - segments : dict
            Mapping of segment IDs to their text, parent ID, and relation name.
        - groups : dict
            Mapping of group IDs to their type, parent ID, and relation name.
        - relation_counts : defaultdict
            Dictionary counting relations by type and direction ('total', 'right', 'left', 'non').
        - rst_relations : list
            List of relation names of type 'rst'.
        - multinuc_relations : list
            List of relation names of type 'multinuc'.
    """

    tree = ET.parse(file_path)
    root = tree.getroot()
    segments = {}
    groups = {}
    relation_counts = defaultdict(lambda: defaultdict(lambda: {'total': 0, 'right': 0, 'left': 0, 'non': 0}))
    rst_relations = []
    multinuc_relations = []

    # Extract relations from the header
    for rel in root.find('header').find('relations').findall('rel'):
        rel_name = rel.get('name')
        rel_type = rel.get('type')
        if rel_type == 'rst':
            rst_relations.append(rel_name)
        elif rel_type == 'multinuc':
            multinuc_relations.append(rel_name)

    # Extract segments
    for segment in root.find('body').findall('segment'):
        seg_id = segment.get('id')
        text = segment.text.strip() if segment.text else ""
        parent = segment.get('parent')
        relname = segment.get('relname')

        segments[seg_id] = {'text': text, 'parent': parent, 'relname': relname}

    # Extract groups
    for group in root.find('body').findall('group'):
        group_id = group.get('id')
        group_type = group.get('type')
        parent = group.get('parent')
        relname = group.get('relname')

        groups[group_id] = {'type': group_type, 'parent': parent, 'relname': relname}

    return segments, groups, relation_counts, rst_relations, multinuc_relations


#######################################################################################################################

class Node:
    """
    Represents a node in a tree structure.

    Each node contains an identifier, optional text content, a type,
    a relation name, and a list of child nodes. This class allows
    for the creation of hierarchical data structures and provides
    methods for adding children, printing the tree structure, and
    collecting relation and position information.

    Attributes:
    -----------
    node_id (str): A unique identifier for the node.
    text (str, optional): Text content associated with the node.
    node_type (str, optional): The type of the node (e.g., 'leaf', 'branch').
    relname (str, optional): The name of the relation associated with the node.
    children (list[Node]): A list of child nodes connected to this node.

    Methods:
    --------
    add_child(child_node: Node) -> None:
        Adds a child node to the current node's children.

    pretty_print(level: int = 0, prefix: str = "") -> str:
        Returns a formatted string representation of the tree structure rooted at this node.

    collect_relations_and_positions(level: int = 0) -> tuple:
        Analyzes the node and its children to count relation occurrences
        and their positions within the tree structure. Returns a tuple
        containing a counter of relations and a counter of their positions.

    __repr__() -> str:
        Returns a string representation of the Node object, useful for debugging.
    """

    def __init__(self, node_id, text=None, node_type=None, relname=None):
        self.node_id = node_id
        self.text = text
        self.node_type = node_type
        self.relname = relname
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def pretty_print(self, level=0, prefix=""):
        # Format for the current node
        node_info = f"{self.node_id}: {self.text or 'No text'}"
        if self.relname:
            node_info += f" (relname: {self.relname})"
        if self.node_type:
            node_info += f" (type: {self.node_type})"

        # Print tree line
        tree_str = f"{prefix}{'└── ' if level > 0 else ''}{node_info}\n"

        # Prepare prefix for children
        if level > 0:
            prefix += "    " if "└" in prefix else "│   "

        # Recursive pretty print for children
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            child_prefix = prefix + ("└── " if is_last else "├── ")
            tree_str += child.pretty_print(level + 1, child_prefix)

        return tree_str

    def collect_relations_and_positions(self, level=0):
        relations_count = Counter()
        position_count = defaultdict(lambda: Counter())

        # Determine position based on level and children
        if level <= 2:
            position = 'top'
        elif not self.children:
            position = 'bottom'
        elif all(not child.children for child in self.children):
            position = 'bottom'
        else:
            position = 'middle'

        # Count the relation and store the position, excluding 'span'
        if self.relname and self.relname != 'span':
            relations_count[self.relname] += 1
            position_count[self.relname][position] += 1

        # Recursive count and position collection for children
        for child in self.children:
            child_relations, child_positions = child.collect_relations_and_positions(level + 1)
            relations_count.update(child_relations)
            for relname, pos_counter in child_positions.items():
                position_count[relname].update(pos_counter)

        return relations_count, position_count

    def __repr__(self):
        return f"Node({self.node_id}, text={self.text}, relname={self.relname})"


#######################################################################################################################

def build_tree(nodes_data, structure_data):
    """
    Constructs a tree from node and structure data.

    Creates `Node` instances from `nodes_data` and `structure_data`, establishing
    parent-child relationships and identifying the root node.

    Parameters:
    -----------
    nodes_data : dict
        A dictionary of node IDs to their attributes (e.g., 'text', 'relname').

    structure_data : dict
        A dictionary of node IDs to their structural attributes (e.g., 'type', 'relname').

    Returns:
    --------
    Node or None:
        The root node of the tree, or None if no root exists.

    Example:
    --------
    nodes_data = {'1': {'text': 'Die Kränzliner , Mankerer , Wustrauer , Walchower und Protzener fühlen sich ungerecht behandelt .', 'parent': '26', 'relname': 'reason-N'}}
    structure_data = {'17': {'type': 'span', 'parent': '18', 'relname': 'span'}}
    """

    nodes = {}

    # Create all nodes from nodes_data
    for node_id, node_info in nodes_data.items():
        nodes[node_id] = Node(
            node_id,
            text=node_info.get('text'),
            relname=node_info.get('relname')
        )

    # Create nodes from structure_data if not already in nodes
    for node_id, node_info in structure_data.items():
        if node_id not in nodes:
            nodes[node_id] = Node(
                node_id,
                node_type=node_info.get('type'),
                relname=node_info.get('relname')
            )

    # Establish parent-child relationships
    root = None
    for node_id, node in nodes.items():
        parent_id = nodes_data.get(node_id, {}).get('parent') or structure_data.get(node_id, {}).get('parent')
        if parent_id is None:
            root = node
        else:
            parent_node = nodes.get(parent_id)
            if parent_node:
                parent_node.add_child(node)

    return root


#######################################################################################################################

def print_tree(root):
    if root:
        print(root.pretty_print())
    else:
        print("No root node found!")


#######################################################################################################################

def analyze_relations_and_positions(root):
    if not root:
        print("No root node for analysis!")
        return

    relations_count, position_count = root.collect_relations_and_positions()

    # Sort relations by count in descending order
    sorted_relations = sorted(relations_count.items(), key=lambda x: x[1], reverse=True)

    print("\nRelation counts:")
    for relname, count in sorted_relations:
        # Build positional breakdown for each relation
        pos_breakdown = ", ".join(f"{pos}: {position_count[relname][pos]} times"
                                  for pos in ['top', 'middle', 'bottom']
                                  if position_count[relname][pos] > 0)
        print(f"{relname}: {count} times ({pos_breakdown})")


#######################################################################################################################

if __name__ == "__main__":
    file_path = 'C:/Users/haufa/OneDrive/Desktop/hiwi/Annotationsvergleich/RST/UP_academic_census-Dietrmar.rs3'
    segments, groups, relation_counts, rst_relations, multinuc_relations = parse_rs3(file_path)

    # Sample data
    nodes_data = segments
    structure_data = groups

    # Build tree from data
    root = build_tree(nodes_data, structure_data)

    # Print the tree
    print("Tree Structure:")
    print_tree(root)

    # Analyze relations and positions
    print("\nAnalysis of Relations and Positions:")
    analyze_relations_and_positions(root)