# Errors and Corrections in the `Person` Class

## Original `Person` Class Code (as provided in the task description)

```python
import datetime

class Person:
    def __init__(self, name, year_of_birth, address=''):
        self.name = name
        self.yob = year_of_birth
        self.address = address

    def get_age(self):
        now = datetime.datetime.now()
        return self.yob - now.year # Identified Error 1

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = self.name # Identified Error 2

    def set_address(self, address):
        self.address == address # Identified Error 3

    def get_address(self):
        return self.address

    def is_homeless(self):
        '''
        returns True if address is not set, false in other case
        '''
        return address is None # Identified Error 4
```

## Identified Errors and Their Corrections

Through unit testing, the following errors were discovered in the original `Person` class implementation:

### Identified Error 1: Incorrect Age Calculation in `get_age()` Method

  * **Description:** The original `get_age()` method calculated age by subtracting the current year from the year of birth (`self.yob - now.year`). This would result in an incorrect age, often a negative value (e.g., if `yob` is 1990 and `now.year` is 2023, the result would be -33). The correct calculation should be the current year minus the year of birth.
  * **Correction:** Changed `return self.yob - now.year` to `return now.year - self.yob`.

### Identified Error 2: `set_name()` Method Fails to Update the Name

  * **Description:** The original `set_name(self, name)` method contained the line `self.name = self.name`. This line attempts to assign the current value of `self.name` back to itself, effectively ignoring the new `name` parameter passed to the method. As a result, the person's name could never be updated.
  * **Correction:** Changed `self.name = self.name` to `self.name = name`.

### Identified Error 3: `set_address()` Method Fails to Update the Address

  * **Description:** In the original `set_address(self, address)` method, a comparison operator `==` was used instead of the assignment operator `=`. The statement `self.address == address` performs a boolean comparison and discards the result, rather than assigning the new `address` value to the `self.address` attribute. Therefore, the address could never be updated.
  * **Correction:** Changed `self.address == address` to `self.address = address`.

### Identified Error 4: `is_homeless()` Method Uses Undefined Variable and Incomplete Logic

  * **Description:** The original `is_homeless()` method attempted to use a local variable `address` (`return address is None`) which was not defined within its scope, leading to a `NameError`. Additionally, the problem description implies that a person is homeless if their address is "not set," which should include both `None` and an empty string `''`. The original logic only checked for `None`.
  * **Correction:** Changed `return address is None` to `return self.address is None or self.address == ''`. This correctly references the instance's address attribute and includes the check for an empty string.

## Corrected `Person` Class Code (Final Version)

```python
import datetime
from typing import Optional

class Person:
    """
    A class representing a person with a name, year of birth, and address.
    """
    def __init__(self, name: str, year_of_birth: int, address: Optional[str] = '') -> None:
        self.name = name
        self.yob = year_of_birth
        self.address = address

    def get_age(self) -> int:
        now = datetime.datetime.now()
        return now.year - self.yob # Corrected

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name # Corrected

    def set_address(self, address: Optional[str]) -> None:
        self.address = address # Corrected

    def get_address(self) -> Optional[str]:
        return self.address

    def is_homeless(self) -> bool:
        """
        Returns True if address is not set (None or empty string), False otherwise.
        """
        return self.address is None or self.address == '' # Corrected
```
