#!/usr/bin/env python3
"""
Quick test script to verify that both windows display correctly
"""
import sys

print("Testing display windows...")
print("=" * 60)

# Test pygame window
print("1. Testing Pygame window...")
try:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((15, 15))
    pygame.display.set_caption('Test - Snake Game Window')
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 36)
    text = font.render('Pygame Window Works!', True, (255, 255, 255))
    screen.blit(text, (150, 200))
    pygame.display.flip()
    print("   ✓ Pygame window should be visible")
    print("   Close the window to continue...")
    
    # Wait a bit for user to see it
    import time
    time.sleep(2)
    
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
except Exception as e:
    print(f"   ✗ Pygame error: {e}")
    sys.exit(1)

# Test matplotlib window
print("\n2. Testing Matplotlib window...")
try:
    import matplotlib
    import sys
    # Use macOSX backend on macOS to avoid tkinter conflicts
    if sys.platform == 'darwin':
        matplotlib.use('macOSX')
    else:
        matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.text(0.5, 0.5, 'Matplotlib Dashboard Works!', 
            ha='center', va='center', fontsize=20, 
            transform=ax.transAxes)
    ax.set_title('Test - Training Dashboard')
    plt.show(block=False)
    plt.pause(0.1)
    print("   ✓ Matplotlib window should be visible")
    print("   Close the window to continue...")
    
    import time
    time.sleep(2)
    
    plt.close(fig)
except Exception as e:
    print(f"   ✗ Matplotlib error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("All display tests passed!")
print("If you saw both windows, the display is working correctly.")
print("=" * 60)

