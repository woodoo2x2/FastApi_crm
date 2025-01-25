class OrderNotFoundException(Exception):
    detail = 'Order not found'


class ClientNotFoundException(Exception):
    detail = 'Client not found'


class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'Not correct password'


class MailConfigError(Exception):
    detail = 'Mail Config is invalid'


class MailNotSendedException(Exception):
    detail = 'Mail not sended'


class TokenNotCorrectException(Exception):
    detail = 'Token not correct'


class TokenExpiredException(Exception):
    detail = 'Token Expired'
