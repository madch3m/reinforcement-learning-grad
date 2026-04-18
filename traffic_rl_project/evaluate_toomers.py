"""
Evaluate baseline controllers against real Toomer's Corner traffic data.

Input: traffic_rl_project/data/toomers_traffic.csv
  Columns: minute, north, south, east, west (vehicles per minute per direction)

Output: traffic_rl_project/results/toomers/*.png and summary.txt

Caveats:
  - Real data is likely aggregated across multiple lanes per approach.
    We divide by LANES_PER_APPROACH to get a per-lane arrival rate.
  - Simple TrafficSignalEnv doesn't model right-turn-on-red rules or
    pedestrians; treat results as directional performance only.
"""

import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from traffic_rl_project import (  # noqa: E402
    ActuatedController,
    FixedTimeController,
    MaxPressureController,
    TrafficSignalEnv,
)

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

CSV_PATH = os.path.join(HERE, "data", "toomers_traffic.csv")
OUT_DIR = os.path.join(HERE, "results", "toomers")
os.makedirs(OUT_DIR, exist_ok=True)

# Toomer's Corner lane configuration: N-S is the heavy arterial (2 lanes per
# approach), E-W is a lighter cross street (1 lane per approach).
# Order: [North, East, South, West]
LANES_PER_APPROACH = [2, 1, 2, 1]
SECONDS_PER_MINUTE = 60
RANDOM_SEED = 42


# ----------------------------------------------------------------------------
# Load and prepare data
# ----------------------------------------------------------------------------

def load_toomers_data(csv_path):
    """Return list of (minute, rates[N,E,S,W]) tuples in vehicles/sec/lane."""
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # CSV is vehicles/min aggregated across all lanes of that approach.
            # Divide by per-approach lane count to get per-lane per-second rate.
            counts = [int(row["north"]), int(row["east"]),
                      int(row["south"]), int(row["west"])]
            rates = [c / SECONDS_PER_MINUTE / lanes
                     for c, lanes in zip(counts, LANES_PER_APPROACH)]
            rows.append((int(row["minute"]), rates))
    return rows


# ----------------------------------------------------------------------------
# Evaluation loop with time-varying arrival rates
# ----------------------------------------------------------------------------

def run_controller_on_data(controller, minute_rates, seed=RANDOM_SEED):
    """Run one controller through all minutes of Toomer's data.

    Returns dict with per-step queue lengths, rewards, throughput, phase history.
    """
    np.random.seed(seed)
    # Initial env with first minute's rates; long episode_length so it won't terminate.
    env = TrafficSignalEnv(
        arrival_rates=minute_rates[0][1],
        min_green_time=10,
        episode_length=len(minute_rates) * SECONDS_PER_MINUTE + 10,
    )
    obs, _ = env.reset()

    history = {
        "queue_lengths": [],    # [[N, E, S, W], ...] per step
        "rewards": [],
        "throughput": [],       # cumulative vehicles passed
        "phases": [],
        "waiting_avg": [],      # avg waiting across queued vehicles
    }

    for minute, rates in minute_rates:
        # Update both env and its traffic generator for this minute
        env.arrival_rates = rates
        env.traffic_gen.base_rates = np.array(rates, dtype=np.float32)
        # Simulate 60 seconds of this minute
        for _ in range(SECONDS_PER_MINUTE):
            action, _ = controller.predict(obs, env=env)
            obs, reward, _, _, info = env.step(action)
            history["queue_lengths"].append([len(q) for q in env.queues])
            history["rewards"].append(reward)
            history["throughput"].append(env.total_vehicles_passed)
            history["phases"].append(env.current_phase)
            all_waiting = [v.waiting_time for q in env.queues for v in q]
            history["waiting_avg"].append(np.mean(all_waiting) if all_waiting else 0.0)

    return {
        "name": controller.name,
        "total_passed": env.total_vehicles_passed,
        "total_arrived": env.total_vehicles_arrived,
        "avg_waiting": env.total_waiting_time / max(env.total_vehicles_arrived, 1),
        "avg_throughput": env.total_vehicles_passed / env.current_time,
        "final_queue_total": sum(len(q) for q in env.queues),
        "history": history,
    }


# ----------------------------------------------------------------------------
# Visualizations
# ----------------------------------------------------------------------------

def plot_all(results, data, out_dir):
    """Generate 5 comparison plots."""
    controllers = list(results.keys())
    colors = {"Fixed-Time": "#3498db", "Actuated": "#2ecc71", "Max-Pressure": "#e67e22"}

    # Plot 1: Arrival rate profile from CSV
    fig, ax = plt.subplots(figsize=(10, 4))
    minutes = [m for m, _ in data]
    arrays = np.array([r for _, r in data])  # shape (15, 4) in veh/sec/lane
    labels = ["North", "East", "South", "West"]
    for i, label in enumerate(labels):
        # Convert back to raw veh/min per approach for the plot
        raw = arrays[:, i] * LANES_PER_APPROACH[i] * 60
        ax.plot(minutes, raw, marker="o", label=f"{label} ({LANES_PER_APPROACH[i]} lanes)")
    ax.set_xlabel("Minute")
    ax.set_ylabel("Vehicles per Minute (raw from CSV)")
    ax.set_title("Toomer's Corner - Traffic Arrival Profile")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    p = os.path.join(out_dir, "01_arrival_profile.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 2: Summary bar chart (avg waiting time)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    waits = [results[c]["avg_waiting"] for c in controllers]
    throughputs = [results[c]["avg_throughput"] for c in controllers]
    bar_colors = [colors[c] for c in controllers]

    axes[0].bar(controllers, waits, color=bar_colors, edgecolor="black")
    axes[0].set_ylabel("Average Waiting Time (seconds)")
    axes[0].set_title("Lower is Better")
    for i, w in enumerate(waits):
        axes[0].text(i, w, f"  {w:.1f}s", ha="center", va="bottom", fontweight="bold")
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].bar(controllers, throughputs, color=bar_colors, edgecolor="black")
    axes[1].set_ylabel("Throughput (vehicles/sec)")
    axes[1].set_title("Higher is Better")
    for i, t in enumerate(throughputs):
        axes[1].text(i, t, f"  {t:.2f}", ha="center", va="bottom", fontweight="bold")
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("Controller Performance on Toomer's Corner Data (15-min evaluation)")
    plt.tight_layout()
    p = os.path.join(out_dir, "02_summary_comparison.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 3: Total queue length over time
    fig, ax = plt.subplots(figsize=(12, 5))
    for c in controllers:
        queues = np.array(results[c]["history"]["queue_lengths"])
        total_queue = queues.sum(axis=1)
        ax.plot(total_queue, label=c, color=colors[c], linewidth=1.5)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Total Queue Length (all 4 approaches)")
    ax.set_title("Queue Evolution Over 15-Minute Evaluation")
    ax.legend()
    ax.grid(True, alpha=0.3)
    # Mark minute boundaries
    for minute_boundary in range(60, 15 * 60, 60):
        ax.axvline(minute_boundary, color="gray", linestyle=":", alpha=0.3)
    plt.tight_layout()
    p = os.path.join(out_dir, "03_queue_evolution.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 4: Cumulative throughput
    fig, ax = plt.subplots(figsize=(12, 5))
    for c in controllers:
        tp = results[c]["history"]["throughput"]
        ax.plot(tp, label=c, color=colors[c], linewidth=2)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Cumulative Vehicles Passed")
    ax.set_title("Throughput Accumulation Over Evaluation")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    p = os.path.join(out_dir, "04_cumulative_throughput.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 5: Per-approach queue comparison
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    approach_names = ["North", "East", "South", "West"]
    for idx, approach_name in enumerate(approach_names):
        ax = axes[idx // 2][idx % 2]
        for c in controllers:
            queues = np.array(results[c]["history"]["queue_lengths"])
            ax.plot(queues[:, idx], label=c, color=colors[c], linewidth=1.2, alpha=0.85)
        ax.set_title(f"{approach_name} Approach")
        ax.set_ylabel("Queue Length")
        ax.grid(True, alpha=0.3)
        if idx == 0:
            ax.legend(loc="upper right", fontsize=9)
    axes[1][0].set_xlabel("Time (seconds)")
    axes[1][1].set_xlabel("Time (seconds)")
    fig.suptitle("Per-Approach Queue Lengths", fontsize=14)
    plt.tight_layout()
    p = os.path.join(out_dir, "05_per_approach_queues.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Toomer's Corner Traffic Evaluation")
    print("=" * 70)

    data = load_toomers_data(CSV_PATH)
    # Total raw vehicle count across all approaches
    total_arrivals = sum(
        sum(rate * lanes * SECONDS_PER_MINUTE
            for rate, lanes in zip(rates, LANES_PER_APPROACH))
        for _, rates in data
    )
    print(f"\nData loaded: {len(data)} minutes")
    print(f"Total arrivals (raw, across all lanes): {int(total_arrivals):,} vehicles")
    print(f"Lane configuration [N, E, S, W]: {LANES_PER_APPROACH}")
    print(f"Max per-lane rate: {max(max(r) for _, r in data):.2f} veh/sec")
    print()

    controllers = [
        FixedTimeController(green_time=30),
        ActuatedController(min_green=10, max_green=60),
        MaxPressureController(),
    ]

    results = {}
    for ctrl in controllers:
        print(f"Running {ctrl.name}...")
        results[ctrl.name] = run_controller_on_data(ctrl, data)

    # Print summary table
    print("\n" + "=" * 70)
    print(f"{'Controller':<16} {'Passed':>8} {'Arrived':>9} "
          f"{'Avg Wait (s)':>13} {'Throughput':>11} {'Final Q':>8}")
    print("-" * 70)
    for name, r in results.items():
        print(f"{name:<16} {r['total_passed']:>8} {r['total_arrived']:>9} "
              f"{r['avg_waiting']:>13.2f} {r['avg_throughput']:>11.3f} "
              f"{r['final_queue_total']:>8}")
    print("=" * 70)

    # Save summary text
    with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
        f.write("Toomer's Corner Traffic Evaluation\n")
        f.write("=" * 70 + "\n")
        f.write(f"Data: {CSV_PATH}\n")
        f.write(f"Duration: {len(data)} minutes ({len(data) * 60} seconds)\n")
        f.write(f"Lane configuration [N, E, S, W]: {LANES_PER_APPROACH}\n\n")
        f.write(f"{'Controller':<16} {'Passed':>8} {'Arrived':>9} "
                f"{'Avg Wait (s)':>13} {'Throughput':>11} {'Final Q':>8}\n")
        f.write("-" * 70 + "\n")
        for name, r in results.items():
            f.write(f"{name:<16} {r['total_passed']:>8} {r['total_arrived']:>9} "
                    f"{r['avg_waiting']:>13.2f} {r['avg_throughput']:>11.3f} "
                    f"{r['final_queue_total']:>8}\n")

    print("\nGenerating visualizations...")
    plot_all(results, data, OUT_DIR)
    print(f"\nAll outputs saved to: {OUT_DIR}/")


if __name__ == "__main__":
    main()
