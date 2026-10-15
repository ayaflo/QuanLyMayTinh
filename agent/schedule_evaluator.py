"""Weekly schedule matrix evaluator for Open Guardian Kids.
Evaluates 7x48 binary schedule string (336 slots) to determine if computer usage is allowed.
"""

from datetime import datetime
from typing import Optional, Tuple


def get_slot_index(dt: datetime) -> Tuple[int, int, int]:
    """Calculate (weekday, slot_in_day, matrix_index) for given datetime.
    
    - weekday: 0 (Monday) .. 6 (Sunday)
    - slot_in_day: 0 (00:00-00:30) .. 47 (23:30-24:00)
    - matrix_index: 0 .. 335
    """
    weekday = dt.weekday()  # Monday is 0 and Sunday is 6
    slot = dt.hour * 2 + (1 if dt.minute >= 30 else 0)
    matrix_index = weekday * 48 + slot
    return weekday, slot, matrix_index


def is_time_allowed(schedule_matrix: str, dt: Optional[datetime] = None) -> bool:
    """Check if the given datetime is allowed by the 7x48 schedule matrix.
    
    Returns True if allowed ('1'), False if blocked ('0').
    """
    if not schedule_matrix or len(schedule_matrix) < 336:
        return True  # Default open if unconfigured

    if dt is None:
        dt = datetime.now()

    _, _, matrix_index = get_slot_index(dt)
    if 0 <= matrix_index < len(schedule_matrix):
        return schedule_matrix[matrix_index] == "1"

    return True


def get_minutes_until_next_block(schedule_matrix: str, dt: Optional[datetime] = None) -> int:
    """Calculate consecutive allowed minutes remaining before the next scheduled block slot.
    
    Returns minutes (or 999 if no upcoming block today).
    """
    if not schedule_matrix or len(schedule_matrix) < 336:
        return 999

    if dt is None:
        dt = datetime.now()

    weekday, slot, matrix_index = get_slot_index(dt)
    if schedule_matrix[matrix_index] == "0":
        return 0

    # Minutes remaining in current 30m slot
    mins_in_current_slot = 30 - (dt.minute % 30)

    # Check forward slots up to end of week
    remaining_mins = mins_in_current_slot
    curr_idx = matrix_index + 1

    while curr_idx < 336:
        if schedule_matrix[curr_idx] == "0":
            break
        remaining_mins += 30
        curr_idx += 1

    return remaining_mins
