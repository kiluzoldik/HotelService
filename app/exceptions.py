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