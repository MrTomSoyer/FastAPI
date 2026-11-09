# app/services.py
from datetime import datetime, timezone

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def add_item(
        session: AsyncSession,
        orm_model: type[models.Ad],
        item_data: schemas.CreateAdRequest
) -> models.Ad:
    """
    Универсальная функция для добавления записи в БД.
    """
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as e:
        await session.rollback()
        # Проверяем, является ли ошибка нарушением уникальности (код 23505 для PostgreSQL)
        if isinstance(e.orig, UniqueViolationError) and e.orig.pgcode == '23505':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with such data already exists."
            )
        else:
            # Если это другая ошибка целостности, пробрасываем её дальше
            raise e


async def get_item(
        session: AsyncSession,
        orm_model: type[models.Ad],
        item_id: int | None = None,
        filters: schemas.AdvertisementFilter | None = None,
):
    if item_id is not None:
        stmt = select(orm_model).where(orm_model.id == item_id)

    else:
        stmt = select(orm_model)

        if filters is not None:
            filter_dict = filters.model_dump(exclude_unset=True)

            for key, value in filter_dict.items():
                column = getattr(orm_model, key)

                if isinstance(value, str):
                    stmt = stmt.where(column.ilike(f"%{value}"))
                else:
                    stmt = stmt.where(column == value)

    result = await session.execute(stmt)

    if item_id is not None:
        item = result.scalar_one_or_none()
    else:
        item = result.scalars().all()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} not found"
        )

    return item


async def update_item(
        session: AsyncSession,
        orm_model: type[models.Ad],
        item_id: int,
        update_data: schemas.UpdateAdRequest
) -> models.Ad:
    """
    Обновляет запись. Если done=True, автоматически проставляет finish_time.
    """
    item = await get_item(session, orm_model, item_id)

    # Преобразуем update_data в словарь, исключая поля со значением None
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
        session: AsyncSession,
        orm_model: type[models.Ad],
        item_id: int
) -> None:
    """
    Удаляет запись.
    """
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()
