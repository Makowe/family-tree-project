from typing import List, Optional

import rdflib

def get_relation(
        graph: rdflib.Graph,
        subject: rdflib.URIRef,
        object: rdflib.URIRef) -> Optional[rdflib.URIRef]:
    pass


def get_all_relations(
        graph: rdflib.Graph,
        subject: rdflib.URIRef,
        object: rdflib.URIRef) -> List[rdflib.URIRef]:
    pass


def add_relation(
        graph: rdflib.Graph,
        subject: rdflib.URIRef,
        predicate: rdflib.URIRef,
        object: rdflib.URIRef):
    pass


def remove_relation(
        graph: rdflib.Graph,
        subject: rdflib.URIRef,
        predicate: rdflib.URIRef,
        object: rdflib.URIRef):
    pass

