from app.use_cases.exceptions.base import UseCaseException


class BatchNotFoundException(UseCaseException):
    @property
    def message(self):
        return "Batch not found"

    def __str__(self):
        return self.message
