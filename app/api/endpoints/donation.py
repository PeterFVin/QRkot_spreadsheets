from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGet
from app.services.invest_funcs import func_donation

DONATION_CREATE_ERROR_MESSAGE = 'Необходимо заполнить поле full_amount!'

router = APIRouter()


@router.post(
    '/',
    response_model=DonationGet,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    if donation.full_amount is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=DONATION_CREATE_ERROR_MESSAGE
        )
    new_donation = await donation_crud.create(
        donation, session, user, no_commit=True
    )
    session.add_all(
        func_donation(
            new_donation,
            await charity_project_crud.get_incompleted(session)))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationGet],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> list[str]:
    return await donation_crud.get_by_user(
        session=session, user=user
    )
