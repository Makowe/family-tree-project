import datetime
from typing import Dict, List

import rdflib

import family_tree_backend.rdf_interface
from family_tree_backend import rdf_interface, vocab
from family_tree_backend.exceptions import InvalidFamilyTreeError
from family_tree_backend.person import Person


class FamilyTree:

    def __init__(self, ft_name: str):
        self._persons: Dict[rdflib.URIRef, Person] = {}
        self._graph = family_tree_backend.rdf_interface.load_graph(ft_name)

        self._import_ft(ft_name)
        self._last_update: int = hash(self)

        self._auto_complete()

    def __hash__(self):
        return hash((
            self._graph, tuple(self._persons.values())
        ))

    @property
    def persons(self) -> List[Person]:
        return list(self._persons.values())

    @property
    def graph(self, ) -> rdflib.Graph:
        if self._graph_is_up_to_date():
            return self._graph
        else:
            return self._update_graph()

    def _update_graph(self) -> rdflib.Graph:
        self._graph = rdflib.Graph()
        for person in self._persons.values():
            [self._graph.add(triple) for triple in person.triples]
        self._last_update = hash(self)
        return self._graph

    def _graph_is_up_to_date(self) -> bool:
        return hash(self) == self._last_update

    def _import_ft(self, ft_name: str):

        person_nodes = rdf_interface.get_nodes_of_type(self._graph, vocab.FT.person)
        for node in person_nodes:
            person = self._create_person(node)
            self._add_relatives(person, vocab.FT.child)
            self._add_relatives(person, vocab.FT.parent)

    def _create_person(self, node: rdflib.URIRef) -> Person:
        if node in self._persons.keys():
            return self._persons[node]

        first_name = self._graph.value(subject=node, predicate=vocab.FT.first_name.uri)
        last_name = self._graph.value(subject=node, predicate=vocab.FT.last_name.uri)
        birthday = self._graph.value(subject=node, predicate=vocab.FT.birthday.uri)
        if birthday is not None:
            birthday = datetime.date.fromisoformat(birthday)
        sex = self._graph.value(subject=node, predicate=vocab.FT.sex.uri)

        person = Person(node, first_name, last_name, birthday, sex)
        self._persons[node] = person
        return person

    def _add_relatives(self, person: Person, relation: vocab.Vocab):
        relatives_nodes = self._graph.objects(subject=person.urn, predicate=relation.uri)
        for relative_node in relatives_nodes:
            if not isinstance(relative_node, rdflib.URIRef):
                raise InvalidFamilyTreeError(f"The {relation.term} of {person.urn} is not an URI.")
            relative = self._create_person(relative_node)
            person.add_relative(relative, relation)

    def _auto_complete(self):
        self._add_parent_child_relations()

    def _add_parent_child_relations(self):
        for person in self._persons.values():
            [c.add_parent(person) for c in person.children]
            [p.add_child(person) for p in person.parents]
