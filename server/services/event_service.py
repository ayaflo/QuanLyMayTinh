"""Batch event ingestion service for Open Guardian Kids (F3 & NT2).
Accepts minimal telemetry batches from Client Agents with idempotency keys to guarantee exactly-once ingestion.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timezone

try:
    from ..models import ActivityEvent
    from ..schemas import BatchEventIngestRequest, BatchEventIngestResponse
except (ImportError, ValueError):
    from server.models import ActivityEvent
    from server.schemas import BatchEventIngestRequest, BatchEventIngestResponse


def utc_now():
    return datetime.now(timezone.utc)


def ingest_batch_events(db: Session, batch: BatchEventIngestRequest) -> BatchEventIngestResponse:
    """Ingest a batch of telemetry events.
    Enforces idempotency using idempotency_key to safely handle offline replay without duplicates.
    """
    received_count = len(batch.events)
    ingested_count = 0
    duplicate_count = 0

    if not batch.events:
        return BatchEventIngestResponse(received=0, ingested=0, duplicates=0, status="success")

    # Fetch existing keys in this batch to minimize individual queries
    batch_keys = [ev.idempotency_key for ev in batch.events]
    existing_keys = set(
        k for (k,) in db.query(ActivityEvent.idempotency_key).filter(
            ActivityEvent.idempotency_key.in_(batch_keys)
        ).all()
    )

    new_events = []
    seen_in_batch = set()

    for item in batch.events:
        if item.idempotency_key in existing_keys or item.idempotency_key in seen_in_batch:
            duplicate_count += 1
            continue

        seen_in_batch.add(item.idempotency_key)
        # Ensure subject conforms to NT2 minimal disclosure (truncate full URL if ever sent)
        clean_subject = item.subject.split("/")[0].strip() if item.type in ("web_access", "blocked_domain") else item.subject.strip()

        event_record = ActivityEvent(
            idempotency_key=item.idempotency_key,
            ts=item.ts,
            device_id=item.device_id,
            child_id=item.child_id,
            type=item.type,
            subject=clean_subject,
            duration_sec=item.duration_sec,
            policy_id=item.policy_id,
            created_at=utc_now()
        )
        new_events.append(event_record)
        ingested_count += 1

    if new_events:
        db.add_all(new_events)
        db.commit()

    return BatchEventIngestResponse(
        received=received_count,
        ingested=ingested_count,
        duplicates=duplicate_count,
        status="success"
    )
