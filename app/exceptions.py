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
        
class HotelNotFoundException(BookingHTTPException):
    status_code = 404
    detail = "Отель не найден"
    
class RoomNotFoundException(BookingHTTPException):
    status_code = 404
    detail = "Номер не найден"