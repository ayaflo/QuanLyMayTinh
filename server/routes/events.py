"""Telemetry event ingestion API routes for Open Guardian Kids (F3 & NT2).
Receives minimal telemetry batches from Client Agents with idempotency keys.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..schemas import BatchEventIngestRequest, BatchEventIngestResponse
    from ..services.event_service import ingest_batch_events
except (ImportError, ValueError):
    from server.database import get_db
    from server.schemas import BatchEventIngestRequest, BatchEventIngestResponse
    from server.services.event_service import ingest_batch_events

router = APIRouter(prefix="/api/v1/events", tags=["Events"])


@router.post("/batch", response_model=BatchEventIngestResponse, status_code=status.HTTP_200_OK, summary="Tiếp nhận lô sự kiện tối thiểu từ tác tử (F3 & NT2)")
def receive_event_batch(
    batch_in: BatchEventIngestRequest,
    db: Session = Depends(get_db)
) -> BatchEventIngestResponse:
    """Ingest a batch of minimal telemetry events.
    Automatically deduplicates repeated submissions via unique idempotency_key.
    """
    return ingest_batch_events(db, batch_in)
