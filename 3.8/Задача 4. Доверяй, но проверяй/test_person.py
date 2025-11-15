import unittest
import datetime
import sys
import os

# Import the Person class from the 'person' module.
# Ensure 'person.py' is in the same directory as 'test_person.py' for this import to work.
from person import Person


class TestPerson(unittest.TestCase):
    """
    Unit tests for the corrected Person class.
    Each method of the Person class is covered by at least one test.
    """

    def setUp(self) -> None:
        """
        Set up a fresh Person instance before each test to ensure isolation.
        Includes instances with and without an initial address.
        """
        self.person1 = Person("Alice", 1990, "123 Main St")
        self.person2 = Person("Bob", 2000)  # Address defaults to ''
        self.person3 = Person("Charlie", 1985, None) # Address explicitly set to None

    def test_init(self) -> None:
        """
        Tests the __init__ method for correct initialization of attributes
        (name, year of birth, and address, including default and None values).
        """
        self.assertEqual(self.person1.name, "Alice")
        self.assertEqual(self.person1.yob, 1990)
        self.assertEqual(self.person1.address, "123 Main St")

        self.assertEqual(self.person2.name, "Bob")
        self.assertEqual(self.person2.yob, 2000)
        self.assertEqual(self.person2.address, '') # Default empty string address

        self.assertEqual(self.person3.name, "Charlie")
        self.assertEqual(self.person3.yob, 1985)
        self.assertIsNone(self.person3.address) # Explicitly None address

    def test_get_age(self) -> None:
        """
        Tests the get_age method to ensure accurate calculation of age
        based on the current year. Includes edge cases like a person born
        in the current year.
        """
        current_year = datetime.datetime.now().year
        self.assertEqual(self.person1.get_age(), current_year - self.person1.yob)
        self.assertEqual(self.person2.get_age(), current_year - self.person2.yob)
        self.assertEqual(self.person3.get_age(), current_year - self.person3.yob)

        # Test for a person born in the current year
        person_born_this_year = Person("Baby", current_year)
        self.assertEqual(person_born_this_year.get_age(), 0)

        # Test for an older person
        person_older = Person("Elder", 1950)
        self.assertEqual(person_older.get_age(), current_year - 1950)

    def test_get_name(self) -> None:
        """
        Tests the get_name method to ensure it returns the correct name.
        """
        self.assertEqual(self.person1.get_name(), "Alice")
        self.assertEqual(self.person2.get_name(), "Bob")
        self.assertEqual(self.person3.get_name(), "Charlie")

    def test_set_name(self) -> None:
        """
        Tests the set_name method to verify that the person's name can be
        successfully updated.
        """
        new_name = "Alicia"
        self.person1.set_name(new_name)
        self.assertEqual(self.person1.name, new_name)
        self.assertEqual(self.person1.get_name(), new_name)

        self.person2.set_name("Robert")
        self.assertEqual(self.person2.get_name(), "Robert")

    def test_set_address(self) -> None:
        """
        Tests the set_address method, including setting to a new string,
        an empty string, and None.
        """
        new_address = "456 Oak Ave"
        self.person1.set_address(new_address)
        self.assertEqual(self.person1.address, new_address)
        self.assertEqual(self.person1.get_address(), new_address)

        self.person2.set_address("") # Set to an empty string
        self.assertEqual(self.person2.address, "")
        self.assertEqual(self.person2.get_address(), "")

        self.person3.set_address(None) # Set to None
        self.assertIsNone(self.person3.address)
        self.assertIsNone(self.person3.get_address())

        self.person1.set_address("789 Pine Rd") # Change an existing address
        self.assertEqual(self.person1.get_address(), "789 Pine Rd")

    def test_get_address(self) -> None:
        """
        Tests the get_address method to ensure it returns the current address,
        including empty string and None cases.
        """
        self.assertEqual(self.person1.get_address(), "123 Main St")
        self.assertEqual(self.person2.get_address(), '')
        self.assertIsNone(self.person3.get_address())

        self.person1.set_address("New Address")
        self.assertEqual(self.person1.get_address(), "New Address")

    def test_is_homeless(self) -> None:
        """
        Tests the is_homeless method to correctly identify homelessness,
        where an empty string or None address indicates homelessness.
        """
        # Person1 initially has an address
        self.assertFalse(self.person1.is_homeless())

        # Person2 initially has an empty string address (considered homeless)
        self.assertTrue(self.person2.is_homeless()) 

        # Person3 initially has a None address (considered homeless)
        self.assertTrue(self.person3.is_homeless())

        # Test changing address status
        self.person2.set_address("789 Beach Blvd") # Give person2 an address
        self.assertFalse(self.person2.is_homeless())

        self.person1.set_address(None) # Make person1 homeless (None)
        self.assertTrue(self.person1.is_homeless())
        
        self.person1.set_address("") # Make person1 homeless (empty string)
        self.assertTrue(self.person1.is_homeless())


if __name__ == '__main__':
    # This block allows running the tests directly when the file is executed.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
