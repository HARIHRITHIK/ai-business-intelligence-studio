from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
import os
import time

from api.routes import router as api_router
from api.routes import sessions

app = FastAPI(
    title="AI Business Intelligence Studio",
    description="Transform raw business data into actionable intelligence.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


async def cleanup_sessions():
    """Remove sessions older than 2 hours every 30 minutes."""
    while True:
        await asyncio.sleep(1800)  # Check every 30 minutes
        try:
            cutoff = time.time() - 7200  # 2 hours
            expired = [
                sid for sid, data in sessions.items()
                if data.get("created_at", 0) < cutoff
            ]
            for sid in expired:
                sessions.pop(sid, None)
        except Exception:
            pass


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_sessions())


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "active_sessions": len(sessions)
    }


# Serve React build as static files (production)
frontend_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")
frontend_dist = os.path.normpath(frontend_dist)

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't intercept API routes (shouldn't happen but safe guard)
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend not built")
