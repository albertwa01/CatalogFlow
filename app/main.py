from fastapi import FastAPI
from app.api.v1.routers import health
from app.database.sync.session import engine
from contextlib import asynccontextmanager
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Handles DB initialization, connection test, and pool pre-warming.
    """
    # -------------------------
    # Startup
    # -------------------------

    # Test DB connection
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("Database initialized and connection pool ready")
    except Exception as e:
        print(f"Database connection failed: {e}")

    #  Pre-warm connection pool
    conns = []
    for _ in range(10):  # pool_size
        conn = engine.connect()
        conns.append(conn)
    for conn in conns:
        conn.close()
    print("DB connection pool pre-warmed")

    # Yield to indicate the app is running
    yield

    # -------------------------
    # Shutdown
    # -------------------------
    # Here you can clean up resources like cache, queues, etc.
    print("App is shutting down")
    
    
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    debug=settings.APP_ENV == "development"
)

# Include routers
app.include_router(health.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}