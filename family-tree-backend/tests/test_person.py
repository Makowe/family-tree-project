import datetime

import pytest
import rdflib

from family_tree_backend.model import vocab
from family_tree_backend.model.person import Sex, Person


def test_loading_sex():
    assert Sex.from_string("M") == Sex.MALE
    assert Sex.from_string("Male") == Sex.MALE
    assert Sex.from_string("F") == Sex.FEMALE
    assert Sex.from_string("Female") == Sex.FEMALE
    assert Sex.from_string("D") == Sex.DIVERSE
    assert Sex.from_string("Diverse") == Sex.DIVERSE
    assert Sex.from_string(12) is None
    assert Sex.from_string("X") is None

def test_getters():
    urn = rdflib.URIRef("urn:test:aliceSmith")
    date = datetime.date.fromisoformat("1980-01-01")
    person = Person(urn, "Alice", "Smith",
                    date, Sex.FEMALE)
    assert person.urn == urn
    assert person.first_name == "Alice"
    assert person.last_name == "Smith"
    assert person.birthday == date
    assert person.sex == Sex.FEMALE

    assert person.triples == [
        (urn, vocab.RDF.type.uri, vocab.FT.person.uri),
        (urn, vocab.FT.first_name.uri, rdflib.Literal('Alice')),
        (urn, vocab.FT.last_name.uri, rdflib.Literal('Smith')),
        (urn, vocab.FT.birthday.uri, rdflib.Literal('1980-01-01', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema#date'))),
        (urn, vocab.FT.sex.uri, rdflib.Literal('F'))]

def test_getters_empty_data():
    urn = rdflib.URIRef("urn:test:aliceSmith")
    person = Person(urn)
    assert person.urn == urn
    assert person.first_name is None
    assert person.last_name is None
    assert person.birthday is None
    assert person.sex is None

def test_child_parent():
    person = Person(rdflib.URIRef("urn:test:aliceSmith"))

    assert len(person.children) == 0
    assert len(person.parents) == 0

    old_hash = hash(person)
    person2 = Person(rdflib.URIRef("urn:test:bobSmith"))
    person3 = Person(rdflib.URIRef("urn:test:claireSmith"))
    person4 = Person(rdflib.URIRef("urn:test:doraSmith"))

    person.add_parent(person2)
    assert old_hash != hash(person)
    old_hash = hash(person)
    assert len(person.parents) == 1
    assert person.parents[0] is person2

    person.add_parent(person3)
    assert old_hash != hash(person)
    old_hash = hash(person)
    assert len(person.parents) == 2
    assert person.parents[1] is person3

    person.add_child(person4)
    assert old_hash != hash(person)
    old_hash = hash(person)
    assert len(person.children) == 1
    assert person.children[0] is person4

    expected_triples = [
        (person.urn, rdflib.URIRef('urn:family-tree:model#parent'), person2.urn),
        (person.urn, rdflib.URIRef('urn:family-tree:model#parent'), person3.urn),
        (person.urn, rdflib.URIRef('urn:family-tree:model#child'), person4.urn),
    ]
    for triple in expected_triples:
        assert triple in person.triples

def test_add_relative():
    person = Person(rdflib.URIRef("urn:test:aliceSmith"))
    person2 = Person(rdflib.URIRef("urn:test:bobSmith"))
    person3 = Person(rdflib.URIRef("urn:test:claireSmith"))

    person.add_relative(person2, vocab.FT.child)
    person.add_relative(person3, vocab.FT.parent)
    assert person.children[0] is person2
    assert person.parents[0] is person3
    with pytest.raises(ValueError):
        person.add_relative(person3, vocab.FT.first_name)
