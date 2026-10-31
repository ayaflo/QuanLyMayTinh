"""Screen time tracker and anti-tamper time governance for Open Guardian Kids.
Uses monotonic CPU clock (time.monotonic) to prevent time manipulation,
detects user inactivity (> 5m), issues warnings (10m, 5m, 1m), and grants 60s grace period.
"""

import time
import threading
from datetime import datetime, timezone
from typing import Optional, Callable, Dict, Any

try:
    from .idle_detector import is_user_idle
    from .schedule_evaluator import is_time_allowed, get_minutes_until_next_block
    from .storage import get_daily_usage, update_daily_usage, load_policy_cache
except ImportError:
    from idle_detector import is_user_idle
    from schedule_evaluator import is_time_allowed, get_minutes_until_next_block
    from storage import get_daily_usage, update_daily_usage, load_policy_cache


class ScreenTimeTracker:
    """Tracks active screen time using monotonic clock and enforces daily quotas."""

    def __init__(
        self,
        on_lock_trigger: Optional[Callable[[str], None]] = None,
        on_warning: Optional[Callable[[str], None]] = None,
        on_schedule_block: Optional[Callable[[str], None]] = None,
        on_schedule_allowed: Optional[Callable[[], None]] = None
    ):
        self.on_lock_trigger = on_lock_trigger
        self.on_warning = on_warning
        self.on_schedule_block = on_schedule_block
        self.on_schedule_allowed = on_schedule_allowed

        self.running = False
        self._thread: Optional[threading.Thread] = None

        # Schedule countdown tracking
        self.schedule_countdown_active = False
        self.locked_by_schedule = False

        # Current date tracking (YYYY-MM-DD)
        self.current_date_str = datetime.now().strftime("%Y-%m-%d")

        # In-memory tracking
        self.used_seconds = 0
        self.bonus_minutes = 0
        self.is_locked = False
        self.grace_period_active = False
        self.grace_start_monotonic = 0.0

        # Warning flags to prevent repeated notifications
        self.warned_10m = False
        self.warned_5m = False
        self.warned_1m = False

        # Load persisted usage for today
        self._load_today_usage()

    def _load_today_usage(self) -> None:
        """Load persisted seconds from local SQLite."""
        self.current_date_str = datetime.now().strftime("%Y-%m-%d")
        data = get_daily_usage(self.current_date_str)
        self.used_seconds = data.get("used_seconds", 0)
        self.bonus_minutes = data.get("bonus_minutes", 0)
        self.is_locked = bool(data.get("is_locked", 0))

    def _save_today_usage(self) -> None:
        """Persist current seconds into local SQLite."""
        update_daily_usage(
            date_str=self.current_date_str,
            used_seconds=int(self.used_seconds),
            bonus_minutes=self.bonus_minutes,
            is_locked=1 if self.is_locked else 0
        )

    def add_bonus_minutes(self, minutes: int) -> None:
        """Add bonus time awarded by parent via WebSocket command."""
        self.bonus_minutes += minutes
        self.is_locked = False
        self.locked_by_schedule = False
        self.schedule_countdown_active = False
        self.grace_period_active = False
        # Reset warnings if time increased significantly
        if self.get_remaining_seconds() > 600:
            self.warned_10m = False
        if self.get_remaining_seconds() > 300:
            self.warned_5m = False
        if self.get_remaining_seconds() > 60:
            self.warned_1m = False
        self._save_today_usage()

    def get_effective_quota_seconds(self) -> int:
        """Calculate total allowed seconds for today based on weekday/weekend and bonus."""
        now = datetime.now()
        is_weekend = now.weekday() in (5, 6)

        policy = load_policy_cache()
        if policy:
            base_quota_minutes = policy["weekend_quota_minutes"] if is_weekend else policy["weekday_quota_minutes"]
        else:
            base_quota_minutes = 150 if is_weekend else 90

        total_minutes = base_quota_minutes + self.bonus_minutes
        return total_minutes * 60

    def get_remaining_seconds(self) -> int:
        """Return remaining allowed seconds for today."""
        total_seconds = self.get_effective_quota_seconds()
        remaining = total_seconds - self.used_seconds
        return max(0, int(remaining))

    def get_remaining_minutes(self) -> int:
        """Return remaining minutes rounded down."""
        return self.get_remaining_seconds() // 60

    def verify_server_time_drift(self, server_time_utc: datetime) -> Optional[float]:
        """Verify time difference between server UTC and local system UTC.
        
        If drift > 300s (5 minutes), logs an alert (M6).
        """
        local_utc = datetime.now(timezone.utc)
        if server_time_utc.tzinfo is None:
            server_time_utc = server_time_utc.replace(tzinfo=timezone.utc)

        drift_seconds = abs((local_utc - server_time_utc).total_seconds())
        if drift_seconds > 300.0:
            if self.on_warning:
                self.on_warning(f"Cảnh báo: Đồng hồ hệ thống lệch {int(drift_seconds)} giây so với máy chủ!")
            return drift_seconds
        return None

    def recheck_schedule_now(self) -> bool:
        """Immediately evaluate the current schedule matrix and trigger countdown/lock if forbidden.
        
        Returns True if time is currently allowed, False if blocked by schedule.
        """
        try:
            policy = load_policy_cache()
            matrix = policy.get("schedule_matrix", "") if policy else ""
            allowed = is_time_allowed(matrix)
            if not allowed:
                # Outside scheduled hours
                if not self.locked_by_schedule and not self.schedule_countdown_active:
                    self.schedule_countdown_active = True
                    reason = "Đang trong khoảng thời gian cấm sử dụng máy tính theo lịch của cha mẹ"
                    if self.on_schedule_block:
                        self.on_schedule_block(reason)
                    else:
                        self.is_locked = True
                        self.locked_by_schedule = True
                        self._save_today_usage()
                        if self.on_lock_trigger:
                            self.on_lock_trigger(reason)
                elif self.locked_by_schedule:
                    self.is_locked = True
                return False
            else:
                # Inside scheduled hours
                if self.schedule_countdown_active:
                    self.schedule_countdown_active = False
                    if self.on_schedule_allowed:
                        self.on_schedule_allowed()
                if self.locked_by_schedule and self.get_remaining_seconds() > 0:
                    self.is_locked = False
                    self.locked_by_schedule = False
                    self._save_today_usage()
                return True
        except Exception as e:
            print(f"[TRACKER] Error in recheck_schedule_now: {e}")
            return True

    def start(self) -> None:
        """Start tracking loop in a background thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="ScreenTimeTracker")
        self._thread.start()

    def stop(self) -> None:
        """Stop tracking loop and save state."""
        self.running = False
        self._save_today_usage()

    def _run_loop(self) -> None:
        """Core tracking loop executing every second using time.monotonic()."""
        last_monotonic = time.monotonic()

        while self.running:
            try:
                time.sleep(1.0)
                now_mono = time.monotonic()
                delta_seconds = now_mono - last_monotonic
                last_monotonic = now_mono

                # Check if day changed (midnight rollover)
                today_str = datetime.now().strftime("%Y-%m-%d")
                if today_str != self.current_date_str:
                    self._save_today_usage()
                    self._load_today_usage()
                    self.warned_10m = False
                    self.warned_5m = False
                    self.warned_1m = False
                    self.is_locked = False
                    self.locked_by_schedule = False
                    self.schedule_countdown_active = False
                    self.grace_period_active = False

                # Check schedule matrix (F1 7x48)
                policy = load_policy_cache()
                matrix = policy.get("schedule_matrix", "") if policy else ""
                allowed_by_schedule = is_time_allowed(matrix)

                # If currently outside scheduled hours
                if not allowed_by_schedule:
                    # Trigger schedule block if not already in a schedule-based countdown/lock.
                    if not self.locked_by_schedule and not self.schedule_countdown_active:
                        self.schedule_countdown_active = True
                        reason = "Đang trong khoảng thời gian cấm sử dụng máy tính theo lịch của cha mẹ"
                        if self.on_schedule_block:
                            self.on_schedule_block(reason)
                        else:
                            self.is_locked = True
                            self.locked_by_schedule = True
                            self._save_today_usage()
                            if self.on_lock_trigger:
                                self.on_lock_trigger(reason)
                    elif self.locked_by_schedule:
                        self.is_locked = True
                    continue
                else:
                    # Outside forbidden hours (time is allowed)
                    if self.schedule_countdown_active:
                        self.schedule_countdown_active = False
                        if self.on_schedule_allowed:
                            self.on_schedule_allowed()
                    if self.locked_by_schedule and self.get_remaining_seconds() > 0:
                        self.is_locked = False
                        self.locked_by_schedule = False
                        self._save_today_usage()

                # Check user inactivity (Idle > 5m = 300s)
                if is_user_idle(300.0):
                    # User is away: DO NOT increment used screen time
                    continue

                # Increment active screen time using monotonic delta
                self.used_seconds += delta_seconds
                remaining = self.get_remaining_seconds()

                # Warning thresholds (NT4)
                if remaining <= 600 and not self.warned_10m and remaining > 300:
                    self.warned_10m = True
                    if self.on_warning:
                        self.on_warning("Em còn 10 phút sử dụng máy tính hôm nay.")

                elif remaining <= 300 and not self.warned_5m and remaining > 60:
                    self.warned_5m = True
                    if self.on_warning:
                        self.on_warning("Em còn 5 phút sử dụng máy tính. Hãy chuẩn bị lưu lại bài tập nhé!")

                elif remaining <= 60 and not self.warned_1m and remaining > 0:
                    self.warned_1m = True
                    if self.on_warning:
                        self.on_warning("Chỉ còn 1 phút! Máy tính sắp khóa màn hình.")

                # Grace period logic (60 seconds)
                if remaining <= 0:
                    if not self.grace_period_active:
                        self.grace_period_active = True
                        self.grace_start_monotonic = time.monotonic()
                        if self.on_warning:
                            self.on_warning("Đã hết giờ sử dụng! Em có đúng 60 giây ân hạn để lưu bài trước khi khóa máy.")
                    else:
                        grace_elapsed = time.monotonic() - self.grace_start_monotonic
                        if grace_elapsed >= 60.0:
                            self.is_locked = True
                            self._save_today_usage()
                            if self.on_lock_trigger:
                                self.on_lock_trigger("Hết thời gian sử dụng trong ngày!")

                # Periodic save every 30 seconds
                if int(self.used_seconds) % 30 == 0:
                    self._save_today_usage()
            except Exception as e:
                # Catch-all to ensure tracking loop never crashes
                time.sleep(1.0)
