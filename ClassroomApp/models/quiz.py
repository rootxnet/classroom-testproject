from dataclasses import dataclass
from typing import List

from models.teacher import Teacher


@dataclass(frozen=True)  # make immutable, enables comparison checks
class Answer:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Value field cannot be empty")


@dataclass(frozen=True)
class Question:
    text: str
    choices: List[Answer]
    answers: List[Answer]
    weight: int = 1

    def __validate_non_duplicates(self, resource, message):
        dupes = [x for x in resource if resource.count(x) >= 2]
        if dupes:
            raise ValueError("{}: {}".format(message, ", ".join(set([d.value for d in dupes]))))

    def __post_init__(self):
        if not self.choices:
            raise ValueError("Choices field cannot be empty")

        if not self.answers:
            raise ValueError("Answer field cannot be empty")

        if not set(self.answers) <= set(self.choices):
            raise ValueError("Choices field does not contain specified answer(s)")

        # check for duplicate choices
        self.__validate_non_duplicates(resource=self.choices,
                                       message="Choices field contains duplicates")
        # check for duplicate answers
        self.__validate_non_duplicates(resource=self.answers,
                                       message="Answers field contains duplicates")

    def check(self, provided_answer):
        return set(self.answers) == set(provided_answer)


@dataclass(frozen=True)
class Quiz:
    title: str
    question_set: List[Question]
    author: Teacher

    def __post_init__(self):
        if not self.title:
            raise ValueError("Title field cannot be empty")

        if not self.author or not type(self.author) == Teacher:
            raise ValueError("Author is empty or wrong type (Teacher)")

        if not type(self.question_set) == list or not len(self.question_set):
            raise ValueError("Field question_set cannot be empty, provide a list of Question instances")

        # put this quiz in teacher's quiz_set
        if self not in self.author.quiz_set:
            self.author.quiz_set.append(self)

    def validate(self, user_answers):
        failed = []
        for question, answers in user_answers:
            # this will list all answers that were either wrong or missing
            wrong_answers = set(question.answers) ^ set(answers)
            if wrong_answers:
                failed.append(
                    (question, wrong_answers)
                )

        return failed
