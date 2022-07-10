from typing import List

import rdflib

from family_tree_backend import vocab

SOURCE_PATH = "family_tree_data"


def get_nodes_of_type(graph, node_type: vocab.Vocab) -> List[rdflib.URIRef]:
    result = []
    generator = graph.subjects(
        predicate=vocab.RDF.type.uri,
        object=node_type.uri)
    for node in generator:
        result.append(node)
    return result


def load_graph(ft_name: str) -> rdflib.Graph:
    graph = rdflib.Graph()
    graph.parse(f"{SOURCE_PATH}/{ft_name}.ttl")
    return graph


def store_graph(graph: rdflib.Graph, ft_name: str):
    path = f"{SOURCE_PATH}/{ft_name}.ttl"
    with open(path, "w+") as f:
        f.write("")

    graph.serialize(destination=path, encoding="utf8")