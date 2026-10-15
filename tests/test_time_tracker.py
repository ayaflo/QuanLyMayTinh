"""Automated tests for Monotonic Time Tracker and Schedule Matrix Evaluator (F1 & M6).
"""

from datetime import datetime, timezone, timedelta
from agent.schedule_evaluator import is_time_allowed, get_slot_index, get_minutes_until_next_block
from agent.screen_time_tracker import ScreenTimeTracker


def test_schedule_evaluator_slots_and_matrix():
    """Verify that schedule evaluator correctly identifies allowed and blocked time slots."""
    # Build a test matrix: All allowed ('1') except Monday 00:00 - 00:30 (slot 0 is '0')
    test_matrix = "0" + ("1" * 335)

    # Monday 00:15 (slot 0) -> Should be False
    monday_midnight = datetime(2026, 10, 12, 0, 15)  # 2026-10-12 is Monday
    assert is_time_allowed(test_matrix, monday_midnight) is False

    # Monday 00:45 (slot 1) -> Should be True
    monday_slot1 = datetime(2026, 10, 12, 0, 45)
    assert is_time_allowed(test_matrix, monday_slot1) is True


def test_schedule_evaluator_slot_index_mapping():
    """Verify mapping of datetime to weekday and 48 slots."""
    # Monday 14:45 -> weekday 0, slot 14*2 + 1 = 29, matrix_index 29
    dt_mon = datetime(2026, 10, 12, 14, 45)
    w, s, idx = get_slot_index(dt_mon)
    assert w == 0
    assert s == 29
    assert idx == 29

    # Tuesday 08:10 -> weekday 1, slot 8*2 + 0 = 16, matrix_index 1*48 + 16 = 64
    dt_tue = datetime(2026, 10, 13, 8, 10)
    w2, s2, idx2 = get_slot_index(dt_tue)
    assert w2 == 1
    assert s2 == 16
    assert idx2 == 64


def test_time_tracker_remaining_and_bonus():
    """Verify screen time tracker remaining calculations and bonus minute increments."""
    tracker = ScreenTimeTracker()
    tracker.used_seconds = 1800  # 30 minutes used
    tracker.bonus_minutes = 0

    base_quota_sec = tracker.get_effective_quota_seconds()
    expected_remaining = base_quota_sec - 1800
    assert tracker.get_remaining_seconds() == expected_remaining

    # Add 15 minutes bonus
    tracker.add_bonus_minutes(15)
    assert tracker.bonus_minutes == 15
    assert tracker.get_remaining_seconds() == expected_remaining + (15 * 60)


def test_server_time_drift_detection_m6():
    """Verify detection of system clock tampering (> 300s drift) under requirement M6."""
    warnings = []
    tracker = ScreenTimeTracker(on_warning=lambda msg: warnings.append(msg))

    now_utc = datetime.now(timezone.utc)

    # 1. Normal sync (drift 2 seconds) -> No alert
    normal_server_time = now_utc - timedelta(seconds=2)
    assert tracker.verify_server_time_drift(normal_server_time) is None
    assert len(warnings) == 0

    # 2. Tampered clock (e.g. child turned clock back by 3 hours = 10800s)
    tampered_server_time = now_utc + timedelta(hours=3)
    drift = tracker.verify_server_time_drift(tampered_server_time)
    assert drift is not None
    assert drift >= 10790
    assert len(warnings) == 1
    assert "lệch" in warnings[0]
