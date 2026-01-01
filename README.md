# Snake Reinforcement Learning

A Deep Q-Network (DQN) implementation that learns to play the classic Snake game using Pygame and PyTorch.

## Features

- Classic Snake game implementation in Pygame
- Deep Q-Network (DQN) reinforcement learning agent
- **Comprehensive real-time training dashboard** with multiple visualizations:
  - Score progression over time
  - Mean score trends
  - Live statistics panel
  - Recent games bar chart
  - Score distribution histogram
  - Training progress metrics
- Enhanced game window with real-time statistics
- Automatic model saving when new records are achieved
- State representation based on danger detection and food location

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Agent

To train the agent, simply run:

```bash
python train.py
```

The agent will:
- Start playing games and learning from experience
- Display the game window showing the snake playing with real-time stats
- Open a comprehensive training dashboard with 6 different visualizations:
  - **Score Plot**: Individual game scores and record progression
  - **Mean Score Plot**: Average performance over time with best mean indicator
  - **Live Statistics**: Key metrics including games played, scores, exploration rate, memory size
  - **Recent Games**: Bar chart of the last 20 games with color-coded performance
  - **Score Distribution**: Histogram showing score frequency patterns
  - **Training Progress**: Visual indicator of when records are broken
- Automatically save the model when a new record is achieved
- Print detailed game statistics to the console

### How It Works

The agent uses a Deep Q-Network (DQN) with the following components:

1. **State Representation**: 11 features including:
   - Danger detection (straight, right, left)
   - Current direction (left, right, up, down)
   - Food location relative to head (left, right, up, down)

2. **Action Space**: 3 actions
   - [1, 0, 0]: Continue straight
   - [0, 1, 0]: Turn right
   - [0, 0, 1]: Turn left

3. **Reward System**:
   - +10 for eating food
   - -10 for collision/death
   - 0 for normal movement

4. **Neural Network**: 3-layer fully connected network
   - Input: 11 features
   - Hidden layers: 256 neurons each
   - Output: 3 Q-values (one per action)

5. **Training**:
   - Epsilon-greedy exploration (epsilon decreases with games)
   - Experience replay with batch training
   - Short-term and long-term memory training

## Files

- `snake_game.py`: Snake game implementation using Pygame
- `dqn_agent.py`: DQN agent with neural network and training logic
- `train.py`: Main training script
- `visualizer.py`: Comprehensive training dashboard visualization
- `requirements.txt`: Python dependencies
- `model/`: Directory where trained models are saved (created automatically)

## Training Tips

- The agent starts with random exploration and gradually learns
- Training can take many games (100+ games) before seeing good performance
- The model is saved automatically when new records are achieved
- You can stop and restart training - the model will be loaded if it exists

## Customization

You can adjust hyperparameters in `dqn_agent.py`:
- `BATCH_SIZE`: Number of experiences sampled for training (default: 1000)
- `LR`: Learning rate (default: 0.001)
- `gamma`: Discount factor (default: 0.9)
- Hidden layer size: Currently 256 neurons

You can also adjust game settings in `snake_game.py`:
- `BLOCK_SIZE`: Size of each block (default: 20)
- `SPEED`: Game speed/frames per second (default: 40)
- Window size: `w` and `h` parameters (default: 640x480)

## Requirements

- Python 3.7+
- Pygame 2.5.2+
- PyTorch 2.0.0+
- NumPy 1.24.0+
- Matplotlib 3.7.0+

## License

This project is open source and available for educational purposes.

