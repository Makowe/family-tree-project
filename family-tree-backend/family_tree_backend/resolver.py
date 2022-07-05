import rdflib

SOURCE_PATH = "family_tree_data"


def load_family_tree(ft_name: str) -> rdflib.Graph:
    graph = rdflib.Graph()
    graph.parse(f"{SOURCE_PATH}/{ft_name}.ttl")
    return graph


def store_family_tree(graph: rdflib.Graph, ft_name: str):
    graph.serialize(destination=f"{SOURCE_PATH}/{ft_name}.ttl", encoding="utf8")
