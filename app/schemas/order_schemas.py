from pydantic import BaseModel

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total: float
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True