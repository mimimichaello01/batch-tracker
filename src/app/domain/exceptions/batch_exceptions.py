from dataclasses import dataclass
from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ClosedPartyException(ApplicationException):
    message: str = "Партия уже закрыта. Нельзя добавить код."

    def __str__(self):
        return self.message

@dataclass(eq=False)
class ProductIsAggregatedException(ApplicationException):
    message: str = "Код уже агрегирован и не может быть добавлен в партию."

    def __str__(self):
        return self.message
