class OrderNotFoundException(Exception):
    detail = 'Order not found'


class ClientNotFoundException(Exception):
    detail = 'Client not found'
