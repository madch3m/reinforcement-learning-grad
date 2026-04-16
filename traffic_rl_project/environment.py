"""Core traffic signal environment used across the project."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional

import gymnasium as gym
import numpy as np
from gymnasium import spaces


@dataclass
class Vehicle:
    """Represents a single vehicle in the simulation."""

    arrival_time: float
    lane: int
    waiting_time: float = 0.0
    has_passed: bool = False

    def update_waiting_time(self, dt: float) -> None:
        """Advance waiting time while the vehicle remains queued."""
        if not self.has_passed:
            self.waiting_time += dt


class TrafficGenerator:
    """Generates vehicles according to simple arrival patterns."""

    def __init__(self, arrival_rates: List[float], pattern: str = "uniform"):
        self.base_rates = np.array(arrival_rates, dtype=np.float32)
        self.pattern = pattern

    def generate_vehicles(self, dt: float, current_time: float) -> List[Vehicle]:
        """Generate new vehicles using a Bernoulli approximation per timestep."""
        rates = self._get_current_rates(current_time)
        vehicles: List[Vehicle] = []

        for lane, rate in enumerate(rates):
            if np.random.random() < float(rate) * dt:
                vehicles.append(Vehicle(current_time, lane))

        return vehicles

    def _get_current_rates(self, time: float) -> np.ndarray:
        if self.pattern == "uniform":
            return self.base_rates
        if self.pattern == "rush_hour":
            multiplier = 1.5 + 0.5 * np.sin(2 * np.pi * time / 3600.0)
            return self.base_rates * multiplier
        if self.pattern == "random":
            return self.base_rates * np.random.uniform(0.5, 1.5, size=4)
        return self.base_rates


class TrafficSignalEnv(gym.Env):
    """Gymnasium-compatible 4-way traffic signal environment."""

    metadata = {"render_modes": ["human", "rgb_array"]}

    PHASES = {
        0: {"ns": "green", "ew": "red"},
        1: {"ns": "yellow", "ew": "red"},
        2: {"ns": "red", "ew": "green"},
        3: {"ns": "red", "ew": "yellow"},
    }

    def __init__(
        self,
        arrival_rates: List[float] = [0.2, 0.2, 0.2, 0.2],
        episode_length: int = 3600,
        dt: float = 1.0,
        min_green_time: int = 10,
        yellow_time: int = 3,
        max_queue_length: int = 50,
        traffic_pattern: str = "uniform",
        render_mode: Optional[str] = None,
    ):
        super().__init__()

        self.arrival_rates = arrival_rates
        self.episode_length = episode_length
        self.dt = dt
        self.min_green_time = min_green_time
        self.yellow_time = yellow_time
        self.max_queue_length = max_queue_length
        self.traffic_pattern = traffic_pattern
        self.render_mode = render_mode

        self.observation_space = spaces.Box(
            low=0,
            high=np.array([max_queue_length] * 4 + [1000.0] * 4 + [3.0, 120.0], dtype=np.float32),
            shape=(10,),
            dtype=np.float32,
        )
        self.action_space = spaces.Discrete(2)

        self.traffic_gen = TrafficGenerator(arrival_rates, pattern=traffic_pattern)
        self.queues: List[Deque[Vehicle]] = []
        self.history: Dict[str, List] = {}
        self.reset()

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)

        self.current_time = 0.0
        self.current_phase = 0
        self.phase_time = 0.0
        self.queues = [deque() for _ in range(4)]
        self.total_waiting_time = 0.0
        self.total_vehicles_passed = 0
        self.total_vehicles_arrived = 0
        self.history = {
            "queue_lengths": [],
            "waiting_times": [],
            "throughput": [],
            "phases": [],
        }

        return self._get_observation(), {}

    def step(self, action: int):
        for vehicle in self.traffic_gen.generate_vehicles(self.dt, self.current_time):
            if len(self.queues[vehicle.lane]) < self.max_queue_length:
                self.queues[vehicle.lane].append(vehicle)
                self.total_vehicles_arrived += 1

        if action == 1 and self.phase_time >= self.min_green_time:
            self.current_phase = (self.current_phase + 1) % 4
            self.phase_time = 0.0
        else:
            self.phase_time += self.dt

        vehicles_passed = self._process_vehicles()

        total_waiting = 0.0
        for queue in self.queues:
            for vehicle in queue:
                vehicle.update_waiting_time(self.dt)
                total_waiting += vehicle.waiting_time

        reward = self._calculate_reward(vehicles_passed, total_waiting)

        self.total_vehicles_passed += vehicles_passed
        self.total_waiting_time += total_waiting
        self._log_state()
        self.current_time += self.dt

        terminated = self.current_time >= self.episode_length
        truncated = False
        obs = self._get_observation()
        info = {
            "vehicles_passed": self.total_vehicles_passed,
            "avg_waiting_time": self.total_waiting_time / max(self.total_vehicles_arrived, 1),
            "throughput": self.total_vehicles_passed / max(self.current_time, 1.0),
        }

        return obs, float(reward), terminated, truncated, info

    def _process_vehicles(self) -> int:
        vehicles_passed = 0
        phase_info = self.PHASES[self.current_phase]

        if phase_info["ns"] == "green":
            for lane in (0, 2):
                if self.queues[lane] and np.random.random() < 0.5 * self.dt:
                    vehicle = self.queues[lane].popleft()
                    vehicle.has_passed = True
                    vehicles_passed += 1

        if phase_info["ew"] == "green":
            for lane in (1, 3):
                if self.queues[lane] and np.random.random() < 0.5 * self.dt:
                    vehicle = self.queues[lane].popleft()
                    vehicle.has_passed = True
                    vehicles_passed += 1

        return vehicles_passed

    def _calculate_reward(self, vehicles_passed: int, total_waiting: float) -> float:
        throughput_reward = vehicles_passed * 1.0
        waiting_penalty = -0.01 * total_waiting
        queue_penalty = -0.1 * sum(len(queue) for queue in self.queues)
        switching_penalty = -0.1 if self.phase_time == 0 else 0.0
        return throughput_reward + waiting_penalty + queue_penalty + switching_penalty

    def _get_observation(self) -> np.ndarray:
        queue_lengths = np.array([len(queue) for queue in self.queues], dtype=np.float32)
        avg_waiting = np.zeros(4, dtype=np.float32)
        for idx, queue in enumerate(self.queues):
            if queue:
                avg_waiting[idx] = float(np.mean([vehicle.waiting_time for vehicle in queue]))
        phase_state = np.array([self.current_phase, self.phase_time], dtype=np.float32)
        return np.concatenate([queue_lengths, avg_waiting, phase_state]).astype(np.float32)

    def _log_state(self) -> None:
        self.history["queue_lengths"].append([len(queue) for queue in self.queues])
        self.history["waiting_times"].append(
            [
                float(np.mean([vehicle.waiting_time for vehicle in queue])) if queue else 0.0
                for queue in self.queues
            ]
        )
        self.history["throughput"].append(self.total_vehicles_passed)
        self.history["phases"].append(self.current_phase)

    def render(self):
        if self.render_mode == "rgb_array":
            return self._get_observation()
        if self.render_mode == "human":
            print(
                f"time={self.current_time:.0f}s phase={self.current_phase} "
                f"queues={[len(queue) for queue in self.queues]}"
            )
        return None

    def close(self):
        return None
