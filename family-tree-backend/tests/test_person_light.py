import datetime

import rdflib

from family_tree_backend.model.person import Person, Sex
from family_tree_backend.model.person_light import PersonLight


def test_person_light_from_complete_person():
    urn = rdflib.URIRef("urn:test:aliceSmith")
    date = datetime.date.fromisoformat("1980-01-01")
    person = Person(urn, "Alice", "Smith",
                    date, Sex.FEMALE)

    person_light = PersonLight.from_person(person)
    assert person_light.urn == "urn:test:aliceSmith"
    assert person_light.first_name == "Alice"
    assert person_light.last_name == "Smith"
    assert person_light.birthday == "1980-01-01"
    assert person_light.sex == "F"


def test_person_light_from_incomplete_person():
    urn = rdflib.URIRef("urn:test:aliceSmith")
    person = Person(urn)
    person_light = PersonLight.from_person(person)
    assert person_light.urn == "urn:test:aliceSmith"
    assert person_light.first_name is None
    assert person_light.last_name is None
    assert person_light.birthday is None
    assert person_light.sex is None

def test_person_light_with_childen():
    person = Person(rdflib.URIRef("urn:test:aliceSmith"))
    person2 = Person(rdflib.URIRef("urn:test:bobSmith"))
    person3 = Person(rdflib.URIRef("urn:test:claireSmith"))

    person.add_child(person2)
    person.add_child(person3)
    person_light = PersonLight.from_person(person)
    assert person_light.children == [
        "urn:test:bobSmith", "urn:test:claireSmith"
    ]

def test_person_light_with_parents():
    person = Person(rdflib.URIRef("urn:test:aliceSmith"))
    person2 = Person(rdflib.URIRef("urn:test:bobSmith"))
    person3 = Person(rdflib.URIRef("urn:test:claireSmith"))

    person.add_parent(person2)
    person.add_parent(person3)
    person_light = PersonLight.from_person(person)
    assert person_light.parents == [
        "urn:test:bobSmith", "urn:test:claireSmith"
    ]

