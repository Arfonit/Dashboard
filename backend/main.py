#uvicorn main:app --reload
from fastapi import FastAPI
from routers.dashboard_routers import router as dashboard
from routers.income_routers import router as income
from routers.project_routers import router as project
from routers.comment_routers import router as comment
from routers.company_routers import router as company
from routers.payment_routers import router as payment
from logger import logger

app = FastAPI()

app.include_router(dashboard)
app.include_router(income)
app.include_router(project)
app.include_router(comment)
app.include_router(company)
app.include_router(payment)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"status={response.status_code}")
    return response



