# 🚀 Deployment Guide: Traffic Signal RL to Hugging Face Spaces

## Quick Start (5 minutes)

### Step 1: Prepare Your Files

You need these 3 files:
```
├── gradio_traffic_app.py          # Main application
├── requirements_gradio.txt        # Dependencies
└── README.md                      # Space description (rename from README_SPACE.md)
```

### Step 2: Create a Hugging Face Account

1. Go to https://huggingface.co/
2. Click "Sign Up" (free account)
3. Verify your email

### Step 3: Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the form:
   - **Space name**: `traffic-signal-rl` (or your choice)
   - **License**: MIT
   - **Select the Space SDK**: Gradio
   - **Space hardware**: CPU basic (free tier)
   - Make it **Public** (so others can use it)

4. Click "Create Space"

### Step 4: Upload Your Files

**Option A: Web Interface (Easiest)**

1. In your new Space, click "Files" tab
2. Click "Add file" → "Upload files"
3. Upload all 3 files:
   - `gradio_traffic_app.py`
   - `requirements_gradio.txt`
   - Rename `README_SPACE.md` to `README.md` and upload
4. Click "Commit changes to main"

**Option B: Git (Advanced)**

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/traffic-signal-rl
cd traffic-signal-rl

# Copy your files
cp gradio_traffic_app.py .
cp requirements_gradio.txt .
cp README_SPACE.md README.md

# Commit and push
git add .
git commit -m "Initial deployment of traffic signal RL app"
git push
```

### Step 5: Wait for Build

1. Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/traffic-signal-rl`
2. The app will automatically build (takes 1-2 minutes)
3. Watch the "Building" status → "Running"
4. Once running, you'll see the app interface!

### Step 6: Share Your Space! 🎉

Your app is now live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/traffic-signal-rl
```

Share this link with anyone - they can use it without installing anything!

---

## Customization Options

### Change App Title/Emoji

Edit the top of `README.md`:
```yaml
---
title: Your Custom Title
emoji: 🚦  # Change to any emoji
colorFrom: yellow
colorTo: red
---
```

### Adjust Default Settings

In `gradio_traffic_app.py`, modify default values:

```python
# Example: Change default controller
controller_choice = gr.Radio(
    choices=["Fixed-Time", "Actuated", "Max-Pressure"],
    value="Max-Pressure",  # Changed from "Actuated"
    ...
)

# Example: Change default traffic rates
north_rate = gr.Slider(0.1, 0.5, value=0.35, ...)  # Changed from 0.25
```

### Add More Traffic Patterns

Add new preset buttons:

```python
with gr.Row():
    balanced_btn = gr.Button("⚖️ Balanced Traffic")
    rush_hour_btn = gr.Button("🏙️ Rush Hour (N-S)")
    asymmetric_btn = gr.Button("🔀 Asymmetric")
    # Add your custom scenario
    heavy_east_btn = gr.Button("➡️ Heavy East Traffic")

heavy_east_btn.click(
    lambda: (0.15, 0.45, 0.15, 0.25),
    outputs=[north_rate, east_rate, south_rate, west_rate]
)
```

---

## Upgrading to Better Hardware

### Free Tier Limitations
- CPU basic (free)
- Good for demos and light usage
- May be slow with many simultaneous users

### Upgrade Options

1. **CPU upgrade** ($0.03/hour)
   - Better performance
   - Handle more users

2. **GPU** (if you add ML models later)
   - T4 GPU: $0.60/hour
   - A10G GPU: $1.05/hour

To upgrade:
1. Go to your Space settings
2. Click "Settings" tab
3. Under "Space hardware" select your tier
4. Confirm billing

---

## Troubleshooting

### Build Failed

**Check requirements.txt**
```bash
# Make sure file is named exactly: requirements_gradio.txt
# NOT: requirements.txt (unless you rename it in app)
```

**Check Python version**
Spaces use Python 3.10 by default. If you need a different version, create `runtime.txt`:
```
python-3.10
```

### App Shows Error

**View Logs**
1. Go to your Space
2. Click "Logs" at the bottom
3. Look for error messages

**Common fixes:**
- Missing imports: Add to `requirements_gradio.txt`
- File not found: Check file names match exactly
- Syntax errors: Test locally first

### Test Locally First

```bash
# Install Gradio
pip install gradio numpy matplotlib Pillow

# Run locally
python gradio_traffic_app.py

# Open browser to: http://127.0.0.1:7860
```

---

## Advanced Features

### Add Authentication

Restrict who can use your app:

```python
demo.launch(auth=("username", "password"))
```

### Enable Queuing

Handle many simultaneous users:

```python
demo.queue(max_size=20)
demo.launch()
```

### Add Analytics

Track usage in your Space settings:
1. Settings → "Visibility" → Enable "Track usage"

### Make It Private

1. Go to Space settings
2. Change visibility to "Private"
3. Only you (and collaborators) can access

---

## Integration with RL Training

### Option 1: Upload Trained Models

If you train an RL agent (using the main notebook):

```python
# After training
agent.save("traffic_ppo_model")

# Upload traffic_ppo_model.zip to your Space
```

Then load it in Gradio:

```python
from stable_baselines3 import PPO

# In your Gradio app
class RLController:
    def __init__(self):
        self.model = PPO.load("traffic_ppo_model")
        self.name = "RL Agent (PPO)"
    
    def predict(self, obs):
        return self.model.predict(obs, deterministic=True)
```

### Option 2: Live Training

For advanced users, enable training in the Space:

```python
with gr.Tab("Train New Agent"):
    gr.Markdown("### Train a custom RL agent")
    train_btn = gr.Button("Start Training")
    
    # Add training logic
```

⚠️ **Warning**: Training requires GPU hardware (not free tier)

---

## Sharing Your Work

### Get Featured

Hugging Face features cool Spaces! To increase visibility:

1. **Write a good README**: Clear description, screenshots
2. **Add example scenarios**: Show interesting use cases
3. **Tag appropriately**: Add tags like `reinforcement-learning`, `traffic`, `simulation`
4. **Share on social media**: Twitter, LinkedIn with @huggingface

### Embed in Website

You can embed your Space in any website:

```html
<gradio-app src="https://huggingface.co/spaces/YOUR_USERNAME/traffic-signal-rl"></gradio-app>
<script type="module" src="https://gradio.s3-us-west-2.amazonaws.com/4.0.0/gradio.js"></script>
```

---

## Cost Estimates

### Free Tier
- **Cost**: $0
- **Limits**: CPU basic, may sleep after inactivity
- **Best for**: Personal projects, demos, learning

### Persistent with Upgrade
- **CPU upgrade**: ~$22/month (24/7)
- **GPU T4**: ~$432/month (if running 24/7)
- **Best for**: Production apps, research tools

💡 **Tip**: Use "Sleep after inactivity" to reduce costs!

---

## Next Steps

1. ✅ Deploy your basic app
2. 🎨 Customize the interface
3. 🤖 Add your trained RL models
4. 📊 Add more visualizations
5. 🔗 Share with the community!

**Questions?** Check Hugging Face Spaces documentation:
https://huggingface.co/docs/hub/spaces

---

**Happy Deploying! 🚀**
