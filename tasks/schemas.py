import datetime
from dataclasses import Field
from typing import Optional

from pydantic import BaseModel

from tasks.models import DeliveryMethod


class OrderBase(BaseModel):
    name: Optional[str] = Field(default="Task", description="Название заказа")
    description: Optional[str] = Field(default=None, description="Описание заказа")
    date_of_creation: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="Дата создания заказа"
    )
    date_of_send: Optional[datetime] = Field(default=None, description="Дата отправки заказа")
    address: Optional[str] = Field(default=None, description="Адрес доставки")
    delivery_method: DeliveryMethod = Field(
        default=DeliveryMethod.COURIER, description="Способ доставки"
    )
    price: Optional[int] = Field(default=0, ge=0, description="Цена заказа")


class OrderCreateSchema(OrderBase):
    pass

class OrderUpdateSchema(OrderBase):
    pass