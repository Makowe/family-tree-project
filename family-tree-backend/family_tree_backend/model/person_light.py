from typing import List, Optional

import pydantic

from family_tree_backend.model.person import Person


class PersonLight(pydantic.BaseModel):
    """ A simple representation of a person without nesting and cycles between people.
    Is used for the API.
    """
    urn: str
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[str]
    sex: Optional[str]
    children: List[str]
    parents: List[str]

    @staticmethod
    def from_person(person: Person):
        return PersonLight(
            urn=str(person.urn),
            first_name=person.first_name,
            last_name=person.last_name,
            birthday=str(person.birthday) if person.birthday else None,
            sex=str(person.sex) if person.sex else None,
            children=[str(c.urn) for c in person.children],
            parents=[str(p.urn) for p in person.parents],
        )
