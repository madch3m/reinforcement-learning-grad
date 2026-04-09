# 🚦 Traffic Signal Optimization with Reinforcement Learning

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)

A complete reinforcement learning project for traffic signal optimization, including training notebooks, baseline controllers, interactive visualization, and deployment tools for Hugging Face Spaces.

![Traffic Intersection Demo](https://img.shields.io/badge/Demo-Coming%20Soon-brightgreen)

## 🌟 Features

- **🎓 Educational Notebooks**: Step-by-step implementation of RL for traffic control
- **🤖 Multiple Controllers**: Fixed-Time, Actuated, Max-Pressure, and RL-based
- **📊 Comprehensive Evaluation**: Metrics and analysis for non-episodic tasks
- **🎮 Interactive Gradio App**: Real-time visualization and comparison
- **🚀 Production Ready**: Deploy to Hugging Face Spaces in minutes
- **💻 VS Code Integration**: Pre-configured workspace and extensions

## 📁 Project Structure

```
traffic-signal-rl-complete/
├── traffic_rl_project/              # Main RL implementation
│   ├── traffic_signal_rl.ipynb     # Complete training notebook
│   ├── requirements.txt             # Python dependencies
│   ├── test_setup.py               # Environment verification
│   └── README.md                   # Detailed documentation
│
├── gradio_app/                      # Interactive web application
│   ├── gradio_traffic_app.py       # Gradio application
│   ├── requirements_gradio.txt     # Gradio dependencies
│   ├── README_SPACE.md             # Hugging Face Space README
│   └── DEPLOYMENT_GUIDE.md         # Deployment instructions
│
├── non_episodic_evaluation_guide.ipynb  # Evaluation methods guide
├── traffic_rl.code-workspace       # VS Code workspace
├── VSCODE_GUIDE.md                 # VS Code setup guide
├── open_in_vscode.bat              # Windows launcher
├── open_in_vscode.sh               # Mac/Linux launcher
└── README.md                       # This file
```

## 🚀 Quick Start

### Option 1: Using VS Code (Recommended)

**Windows:**
```bash
# Download the repository
git clone https://github.com/YOUR_USERNAME/traffic-signal-rl.git
cd traffic-signal-rl

# Double-click open_in_vscode.bat
# Or run:
code traffic_rl.code-workspace
```

**Mac/Linux:**
```bash
# Download the repository
git clone https://github.com/YOUR_USERNAME/traffic-signal-rl.git
cd traffic-signal-rl

# Run the launcher
chmod +x open_in_vscode.sh
./open_in_vscode.sh

# Or open directly
code traffic_rl.code-workspace
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/traffic-signal-rl.git
cd traffic-signal-rl

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r traffic_rl_project/requirements.txt
pip install -r gradio_app/requirements_gradio.txt

# Run Jupyter notebook
jupyter notebook traffic_rl_project/traffic_signal_rl.ipynb

# Or run Gradio app
python gradio_app/gradio_traffic_app.py
```

## 📚 Documentation

### For Learning & Development
- **[Traffic Signal RL Notebook](traffic_rl_project/README.md)**: Complete guide to the RL implementation
- **[Non-Episodic Evaluation Guide](non_episodic_evaluation_guide.ipynb)**: How to evaluate continuing tasks
- **[VS Code Guide](VSCODE_GUIDE.md)**: Setup and usage in VS Code

### For Deployment
- **[Deployment Guide](gradio_app/DEPLOYMENT_GUIDE.md)**: Deploy to Hugging Face Spaces
- **[Gradio App Documentation](gradio_app/README_SPACE.md)**: App features and usage

## 🎯 What You'll Learn

### Reinforcement Learning Concepts
- Custom Gymnasium environment creation
- State and action space design
- Reward function engineering
- PPO (Proximal Policy Optimization) implementation
- Baseline controller comparison

### Traffic Signal Control
- Fixed-time signal control
- Actuated control strategies
- Max-pressure algorithms
- Queue management
- Performance optimization

### Evaluation Methods
- Average reward rate metrics
- Sliding window analysis
- Steady-state distribution
- Stability metrics
- Statistical comparison

### Deployment & Visualization
- Interactive web applications with Gradio
- Real-time simulation visualization
- Performance monitoring
- Cloud deployment (Hugging Face Spaces)

## 🎮 Interactive Demo

### Local Demo
```bash
cd gradio_app
python gradio_traffic_app.py
# Open browser to http://localhost:7860
```

### Live Demo (Coming Soon)
🌐 [Try it on Hugging Face Spaces](#) - Deploy your own using the deployment guide!

## 📊 Performance Metrics

The RL agent is evaluated on:
- **Average Waiting Time**: Time vehicles spend in queue
- **Throughput**: Rate of vehicles passing through intersection
- **Queue Stability**: Variance in queue lengths over time
- **Comparative Performance**: vs Fixed-Time, Actuated, Max-Pressure

## 🛠️ Requirements

### Python Version
- Python 3.8 or higher

### Core Dependencies
```
gymnasium>=0.29.0
stable-baselines3>=2.0.0
torch>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
gradio>=4.0.0
```

See individual `requirements.txt` files for complete dependency lists.

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- 🐛 **Report bugs** by opening an issue
- 💡 **Suggest features** or enhancements
- 📝 **Improve documentation**
- 🔧 **Submit pull requests**

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📖 Usage Examples

### Training a New Agent
```python
from stable_baselines3 import PPO
from traffic_rl_project.environment import TrafficSignalEnv

# Create environment
env = TrafficSignalEnv(arrival_rates=[0.25, 0.25, 0.25, 0.25])

# Initialize agent
agent = PPO("MlpPolicy", env, verbose=1)

# Train
agent.learn(total_timesteps=200_000)

# Save
agent.save("my_traffic_agent")
```

### Evaluating Controllers
```python
from traffic_rl_project.baselines import FixedTimeController, ActuatedController

# Compare controllers
controllers = [
    FixedTimeController(green_time=30),
    ActuatedController(min_green=15, max_green=45)
]

# Run evaluation
results = compare_controllers(controllers, env, n_episodes=10)
print(results)
```

### Running Gradio App
```python
import gradio as gr
from gradio_app.gradio_traffic_app import demo

# Launch with custom settings
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=True  # Creates public link
)
```

## 🔬 Experiments & Extensions

### Suggested Extensions
- 🚗 Multi-intersection coordination
- 🌐 Real-world traffic data integration
- 🎓 Transfer learning across intersections
- 📱 Mobile app integration
- 🔄 Online learning and adaptation
- 🚶 Pedestrian crossing logic

### Research Directions
- ~~Compare with SUMO (Simulation of Urban MObility)~~ ✅ Integrated via `sumo-rl` with 6 built-in scenarios
- Implement multi-agent RL approaches
- Test on real traffic patterns
- Optimize for different objectives (emissions, energy, equity)

## 📝 Citation

If you use this project in your research or work, please cite:

```bibtex
@misc{traffic-signal-rl,
  author = {Your Name},
  title = {Traffic Signal Optimization with Reinforcement Learning},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/YOUR_USERNAME/traffic-signal-rl}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Stable-Baselines3](https://stable-baselines3.readthedocs.io/)
- Interactive UI powered by [Gradio](https://gradio.app/)
- Inspired by research in adaptive traffic control systems
- Thanks to the reinforcement learning community

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/traffic-signal-rl/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/traffic-signal-rl/discussions)

## 🗺️ Roadmap

- [x] Basic RL implementation
- [x] Baseline controllers
- [x] Interactive Gradio app
- [x] Non-episodic evaluation guide
- [x] VS Code integration
- [x] SUMO integration
- [ ] Multi-intersection support
- [ ] Real traffic data examples
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Advanced visualization dashboard

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for traffic engineering and reinforcement learning enthusiasts**
