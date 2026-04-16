"""Evaluation helpers for baseline and RL controllers."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import numpy as np


def evaluate_baseline(controller, env, n_episodes: int = 5) -> Dict[str, float]:
    """Evaluate a baseline controller over multiple episodes."""
    metrics = {
        "avg_waiting_time": [],
        "throughput": [],
        "total_passed": [],
    }

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        info = {}

        while not done:
            action = controller.select_action(obs, env)
            obs, _, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        metrics["avg_waiting_time"].append(info["avg_waiting_time"])
        metrics["throughput"].append(info["throughput"])
        metrics["total_passed"].append(info["vehicles_passed"])

    return {
        "controller": controller.name,
        "avg_waiting_time": float(np.mean(metrics["avg_waiting_time"])),
        "avg_throughput": float(np.mean(metrics["throughput"])),
        "avg_vehicles_passed": float(np.mean(metrics["total_passed"])),
        "std_waiting_time": float(np.std(metrics["avg_waiting_time"])),
    }


def evaluate_agent(model, env, n_episodes: int = 10, render: bool = False) -> Dict[str, float]:
    """Evaluate an RL model exposing a Stable-Baselines-like predict method."""
    metrics = {
        "avg_waiting_time": [],
        "throughput": [],
        "total_passed": [],
        "episode_rewards": [],
    }

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        episode_reward = 0.0
        info = {}

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            done = terminated or truncated

            if render:
                env.render()

        metrics["avg_waiting_time"].append(info["avg_waiting_time"])
        metrics["throughput"].append(info["throughput"])
        metrics["total_passed"].append(info["vehicles_passed"])
        metrics["episode_rewards"].append(episode_reward)

    return {
        "controller": "RL Agent (PPO)",
        "avg_waiting_time": float(np.mean(metrics["avg_waiting_time"])),
        "avg_throughput": float(np.mean(metrics["throughput"])),
        "avg_vehicles_passed": float(np.mean(metrics["total_passed"])),
        "std_waiting_time": float(np.std(metrics["avg_waiting_time"])),
        "avg_episode_reward": float(np.mean(metrics["episode_rewards"])),
    }


def compare_controllers(
    controllers: Iterable[Any],
    env,
    n_episodes: int = 10,
    rl_model: Optional[Any] = None,
) -> List[Dict[str, float]]:
    """Evaluate a list of baseline controllers and an optional RL model."""
    results = [evaluate_baseline(controller, env, n_episodes=n_episodes) for controller in controllers]
    if rl_model is not None:
        results.append(evaluate_agent(rl_model, env, n_episodes=n_episodes))
    return results
