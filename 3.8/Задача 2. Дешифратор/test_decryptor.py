import unittest
import sys
import os

# To import the decrypt function from 'decrypt_function.py', ensure it's in the same directory.
# If your function is in a different structure, you might need to adjust this import.
try:
    from decrypt_function import decrypt
except ImportError:
    print("Error: Could not import 'decrypt' function from decrypt_function.py. Ensure the file exists and is accessible.")
    sys.exit(1) # Exit if the function cannot be imported for testing.


class TestDecryptor(unittest.TestCase):
    """
    Unit tests for the decrypt function.
    Tests are grouped logically by the types of dot operations and edge cases,
    covering all examples provided in the problem description.
    """

    def test_no_dots_or_single_dot_rule(self) -> None:
        """
        Tests scenarios where no dots are present or only single dots
        which should be removed without affecting preceding characters.
        """
        test_cases = [
            ("абра-кадабра", "абра-кадабра", "No dots, should remain unchanged"),
            ("абра-кадабра.", "абра-кадабра", "Single dot at end, removed"),
            ("hello.world", "helloworld", "Single dot in middle, removed"),
            ("a.b.c.", "abc", "Multiple single dots, all removed"),
            (".", "", "Only a single dot, should be empty"),
            ("", "", "Empty input string")
        ]
        for encrypted, expected, description in test_cases:
            with self.subTest(f"{description} (Input: '{encrypted}')"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot_rule(self) -> None:
        """
        Tests scenarios where double dots trigger the removal of the preceding character.
        """
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра", "Simple double dot removal"),
            ("абра--..кадабра", "абра-кадабра", "Double dot removing a hyphen"),
            ("1..2.3", "23", "Numbers with double dot, then single dot"),
            ("..abc", "abc", "Double dot at start, no preceding char to remove"),
            ("!a..b", "!b", "Double dot after punctuation removing 'a'")
        ]
        for encrypted, expected, description in test_cases:
            with self.subTest(f"{description} (Input: '{encrypted}')"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_combined_and_complex_rules(self) -> None:
        """
        Tests scenarios combining single and double dot rules, and more complex sequences.
        """
        test_cases = [
            ("абраа..-.кадабра", "абра-кадабра", "Double then single dot on adjacent chars"),
            ("абрау...-кадабра", "абра-кадабра", "Double then single dot, example from problem"), # 'у' removed by '..', then '.' handled
            ("abcde..f.g..h", "abcdf.h", "Complex sequence of removals and single dots"),
            ("x.y..z", "xz", "Single dot, then double dot removing 'y'")
        ]
        for encrypted, expected, description in test_cases:
            with self.subTest(f"{description} (Input: '{encrypted}')"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_edge_cases_and_extensive_removals(self) -> None:
        """
        Tests various edge cases, including extensive removals leading to empty strings.
        """
        test_cases = [
            ("абра........", "", "Extensive double dots, resulting in an empty string"),
            ("абр......a.", "a", "Extensive removal leaving only one character"),
            ("1.......................", "", "Very long removal sequence, resulting in empty"),
            ("...", "", "Multiple dots at start, no effect"),
            ("a.", "a", "Single char then single dot"),
            ("a..", "", "Single char then double dot, removes char"),
            ("b.c", "bc", "Standard removal")
        ]
        for encrypted, expected, description in test_cases:
            with self.subTest(f"{description} (Input: '{encrypted}')"):
                self.assertEqual(decrypt(encrypted), expected)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
