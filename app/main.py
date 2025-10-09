from fastapi import FastAPI,Request
from app.database.sync.session import engine
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logger import logger
import time 
from sqlalchemy import text


#import all routes
from app.api.v1.routers import health
from app.api.v1.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup/shutdown events:
    - Tests DB connection
    - Pre-warms connection pool
    - Initializes logger
    """
    # -------------------------
    # Startup
    # -------------------------
    logger.info("Application startup initiated")

    # Test DB connection
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database initialized and connection pool ready")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    # Pre-warm connection pool
    conns = []
    for _ in range(10):  # pool_size
        conn = engine.connect()
        conns.append(conn)
    for conn in conns:
        conn.close()
    logger.info("DB connection pool pre-warmed")

    yield  # Application is running

    # -------------------------
    # Shutdown
    # -------------------------
    logger.info("Application shutdown initiated")
    # Cleanup tasks like cache, queues can be added here
    logger.info("Application shutdown complete")
    

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    debug=settings.APP_ENV == "development"
)


# -----------------------------
# Middleware: log each request
# -----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = round((time.time() - start_time) * 1000, 2)

    logger.info({
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "execution_time_ms": process_time_ms
    })

    return response


# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}