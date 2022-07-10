from typing import Union

import rdflib

FT_NAMESPACE = "urn:family-tree:model#"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


class Vocab:
    def __init__(self, namespace: str, term: str):
        self.namespace = namespace
        self.term = term
        self.uri = rdflib.URIRef(self.namespace + self.term)

    def __str__(self) -> str:
        return self.namespace + self.term

    def __eq__(self, other: Union[rdflib.URIRef, 'Vocab', str]) -> bool:
        return str(self) == str(other) or self.term == str(other)


class FT:
    person = Vocab(FT_NAMESPACE, "Person")
    child = Vocab(FT_NAMESPACE, "child")
    parent = Vocab(FT_NAMESPACE, "parent")
    first_name = Vocab(FT_NAMESPACE, "firstName")
    last_name = Vocab(FT_NAMESPACE, "lastName")
    birthday = Vocab(FT_NAMESPACE, "birthday")
    sex = Vocab(FT_NAMESPACE, "sex")

    # planned
    # partner = Vocab(FT_NAMESPACE, "partner")
    # sibling = Vocab(FT_NAMESPACE, "sibling")


class RDF:
    type = Vocab(RDF_NAMESPACE, "type")
