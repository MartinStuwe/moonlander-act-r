import pygame.display
from main import run_visualization
from config import level_size_x, scaling_tiny_vis, edge


# how many frames per second
FPS = 60

# level height
level_size_y = 400  # should be equal to world_y_height from moonlander_environment

# pygame general setup
pygame.init()
screen = pygame.display.set_mode(((level_size_x+(2*edge))*scaling_tiny_vis, level_size_y*scaling_tiny_vis))

run_visualization(surface=screen, scaling=scaling_tiny_vis, tiny_visualization=True, FPS=FPS, keyboard_input=False,
                  obstacles_lists_file='obstacles_list_0.csv', drift_ranges_file='drift_ranges_0.csv',
                  wall_list_file=f'walls_dict_0.csv', trial=0)
