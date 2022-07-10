import datetime
from enum import Enum
from typing import List, Optional, Tuple

import rdflib

from family_tree_backend import vocab


class Sex(Enum):
    MALE = "M"
    FEMALE = "F"
    DIVERSE = "D"


class Person:
    def __init__(self, urn: rdflib.URIRef,
                 first_name: Optional[str],
                 last_name: Optional[str],
                 birthday: Optional[datetime.date],
                 sex: Optional[Sex]):
        self._urn = urn
        self._first_name = first_name
        self._last_name = last_name
        self._birthday = birthday
        self._sex = sex
        self._children = []
        self._parents = []

    def __hash__(self):
        return hash((
            self._urn, self._first_name, self._last_name, self._birthday, self._sex,
            tuple([c.urn for c in self._children]), tuple([p.urn for p in self._parents])
        ))

    @property
    def urn(self) -> rdflib.URIRef:
        return self._urn

    @property
    def first_name(self) -> Optional[str]:
        return self._first_name

    @property
    def last_name(self) -> Optional[str]:
        return self._last_name

    @property
    def birthday(self) -> Optional[datetime.date]:
        return self._birthday

    @property
    def sex(self) -> Optional[Sex]:
        return self._sex

    @property
    def parents(self) -> List['Person']:
        return self._parents

    @property
    def parents(self) -> List['Person']:
        return self._parents

    @property
    def children(self) -> List['Person']:
        return self._children

    def add_parent(self, parent: 'Person'):
        if parent not in self._parents:
            self._parents.append(parent)

    def add_child(self, child: 'Person'):
        if child not in self.children:
            self._children.append(child)

    def add_relative(self, relative: 'Person', relation: vocab.Vocab):
        if relation == "child":
            self.add_child(relative)
        elif relation == "parent":
            self.add_parent(relative)
        else:
            raise ValueError(f"unknown relation {str(relation)}")

    @property
    def triples(self) -> List[Tuple[rdflib.term.Node, rdflib.term.Node, rdflib.term.Node]]:
        result = [
            (self.urn, vocab.RDF.type.uri, vocab.FT.person.uri),
            (self.urn, vocab.FT.first_name.uri, rdflib.Literal(self.first_name)),
            (self.urn, vocab.FT.last_name.uri, rdflib.Literal(self.last_name)),
            (self.urn, vocab.FT.birthday.uri, rdflib.Literal(self.birthday)),
            (self.urn, vocab.FT.sex.uri, rdflib.Literal(self.sex)),
        ]
        [result.append((self.urn, vocab.FT.parent.uri, p.urn)) for p in self.parents]
        [result.append((self.urn, vocab.FT.child.uri, c.urn)) for c in self.children]
        return result
