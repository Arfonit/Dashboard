from db import SessionLocal
from logger import logger
from repository.dashboard_repository import (refresh_dashboard_repository,
                                            get_dashboard_main_repository)


async def load_dashboard():

    try:

        async with SessionLocal() as session:

            await refresh_dashboard_repository(session)

            await session.commit()

            dashboard = await get_dashboard_main_repository(session)

            logger.info("dashboard loaded")

            return dashboard

    except Exception:

        logger.exception("dashboard load failed")

        raise