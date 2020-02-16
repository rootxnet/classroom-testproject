import unittest

from models.classrom import Classroom
from models.quiz import Answer, Question, Quiz
from models.student import Student
from models.teacher import Teacher


class ClassroomTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_teacher_creation(self):
        """
        A manager wants to create new teacher in the system
        """
        # test valid Teacher creation
        t1 = Teacher(
            first_name="Johnny",
            last_name="Cash"
        )
        self.assertEqual(t1.first_name, "Johnny")
        self.assertEqual(t1.last_name, "Cash")

        # test required fields, first_name and last_name are required
        with self.assertRaisesRegex(TypeError, "last_name"):
            t0 = Teacher(first_name="Johnny")

        with self.assertRaisesRegex(TypeError, "first_name"):
            t0 = Teacher(last_name="Cash")

        # test Singleton/DB-like properties of Teacher objects,
        # teachers with the same fields are considered the same instance
        t2 = Teacher("David", "Ng")
        t3 = Teacher("David", "Ng")
        self.assertEqual(t2.id, t3.id)

        print("*****************")
        print(Teacher.objects.get(first_name="Davisd"))
        print("*****************")

    def test_student_creation(self):
        # test required fields, first_name and last_name are required
        with self.assertRaisesRegex(TypeError, "last_name"):
            s0 = Student(first_name="Bob")
        with self.assertRaisesRegex(TypeError, "first_name"):
            s0 = Student(last_name="Dylan")

        # test valid Student creation
        s1 = Student(
            first_name="Bob",
            last_name="Dylan"
        )
        self.assertEqual(s1.first_name, "Bob")
        self.assertEqual(s1.last_name, "Dylan")

    def test_classroom_creation(self):
        # test required fields teacher is required, class can be empty otherwise
        with self.assertRaisesRegex(ValueError, "Teacher"):
            c0 = Classroom(teacher=None)

        # test valid Classroom creation
        t1 = Teacher(
            first_name="Johnny",
            last_name="Cash"
        )

        s1 = Student(first_name="Bob", last_name="Dylan")
        s2 = Student(first_name="Willie", last_name="Nelson")
        s3 = Student(first_name="John", last_name="Lennon")

        c1 = Classroom(
            teacher=t1,
            students=[s1, s2, s3]
        )
        self.assertEqual(c1.teacher, t1)
        self.assertEqual(c1.students, [s1, s2, s3])

        # Test post-creation student assignment
        s4 = Student(first_name="Elvis", last_name="Presley")
        c1.students.append(s4)
        self.assertTrue(s4 in c1.students)

        # Test post-creation student removal
        c1.students.remove(s4)
        self.assertFalse(s4 in c1.students)

    def test_answer_creation(self):
        # test required field
        with self.assertRaisesRegex(ValueError, "Value"):
            a0 = Answer(value="")

        # test value assignment
        a1 = Answer(value="2")
        self.assertEqual(a1.value, "2")

    def test_question_creation(self):
        a1 = Answer(value="2")
        a2 = Answer(value="-2")
        a3 = Answer(value="4")
        a4 = Answer(value="4")  # technically the same as a3

        # test required fields, choices is required, class can be empty otherwise
        with self.assertRaises(ValueError):
            q0 = Question(text="What is the value of x in equation x² - 4 = 0",
                          answers=[],
                          choices=[])

        q1 = Question(
            text="What is the value of x in equation x² - 4 = 0",
            choices=[a1, a2, a3],
            answers=[a1, a2],
        )

        # check for duplicate choices
        with self.assertRaisesRegex(ValueError, "Choices"):
            q0 = Question(text="What is the value of x in equation x² - 4 = 0",
                          choices=[a1, a2, a3, a4],
                          answers=[a1, a2], )

        # check for duplicate answers
        with self.assertRaisesRegex(ValueError, "Answers"):
            q0 = Question(text="What is the value of x in equation x² - 4 = 0",
                          choices=[a1, a2, a3],
                          answers=[a1, a3, a4], )

        # check integrity of choices and answers fields
        self.assertTrue({a1, a2, a3} == set(q1.choices))
        self.assertTrue({a1, a2} == set(q1.answers))

    def test_quiz_creation(self):
        t1 = Teacher(
            first_name="Johnny",
            last_name="Cash"
        )

        a1 = Answer(value="2")
        a2 = Answer(value="-2")
        a3 = Answer(value="4")

        q1 = Question(
            text="What is the value of x in equation x² - 4 = 0",
            choices=[a1, a2, a3],
            answers=[a1, a2],
        )

        # valid quiz creation
        quiz1 = Quiz(
            title="Math Quiz",
            question_set=[q1, ],
            author=t1
        )

        # check Quiz field validation
        with self.assertRaisesRegex(ValueError, "Title"):
            quiz0 = Quiz(title="", question_set=[q1, ], author=t1)

        with self.assertRaisesRegex(ValueError, "Author"):
            quiz0 = Quiz(title="Test", question_set=[q1, ], author=None)
            quiz0 = Quiz(title="Test", question_set=[q1, ], author=q1)

        with self.assertRaisesRegex(ValueError, "Question"):
            quiz0 = Quiz(title="Test", question_set=[], author=t1)

        # test whether quiz can be found in Teacher's quiz_set field
        self.assertTrue(quiz1 in t1.quiz_set)

    def test_quiz_validation(self):
        t1 = Teacher(
            first_name="KEK",
            last_name="BUR"
        )

        a1a = Answer(value="2")
        a1b = Answer(value="-2")
        a1c = Answer(value="4")

        q1 = Question(
            text="What is the value of x in equation x² - 4 = 0",
            choices=[a1a, a1b, a1c],
            answers=[a1a, a1b],
        )

        a2a = Answer(value="1")
        a2b = Answer(value="2")
        a2c = Answer(value="-1")

        q2 = Question(
            text="What is the value of x in equation x⁰ = 1",
            choices=[a2a, a2b, a2c],
            answers=[a2a, a2b, a2c],
        )
        # valid quiz creation
        quiz1 = Quiz(
            title="Math Quiz",
            question_set=[q1, q2],
            author=t1
        )

        answer_set = (
            (q1, [a1a, ]),
            (q2, [a2a, a2c, a2b, ])
        )

        # import gc
        # gc.collect()
        # for l in gc.get_referrers(t1):
        #     print(l)
        print("8*8****")
        print()
        print("8*8****")

        t1 = Teacher("Am", "Bam")
        t2 = Teacher("KEK", "BUR")
        t3 = Teacher("BOB", "OMG")
        t4 = Teacher("Am", "Bam")
        print(t1, t2, t3, t4)
        print(id(t1), id(t2), id(t3), id(t4))
        print(t1.quiz_set)
        print(t2.quiz_set)
        print(t3.quiz_set)
        print(t4.quiz_set)
        print("+++")
        print(
            quiz1.validate(answer_set)
        )
