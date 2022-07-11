import datetime

import rdflib

from family_tree_backend.person import Person, Sex

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
