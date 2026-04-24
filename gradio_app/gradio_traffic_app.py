"""Traffic Signal RL Visualization with Gradio."""

import io
import os
import sys

import gradio as gr
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from traffic_rl_project import (
    ActuatedController,
    FixedTimeController,
    MaxPressureController,
    TrafficSignalEnv,
)


def create_intersection_visualization(env, step_num):
    """Create a visual representation of the intersection."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax_intersection = axes[0]
    ax_intersection.set_xlim(-10, 10)
    ax_intersection.set_ylim(-10, 10)
    ax_intersection.set_aspect('equal')
    ax_intersection.axis('off')
    ax_intersection.set_title(f'Intersection View (Step {step_num})', fontsize=14, fontweight='bold')

    road_color = '#555555'
    ax_intersection.add_patch(patches.Rectangle((-2, -10), 4, 20,
                                               facecolor=road_color, edgecolor='white', linewidth=2))
    ax_intersection.add_patch(patches.Rectangle((-10, -2), 20, 4,
                                               facecolor=road_color, edgecolor='white', linewidth=2))
    ax_intersection.add_patch(patches.Rectangle((-2, -2), 4, 4,
                                               facecolor='#666666', edgecolor='white', linewidth=2))

    phase_info = env.PHASES[env.current_phase]

    # Lane index → cardinal direction: 0=N, 1=E, 2=S, 3=W.
    light_positions = {
        0: (0, 4),
        1: (4, 0),
        2: (0, -4),
        3: (-4, 0),
    }

    for lane, (x, y) in light_positions.items():
        if lane in (0, 2):
            color = 'green' if phase_info['ns'] == 'green' else \
                   'yellow' if phase_info['ns'] == 'yellow' else 'red'
        else:
            color = 'green' if phase_info['ew'] == 'green' else \
                   'yellow' if phase_info['ew'] == 'yellow' else 'red'

        ax_intersection.add_patch(patches.Circle((x, y), 0.5,
                                                facecolor=color, edgecolor='black', linewidth=2))

    vehicle_positions = {
        0: lambda i: (0.5, 5 + i * 0.8),
        1: lambda i: (5 + i * 0.8, 0.5),
        2: lambda i: (-0.5, -5 - i * 0.8),
        3: lambda i: (-5 - i * 0.8, -0.5),
    }

    for lane, queue in enumerate(env.queues):
        for i, vehicle in enumerate(list(queue)[:10]):
            x, y = vehicle_positions[lane](i)
            ax_intersection.add_patch(patches.Rectangle((x-0.3, y-0.3), 0.6, 0.6,
                                                        facecolor='#FFD700',
                                                        edgecolor='black', linewidth=1))

    label_positions = {
        0: (0, 8, 'N'),
        1: (8, 0, 'E'),
        2: (0, -8, 'S'),
        3: (-8, 0, 'W'),
    }

    for lane, (x, y, direction) in label_positions.items():
        queue_len = len(env.queues[lane])
        ax_intersection.text(x, y, f'{direction}: {queue_len}',
                           ha='center', va='center', fontsize=12,
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax_metrics = axes[1]
    ax_metrics.axis('off')

    metrics_text = f"""
    TIME STEP: {step_num}
    
    SIGNAL STATUS:
    • Current Phase: {env.current_phase}
    • Phase Time: {env.phase_time:.1f}s
    • NS Light: {phase_info['ns'].upper()}
    • EW Light: {phase_info['ew'].upper()}
    
    QUEUE LENGTHS:
    • North: {len(env.queues[0])}
    • East: {len(env.queues[1])}
    • South: {len(env.queues[2])}
    • West: {len(env.queues[3])}
    • Total: {sum(len(q) for q in env.queues)}
    
    PERFORMANCE:
    • Vehicles Passed: {env.total_vehicles_passed}
    • Vehicles Arrived: {env.total_vehicles_arrived}
    • Avg Waiting Time: {env.total_waiting_time / max(env.total_vehicles_arrived, 1):.2f}s
    • Throughput: {env.total_vehicles_passed / max(env.current_time, 1):.4f} veh/s
    """
    
    ax_metrics.text(0.1, 0.95, metrics_text, transform=ax_metrics.transAxes,
                   fontsize=11, verticalalignment='top', family='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)

    return img


def create_performance_plots(history):
    """Create performance plots over time."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    steps = range(len(history['queue_lengths']))
    labels = ['North', 'East', 'South', 'West']

    queue_data = np.array(history['queue_lengths'])
    for i in range(4):
        axes[0].plot(steps, queue_data[:, i], label=labels[i], linewidth=2)
    axes[0].set_ylabel('Queue Length', fontsize=11)
    axes[0].set_title('Queue Lengths Over Time', fontsize=13, fontweight='bold')
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.3)

    waiting_data = np.array(history['waiting_times'])
    for i in range(4):
        axes[1].plot(steps, waiting_data[:, i], label=labels[i], linewidth=2)
    axes[1].set_ylabel('Avg Waiting Time (s)', fontsize=11)
    axes[1].set_title('Average Waiting Time per Lane', fontsize=13, fontweight='bold')
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(steps, history['throughput'], linewidth=2, color='green')
    axes[2].set_xlabel('Time Step', fontsize=11)
    axes[2].set_ylabel('Vehicles Passed', fontsize=11)
    axes[2].set_title('Cumulative Throughput', fontsize=13, fontweight='bold')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)

    return img


def run_simulation(controller_type, north_rate, east_rate, south_rate, west_rate,
                  num_steps, green_time, min_green, max_green):
    """Run the simulation and return visualizations."""
    arrival_rates = [north_rate, east_rate, south_rate, west_rate]
    env = TrafficSignalEnv(arrival_rates=arrival_rates, episode_length=num_steps)

    if controller_type == "Fixed-Time":
        controller = FixedTimeController(green_time=green_time)
    elif controller_type == "Actuated":
        controller = ActuatedController(min_green=min_green, max_green=max_green)
    else:
        controller = MaxPressureController()

    obs, _ = env.reset()

    history = {
        'queue_lengths': [],
        'waiting_times': [],
        'throughput': [],
        'phases': []
    }

    for step in range(num_steps):
        action, _ = controller.predict(obs, env)
        obs, reward, terminated, truncated, info = env.step(action)

        history['queue_lengths'].append([len(q) for q in env.queues])
        avg_waiting = []
        for queue in env.queues:
            if queue:
                avg_waiting.append(np.mean([v.waiting_time for v in queue]))
            else:
                avg_waiting.append(0)
        history['waiting_times'].append(avg_waiting)
        history['throughput'].append(env.total_vehicles_passed)
        history['phases'].append(env.current_phase)

    final_intersection = create_intersection_visualization(env, num_steps)
    performance_plots = create_performance_plots(history)

    summary = f"""
    ## Simulation Complete!
    
    **Controller:** {controller_type}
    **Duration:** {num_steps} steps
    
    ### Final Statistics:
    - **Total Vehicles Passed:** {env.total_vehicles_passed}
    - **Total Vehicles Arrived:** {env.total_vehicles_arrived}
    - **Average Waiting Time:** {env.total_waiting_time / max(env.total_vehicles_arrived, 1):.2f} seconds
    - **Throughput Rate:** {env.total_vehicles_passed / num_steps:.4f} vehicles/step
    - **Final Queue Lengths:** N:{len(env.queues[0])}, E:{len(env.queues[1])}, S:{len(env.queues[2])}, W:{len(env.queues[3])}
    """
    
    return final_intersection, performance_plots, summary


def run_comparison(north_rate, east_rate, south_rate, west_rate, num_steps):
    """Run comparison of all controllers."""
    arrival_rates = [north_rate, east_rate, south_rate, west_rate]
    controllers = [
        FixedTimeController(green_time=30),
        ActuatedController(min_green=15, max_green=45),
        MaxPressureController()
    ]

    results = []

    for controller in controllers:
        env = TrafficSignalEnv(arrival_rates=arrival_rates, episode_length=num_steps)
        obs, _ = env.reset()

        for step in range(num_steps):
            action, _ = controller.predict(obs, env)
            obs, reward, terminated, truncated, info = env.step(action)

        results.append({
            'Controller': controller.name,
            'Avg Waiting Time': f"{env.total_waiting_time / max(env.total_vehicles_arrived, 1):.2f}s",
            'Throughput': f"{env.total_vehicles_passed / num_steps:.4f}",
            'Vehicles Passed': env.total_vehicles_passed,
            'Final Queue': sum(len(q) for q in env.queues)
        })

    comparison_text = "## Controller Comparison\n\n"
    comparison_text += "| Controller | Avg Wait Time | Throughput | Vehicles Passed | Final Queue |\n"
    comparison_text += "|------------|---------------|------------|-----------------|-------------|\n"
    for r in results:
        comparison_text += f"| {r['Controller']} | {r['Avg Waiting Time']} | {r['Throughput']} | {r['Vehicles Passed']} | {r['Final Queue']} |\n"
    
    return comparison_text


with gr.Blocks(title="Traffic Signal RL Visualization") as demo:
    gr.Markdown("""
    # 🚦 Traffic Signal Optimization with Reinforcement Learning
    
    Interactive visualization of traffic signal control strategies. Compare different controllers
    and see how they handle various traffic patterns.
    
    **Try different scenarios:**
    - Balanced traffic: All lanes equal
    - Rush hour: High North-South traffic
    - Asymmetric: Different rates for each direction
    """)
    
    with gr.Tab("Single Simulation"):
        gr.Markdown("### Run a single simulation with your chosen controller and traffic pattern")
        
        with gr.Row():
            with gr.Column(scale=1):
                controller_choice = gr.Radio(
                    choices=["Fixed-Time", "Actuated", "Max-Pressure"],
                    value="Actuated",
                    label="Controller Type",
                    info="Select the traffic signal control strategy"
                )
                
                gr.Markdown("#### Traffic Arrival Rates (vehicles/second)")
                north_rate = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="North")
                east_rate = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="East")
                south_rate = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="South")
                west_rate = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="West")
                
                num_steps = gr.Slider(100, 1000, value=300, step=50, 
                                     label="Simulation Steps",
                                     info="Number of time steps to simulate")
                
                with gr.Accordion("Advanced Controller Settings", open=False):
                    green_time = gr.Slider(10, 60, value=30, step=5,
                                          label="Fixed-Time Green Duration (s)")
                    min_green = gr.Slider(5, 30, value=15, step=5,
                                         label="Actuated Min Green (s)")
                    max_green = gr.Slider(30, 90, value=45, step=5,
                                         label="Actuated Max Green (s)")
                
                run_btn = gr.Button("🚀 Run Simulation", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                intersection_img = gr.Image(label="Intersection Visualization", type="pil")
                summary_md = gr.Markdown()
        
        with gr.Row():
            performance_img = gr.Image(label="Performance Metrics Over Time", type="pil")
        
        run_btn.click(
            fn=run_simulation,
            inputs=[controller_choice, north_rate, east_rate, south_rate, west_rate,
                   num_steps, green_time, min_green, max_green],
            outputs=[intersection_img, performance_img, summary_md]
        )

        gr.Markdown("### 🎯 Quick Scenarios")
        with gr.Row():
            balanced_btn = gr.Button("⚖️ Balanced Traffic")
            rush_hour_btn = gr.Button("🏙️ Rush Hour (N-S)")
            asymmetric_btn = gr.Button("🔀 Asymmetric")
        
        balanced_btn.click(
            lambda: (0.25, 0.25, 0.25, 0.25),
            outputs=[north_rate, east_rate, south_rate, west_rate]
        )
        rush_hour_btn.click(
            lambda: (0.4, 0.15, 0.4, 0.15),
            outputs=[north_rate, east_rate, south_rate, west_rate]
        )
        asymmetric_btn.click(
            lambda: (0.35, 0.2, 0.25, 0.3),
            outputs=[north_rate, east_rate, south_rate, west_rate]
        )
    
    with gr.Tab("Controller Comparison"):
        gr.Markdown("""
        ### Compare all controllers side-by-side
        
        Run all three controllers on the same traffic pattern and compare their performance.
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Traffic Arrival Rates")
                comp_north = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="North")
                comp_east = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="East")
                comp_south = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="South")
                comp_west = gr.Slider(0.1, 0.5, value=0.25, step=0.05, label="West")
                comp_steps = gr.Slider(100, 1000, value=500, step=50, label="Simulation Steps")
                
                compare_btn = gr.Button("📊 Compare Controllers", variant="primary", size="lg")
        
        comparison_output = gr.Markdown()
        
        compare_btn.click(
            fn=run_comparison,
            inputs=[comp_north, comp_east, comp_south, comp_west, comp_steps],
            outputs=comparison_output
        )
    
    with gr.Tab("About"):
        gr.Markdown("""
        ## About This Application
        
        This interactive demo visualizes traffic signal control using different strategies:
        
        ### Controllers:
        
        1. **Fixed-Time Controller**
           - Traditional approach with predetermined cycle times
           - Simple but inflexible to traffic variations
        
        2. **Actuated Controller**
           - Extends green time when vehicles are detected
           - Adapts to traffic demand within limits
        
        3. **Max-Pressure Controller**
           - Prioritizes direction with highest "pressure" (queue length)
           - More responsive to traffic imbalances
        
        ### Environment Details:
        
        - **State Space**: Queue lengths, waiting times, signal phase
        - **Action Space**: Maintain current phase or switch
        - **Reward**: Balances throughput and waiting time
        
        ### How to Use:
        
        1. Choose a controller type
        2. Set traffic arrival rates for each direction
        3. Run the simulation to see real-time performance
        4. Compare different strategies in the comparison tab
        
        ### Metrics Explained:
        
        - **Queue Length**: Number of vehicles waiting at each approach
        - **Waiting Time**: Average time vehicles spend waiting
        - **Throughput**: Rate of vehicles passing through intersection
        
        Built with Gradio for deployment on Hugging Face Spaces 🤗
        """)

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
