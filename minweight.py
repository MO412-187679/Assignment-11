"""Find minimum weight cycle in 'weights.txt'."""
import os.path
import networkx as nx
import numpy as np


def path_to(filename: str):
    """Relative path to `filename` from current 'minweight.py' file."""
    try:
        basedir = os.path.dirname(__file__)
        fullpath = os.path.join(basedir, filename)
        return fullpath
    # some environemnts (like bpython) don't define '__file__',
    # so we assume that the file is in the current directory
    except NameError:
        return filename


def parse_matrix(text: str):
    """Parse text as numeric matrix following 'numpy' format."""
    def numeric_substring(s: str):
        """Removes leading '[' and trailing ']' alongside whitespace around it."""
        return s.strip().lstrip('[').rstrip(']').strip()

    return np.asarray([
        [
            float(item.strip())
            for item in numeric_substring(line).split()
        ]
        for line in numeric_substring(text).split('\n')
    ])


def read_weights(*, filename: str = path_to('weights.txt')):
    """Read weights from the provided file."""

    with open(filename, 'r') as file:
        contents = file.read()
        matrices = (mat.strip() for mat in file.read().split('\n\n'))

    weight: dict[str, np.ndarray] = {}

    for text in contents.split('\n\n'):
        if not (text := text.strip()):
            continue

        name, matrix = text.split('\n', maxsplit=1)
        weight[name.strip()] = parse_matrix(matrix)

    return weight


def read_graph(student: str) -> nx.Graph:
    """Read weighted graph for the given student."""
    weights = read_weights()
    names = {idx: name for idx, name in enumerate(weights.keys())}

    graph = nx.from_numpy_matrix(weights[student])
    return nx.relabel_nodes(graph, names)


def minimum_cycle(graph: nx.Graph) -> list[str]:
    """Find the minimum weight cycle on graph."""
    cycle = nx.approximation.traveling_salesman_problem(graph, cycle=True)
    return cycle[:-1]


def draw_graph(graph: nx.Graph, cycle: list[str]):
    """Draw graph and its components using Matplotlib."""
    from matplotlib import pyplot as plt  # matplotlib is only required for drawing

    # node position (Kamada-Kawai requires SciPy)
    try:
        position = nx.kamada_kawai_layout(graph)
    except ModuleNotFoundError:
        position = None
    # node drawing
    nx.draw(graph, position, with_labels=True, node_size=1000, font_size=10)

    # edges
    capacity = {(u,v): c for u,v,c in graph.edges.data('weight')}
    nx.draw_networkx_edge_labels(graph, position, edge_labels=capacity)

    # draw on a new window
    plt.show(block=True)


if __name__ == '__main__':
    from argparse import ArgumentParser

    # arguments
    parser = ArgumentParser('minweight.py')
    parser.add_argument('-d', '--draw', action='store_true',
        help='draw NetworkX graph using Matplotlib')

    # reading input
    args = parser.parse_args()
    graph = read_graph('Ti')

    # minimum weight
    cycle = minimum_cycle(graph)
    print(cycle)

    # rendering with matplolib
    if args.draw:
        draw_graph(graph, cycle)
