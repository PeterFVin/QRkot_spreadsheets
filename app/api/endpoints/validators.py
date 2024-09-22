from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject

CHARITY_CREATE_ERROR_MESSAGE = 'Необходимо заполнить все поля!'
CHECK_DUPLICATE_ERROR_MESSAGE = 'Проект с таким именем уже существует!'
CHECK_EXISTS_ERROR_MESSAGE = 'Такого проекта не существует!'
CHECK_DELETE_CLOSED_ERROR_MESSAGE = 'Этот проект закрыт, его нельзя удалить!'
CHECK_DELETE_INVESTED_ERROR_MESSAGE = ('В этот проект уже внесены средства, '
                                       'его нельзя удалить!')
CHECK_UPDATE_CLOSED_ERROR_MESSAGE = 'Этот проект закрыт, его нельзя удалить!'
CHECK_UPDATE_INVESTED_ERROR_MESSAGE = ('Общая сумма проекта должна '
                                       'быть не меньше внесённой!')


def check_charity_project_fields(
        charity_project: str,
) -> None:
    if charity_project.name is None or charity_project.description is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=CHARITY_CREATE_ERROR_MESSAGE
        )


async def check_name_duplicate(
        charity_project: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        charity_project,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CHECK_DUPLICATE_ERROR_MESSAGE
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CHECK_EXISTS_ERROR_MESSAGE
        )
    return charity_project


async def check_update_project_closed(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CHECK_UPDATE_CLOSED_ERROR_MESSAGE
        )
    return charity_project


def check_update_project_invested(
        project,
        full_amount,
) -> CharityProject:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=CHECK_UPDATE_INVESTED_ERROR_MESSAGE
        )
    return project


async def check_delete_project_invested(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CHECK_DELETE_INVESTED_ERROR_MESSAGE
        )
    return charity_project


async def check_delete_project_closed(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CHECK_DELETE_CLOSED_ERROR_MESSAGE
        )
    return charity_project
