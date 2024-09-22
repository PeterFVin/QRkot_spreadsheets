from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalar()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ):
        close_projects_date_sorted = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1).order_by(
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)))
        return close_projects_date_sorted.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
