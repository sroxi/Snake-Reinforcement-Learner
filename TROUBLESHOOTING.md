# Troubleshooting Guide

## Can't See Windows

If you can't see the game window or dashboard, try these solutions:

### 1. Test Display Windows

Run the test script to verify your display setup:
```bash
python test_display.py
```

This will show both the Pygame window and Matplotlib dashboard to confirm they work.

### 2. Check Dependencies

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### 3. Matplotlib Backend Issues

If the dashboard doesn't appear, try setting the matplotlib backend explicitly:

**On macOS/Linux:**
```bash
export MPLBACKEND=TkAgg
python train.py
```

**On Windows:**
```cmd
set MPLBACKEND=TkAgg
python train.py
```

Or add this to the top of `visualizer.py`:
```python
import matplotlib
matplotlib.use('TkAgg')  # Already included, but you can try 'Qt5Agg' or 'Agg'
```

### 4. Window Behind Other Windows

- Check if windows are minimized or behind other applications
- On macOS, check Mission Control or use Cmd+Tab to switch windows
- The dashboard window should be titled "Snake RL Training Dashboard"
- The game window should be titled "Snake RL"

### 5. Headless/No Display Environment

If you're running on a server without a display:
- The game window won't work (Pygame requires a display)
- You can modify the code to run headless for training only
- Consider using SSH with X11 forwarding: `ssh -X user@server`

### 6. Check Console Output

The program should print:
```
============================================================
Snake RL Training Started
============================================================
Close the game window or press Ctrl+C to stop training
============================================================
Initializing visualization...
Dashboard window should be visible now!
```

If you see errors, check:
- Python version (needs 3.7+)
- All packages installed correctly
- No permission issues

### 7. Common Errors

**"No module named 'pygame'"**
```bash
pip install pygame
```

**"No module named 'torch'"**
```bash
pip install torch
```

**"No display name and no $DISPLAY environment variable"**
- You're on a headless system
- Need X11 forwarding or a display server

**Matplotlib window doesn't appear**
- Try different backends: `TkAgg`, `Qt5Agg`, `macOSX` (on Mac)
- Check if you have tkinter installed: `python -m tkinter`

### 8. Force Window to Front

If windows are hidden, try:
- Alt+Tab (Windows/Linux) or Cmd+Tab (Mac) to switch between windows
- Check your taskbar/dock for the windows
- Close and restart the program

### 9. Slow Performance

If the visualization is slow:
- The dashboard updates after each game (not each frame)
- Wait for the first game to complete
- The first game might take a while as the agent explores randomly

### 10. Still Not Working?

1. Check Python version: `python --version` (should be 3.7+)
2. Reinstall dependencies: `pip install --upgrade -r requirements.txt`
3. Run test script: `python test_display.py`
4. Check for error messages in the console

## Quick Fixes

**Reset everything:**
```bash
# Remove any cached models
rm -rf model/

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run test
python test_display.py

# Run training
python train.py
```

