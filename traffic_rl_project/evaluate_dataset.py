"""
Evaluate baseline controllers across ALL Toomer's Corner sessions.

Reads the consolidated dataset built by build_dataset.py and runs each
controller (Fixed-Time, Actuated, Max-Pressure) on each session separately.
Produces per-session metrics and an aggregate comparison.
"""

import csv
import os
import sys
from collections import defaultdict

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

DATASET_CSV = os.path.join(HERE, "data", "toomers_dataset.csv")
OUT_DIR = os.path.join(HERE, "results", "dataset")
os.makedirs(OUT_DIR, exist_ok=True)

LANES_PER_APPROACH = [2, 1, 2, 1]   # [N, E, S, W] — matches Toomer's layout
SECONDS_PER_MINUTE = 60
RANDOM_SEED = 42


def load_dataset_by_session(csv_path):
    """Group rows by session_id, preserving minute order."""
    sessions = defaultdict(list)
    videos = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["session_id"]
            videos[sid] = row["video_file"]
            sessions[sid].append({
                "minute": int(row["minute"]),
                "north": int(row["north"]),
                "south": int(row["south"]),
                "east":  int(row["east"]),
                "west":  int(row["west"]),
            })
    for sid in sessions:
        sessions[sid].sort(key=lambda r: r["minute"])
    return dict(sessions), videos


def rows_to_rates(rows):
    """Convert minute-by-minute counts to per-second per-lane arrival rates
    in env order [N, E, S, W]."""
    rates_by_minute = []
    for r in rows:
        counts = [r["north"], r["east"], r["south"], r["west"]]
        rates = [c / SECONDS_PER_MINUTE / lanes
                 for c, lanes in zip(counts, LANES_PER_APPROACH)]
        rates_by_minute.append(rates)
    return rates_by_minute


def run_session(controller, rates_by_minute, seed=RANDOM_SEED):
    """Run one controller on one session's minute-by-minute rates."""
    np.random.seed(seed)
    env = TrafficSignalEnv(
        arrival_rates=rates_by_minute[0],
        min_green_time=10,
        episode_length=len(rates_by_minute) * SECONDS_PER_MINUTE + 10,
    )
    obs, _ = env.reset()

    queue_len_trace = []
    throughput_trace = []

    for rates in rates_by_minute:
        env.arrival_rates = rates
        env.traffic_gen.base_rates = np.array(rates, dtype=np.float32)
        for _ in range(SECONDS_PER_MINUTE):
            action, _ = controller.predict(obs, env=env)
            obs, _, _, _, _ = env.step(action)
            queue_len_trace.append(sum(len(q) for q in env.queues))
            throughput_trace.append(env.total_vehicles_passed)

    return {
        "vehicles_passed": env.total_vehicles_passed,
        "vehicles_arrived": env.total_vehicles_arrived,
        "avg_waiting": env.total_waiting_time / max(env.total_vehicles_arrived, 1),
        "throughput": env.total_vehicles_passed / env.current_time,
        "final_queue": sum(len(q) for q in env.queues),
        "queue_trace": queue_len_trace,
        "throughput_trace": throughput_trace,
    }


def controller_factory():
    return [
        FixedTimeController(green_time=30),
        ActuatedController(min_green=10, max_green=60),
        MaxPressureController(),
    ]


def evaluate_all(sessions, videos):
    """Return nested dict: results[session_id][controller_name] -> metrics."""
    results = {}
    for sid, rows in sessions.items():
        print(f"\nSession {sid} ({len(rows)} min, {videos[sid]})")
        rates = rows_to_rates(rows)
        session_results = {}
        for ctrl in controller_factory():
            r = run_session(ctrl, rates)
            session_results[ctrl.name] = r
            print(f"  {ctrl.name:<14} passed={r['vehicles_passed']:>5}  "
                  f"throughput={r['throughput']:.3f}  "
                  f"avg_wait={r['avg_waiting']:.1f}s")
        results[sid] = session_results
    return results


def write_summary_csv(results, sessions, videos, out_path):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "video", "duration_min", "controller",
            "vehicles_passed", "vehicles_arrived",
            "avg_waiting_sec", "throughput_veh_per_sec", "final_queue",
        ])
        for sid in sorted(results.keys()):
            dur = len(sessions[sid])
            for ctrl_name, r in results[sid].items():
                writer.writerow([
                    sid, videos[sid], dur, ctrl_name,
                    r["vehicles_passed"], r["vehicles_arrived"],
                    f"{r['avg_waiting']:.2f}", f"{r['throughput']:.4f}",
                    r["final_queue"],
                ])


def plot_aggregate(results, sessions, out_dir):
    """Cross-session comparison plots."""
    session_ids = sorted(results.keys())
    ctrl_names = ["Fixed-Time", "Actuated", "Max-Pressure"]
    colors = {"Fixed-Time": "#3498db", "Actuated": "#2ecc71", "Max-Pressure": "#e67e22"}

    short_ids = [sid.replace("Session_", "") for sid in session_ids]

    # Plot 1: Vehicles passed per session, grouped by controller
    fig, ax = plt.subplots(figsize=(13, 5))
    x = np.arange(len(session_ids))
    width = 0.27
    for i, cname in enumerate(ctrl_names):
        vals = [results[sid][cname]["vehicles_passed"] for sid in session_ids]
        ax.bar(x + (i - 1) * width, vals, width, label=cname,
               color=colors[cname], edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(short_ids, rotation=40, ha="right", fontsize=9)
    ax.set_ylabel("Vehicles Passed")
    ax.set_title("Vehicles Passed per Session, by Controller")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    p = os.path.join(out_dir, "01_passed_by_session.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 2: Avg waiting time per session
    fig, ax = plt.subplots(figsize=(13, 5))
    for i, cname in enumerate(ctrl_names):
        vals = [results[sid][cname]["avg_waiting"] for sid in session_ids]
        ax.bar(x + (i - 1) * width, vals, width, label=cname,
               color=colors[cname], edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(short_ids, rotation=40, ha="right", fontsize=9)
    ax.set_ylabel("Avg Waiting Time (seconds)")
    ax.set_title("Average Waiting Time per Session, by Controller (lower is better)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    p = os.path.join(out_dir, "02_waiting_by_session.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")

    # Plot 3: Aggregate totals across all sessions
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    total_passed = {
        c: sum(results[sid][c]["vehicles_passed"] for sid in session_ids)
        for c in ctrl_names
    }
    avg_throughput = {
        c: np.mean([results[sid][c]["throughput"] for sid in session_ids])
        for c in ctrl_names
    }
    avg_waiting = {
        c: np.mean([results[sid][c]["avg_waiting"] for sid in session_ids])
        for c in ctrl_names
    }

    bar_colors = [colors[c] for c in ctrl_names]
    axes[0].bar(ctrl_names, [total_passed[c] for c in ctrl_names],
                color=bar_colors, edgecolor="black")
    axes[0].set_ylabel("Vehicles Passed")
    axes[0].set_title(f"Total Vehicles Passed Across All Sessions")
    for i, c in enumerate(ctrl_names):
        axes[0].text(i, total_passed[c], f"  {total_passed[c]:,}",
                     ha="center", va="bottom", fontweight="bold")
    axes[0].grid(axis="y", alpha=0.3)

    axes[1].bar(ctrl_names, [avg_throughput[c] for c in ctrl_names],
                color=bar_colors, edgecolor="black")
    axes[1].set_ylabel("Mean Throughput (veh/sec)")
    axes[1].set_title("Mean Throughput per Session")
    for i, c in enumerate(ctrl_names):
        axes[1].text(i, avg_throughput[c], f"  {avg_throughput[c]:.3f}",
                     ha="center", va="bottom", fontweight="bold")
    axes[1].grid(axis="y", alpha=0.3)

    axes[2].bar(ctrl_names, [avg_waiting[c] for c in ctrl_names],
                color=bar_colors, edgecolor="black")
    axes[2].set_ylabel("Mean Avg Waiting (sec)")
    axes[2].set_title("Mean Average Waiting Time")
    for i, c in enumerate(ctrl_names):
        axes[2].text(i, avg_waiting[c], f"  {avg_waiting[c]:,.0f}s",
                     ha="center", va="bottom", fontweight="bold")
    axes[2].grid(axis="y", alpha=0.3)

    fig.suptitle("Aggregate Controller Performance Across All 7 Sessions",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    p = os.path.join(out_dir, "03_aggregate_summary.png")
    plt.savefig(p, dpi=100); plt.close()
    print(f"  Saved: {p}")


def main():
    print("=" * 70)
    print("Dataset-Wide Controller Evaluation")
    print("=" * 70)
    if not os.path.exists(DATASET_CSV):
        print(f"ERROR: {DATASET_CSV} not found. Run build_dataset.py first.")
        sys.exit(1)

    sessions, videos = load_dataset_by_session(DATASET_CSV)
    print(f"Loaded {len(sessions)} sessions "
          f"({sum(len(v) for v in sessions.values())} total minutes)")
    print(f"Lane config [N, E, S, W]: {LANES_PER_APPROACH}")

    results = evaluate_all(sessions, videos)

    summary_csv = os.path.join(OUT_DIR, "all_sessions_summary.csv")
    write_summary_csv(results, sessions, videos, summary_csv)
    print(f"\nWrote per-session CSV:  {summary_csv}")

    print("\nGenerating aggregate plots...")
    plot_aggregate(results, sessions, OUT_DIR)
    print(f"\nAll outputs saved to: {OUT_DIR}/")


if __name__ == "__main__":
    main()
