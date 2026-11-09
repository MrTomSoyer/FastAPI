from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: int
    author: str
    created_at: datetime


class AdvertisementFilter(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None


class CreateAdRequest(AdvertisementBase):
    pass


class GetAdResponse(AdvertisementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CreateAdResponse(GetAdResponse):
    id: int


class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None
    created_at: datetime | None = None


class UpdateAdResponse(GetAdResponse):
    pass


class OKResponse(BaseModel):
    status: str = "ok"