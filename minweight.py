"""Find minimum weight cycle in 'weights.txt'."""
from itertools import pairwise
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
    cycle = nx.approximation.christofides(graph)
    cycle = nx.approximation.simulated_annealing_tsp(graph, cycle, max_iterations=25, N_inner=250)
    cycle = nx.approximation.threshold_accepting_tsp(graph, cycle, max_iterations=25, N_inner=250)
    return cycle  # should be enough for 13 nodes


def path_weight(graph: nx.Graph, path: list[str]) -> float:
    """Total weight of path in graph."""
    return nx.path_weight(graph, path, 'weight')


def draw_graph(graph: nx.Graph, cycle: list[str]):
    """Draw graph and its components using Matplotlib."""
    from matplotlib import pyplot as plt  # matplotlib is only required for drawing

    # edges in cycle with stronger colors
    cycle_edges = set(pairwise(cycle)) | set(pairwise(reversed(cycle)))
    colors = ['black' if edge in cycle_edges else 'lightgray' for edge in graph.edges()]
    style = ['solid' if edge in cycle_edges else 'dashed' for edge in graph.edges()]

    # edge weights as widths
    weights = nx.get_edge_attributes(graph, "weight")
    def map_width(weight: float, width: tuple[float, float] = (0.5, 2), maxweight: float = max(weights.values())):
        minwidth, maxwidth = width
        return (weight / maxweight) * (maxwidth - minwidth) + minwidth

    widths = [map_width(weights[edge]) for edge in graph.edges()]

    # nodes
    position = nx.kamada_kawai_layout(graph)
    nx.draw(graph, position,
        with_labels=True, node_size=1000, font_size=10,
        alpha=0.8, style=style, edge_color=colors, width=widths,
    )

    # draw on a new window
    plt.show(block=True)


if __name__ == '__main__':
    from argparse import ArgumentParser

    # arguments
    parser = ArgumentParser('minweight.py')
    parser.add_argument('student', nargs='?', default='Ti',
        help='matrix selector from the input file (default: Ti)')
    parser.add_argument('-d', '--draw', action='store_true',
        help='draw NetworkX graph using Matplotlib')

    # reading input
    args = parser.parse_args()
    graph = read_graph(args.student)

    # minimum weight
    cycle = minimum_cycle(graph)
    print(cycle)
    print('Weight:', path_weight(graph, cycle))

    # rendering with matplolib
    if args.draw:
        draw_graph(graph, cycle)
