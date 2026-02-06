from snake_game import SnakeGame
from dqn_agent import Agent
from visualizer import TrainingVisualizer
import numpy as np
import os

def train():
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    visualizer = TrainingVisualizer()
    
    # Try to load existing model
    if agent.model.load():
        print("Loaded existing model")
    
    print("=" * 60)
    print("Snake RL Training Started")
    print("=" * 60)
    print("Click the Quit button in the game window, or press Ctrl+C to stop")
    print("=" * 60)
    print("\nInitializing visualization...")
    print("You should see:")
    print("  1. A Pygame window titled 'Snake RL' (the game)")
    print("  2. A Matplotlib window titled 'Snake RL Training Dashboard'")
    print("\nIf windows don't appear, check TROUBLESHOOTING.md")
    print("=" * 60)
    
    # Show initial empty visualization
    visualizer.update(0, 0, 0.0, 0, 80, 0)
    print("\nDashboard initialized! Waiting for first game to complete...")
    print("(The dashboard will update after each game ends)\n")
    
    try:
        mean_score = 0.0
        while True:
            # Get old state
            state_old = agent.get_state(game)
            
            # Get move
            final_move = agent.get_action(state_old)
            
            # Perform move and get new state (pass stats for display)
            reward, done, score, user_quit = game.play_step(final_move, agent.n_games, record, mean_score)
            state_new = agent.get_state(game)
            
            if user_quit:
                print("\nQuit button pressed. Stopping training...")
                break
            
            # Train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            
            # Remember
            agent.remember(state_old, final_move, reward, state_new, done)
            
            if done:
                # Train long memory, update visualization
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()
                
                if score > record:
                    record = score
                    agent.model.save()
                    print(f'🎉 NEW RECORD! Score: {score} - Model saved!')
                
                # Calculate statistics
                total_score += score
                mean_score = total_score / agent.n_games
                
                # Get epsilon and memory size for display
                epsilon = max(0, 80 - agent.n_games)
                memory_size = len(agent.memory)
                
                # Update visualization
                visualizer.update(agent.n_games, score, mean_score, record, epsilon, memory_size)
                
                # Console output
                print(f'Game {agent.n_games:4d} | Score: {score:3d} | Mean: {mean_score:5.2f} | Record: {record:3d} | ε: {epsilon:5.1f} | Memory: {memory_size:6d}')
                
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Training stopped by user (Ctrl+C)")
        print("=" * 60)
    finally:
        print(f"Final Statistics:")
        print(f"  Total Games: {agent.n_games}")
        print(f"  Record Score: {record}")
        print(f"  Mean Score: {total_score / max(1, agent.n_games):.2f}")
        print("=" * 60)
        visualizer.close()
        import pygame
        pygame.quit()

if __name__ == '__main__':
    train()

