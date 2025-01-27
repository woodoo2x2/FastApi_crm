import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.base import Base  # Убедитесь, что импортируется из правильного места


class DeliveryMethod(enum.Enum):
    COURIER = "COURIER"
    SELFPICKUP = "SELFPICKUP"

class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    PAID = "PAID"
    COMPLETED = "COMPLETED"

    def __str__(self):
        return self.value
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Task")
    description = Column(String, nullable=True)
    date_of_creation = Column(DateTime, default=datetime.utcnow)
    date_of_send = Column(DateTime, nullable=True)
    address = Column(String, nullable=True)
    delivery_method = Column(Enum(DeliveryMethod), default=DeliveryMethod.COURIER)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    price = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"))
    responsable_id = Column(Integer, ForeignKey("users.id"))

    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)

    client = relationship("Client", back_populates="orders")
    author = relationship("User", foreign_keys=[author_id])
    responsable = relationship("User", foreign_keys=[responsable_id])
