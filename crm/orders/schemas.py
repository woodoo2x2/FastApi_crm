from datetime import datetime



from pydantic import BaseModel, Field

from crm.orders.models import DeliveryMethod


class OrderCreateSchema(BaseModel):
    name: str
    description: str | None
    date_of_creation : datetime
    date_of_send: datetime
    address: str | None
    delivery_method:  DeliveryMethod = Field(default=DeliveryMethod.COURIER)
    price: int = Field(default=0)
    client_id: int | None


