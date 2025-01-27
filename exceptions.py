class OrderNotFoundException(Exception):
    detail = 'Order not found'


class ClientNotFoundException(Exception):
    detail = 'Client not found'


class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotConfirmedByAdminException(Exception):
    detail = 'User not confirmed by email. Wait until administrator confirms your account'


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

class AccessTokenNotFound(Exception):
    detail = 'Access token missing or invalid'

class UserNotAdminException(Exception):
    detail = 'User have not permission'