#!/usr/bin/env python3
"""
Quick Start Script for Traffic Signal RL
Run this to verify your setup and see a quick demo.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

print("=" * 80)
print("TRAFFIC SIGNAL RL - QUICK START DEMO")
print("=" * 80)

# Test imports
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

# Simple environment test
print("\n2. Testing simple traffic environment...")

class SimplifiedTrafficEnv(gym.Env):
    """Minimal traffic environment for testing."""
    
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(low=0, high=100, shape=(10,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.zeros(10, dtype=np.float32)
        self.time = 0
        return self.state, {}
    
    def step(self, action):
        self.time += 1
        self.state += np.random.randn(10) * 0.1
        reward = -np.sum(self.state[:4])  # Minimize queue lengths
        terminated = self.time >= 100
        return self.state, reward, terminated, False, {}

try:
    env = SimplifiedTrafficEnv()
    obs, _ = env.reset()
    print(f"   ✓ Environment created successfully")
    print(f"   - Observation space: {env.observation_space}")
    print(f"   - Action space: {env.action_space}")
    
    # Test a few steps
    for i in range(5):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
    print(f"   ✓ Environment step test passed")
    
except Exception as e:
    print(f"   ✗ Environment test failed: {e}")

# Test RL agent creation
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
    
    # Quick training test (very short)
    print("\n4. Running quick training test (100 steps)...")
    agent.learn(total_timesteps=100, progress_bar=False)
    print("   ✓ Training test passed")
    
except Exception as e:
    print(f"   ✗ Agent test failed: {e}")

# Visualization test
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

# Summary
print("\n" + "=" * 80)
print("SETUP VERIFICATION COMPLETE")
print("=" * 80)
print("\nIf all tests passed (✓), you're ready to run the main notebook!")
print("Next step: jupyter notebook traffic_signal_rl.ipynb")
print("\nIf any tests failed (✗), install missing packages:")
print("  pip install -r requirements.txt")
print("=" * 80)
