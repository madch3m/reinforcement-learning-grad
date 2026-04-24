"""
Build a consolidated dataset from all recording session folders.

Reads each Session_*/traffic_counts.csv and Session_*/measured_scenario.json,
produces:
  - traffic_rl_project/data/toomers_dataset.csv  (all minutes, tagged by session)
  - traffic_rl_project/data/toomers_sessions.json (per-session metadata + aggregates)
  - traffic_rl_project/data/dataset_summary.png  (session comparison plot)
"""

import csv
import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SESSIONS_GLOB = os.path.join(HERE, "Session_*")
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUT_CSV = os.path.join(DATA_DIR, "toomers_dataset.csv")
OUT_JSON = os.path.join(DATA_DIR, "toomers_sessions.json")
OUT_PLOT = os.path.join(DATA_DIR, "dataset_summary.png")


def load_sessions():
    """Return list of dicts: one per session, sorted by session id."""
    sessions = []
    for session_dir in sorted(glob.glob(SESSIONS_GLOB)):
        session_id = os.path.basename(session_dir)

        meta_path = os.path.join(session_dir, "measured_scenario.json")
        with open(meta_path) as f:
            meta = json.load(f)

        rows = []
        csv_path = os.path.join(session_dir, "traffic_counts.csv")
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "minute": int(row["minute"]),
                    "north": int(row["north"]),
                    "south": int(row["south"]),
                    "east":  int(row["east"]),
                    "west":  int(row["west"]),
                })

        sessions.append({
            "session_id": session_id,
            "metadata": meta,
            "rows": rows,
        })
    return sessions


def write_consolidated_csv(sessions, path):
    """Write one CSV with session_id and video-tagged minutes."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "video_file", "minute",
            "north", "south", "east", "west", "total",
        ])
        for s in sessions:
            video = s["metadata"].get("video_file", "unknown")
            for r in s["rows"]:
                total = r["north"] + r["south"] + r["east"] + r["west"]
                writer.writerow([
                    s["session_id"], video, r["minute"],
                    r["north"], r["south"], r["east"], r["west"], total,
                ])


def compute_aggregates(sessions):
    """Add per-session aggregates and an overall summary."""
    out = {"sessions": [], "overall": None}
    all_minutes = []

    for s in sessions:
        rows = s["rows"]
        n = len(rows)
        totals = {d: sum(r[d] for r in rows) for d in ("north", "south", "east", "west")}
        peaks = {d: max(r[d] for r in rows) for d in ("north", "south", "east", "west")}
        means = {d: totals[d] / n for d in totals}
        dominant = max(totals, key=totals.get)
        total_vehicles = sum(totals.values())
        out["sessions"].append({
            "session_id": s["session_id"],
            "video_file": s["metadata"].get("video_file"),
            "duration_minutes": n,
            "total_vehicles": total_vehicles,
            "mean_per_minute": means,
            "peak_per_minute": peaks,
            "dominant_direction": dominant,
            "metadata_rates_vehmin": s["metadata"].get("arrival_rates"),
        })
        all_minutes.extend(rows)

    n_total = len(all_minutes)
    totals = {d: sum(r[d] for r in all_minutes) for d in ("north", "south", "east", "west")}
    peaks = {d: max(r[d] for r in all_minutes) for d in ("north", "south", "east", "west")}
    means = {d: totals[d] / n_total for d in totals}
    out["overall"] = {
        "n_sessions": len(sessions),
        "total_minutes": n_total,
        "total_vehicles": sum(totals.values()),
        "mean_per_minute": means,
        "peak_per_minute": peaks,
        "dominant_direction": max(totals, key=totals.get),
    }
    return out


def plot_summary(sessions, aggregates, path):
    """4-panel comparison plot across all sessions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    directions = ["north", "south", "east", "west"]
    dir_colors = {"north": "#3498db", "south": "#2ecc71",
                  "east": "#e67e22", "west": "#e74c3c"}

    ax = axes[0, 0]
    ids = [s["session_id"].replace("Session_", "") for s in sessions]
    totals = [sum(sum(r[d] for d in directions) for r in s["rows"]) for s in sessions]
    durations = [len(s["rows"]) for s in sessions]
    bars = ax.bar(range(len(ids)), totals, color="#34495e", edgecolor="black")
    ax.set_xticks(range(len(ids)))
    ax.set_xticklabels(ids, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("Total Vehicles")
    ax.set_title("Total Vehicles per Session")
    for bar, d in zip(bars, durations):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{d}min", ha="center", va="bottom", fontsize=8)
    ax.grid(axis="y", alpha=0.3)

    ax = axes[0, 1]
    x = np.arange(len(ids))
    width = 0.2
    for i, d in enumerate(directions):
        means = [
            np.mean([r[d] for r in s["rows"]]) for s in sessions
        ]
        ax.bar(x + (i - 1.5) * width, means, width, label=d.title(),
               color=dir_colors[d], edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(ids, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("Mean Vehicles/Minute")
    ax.set_title("Directional Flow by Session")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    ax = axes[1, 0]
    bottom = np.zeros(len(sessions))
    for d in directions:
        shares = []
        for s in sessions:
            total = sum(sum(r[dd] for dd in directions) for r in s["rows"])
            dir_total = sum(r[d] for r in s["rows"])
            shares.append(dir_total / total * 100 if total > 0 else 0)
        ax.bar(range(len(ids)), shares, bottom=bottom,
               label=d.title(), color=dir_colors[d], edgecolor="black", linewidth=0.3)
        bottom += np.array(shares)
    ax.set_xticks(range(len(ids)))
    ax.set_xticklabels(ids, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("Share of Total Traffic (%)")
    ax.set_title("Directional Composition per Session")
    ax.legend(fontsize=9, loc="lower right")
    ax.set_ylim(0, 100)

    ax = axes[1, 1]
    pooled = {d: [] for d in directions}
    for s in sessions:
        for r in s["rows"]:
            for d in directions:
                pooled[d].append(r[d])
    positions = range(1, 5)
    bp = ax.boxplot(
        [pooled[d] for d in directions],
        positions=positions,
        widths=0.6,
        patch_artist=True,
    )
    for patch, d in zip(bp["boxes"], directions):
        patch.set_facecolor(dir_colors[d])
    ax.set_xticks(positions)
    ax.set_xticklabels([d.title() for d in directions])
    ax.set_ylabel("Vehicles per Minute")
    ax.set_title(f"Per-Minute Distribution (n={aggregates['overall']['total_minutes']} minutes)")
    ax.grid(axis="y", alpha=0.3)

    fig.suptitle(
        f"Toomer's Corner Dataset — {aggregates['overall']['n_sessions']} sessions, "
        f"{aggregates['overall']['total_minutes']} minutes, "
        f"{aggregates['overall']['total_vehicles']:,} vehicles",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()


def main():
    print("=" * 70)
    print("Building Toomer's Corner Dataset from Session Folders")
    print("=" * 70)

    sessions = load_sessions()
    print(f"\nFound {len(sessions)} sessions:")
    for s in sessions:
        video = s["metadata"].get("video_file", "?")
        print(f"  - {s['session_id']}: {len(s['rows'])} minutes ({video})")

    write_consolidated_csv(sessions, OUT_CSV)
    print(f"\nWrote consolidated CSV: {OUT_CSV}")

    aggregates = compute_aggregates(sessions)
    with open(OUT_JSON, "w") as f:
        json.dump(aggregates, f, indent=2)
    print(f"Wrote aggregates JSON:  {OUT_JSON}")

    plot_summary(sessions, aggregates, OUT_PLOT)
    print(f"Wrote summary plot:     {OUT_PLOT}")

    overall = aggregates["overall"]
    print("\n" + "=" * 70)
    print("Overall Statistics")
    print("=" * 70)
    print(f"  Sessions:       {overall['n_sessions']}")
    print(f"  Total minutes:  {overall['total_minutes']}")
    print(f"  Total vehicles: {overall['total_vehicles']:,}")
    print(f"  Mean per min (N,S,E,W): "
          f"{overall['mean_per_minute']['north']:.1f}, "
          f"{overall['mean_per_minute']['south']:.1f}, "
          f"{overall['mean_per_minute']['east']:.1f}, "
          f"{overall['mean_per_minute']['west']:.1f}")
    print(f"  Peak per min (N,S,E,W): "
          f"{overall['peak_per_minute']['north']}, "
          f"{overall['peak_per_minute']['south']}, "
          f"{overall['peak_per_minute']['east']}, "
          f"{overall['peak_per_minute']['west']}")
    print(f"  Dominant direction: {overall['dominant_direction'].upper()}")


if __name__ == "__main__":
    main()
