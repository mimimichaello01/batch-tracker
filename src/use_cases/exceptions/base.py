from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException



@dataclass(eq=False)
class UseCaseException(ApplicationException):
    @property
    def message(self):
        return 'В обработки запроса возникла ошибка'
