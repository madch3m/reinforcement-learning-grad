"""Baseline traffic signal controllers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class BaselineController:
    """Base class for non-learning traffic controllers."""

    name: str

    def select_action(self, observation: np.ndarray, env=None) -> int:
        raise NotImplementedError

    def predict(self, observation: np.ndarray, env=None) -> Tuple[int, Optional[None]]:
        """Stable-Baselines-like interface used by the app and tests."""
        return self.select_action(observation, env), None


class FixedTimeController(BaselineController):
    def __init__(self, green_time: int = 30):
        super().__init__("Fixed-Time")
        self.green_time = green_time

    def select_action(self, observation: np.ndarray, env=None) -> int:
        phase_time = float(observation[9]) if env is None else float(env.phase_time)
        return 1 if phase_time >= self.green_time else 0


class ActuatedController(BaselineController):
    def __init__(self, min_green: int = 10, max_green: int = 60):
        super().__init__("Actuated")
        self.min_green = min_green
        self.max_green = max_green

    def select_action(self, observation: np.ndarray, env=None) -> int:
        queue_lengths = observation[:4]
        current_phase = int(observation[8])
        phase_time = float(observation[9])

        if current_phase in (0, 1):
            active_queues = [queue_lengths[0], queue_lengths[2]]
            waiting_queues = [queue_lengths[1], queue_lengths[3]]
        else:
            active_queues = [queue_lengths[1], queue_lengths[3]]
            waiting_queues = [queue_lengths[0], queue_lengths[2]]

        if phase_time >= self.max_green:
            return 1
        if phase_time >= self.min_green and sum(waiting_queues) > sum(active_queues):
            return 1
        return 0


class MaxPressureController(BaselineController):
    def __init__(self, min_phase_time: int = 10):
        super().__init__("Max-Pressure")
        self.min_phase_time = min_phase_time

    def select_action(self, observation: np.ndarray, env=None) -> int:
        queue_lengths = observation[:4]
        current_phase = int(observation[8])
        phase_time = float(observation[9])

        if phase_time < self.min_phase_time:
            return 0

        ns_pressure = queue_lengths[0] + queue_lengths[2]
        ew_pressure = queue_lengths[1] + queue_lengths[3]

        if current_phase in (0, 1):
            return 1 if ew_pressure > ns_pressure * 1.2 else 0
        return 1 if ns_pressure > ew_pressure * 1.2 else 0
