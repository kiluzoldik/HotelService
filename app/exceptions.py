from datetime import date

from fastapi import HTTPException


class BookingException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingException):
    detail = "Все номера забронированы"


class ObjectAlreadyExistsException(BookingException):
    detail = "Объект уже существует"


class DatefromIsLaterThanDatetoException(BookingException):
    detail = "Дата заезда позже или равна дате выезда"


class ViolatesFKException(BookingException):
    detail = "Неверные данные для внешнего ключа"


def check_dates(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise DatefromIsLaterThanDatetoException


class BookingHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = "Номер не найден"


class HotelNotFoundException(BookingException):
    detail = "Отель не найден"


class HotelAlreadyExistsException(BookingException):
    detail = "Отель уже существует"


class HotelAlreadyExistsHTTPException(BookingHTTPException):
    status_code = 409
    detail = "Отель уже существует"


class HotelTitleLengthException(BookingException):
    detail = "Название отеля должно содержать больше 3 символов"


class HotelTitleLengthHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Название отеля должно содержать больше 3 символов"


class HotelTitleLetterException(BookingException):
    detail = "Название отеля должно содержать хотя бы одну букву"


class HotelTitleLetterHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Название отеля должно содержать хотя бы одну букву"


class HotelTitileLetterUpperException(BookingException):
    detail = "Название отеля должно содержать хотя бы одну заглавную букву"


class HotelTitileLetterUpperHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Название отеля должно содержать хотя бы одну заглавную букву"


class HotelLocationLengthException(BookingException):
    detail = "Локация отеля должна быть не менее 5 символов"


class HotelLocationLengthHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Локация отеля должна быть не менее 5 символов"


class RoomNotFoundException(BookingHTTPException):
    detail = "Номер не найден"


class IncorrectTokenException(BookingException):
    detail = "Неверный токен доступа"


class IncorrectPasswordException(BookingException):
    detail = "Неверный пароль"


class IncorrectPasswordOrEmailException(BookingHTTPException):
    status_code = 401
    detail = "Неверный Email или пароль"


class UserAlreadyExistsException(BookingException):
    detail = "Пользователь с таким Email уже существует"


class UserAlreadyExistsHTTPException(BookingHTTPException):
    status_code = 409
    detail = "Пользователь с таким Email уже существует"


class UserEmailNotFoundException(BookingException):
    detail = "Пользователь с таким Email не зарегистрирован"


class UserEmailNotFoundHTTPException(BookingHTTPException):
    detail = "Пользователь с таким Email не зарегистрирован"


class TokenNotFoundException(BookingHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class UserNotAuthenticatedException(BookingException):
    detail = "Вы не авторизованы"


class UserNotAuthenticatedHTTPException(BookingHTTPException):
    status_code = 401
    detail = "Вы не авторизованы"


class AllRoomsAreBookedHTTPException(BookingHTTPException):
    status_code = 409
    detail = "Все номера в этом отеле такого типа уже забронированы"


class LengthPasswordException(BookingException):
    detail = "Пароль должен быть не менее 8 символов"


class DigitPasswordException(BookingException):
    detail = "Пароль должен содержать хотя бы одну цифру"


class UpperLetterPasswordException(BookingException):
    detail = "Пароль должен содержать хотя бы одну заглавную букву"


class SpecialSimbolPasswordException(BookingException):
    detail = "Пароль должен содержать хотя бы один спецсимвол"


class LengthPasswordHTTPException(BookingHTTPException):
    status_code = 422
    detail = "Пароль должен быть не менее 8 символов"


class DigitPasswordHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну цифру"


class UpperLetterPasswordHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну заглавную букву"


class SpecialSimbolPasswordHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы один спецсимвол"


class EmailException(BookingException):
    detail = "Неверный формат Email"


class EmailHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Неверный формат Email"


class FacilityTitleDigitHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Название удобства не доллжно содержать чисел"


class FacilityTitleZeroHTTPException(BookingHTTPException):
    status_code = 400
    detail = "Название удобства должно содержать более двух символов"
