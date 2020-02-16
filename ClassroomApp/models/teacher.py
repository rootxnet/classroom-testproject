from dataclasses import dataclass

from .meta import Person


@dataclass
class Teacher(Person):

    # Teacher being a HashedSingleton, will only have one instance
    # per first_name/last name combination, this makes it possible to
    # easily query all quizzes created for given teacher similar to
    # making a DB query
    quiz_set = None

    def __init__(self, *args, **kwargs):
        # init quizzes as list her to avoid issues with immutable objects
        self.quiz_set = []

        super().__init__(*args, **kwargs)

    def __hash__(self):
        """
        Explicitly defined hash, needed for HashedSingleton operations
        """
        return hash((self.first_name, self.last_name))
