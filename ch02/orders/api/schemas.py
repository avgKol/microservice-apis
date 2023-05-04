# Importing required modules
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

# Importing Pydantic classes for data validation and serialization
from pydantic import BaseModel, conint, validator, conlist

# Defining an Enum class to represent the different sizes of a product
class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"

# Defining an Enum class to represent the different status of an order
class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"

# Defining a Pydantic model to represent an item inside an order
class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1
    
    # Defining a validator method to ensure the value of quantity cannot be None and must be greater than or equal to 1
    @validator("quantity")
    def quantity_non_nullable(cls, value):
        assert value is not None, "quantity may not be None"
        return value

# Defining a Pydantic model to represent a complete order
class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_items=1)

# Defining a Pydantic model to represent an order that has already been created
class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum

# Defining a Pydantic model to represent multiple orders at once
class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]