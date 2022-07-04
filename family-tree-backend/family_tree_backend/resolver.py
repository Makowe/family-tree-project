import rdflib

SOURCE_PATH = "family_tree_data"


def load_turtle(ft_name: str) -> rdflib.Graph:
    graph = rdflib.Graph()
    graph.parse(f"{SOURCE_PATH}/{ft_name}")
    return graph


def update_bidirectional_edges(graph: rdflib.Graph):
    pass