import datetime
from typing import Dict, List, Optional

import rdflib

import family_tree_backend.util.rdf_interface
from family_tree_backend.util import rdf_interface
from family_tree_backend.model import vocab
from family_tree_backend.util.exceptions import InvalidFamilyTreeError
from family_tree_backend.model.person import Person, Sex


class FamilyTree:

    def __init__(self, ft_name: Optional[str] = None):
        self._persons: Dict[rdflib.URIRef, Person] = {}

        self._last_update: int = 0
        """ Stores the hash of the last state when RDF Graph and Family Tree described the
        same information. This field is used as an indicator whether RDF Graph and List of Persons
        are aligned.  
        """

        if ft_name:
            self._graph = family_tree_backend.util.rdf_interface.load_graph(ft_name)
            self.import_ft()
        else:
            self._graph = rdflib.Graph()

        self._auto_complete()

    def __hash__(self):
        return hash((
            self._graph, tuple(self._persons.values())
        ))

    @property
    def persons(self) -> List[Person]:
        return list(self._persons.values())

    def add_person(self, person: Person) -> None:
        if person.urn not in self._persons.keys():
            self._persons[person.urn] = person

    def remove_person(self, person: Person) -> None:
        if person.urn in self._persons.keys():
            self._persons.pop(person.urn)

    @property
    def graph(self, ) -> rdflib.Graph:
        if self._graph_is_up_to_date():
            return self._graph
        else:
            return self._update_graph()

    def _update_graph(self) -> rdflib.Graph:
        """ Regenerates the RDF graph so it is aligned with the List of Persons """
        self._graph = rdflib.Graph()
        for person in self._persons.values():
            [self._graph.add(triple) for triple in person.triples]
        self._set_as_up_to_date()
        return self._graph

    def _graph_is_up_to_date(self) -> bool:
        """ Checks if the information in the RDF Graph and the List of Persons is aligned. """
        return hash(self) == self._last_update

    def _set_as_up_to_date(self):
        self._last_update: int = hash(self)

    def import_ft(self, ft_name: Optional[str] = None):
        if ft_name is not None:
            self._persons = {}
            self._graph = family_tree_backend.util.rdf_interface.load_graph(ft_name)

        person_nodes = rdf_interface.get_nodes_of_type(self._graph, vocab.FT.person)
        for node in person_nodes:
            person = self._create_person(node)
            self._add_relatives(person, vocab.FT.child)
            self._add_relatives(person, vocab.FT.parent)
        self._set_as_up_to_date()
        self._auto_complete()

    def _create_person(self, node: rdflib.URIRef) -> Person:
        if node in self._persons.keys():
            return self._persons[node]

        first_name = self._graph.value(subject=node, predicate=vocab.FT.first_name.uri)
        if first_name is not None:
            first_name = str(first_name)

        last_name = self._graph.value(subject=node, predicate=vocab.FT.last_name.uri)
        if last_name is not None:
            last_name = str(last_name)

        birthday = self._graph.value(subject=node, predicate=vocab.FT.birthday.uri)
        if birthday is not None:
            birthday = datetime.date.fromisoformat(birthday)

        sex = self._graph.value(subject=node, predicate=vocab.FT.sex.uri)
        if sex is not None:
            sex = Sex.from_string(sex)

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
