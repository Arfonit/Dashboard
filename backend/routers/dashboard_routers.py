from fastapi import APIRouter

from services.dashboard_service import load_dashboard

router = APIRouter()

@router.get("/dashboard_main")
async def dashboard():
    return await load_dashboard()