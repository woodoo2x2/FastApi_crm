class OrderNotFoundException(Exception):
    detail = 'Order not found'


class ClientNotFoundException(Exception):
    detail = 'Client not found'


class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'Not correct password'
