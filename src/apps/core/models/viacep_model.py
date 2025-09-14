
from pydantic import BaseModel, Field
from typing import Optional


class ViaCEPBase(BaseModel):
    """
    Base for a address
    """
    cep: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    supplement: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    neighborhood: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    uf: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    ibge: Optional[int] = Field(default=None)
    gia: Optional[int] = Field(default=None)
    ddd: Optional[int] = Field(default=None)
    siafi: Optional[int] = Field(default=None)



