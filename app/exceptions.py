from fastapi import HTTPException, status


class BookException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(status_code=status_code, detail=detail)


class BookNotFoundException(BookException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Buch nicht gefunden")


class BookAlreadyExistsException(BookException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Buch mit dieser ISBN existiert bereits"
        )


class NotEnoughPermissionException(BookException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Nicht genügend Berechtigungen"
        )