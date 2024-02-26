from datetime import datetime
from typing import Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_objects(
    session: AsyncSession,
    model: Union[Donation, CharityProject]
):
    return await session.execute(
        select(model).where(~model.fully_invested)
    )


def update_data(data: Union[Donation, CharityProject]):
    setattr(data, 'fully_invested', True)
    setattr(data, 'close_date', datetime.now())


async def invest(
    projects: List[CharityProject],
    donations: List[Donation]
):
    project_index = 0
    donation_index = 0

    while project_index < len(projects) and donation_index < len(donations):
        project = projects[project_index]
        donation = donations[donation_index]

        project_to_invest = project.full_amount - project.invested_amount
        donation_to_invest = donation.full_amount - donation.invested_amount
        investment = min(project_to_invest, donation_to_invest)

        project.invested_amount += investment
        donation.invested_amount += investment

        if project.invested_amount == project.full_amount:
            update_data(project)
            project_index += 1

        if donation.invested_amount == donation.full_amount:
            update_data(donation)
            donation_index += 1

    return projects, donations


async def save_changes(session: AsyncSession, objects):
    session.add_all(objects)
    await session.commit()


async def investing(session: AsyncSession):
    projects = await get_objects(session, CharityProject)
    donations = await get_objects(session, Donation)
    projects = projects.scalars().all()
    donations = donations.scalars().all()
    projects, donations = await invest(projects, donations)
    await save_changes(session, projects + donations)
