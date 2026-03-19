"""Test"""

from utils.get_family_relationships import get_family_relationships

def test_get_family_relationships():
    """Gets a list of dicitonaries with probands as keys and a list of
    family ids and their relationships as values"""

    relationships = get_family_relationships()

    assert relationships is not None
    print(type(relationships))
    print(f'THE AMOUNT OF FAMILIES IS: {len(relationships)}')

    print(relationships)


if __name__ == "__main__":
    test_get_family_relationships()