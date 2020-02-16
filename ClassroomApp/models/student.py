from dataclasses import dataclass

from .meta import Person


@dataclass
class Student(Person):

    def __hash__(self):
        """
        Explicitly defined hash, needed for HashedSingleton operations
        """
        return hash((self.first_name, self.last_name))
