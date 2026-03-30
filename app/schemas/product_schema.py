from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    category: str
    sport: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    sport: str
    price: float
    stock: int

    class Config:
        from_attributes = True