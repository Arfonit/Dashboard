from sqlalchemy import  text
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'

async def refresh_dashboard_repository(session):
    await session.execute(
        text('REFRESH MATERIALIZED VIEW "data-app".final_dashboard')
    )

async def get_dashboard_main_repository(session):
    dashboard_main = await session.execute(
        text(f'''SELECT 
            unique_project_key,
            project_date,
            company_name,
            project_type,
            comment,
            project_budjet,
            extra_work_price,
            extra_work_hours,
            total_extra_pay,
            fact_payment,
            "%_paid" as percent_paid
        FROM "{SCHEMA}".final_dashboard
        ORDER BY project_date DESC''')
    )
    return [dict(row._mapping) for row in dashboard_main]