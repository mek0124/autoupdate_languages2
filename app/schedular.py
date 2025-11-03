"""Scheduling and timing functionality for AutoUpdateLanguages2"""

from typing import Callable, Awaitable
from datetime import datetime

import asyncio


class Schedular:
    """Handles scheduling and timing operations"""

    def __init__(self, day_count: int, exp_days: int, delay: int):
        self.day_count = day_count
        self.exp_days = exp_days
        self.delay = delay

    async def run_update_sequence(self, update_callback: Callable[[], Awaitable[None]]):
        """Run the periodic update sequence"""
        today, next_update = await self.get_dates()
        print(f"Today: {today}")

        while self.day_count < self.exp_days:
            remaining_days = self.exp_days - self.day_count
            next_update_str = str(next_update.strftime('%m/%d/%Y'))
            print(f"Day #{self.day_count}) File Update In {remaining_days} days on {next_update_str}")
            await asyncio.sleep(self.delay)
            self.day_count += 1

        else:
            await update_callback()

    async def get_dates(self) -> tuple[datetime, datetime]:
        """Get current date and date for next update"""
        
        today = datetime.now()

        try:
            next_update = datetime(
                today.year,
                today.month + 3,
                today.day
            )
        
        except ValueError:
            next_update = datetime(
                today.year + 1,
                1,
                today.day
            )

        return today, next_update
    
    def get_progress(self) -> dict:
        """Get current progress information"""
        return {
            "current_day": self.day_count,
            "total_days": self.exp_days,
            "remaining_days": self.exp_days - self.day_count,
            "progress_percentage": (self.day_count / self.exp_days) * 100
        }