
from fastapi import FastAPI, HTTPException, Query

from app.crawler import crawl

app = FastAPI(
    title="AI Tech Consultant - Knowledge Brain",
    version="0.1.0",
    description="Knowledge ingestion API for the AI Tech Consultant capstone.",
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "knowledge-brain"}


@app.post("/ingest")
def ingest(max_pages: int = Query(default=3, ge=1, le=10)):
    """Run a small, bounded ingestion batch."""
    try:
        return crawl(max_pages=max_pages, delay_seconds=1.0)
    except Exception as exc:
        # Keep internal exception details out of the public response.
        raise HTTPException(
            status_code=500,
            detail="Ingestion failed. Check the application logs.",
        ) from exc
