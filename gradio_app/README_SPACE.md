---
title: Traffic Signal RL Visualization
emoji: 🚦
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: gradio_traffic_app.py
pinned: false
license: mit
---

# Traffic Signal Optimization with Reinforcement Learning 🚦

Interactive visualization of traffic signal control strategies powered by reinforcement learning concepts.

## Features

✨ **Interactive Simulation**: Watch traffic flow in real-time through a 4-way intersection

📊 **Performance Metrics**: Track queue lengths, waiting times, and throughput

🎮 **Multiple Controllers**: Compare Fixed-Time, Actuated, and Max-Pressure strategies

🔧 **Customizable Scenarios**: Adjust traffic rates for each direction

## How to Use

### Single Simulation Tab
1. Select a controller type (Fixed-Time, Actuated, or Max-Pressure)
2. Set arrival rates for each direction (North, East, South, West)
3. Choose simulation duration
4. Click "Run Simulation" to see results

### Controller Comparison Tab
1. Set traffic arrival rates
2. Click "Compare Controllers" to see all three strategies side-by-side
3. View performance metrics in a comparison table

## Controllers Explained

### Fixed-Time Controller
- Uses predetermined signal cycles
- Simple and predictable
- May be inefficient with variable traffic

### Actuated Controller
- Extends green time when vehicles are detected
- Adapts within min/max green time limits
- Better handles traffic variations

### Max-Pressure Controller
- Prioritizes direction with most vehicles (highest pressure)
- Most responsive to traffic imbalances
- Used in advanced traffic management systems

## Key Metrics

- **Queue Length**: Number of vehicles waiting at each approach
- **Average Waiting Time**: Mean time vehicles spend waiting
- **Throughput**: Rate of vehicles passing through (vehicles/second)

## Traffic Scenarios

Try these preset scenarios:
- **Balanced**: Equal traffic from all directions (0.25 veh/s each)
- **Rush Hour**: Heavy North-South traffic (0.4 veh/s), light East-West (0.15 veh/s)
- **Asymmetric**: Different rates for each direction

## Technical Details

Built with:
- **Gradio**: Interactive web interface
- **NumPy**: Numerical computations
- **Matplotlib**: Visualization and plotting

The simulation models:
- 4-way intersection with signal control
- Poisson arrival process for vehicles
- Queue dynamics and signal phases
- Performance tracking over time

## Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-directory>

# Install dependencies
pip install -r requirements_gradio.txt

# Run the app
python gradio_traffic_app.py
```

## Deployment

This app is designed for Hugging Face Spaces. To deploy:

1. Create a new Space on Hugging Face
2. Upload these files:
   - `gradio_traffic_app.py`
   - `requirements_gradio.txt`
   - `README.md`
3. The app will automatically build and launch

## License

MIT License - Feel free to use and modify for your projects!

## Acknowledgments

Based on reinforcement learning concepts for traffic signal optimization. Inspired by research in adaptive traffic control systems and multi-agent coordination.

---

Built with ❤️ for learning and exploring RL in traffic engineering
