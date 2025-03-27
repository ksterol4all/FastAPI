import pytest

class Student:
    def __init__(self, first_name: str, last_name:str, major:str, year:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('5', int)


def test_person_initialization():
    s = Student("john", "doe", "computer science", 5)
    assert s.first_name == "john"
    assert s.last_name == "doe"
    assert s.major == "computer science"
    assert s.year == 5

@pytest.fixture
def default_employee():
    return Student("john", "maxwell", "food science", 4)


def test_new_person(default_employee):
    assert default_employee.first_name == "john"
    assert default_employee.last_name == "maxwell"
    assert default_employee.major == "food science"
    assert default_employee.year == 4


