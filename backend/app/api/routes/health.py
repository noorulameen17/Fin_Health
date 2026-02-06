from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    """Simple health check endpoint"""
    return {"status": "ok", "message": "Service is running"}

@router.get("/status")
async def get_status():
    """Detailed health status"""
    return {
        "status": "healthy",
        "service": "Financial Health Assessment Tool",
        "version": "1.0.0"
    }
