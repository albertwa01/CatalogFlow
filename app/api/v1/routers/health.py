from fastapi import APIRouter
from app.core.logger import logger

router = APIRouter()

@router.get("/health")
def health_check():
    logger.info({"message": "Health endpoint called"})
    try:
        # add actual health checks here
        status = {"status": "ok"}
        logger.info({"message": "Health check successful", "status": status})
        return status
    except Exception as e:
        logger.error({"message": "Health check failed", "error": str(e)})
        return {"status": "error", "detail": str(e)}
