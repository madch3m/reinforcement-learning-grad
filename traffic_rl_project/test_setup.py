#!/usr/bin/env python3
"""
Quick Start Script for Traffic Signal RL
Run this to verify your setup and see a quick demo.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("=" * 80)
print("TRAFFIC SIGNAL RL - QUICK START DEMO")
print("=" * 80)

print("\n1. Testing imports...")
try:
    import gymnasium as gym
    from gymnasium import spaces
    print("   ✓ gymnasium")
except ImportError as e:
    print(f"   ✗ gymnasium - {e}")

try:
    from stable_baselines3 import PPO
    print("   ✓ stable-baselines3")
except ImportError as e:
    print(f"   ✗ stable-baselines3 - {e}")

try:
    import torch
    print(f"   ✓ torch (version {torch.__version__})")
except ImportError as e:
    print(f"   ✗ torch - {e}")

try:
    import pandas as pd
    print("   ✓ pandas")
except ImportError as e:
    print(f"   ✗ pandas - {e}")

try:
    import matplotlib.pyplot as plt
    print("   ✓ matplotlib")
except ImportError as e:
    print(f"   ✗ matplotlib - {e}")

print("\n2. Testing project traffic environment...")

try:
    from traffic_rl_project import FixedTimeController, TrafficSignalEnv

    env = TrafficSignalEnv(arrival_rates=[0.2, 0.2, 0.2, 0.2], episode_length=100)
    obs, _ = env.reset()
    print(f"   ✓ Environment created successfully")
    print(f"   - Observation space: {env.observation_space}")
    print(f"   - Action space: {env.action_space}")

    controller = FixedTimeController(green_time=15)
    for i in range(5):
        action, _ = controller.predict(obs, env)
        obs, reward, terminated, truncated, info = env.step(action)
    print(f"   ✓ Environment step test passed")

except Exception as e:
    print(f"   ✗ Environment test failed: {e}")

print("\n3. Testing RL agent creation...")
try:
    from stable_baselines3 import PPO
    
    agent = PPO(
        "MlpPolicy",
        env,
        verbose=0,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=32
    )
    print("   ✓ PPO agent created successfully")
    print(f"   - Policy type: MlpPolicy")
    print(f"   - Learning rate: 3e-4")

    print("\n4. Running quick training test (100 steps)...")
    agent.learn(total_timesteps=100, progress_bar=False)
    print("   ✓ Training test passed")

except Exception as e:
    print(f"   ✗ Agent test failed: {e}")

print("\n5. Testing visualization...")
try:
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)
    ax.set_title("Visualization Test")
    plt.savefig('test_plot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("   ✓ Matplotlib visualization working")
    print("   - Test plot saved as 'test_plot.png'")
except Exception as e:
    print(f"   ✗ Visualization test failed: {e}")

print("\n" + "=" * 80)
print("SETUP VERIFICATION COMPLETE")
print("=" * 80)
print("\nIf all tests passed (✓), you're ready to run the main notebook!")
print("Next step: jupyter notebook traffic_signal_rl.ipynb")
print("\nIf any tests failed (✗), install missing packages:")
print("  pip install -r requirements.txt")
print("=" * 80)
