"""
Traffic Signal RL Training with SUMO Scenarios.

Uses the sumo-rl library with built-in SUMO network/route files
and trains a PPO agent via stable-baselines3.

Usage:
    python train_sumo.py                          # Train on single intersection (default)
    python train_sumo.py --scenario single        # Single 4-way intersection
    python train_sumo.py --scenario 2way          # 2-way single intersection
    python train_sumo.py --scenario cologne1      # Real-world: Cologne 1 intersection
    python train_sumo.py --scenario ingolstadt1   # Real-world: Ingolstadt 1 intersection
    python train_sumo.py --scenario grid4x4       # 4x4 grid network (advanced)
    python train_sumo.py --timesteps 200000       # Custom training duration
    python train_sumo.py --gui                    # Enable SUMO GUI visualization
"""

import os
import sys
import argparse
import numpy as np

# SUMO_HOME must be set before importing sumo_rl.
import sumo
os.environ["SUMO_HOME"] = os.path.dirname(sumo.__file__)

import sumo_rl
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, BaseCallback


NETS_DIR = os.path.join(os.path.dirname(sumo_rl.__file__), "nets")

SCENARIOS = {
    "single": {
        "name": "Single 4-Way Intersection",
        "net_file": os.path.join(NETS_DIR, "single-intersection", "single-intersection.net.xml"),
        "route_file": os.path.join(NETS_DIR, "single-intersection", "single-intersection.rou.xml"),
        "num_seconds": 5000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
    "2way": {
        "name": "2-Way Single Intersection",
        "net_file": os.path.join(NETS_DIR, "2way-single-intersection", "single-intersection.net.xml"),
        "route_file": os.path.join(NETS_DIR, "2way-single-intersection", "single-intersection.rou.xml"),
        "num_seconds": 5000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
    "cologne1": {
        "name": "Cologne 1 Intersection (Real-World)",
        "net_file": os.path.join(NETS_DIR, "RESCO", "cologne1", "cologne1.net.xml"),
        "route_file": os.path.join(NETS_DIR, "RESCO", "cologne1", "cologne1.rou.xml"),
        "num_seconds": 3000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
    "ingolstadt1": {
        "name": "Ingolstadt 1 Intersection (Real-World)",
        "net_file": os.path.join(NETS_DIR, "RESCO", "ingolstadt1", "ingolstadt1.net.xml"),
        "route_file": os.path.join(NETS_DIR, "RESCO", "ingolstadt1", "ingolstadt1.rou.xml"),
        "num_seconds": 3000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
    "cologne3": {
        "name": "Cologne 3 Intersections (Real-World)",
        "net_file": os.path.join(NETS_DIR, "RESCO", "cologne3", "cologne3.net.xml"),
        "route_file": os.path.join(NETS_DIR, "RESCO", "cologne3", "cologne3.rou.xml"),
        "num_seconds": 3000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
    "grid4x4": {
        "name": "4x4 Grid Network",
        "net_file": os.path.join(NETS_DIR, "RESCO", "grid4x4", "grid4x4.net.xml"),
        "route_file": os.path.join(NETS_DIR, "RESCO", "grid4x4", "grid4x4.rou.xml"),
        "num_seconds": 3000,
        "delta_time": 5,
        "yellow_time": 3,
        "min_green": 10,
        "max_green": 50,
    },
}


class TrainingProgressCallback(BaseCallback):
    """Logs training progress at regular intervals."""

    def __init__(self, log_interval=5000, verbose=1):
        super().__init__(verbose)
        self.log_interval = log_interval
        self.episode_rewards = []
        self.current_episode_reward = 0.0

    def _on_step(self) -> bool:
        reward = self.locals.get("rewards", [0])[0]
        self.current_episode_reward += reward

        done = self.locals.get("dones", [False])[0]
        if done:
            self.episode_rewards.append(self.current_episode_reward)
            self.current_episode_reward = 0.0

        if self.num_timesteps % self.log_interval == 0 and self.episode_rewards:
            recent = self.episode_rewards[-10:]
            avg_reward = np.mean(recent)
            print(
                f"  Step {self.num_timesteps:>8d} | "
                f"Episodes: {len(self.episode_rewards):>4d} | "
                f"Avg Reward (last 10): {avg_reward:>8.2f}"
            )
        return True


def make_env(scenario_cfg, use_gui=False):
    """Create a SUMO environment from a scenario config dict."""
    return sumo_rl.SumoEnvironment(
        net_file=scenario_cfg["net_file"],
        route_file=scenario_cfg["route_file"],
        use_gui=use_gui,
        num_seconds=scenario_cfg["num_seconds"],
        delta_time=scenario_cfg["delta_time"],
        yellow_time=scenario_cfg["yellow_time"],
        min_green=scenario_cfg["min_green"],
        max_green=scenario_cfg["max_green"],
        single_agent=True,
    )


def train(scenario_name, total_timesteps, use_gui, output_dir):
    scenario_cfg = SCENARIOS[scenario_name]
    print("=" * 70)
    print(f"SUMO RL Training — {scenario_cfg['name']}")
    print("=" * 70)
    print(f"  Scenario:   {scenario_name}")
    print(f"  Timesteps:  {total_timesteps:,}")
    print(f"  GUI:        {use_gui}")
    print(f"  Output:     {output_dir}/")
    print()

    for key in ("net_file", "route_file"):
        if not os.path.isfile(scenario_cfg[key]):
            print(f"ERROR: {key} not found: {scenario_cfg[key]}")
            sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print("Creating training environment...")
    train_env = make_env(scenario_cfg, use_gui=use_gui)

    print("Creating evaluation environment...")
    eval_env = make_env(scenario_cfg, use_gui=False)

    print("Initializing PPO agent...")
    model = PPO(
        "MlpPolicy",
        train_env,
        verbose=0,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        ent_coef=0.01,
        tensorboard_log=os.path.join(output_dir, "tensorboard"),
    )

    obs_space = train_env.observation_space
    act_space = train_env.action_space
    print(f"  Observation space: {obs_space} (dim={obs_space.shape[0]})")
    print(f"  Action space:      {act_space} (n={act_space.n})")
    print()

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.join(output_dir, "best_model"),
        log_path=os.path.join(output_dir, "eval_logs"),
        eval_freq=10_000,
        n_eval_episodes=2,
        deterministic=True,
        verbose=1,
    )
    progress_callback = TrainingProgressCallback(log_interval=5000)

    print(f"Training for {total_timesteps:,} timesteps...")
    print("-" * 70)
    model.learn(
        total_timesteps=total_timesteps,
        callback=[eval_callback, progress_callback],
    )
    print("-" * 70)

    final_path = os.path.join(output_dir, f"ppo_{scenario_name}_final")
    model.save(final_path)
    print(f"\nFinal model saved to: {final_path}.zip")

    train_env.close()
    eval_env.close()

    print("\nTraining complete!")
    print(f"  TensorBoard logs: tensorboard --logdir {output_dir}/tensorboard")
    print(f"  Best model:       {output_dir}/best_model/best_model.zip")


def evaluate(model_path, scenario_name, n_episodes=5, use_gui=False):
    """Evaluate a saved model."""
    scenario_cfg = SCENARIOS[scenario_name]
    print("=" * 70)
    print(f"Evaluating model on: {scenario_cfg['name']}")
    print("=" * 70)

    env = make_env(scenario_cfg, use_gui=use_gui)
    model = PPO.load(model_path)

    results = []
    for ep in range(n_episodes):
        obs, info = env.reset()
        total_reward = 0
        done = False
        steps = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            done = terminated or truncated
            steps += 1

        results.append({"episode": ep + 1, "reward": total_reward, "steps": steps})
        print(f"  Episode {ep + 1}: reward={total_reward:.2f}, steps={steps}")

    env.close()

    avg_reward = np.mean([r["reward"] for r in results])
    print(f"\nAverage reward over {n_episodes} episodes: {avg_reward:.2f}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train traffic signal RL with SUMO")
    parser.add_argument(
        "--scenario", default="single", choices=list(SCENARIOS.keys()),
        help="SUMO scenario to use (default: single)"
    )
    parser.add_argument("--timesteps", type=int, default=100_000, help="Total training timesteps")
    parser.add_argument("--gui", action="store_true", help="Enable SUMO GUI")
    parser.add_argument("--output", default="sumo_models", help="Output directory")
    parser.add_argument(
        "--evaluate", type=str, default=None,
        help="Path to a saved model to evaluate (skip training)"
    )
    parser.add_argument("--eval-episodes", type=int, default=5, help="Number of evaluation episodes")

    args = parser.parse_args()

    if args.evaluate:
        evaluate(args.evaluate, args.scenario, args.eval_episodes, args.gui)
    else:
        train(args.scenario, args.timesteps, args.gui, args.output)
