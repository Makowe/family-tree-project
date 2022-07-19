import rdflib

from family_tree_backend.model.family_tree import FamilyTree


def test_empty_family_tree():
    ft = FamilyTree()
    assert (None, None, None) not in ft.graph
    assert len(ft.persons) == 0


def test_import_family_tree():
    ft = FamilyTree("tests/resources/simple_and_complete")
    assert len(ft.persons) == 3
    p1 = None
    p2 = None
    p3 = None
    for p in ft.persons:
        if p.first_name == "Alice":
            p1 = p
        elif p.first_name == "Bob":
            p2 = p
        elif p.first_name == "Clementine":
            p3 = p
        else:
            raise ValueError("Person found that is not specified in the graph")
    assert None not in [p1, p2, p3]