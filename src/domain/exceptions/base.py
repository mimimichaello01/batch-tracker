from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return 'Произошла ошибка приложения'

    def __str__(self):
        return self.message
