# Traffic Signal Optimization with Reinforcement Learning

A complete implementation of a reinforcement learning system for optimizing traffic signal control to minimize waiting times and maximize throughput.

## 📋 Overview

This project implements:
- **Custom Traffic Environment**: Gymnasium-compatible environment simulating a 4-way intersection
- **Multiple Baseline Controllers**: Fixed-time, actuated, and max-pressure controllers
- **RL Agent**: PPO (Proximal Policy Optimization) agent trained to optimize signal timing
- **Comprehensive Evaluation**: Comparison across different traffic scenarios and patterns

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python -m venv traffic_rl_env
source traffic_rl_env/bin/activate  # On Windows: traffic_rl_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Notebook

```bash
jupyter notebook traffic_signal_rl.ipynb
```

Or use JupyterLab:
```bash
jupyter lab traffic_signal_rl.ipynb
```

### 3. Execute Cells

Simply run all cells in order. The notebook is structured to:
1. Set up the environment
2. Implement and test baseline controllers
3. Train the RL agent
4. Evaluate and compare performance
5. Generate visualizations

## 📊 Project Structure

```
traffic_rl_project/
├── traffic_signal_rl.ipynb    # Main notebook
├── environment.py             # Shared Gymnasium environment
├── baselines.py               # Baseline controllers
├── evaluation.py              # Evaluation utilities
├── __init__.py                # Public package exports
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── models/                     # Saved models (created during training)
├── logs/                       # Training logs (created during training)
└── traffic_rl_logs/           # TensorBoard logs (created during training)
```

## 🎯 Key Features

### Environment
- **State Space**: Queue lengths, waiting times, current signal phase, phase duration
- **Action Space**: Maintain current phase or switch to next phase
- **Reward Function**: Balances throughput, waiting time, and queue management

### Baseline Controllers
1. **Fixed-Time**: Traditional fixed-duration signal cycles
2. **Actuated**: Adaptive timing based on queue detection
3. **Max-Pressure**: Prioritizes direction with highest vehicle pressure

### RL Agent (PPO)
- Multi-layer perceptron policy
- Configurable network architecture
- Tensorboard logging for training visualization
- Model checkpointing for best performance

### Evaluation Metrics
- Average waiting time per vehicle
- Throughput (vehicles/second)
- Total vehicles processed
- Queue dynamics over time

## 🔧 Customization

### Modify Traffic Patterns

In the notebook, adjust the `arrival_rates` parameter:

```python
from traffic_rl_project.environment import TrafficSignalEnv

env = TrafficSignalEnv(
    arrival_rates=[0.3, 0.2, 0.3, 0.2],  # [North, East, South, West]
    episode_length=1800,  # 30 minutes
    dt=1.0  # 1-second timesteps
)
```

### Change Reward Function

Edit the `_calculate_reward` method in `TrafficSignalEnv`:

```python
from traffic_rl_project.environment import TrafficSignalEnv

def _calculate_reward(self, vehicles_passed, total_waiting):
    # Your custom reward logic here
    throughput_reward = vehicles_passed * 1.0
    waiting_penalty = -total_waiting * 0.01
    # Add your own components
    return throughput_reward + waiting_penalty
```

### Try Different RL Algorithms

Replace PPO with DQN or A2C:

```python
from stable_baselines3 import DQN

agent = DQN(
    "MlpPolicy",
    train_env,
    learning_rate=1e-3,
    buffer_size=50000,
    learning_starts=1000,
    verbose=1
)
```

## 📈 Training Tips

1. **Start Small**: Begin with shorter episodes (300-600s) for faster iteration
2. **Monitor Progress**: Use TensorBoard to track training
   ```bash
   tensorboard --logdir=./traffic_rl_logs/
   ```
3. **Tune Hyperparameters**: Adjust learning rate, entropy coefficient, network size
4. **Test Scenarios**: Evaluate on diverse traffic patterns (rush hour, asymmetric, etc.)

## 🎓 Learning Outcomes

This project demonstrates:
- Custom Gymnasium environment creation
- Reward function engineering
- Baseline policy implementation
- RL algorithm training and evaluation
- Performance visualization and analysis
- Hyperparameter tuning strategies

## 📚 Dependencies

- `gymnasium`: RL environment interface
- `stable-baselines3`: RL algorithms (PPO, DQN, A2C)
- `numpy`: Numerical computations
- `matplotlib`: Visualization
- `pandas`: Data analysis
- `torch`: Deep learning backend
- `tensorboard`: Training monitoring

## 🚦 Next Steps

To extend this project:

1. **SUMO Integration**: Use realistic traffic simulation with SUMO
2. **Multi-Intersection**: Scale to coordinated signal control
3. **Real-Time Learning**: Implement online learning for adaptation
4. **Pedestrian Crossings**: Add pedestrian logic and safety constraints
5. **Advanced Algorithms**: Try SAC, TD3, or multi-agent RL
6. **Transfer Learning**: Train on one intersection, deploy to others
7. **Real-World Validation**: Test with real traffic data

## 📝 Notes

- Training can take 10-30 minutes depending on `TOTAL_TIMESTEPS`
- GPU acceleration is optional but speeds up training
- Results may vary due to stochastic environment and exploration

## 🤝 Contributing

Feel free to:
- Experiment with different reward functions
- Test new RL algorithms
- Add visualization features
- Extend to more complex scenarios

## 📄 License

This project is for educational purposes. Use and modify as needed.

---

**Happy Training! 🚦🤖**
