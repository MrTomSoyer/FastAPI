# app/app.py
from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from dependencies import get_db_session
from lifespan import lifespan
from services import add_item, get_item, update_item, delete_item

app = FastAPI(
    title="My Ad App",
    description="This is a very simple Ad application API",
    version="0.0.1",
    lifespan=lifespan
)

# Создаём тип для зависимости сессии
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post("/advertisement", response_model=schemas.CreateAdResponse, summary="Создать новое объявление")
async def create_ad(
        ad_data: schemas.CreateAdRequest,
        session: SessionDep
):
    # Используем сервисную функцию
    new_ad = await add_item(session, models.Ad, ad_data)
    return schemas.CreateAdResponse(**new_ad.to_dict())


@app.get("/advertisement/{advertisement_id}", response_model=schemas.GetAdResponse, summary="Получить объявление по ID")
async def get_ad(
        advertisement_id: int,
        session: SessionDep
):
    ad = await get_item(session, models.Ad, advertisement_id)
    # Преобразуем ORM-модель в словарь и затем в Pydantic-схему
    return schemas.GetAdResponse(**ad.to_dict())


@app.get("/advertisement", response_model=list[schemas.GetAdResponse], summary="Получить объявление по полям объявления")
async def get_ad(
        filters: Annotated[schemas.AdvertisementFilter, Query()],
        session: SessionDep
):
    ads = await get_item(session, models.Ad, filters=filters)
    return [
        schemas.GetAdResponse.model_validate(ad)
        for ad in ads
    ]


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.UpdateAdResponse, summary="Обновить объъявление")
async def update_ad(
        advertisement_id: int,
        update_data: schemas.UpdateAdRequest,
        session: SessionDep
):
    updated_ad = await update_item(session, models.Ad, advertisement_id, update_data)
    return schemas.UpdateAdResponse(**updated_ad.to_dict())


@app.delete("/advertisement/{advertisement_id}", response_model=schemas.OKResponse, summary="Удалить объъявление")
async def delete_ad(
        advertisement_id: int,
        session: SessionDep
):
    await delete_item(session, models.Ad, advertisement_id)
    return schemas.OKResponse()
