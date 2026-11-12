from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: Annotated[float, Field(gt=0)]
    author: str


class AdvertisementFilter(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Annotated[float| None, Field(gt=0)] = None
    author: str | None = None


class CreateAdRequest(AdvertisementBase):
    pass


class GetAdResponse(AdvertisementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class CreateAdResponse(GetAdResponse):
    id: int


class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Annotated[float| None, Field(gt=0)] = None
    author: str | None = None


class UpdateAdResponse(GetAdResponse):
    pass


class OKResponse(BaseModel):
    status: str = "ok"