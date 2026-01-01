import matplotlib
import sys
# Use macOSX backend on macOS, TkAgg on others
if sys.platform == 'darwin':
    matplotlib.use('macOSX')  # Native macOS backend, avoids tkinter conflicts
else:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

class TrainingVisualizer:
    def __init__(self):
        plt.ion()  # Turn on interactive mode
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('Snake RL Training Dashboard', fontsize=16, fontweight='bold')
        plt.show(block=False)  # Show the figure immediately
        plt.pause(0.1)  # Small pause to ensure window appears
        
        # Create subplots
        self.ax1 = plt.subplot(2, 3, 1)  # Score plot
        self.ax2 = plt.subplot(2, 3, 2)  # Mean score plot
        self.ax3 = plt.subplot(2, 3, 3)  # Statistics text
        self.ax4 = plt.subplot(2, 3, 4)  # Recent scores bar chart
        self.ax5 = plt.subplot(2, 3, 5)  # Score distribution
        self.ax6 = plt.subplot(2, 3, 6)  # Training metrics
        
        # Initialize data storage
        self.scores = []
        self.mean_scores = []
        self.records = []
        self.game_numbers = []
        
        # Statistics
        self.total_games = 0
        self.current_record = 0
        self.best_mean_score = 0
        self.total_food_eaten = 0
        
    def update(self, game_num, score, mean_score, record, epsilon, memory_size):
        """Update all visualizations with new data"""
        self.total_games = game_num
        self.current_record = record
        if mean_score > 0:
            self.best_mean_score = max(self.best_mean_score, mean_score)
        if score > 0:
            self.total_food_eaten += score
        
        # Only append if we have actual game data (game_num > 0)
        if game_num > 0:
            self.scores.append(score)
            self.mean_scores.append(mean_score)
            self.records.append(record)
            self.game_numbers.append(game_num)
        
        # Keep only last 100 games for performance
        if len(self.scores) > 100:
            self.scores = self.scores[-100:]
            self.mean_scores = self.mean_scores[-100:]
            self.records = self.records[-100:]
            self.game_numbers = self.game_numbers[-100:]
        
        # Clear all axes
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6]:
            ax.clear()
        
        # 1. Score Plot
        self._plot_scores()
        
        # 2. Mean Score Plot
        self._plot_mean_scores()
        
        # 3. Statistics Panel
        self._plot_statistics(epsilon, memory_size)
        
        # 4. Recent Scores Bar Chart
        self._plot_recent_scores()
        
        # 5. Score Distribution
        self._plot_score_distribution()
        
        # 6. Training Metrics
        self._plot_training_metrics()
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
        # Force window to front (platform dependent)
        try:
            self.fig.canvas.manager.window.raise_()
        except:
            pass  # Some backends don't support this
    
    def _plot_scores(self):
        """Plot individual game scores"""
        if len(self.scores) > 0:
            self.ax1.plot(self.game_numbers, self.scores, 'b-', alpha=0.6, linewidth=1, label='Score')
            self.ax1.plot(self.game_numbers, self.records, 'r-', linewidth=2, label='Record')
            self.ax1.legend()
        else:
            self.ax1.text(0.5, 0.5, 'Waiting for game data...', 
                         ha='center', va='center', fontsize=12, transform=self.ax1.transAxes)
        self.ax1.set_title('Game Scores', fontweight='bold')
        self.ax1.set_xlabel('Game Number')
        self.ax1.set_ylabel('Score')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_ylim(ymin=0)
        
    def _plot_mean_scores(self):
        """Plot mean scores over time"""
        if len(self.mean_scores) > 0:
            self.ax2.plot(self.game_numbers, self.mean_scores, 'g-', linewidth=2, label='Mean Score')
            if self.best_mean_score > 0:
                self.ax2.axhline(y=self.best_mean_score, color='orange', linestyle='--', 
                                 linewidth=2, label=f'Best Mean: {self.best_mean_score:.1f}')
            self.ax2.legend()
        else:
            self.ax2.text(0.5, 0.5, 'Waiting for game data...', 
                         ha='center', va='center', fontsize=12, transform=self.ax2.transAxes)
        self.ax2.set_title('Mean Score Over Time', fontweight='bold')
        self.ax2.set_xlabel('Game Number')
        self.ax2.set_ylabel('Mean Score')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(ymin=0)
        
    def _plot_statistics(self, epsilon, memory_size):
        """Display key statistics as text"""
        self.ax3.axis('off')
        
        # Safely get current score and mean score
        current_score = self.scores[-1] if len(self.scores) > 0 else 0
        current_mean = self.mean_scores[-1] if len(self.mean_scores) > 0 else 0.0
        
        # Check improvement
        if len(self.mean_scores) > 10:
            improvement = '↑' if self.mean_scores[-1] > self.mean_scores[-10] else '↓'
        else:
            improvement = '-'
        
        stats_text = f"""
        TRAINING STATISTICS
        {'='*30}
        
        Total Games: {self.total_games}
        Current Score: {current_score}
        Record Score: {self.current_record}
        Mean Score: {current_mean:.2f}
        Best Mean: {self.best_mean_score:.2f}
        
        Total Food Eaten: {self.total_food_eaten}
        Avg Food/Game: {self.total_food_eaten/max(1, self.total_games):.2f}
        
        Exploration Rate (ε): {max(0, epsilon):.1f}
        Memory Size: {memory_size:,}
        
        Improvement: {improvement}
        """
        
        self.ax3.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                      verticalalignment='center', bbox=dict(boxstyle='round', 
                      facecolor='wheat', alpha=0.5))
        self.ax3.set_title('Live Statistics', fontweight='bold')
        
    def _plot_recent_scores(self):
        """Bar chart of recent scores"""
        if len(self.scores) > 0:
            recent_scores = self.scores[-20:] if len(self.scores) >= 20 else self.scores
            recent_games = self.game_numbers[-20:] if len(self.game_numbers) >= 20 else self.game_numbers
            
            colors = ['green' if s >= self.current_record * 0.8 else 'blue' if s >= self.current_record * 0.5 else 'red' 
                     for s in recent_scores]
            
            self.ax4.bar(range(len(recent_scores)), recent_scores, color=colors, alpha=0.7)
            self.ax4.axhline(y=self.current_record, color='red', linestyle='--', 
                           linewidth=2, label=f'Record: {self.current_record}')
            self.ax4.set_title('Recent 20 Games', fontweight='bold')
            self.ax4.set_xlabel('Recent Games')
            self.ax4.set_ylabel('Score')
            self.ax4.legend()
            self.ax4.grid(True, alpha=0.3, axis='y')
            self.ax4.set_ylim(ymin=0)
        
    def _plot_score_distribution(self):
        """Histogram of score distribution"""
        if len(self.scores) >= 10:
            bins = min(15, max(5, len(set(self.scores))))
            self.ax5.hist(self.scores, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
            self.ax5.axvline(x=np.mean(self.scores), color='red', linestyle='--', 
                           linewidth=2, label=f'Mean: {np.mean(self.scores):.1f}')
            self.ax5.axvline(x=np.median(self.scores), color='green', linestyle='--', 
                           linewidth=2, label=f'Median: {np.median(self.scores):.1f}')
            self.ax5.set_title('Score Distribution', fontweight='bold')
            self.ax5.set_xlabel('Score')
            self.ax5.set_ylabel('Frequency')
            self.ax5.legend()
            self.ax5.grid(True, alpha=0.3, axis='y')
        else:
            self.ax5.text(0.5, 0.5, 'Need more data\n(min 10 games)', 
                         ha='center', va='center', fontsize=12)
            self.ax5.set_title('Score Distribution', fontweight='bold')
            self.ax5.axis('off')
    
    def _plot_training_metrics(self):
        """Plot training progress metrics"""
        if len(self.game_numbers) >= 2:
            # Calculate improvement rate
            if len(self.mean_scores) >= 10:
                recent_improvement = np.mean(self.mean_scores[-10:]) - np.mean(self.mean_scores[-20:-10]) if len(self.mean_scores) >= 20 else 0
            else:
                recent_improvement = 0
            
            # Plot record progression
            record_changes = []
            prev_record = 0
            for r in self.records:
                if r > prev_record:
                    record_changes.append(1)
                    prev_record = r
                else:
                    record_changes.append(0)
            
            self.ax6.plot(self.game_numbers, record_changes, 'go-', markersize=8, 
                         label='Record Broken', linewidth=0)
            self.ax6.set_title('Training Progress', fontweight='bold')
            self.ax6.set_xlabel('Game Number')
            self.ax6.set_ylabel('Record Broken (1=Yes, 0=No)')
            self.ax6.set_ylim(-0.1, 1.1)
            self.ax6.legend()
            self.ax6.grid(True, alpha=0.3)
            
            # Add text annotation
            if recent_improvement > 0:
                improvement_text = f"↑ Improving: +{recent_improvement:.2f}"
                color = 'green'
            else:
                improvement_text = f"↓ Stable: {recent_improvement:.2f}"
                color = 'orange'
            
            self.ax6.text(0.02, 0.98, improvement_text, transform=self.ax6.transAxes,
                         fontsize=10, verticalalignment='top', color=color,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        else:
            self.ax6.text(0.5, 0.5, 'Collecting data...', 
                         ha='center', va='center', fontsize=12)
            self.ax6.set_title('Training Progress', fontweight='bold')
            self.ax6.axis('off')
    
    def close(self):
        """Close the visualization"""
        plt.close(self.fig)

