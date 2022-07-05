FT_NAMESPACE = "urn:family-tree:model#"


class FtTerm:
    def __init__(self, term: str):
        self.term = term

    def __str__(self) -> str:
        return FT_NAMESPACE + self.term

    def __eq__(self, other: 'FtTerm') -> bool:
        return self.term == other.term


class FT:
    c_person = FtTerm("Person")
    p_child = FtTerm("child")
    p_parent = FtTerm("parent")
    p_parnter = FtTerm("partner")
    p_sibling = FtTerm("sibling")
    p_first_name = FtTerm("firstName")
    p_last_name = FtTerm("lastName")
    p_birthday = FtTerm("birthday")
    p_sex = FtTerm("sex")
