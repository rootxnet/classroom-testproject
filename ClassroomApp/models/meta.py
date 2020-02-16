from dataclasses import dataclass


class HashedSingleton(type):
    """
    This metaclass is used to emulate some of the features that relational DBs provide.
    Especially unique instances and reverse lookups similar to ForeignKeys.

    If given instance was previously created, return it, otherwise create a new one.
    """
    _instances = []

    def __call__(cls, *args, **kwargs):
        # fake creation of class to see if there is already an identical one
        inst = super().__call__(*args, **kwargs)
        for i in cls._instances:
            if i == inst:
                return i

        cls._instances.append(inst)
        return inst

    @property
    def objects(cls):
        class Manager:
            def filter(self, **kwargs):
                """
                Filter instances of given class via field1=value1, field2=value2
                :param kwargs: list of fields and values to filter objects against
                :return: generator object with instances that matched
                """
                return filter(lambda y: all([getattr(y, field) == value for field, value in kwargs.items()]),
                              cls._instances)

            def get(self, **kwargs):
                """
                Get instance matching exactly the criteria provided via field1=value1, field2=value2
                Raises KeyError if multiple instances matched
                :param kwargs: list of fields and values to filter objects against
                :return: An instance that was found or None
                """
                instances = list(self.filter(**kwargs))
                if len(instances) > 1:
                    raise KeyError("Filter found more than one instance.")
                if not instances:
                    return
                return instances[0]

            def all(self):
                """
                Get all instances of given class
                :return: generator object with all instances
                """
                return cls._instances

        return Manager()


@dataclass
class Person(metaclass=HashedSingleton):
    first_name: str
    last_name: str

    @property
    def id(self):
        """
        In combination with HashedSingleton, this emulated DB-like ID field
        """
        return id(self)
